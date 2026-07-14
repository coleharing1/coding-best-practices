#!/usr/bin/env node

// Contains a minimal, modified implementation of the external-agent session
// import protocol from OpenAI's codex-plugin-cc 1.0.6. Unlike the original
// plugin, this file does not start a Codex thread or run a model turn.

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import readline from "node:readline";
import { spawn, spawnSync } from "node:child_process";

const IMPORT_COMPLETED = "externalAgentConfig/import/completed";
const REQUESTED_IMPORT_TIMEOUT_MS = Number.parseInt(process.env.CROSSCHECK_IMPORT_TIMEOUT_MS || "90000", 10);
const IMPORT_TIMEOUT_MS = Number.isSafeInteger(REQUESTED_IMPORT_TIMEOUT_MS)
  ? Math.min(90_000, Math.max(50, REQUESTED_IMPORT_TIMEOUT_MS))
  : 90_000;
const REQUEST_TIMEOUT_MS = Math.min(30_000, IMPORT_TIMEOUT_MS);
const GRACEFUL_EXIT_MS = 500;
const TERM_WAIT_MS = 1_000;
const KILL_WAIT_MS = 2_000;
const DISABLED_FEATURES = [
  "apps",
  "plugins",
  "remote_plugin",
  "hooks",
  "memories",
  "multi_agent",
  "multi_agent_v2",
  "enable_fanout",
  "standalone_web_search",
  "image_generation",
  "browser_use",
  "browser_use_external",
  "browser_use_full_cdp_access",
  "computer_use",
  "in_app_browser",
  "skill_mcp_dependency_install"
];

function fail(message) {
  throw new Error(message);
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function parseArgs(argv) {
  const options = { json: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--json") {
      options.json = true;
      continue;
    }
    if (["--source", "--cwd", "--title"].includes(arg)) {
      const value = argv[index + 1];
      if (!value) fail(`${arg} requires a value.`);
      options[arg.slice(2)] = value;
      index += 1;
      continue;
    }
    fail(`Unknown argument: ${arg}`);
  }
  if (!options.source) fail("--source <claude-session.jsonl> is required.");
  return options;
}

function resolveSource(requested) {
  const source = fs.realpathSync(path.resolve(requested));
  const projects = fs.realpathSync(path.join(os.homedir(), ".claude", "projects"));
  const relative = path.relative(projects, source);
  if (
    path.extname(source) !== ".jsonl" ||
    relative === "" ||
    relative === ".." ||
    relative.startsWith(`..${path.sep}`) ||
    path.isAbsolute(relative)
  ) {
    fail(`Claude session source must be a JSONL file under ${projects}: ${source}`);
  }
  const stat = fs.statSync(source);
  if (!stat.isFile()) fail(`Claude session source is not a regular file: ${source}`);
  if (typeof process.getuid === "function" && stat.uid !== process.getuid()) {
    fail(`Claude session source is not owned by the current user: ${source}`);
  }
  return source;
}

function runJson(binary, args, cwd) {
  const result = spawnSync(binary, args, {
    cwd,
    env: process.env,
    encoding: "utf8",
    shell: false,
    timeout: 30_000
  });
  if (result.error || result.status !== 0) {
    const detail = result.error?.message || result.stderr?.trim() || `exit ${result.status}`;
    fail(`Failed to inspect Codex configuration: ${detail}`);
  }
  try {
    return JSON.parse(result.stdout);
  } catch {
    fail("Codex configuration inspection returned malformed JSON.");
  }
}

function tomlKey(value) {
  return JSON.stringify(String(value));
}

function appServerArgs(binary, cwd) {
  const servers = runJson(binary, ["mcp", "list", "--json"], cwd);
  if (!Array.isArray(servers)) fail("Codex MCP inventory was not an array; refusing transfer.");
  const args = ["app-server"];
  for (const feature of DISABLED_FEATURES) args.push("--disable", feature);
  args.push("-c", 'approval_policy="never"', "-c", 'sandbox_mode="read-only"');
  for (const server of servers) {
    if (typeof server?.name !== "string" || !server.name) {
      fail("Codex MCP inventory contained an unnamed server; refusing transfer.");
    }
    const transport = server.transport;
    if (!transport || !["stdio", "streamable_http"].includes(transport.type)) {
      fail(`Codex MCP inventory contained an unsupported transport for ${server.name}; refusing transfer.`);
    }
    const prefix = `mcp_servers.${tomlKey(server.name)}`;
    args.push("-c", `${prefix}.enabled=false`);
    // Normalize every inherited transport even though it is disabled. Some
    // Codex surfaces accept legacy values that app-server rejects while
    // loading config, before the enabled flag is consulted.
    if (transport.type === "stdio") {
      args.push("-c", `${prefix}.command="/usr/bin/false"`, "-c", `${prefix}.args=[]`);
    } else {
      args.push("-c", `${prefix}.url="http://127.0.0.1:9"`);
    }
  }
  return args;
}

class AppServerClient {
  constructor(binary, args, cwd) {
    this.nextId = 1;
    this.pending = new Map();
    this.stderr = "";
    this.completed = false;
    this.processClosed = false;
    this.completedPromise = new Promise((resolve, reject) => {
      this.resolveCompleted = resolve;
      this.rejectCompleted = reject;
    });
    void this.completedPromise.catch(() => {});
    this.exitPromise = new Promise((resolve) => {
      this.resolveExit = resolve;
    });
    this.proc = spawn(binary, args, {
      cwd,
      env: process.env,
      stdio: ["pipe", "pipe", "pipe"],
      shell: false,
      // The Python controller owns the transfer process group. Keeping the
      // app-server in that group lets the controller reap the full tree if
      // this helper stalls or is cancelled.
      detached: false
    });
    this.proc.stderr.setEncoding("utf8");
    this.proc.stderr.on("data", (chunk) => {
      this.stderr += chunk;
    });
    this.proc.on("error", (error) => this.rejectAll(error));
    this.proc.on("close", (code, signal) => {
      this.processClosed = true;
      if (!this.completed || this.pending.size) {
        this.rejectAll(new Error(`codex app-server exited (${signal || code}): ${this.stderr.trim()}`));
      }
      this.resolveExit();
    });
    this.lines = readline.createInterface({ input: this.proc.stdout });
    this.lines.on("line", (line) => this.onLine(line));
  }

  rejectAll(error) {
    for (const pending of this.pending.values()) {
      clearTimeout(pending.timer);
      pending.reject(error);
    }
    this.pending.clear();
    if (!this.completed && this.rejectCompleted) this.rejectCompleted(error);
  }

  send(message) {
    this.proc.stdin.write(`${JSON.stringify(message)}\n`);
  }

  request(method, params, timeoutMs = REQUEST_TIMEOUT_MS) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        if (!this.pending.delete(id)) return;
        reject(new Error(`Timed out waiting for Codex response to ${method}.`));
      }, timeoutMs);
      this.pending.set(id, { resolve, reject, method, timer });
      try {
        this.send({ id, method, params });
      } catch (error) {
        clearTimeout(timer);
        this.pending.delete(id);
        reject(error);
      }
    });
  }

  notify(method, params = {}) {
    this.send({ method, params });
  }

  onLine(line) {
    if (!line.trim()) return;
    let message;
    try {
      message = JSON.parse(line);
    } catch {
      this.rejectAll(new Error(`Malformed codex app-server JSONL: ${line}`));
      return;
    }
    if (message.id !== undefined && message.method) {
      this.send({
        id: message.id,
        error: { code: -32601, message: `Crosscheck transfer rejects server request: ${message.method}` }
      });
      return;
    }
    if (message.id !== undefined) {
      const pending = this.pending.get(message.id);
      if (!pending) return;
      this.pending.delete(message.id);
      clearTimeout(pending.timer);
      if (message.error) pending.reject(new Error(message.error.message || `${pending.method} failed`));
      else pending.resolve(message.result || {});
      return;
    }
    if (message.method === IMPORT_COMPLETED) {
      this.completed = true;
      this.resolveCompleted(message.params || {});
    }
  }

  async initialize() {
    await this.request("initialize", {
      clientInfo: { title: "Crosscheck Council Transfer", name: "Claude Code", version: "0.1.0" },
      capabilities: {
        experimentalApi: false,
        requestAttestation: false,
        optOutNotificationMethods: [
          "item/agentMessage/delta",
          "item/reasoning/summaryTextDelta",
          "item/reasoning/summaryPartAdded",
          "item/reasoning/textDelta"
        ]
      }
    });
    this.notify("initialized", {});
  }

  async waitForImport() {
    let timer;
    try {
      await Promise.race([
        this.completedPromise,
        new Promise((_, reject) => {
          timer = setTimeout(() => reject(new Error("Timed out waiting for Codex session import.")), IMPORT_TIMEOUT_MS);
        })
      ]);
    } finally {
      clearTimeout(timer);
    }
  }

  async close() {
    this.lines.close();
    if (!this.proc.stdin.destroyed && this.proc.stdin.writable) {
      this.proc.stdin.end();
      await Promise.race([this.exitPromise, delay(GRACEFUL_EXIT_MS)]);
    }

    if (this.processClosed) return;
    if (this.proc.exitCode === null) {
      this.proc.kill("SIGTERM");
      await Promise.race([this.exitPromise, delay(TERM_WAIT_MS)]);
    }
    if (!this.processClosed && this.proc.exitCode === null) {
      this.proc.kill("SIGKILL");
      await Promise.race([this.exitPromise, delay(KILL_WAIT_MS)]);
      if (!this.processClosed && this.proc.exitCode === null) {
        throw new Error("Failed to terminate Codex app-server process.");
      }
    }
  }
}

function sourceHash(source) {
  return crypto.createHash("sha256").update(fs.readFileSync(source)).digest("hex");
}

function resolveExecutable(requested) {
  const candidates = requested.includes(path.sep)
    ? [path.resolve(requested)]
    : (process.env.PATH || "")
        .split(path.delimiter)
        .filter(Boolean)
        .map((directory) => path.join(directory, requested));
  for (const candidate of candidates) {
    try {
      fs.accessSync(candidate, fs.constants.X_OK);
      const stat = fs.statSync(candidate);
      if (stat.isFile()) return fs.realpathSync(candidate);
    } catch {
      // Continue through PATH without invoking a shell.
    }
  }
  fail(`Codex executable was not found or executable: ${requested}`);
}

function importedThreadId(source) {
  const ledgerPath = path.join(path.resolve(process.env.CODEX_HOME || path.join(os.homedir(), ".codex")), "external_agent_session_imports.json");
  if (!fs.existsSync(ledgerPath)) return null;
  const ledger = JSON.parse(fs.readFileSync(ledgerPath, "utf8"));
  const digest = sourceHash(source);
  const matches = (Array.isArray(ledger?.records) ? ledger.records : []).filter(
    (record) =>
      record?.source_path === source &&
      record?.content_sha256 === digest &&
      typeof record?.imported_thread_id === "string"
  );
  return matches.at(-1)?.imported_thread_id || null;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const source = resolveSource(options.source);
  const cwd = fs.realpathSync(path.resolve(options.cwd || process.cwd()));
  const binary = resolveExecutable(process.env.CROSSCHECK_CODEX_BIN || "codex");
  const client = new AppServerClient(binary, appServerArgs(binary, cwd), cwd);
  try {
    await client.initialize();
    await client.request("externalAgentConfig/import", {
      migrationItems: [
        {
          itemType: "SESSIONS",
          description: `Transfer Claude session ${path.basename(source)}`,
          cwd: null,
          details: {
            plugins: [],
            sessions: [{ path: source, cwd, title: options.title || null }],
            mcpServers: [],
            hooks: [],
            subagents: [],
            commands: []
          }
        }
      ]
    });
    await client.waitForImport();
  } finally {
    await client.close();
  }
  const threadId = importedThreadId(source);
  if (!threadId) fail(`Codex completed the import but did not record a thread.${client.stderr.trim() ? ` ${client.stderr.trim()}` : ""}`);
  const payload = {
    thread_id: threadId,
    resume_command: `codex resume ${threadId}`,
    source_path: source,
    source_sha256: sourceHash(source),
    codex_binary: binary,
    imported_tools: { plugins: 0, mcp_servers: 0, hooks: 0, subagents: 0, commands: 0 }
  };
  if (options.json) process.stdout.write(`${JSON.stringify(payload)}\n`);
  else process.stdout.write(`Codex session ID: ${threadId}\nResume in Codex: ${payload.resume_command}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
});
