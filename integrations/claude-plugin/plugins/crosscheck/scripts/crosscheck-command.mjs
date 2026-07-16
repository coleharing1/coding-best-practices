#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";

const COMMANDS = new Set(["plan", "review", "status", "result", "cancel", "transfer"]);

function fail(message, code = 1) {
  process.stderr.write(`${message}\n`);
  process.exit(code);
}

function controllerBin() {
  return process.env.CROSSCHECKCTL_BIN || "crosscheckctl";
}

function runController(args, options = {}) {
  const result = spawnSync(controllerBin(), args, {
    cwd: options.cwd || process.cwd(),
    env: { ...process.env, CROSSCHECK_CALLER: "claude-plugin" },
    encoding: "utf8",
    shell: false,
    stdio: options.capture ? ["ignore", "pipe", "pipe"] : "inherit"
  });
  if (result.error) {
    fail(`Could not launch crosscheckctl: ${result.error.message}`);
  }
  if (options.noExit) {
    return result;
  }
  if (!options.capture) {
    process.exit(result.status ?? 1);
  }
  if (result.status !== 0) {
    if (result.stdout) process.stdout.write(result.stdout);
    if (result.stderr) process.stderr.write(result.stderr);
    process.exit(result.status ?? 1);
  }
  return result.stdout;
}

function messageText(content) {
  if (typeof content === "string") return content.trim();
  if (!Array.isArray(content)) return "";
  return content
    .filter((part) => part && part.type === "text" && typeof part.text === "string")
    .map((part) => part.text.trim())
    .filter(Boolean)
    .join("\n\n");
}

function isCommandEcho(text) {
  const normalized = text.trim();
  return (
    /^\/?crosscheck:(plan|review|status|result|cancel|transfer)\b/i.test(normalized) ||
    /<command-name>\/?crosscheck:(plan|review|status|result|cancel|transfer)<\/command-name>/i.test(normalized)
  );
}

function precedingUserRequest(transcriptPath) {
  const rows = fs.readFileSync(transcriptPath, "utf8").split(/\r?\n/).filter(Boolean);
  const candidates = [];
  for (const line of rows) {
    let row;
    try {
      row = JSON.parse(line);
    } catch {
      continue;
    }
    if (row?.type !== "user") continue;
    const text = messageText(row?.message?.content ?? row?.content);
    if (!text || isCommandEcho(text) || text.includes("<local-command-stdout>")) continue;
    candidates.push(text);
  }
  const request = candidates.at(-1);
  if (!request) {
    fail("No preceding user request was found in the current Claude transcript.");
  }
  return request;
}

function currentTranscript() {
  const requested = process.env.CROSSCHECK_CLAUDE_TRANSCRIPT_PATH;
  if (!requested) {
    fail("Current Claude transcript is unavailable. Restart Claude after enabling the plugin, then retry.");
  }
  let real;
  try {
    real = fs.realpathSync(requested);
  } catch {
    fail(`Claude transcript not found: ${requested}`);
  }
  if (path.extname(real) !== ".jsonl") {
    fail(`Claude transcript must be JSONL: ${real}`);
  }
  return real;
}

function findRunId(value) {
  if (!value || typeof value !== "object") return null;
  for (const key of ["run_id", "runId"]) {
    if (typeof value[key] === "string" && value[key]) return value[key];
  }
  for (const child of Object.values(value)) {
    const found = findRunId(child);
    if (found) return found;
  }
  return null;
}

function currentRepositoryRoot() {
  const result = spawnSync("git", ["-C", process.cwd(), "rev-parse", "--show-toplevel"], {
    cwd: process.cwd(),
    env: process.env,
    encoding: "utf8",
    shell: false
  });
  if (result.error || result.status !== 0) {
    fail("The current Claude directory is not a readable Git repository; use crosscheckctl with an explicit run ID.");
  }
  return fs.realpathSync(result.stdout.trim());
}

function selectedRunId() {
  const currentRepository = currentRepositoryRoot();
  const selector = process.env.CROSSCHECK_RUN_ID
    ? ["--json", "status", process.env.CROSSCHECK_RUN_ID]
    : ["--json", "status", "--latest", "--repo", currentRepository];
  const raw = runController(selector, { capture: true });
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    fail("crosscheckctl returned malformed JSON while resolving the latest run.");
  }
  const runId = findRunId(parsed);
  if (!runId) fail("No crosscheck run ID was returned for the latest run.");
  const recordedRepository = parsed?.repository?.path;
  if (typeof recordedRepository !== "string" || !recordedRepository) {
    fail("The latest crosscheck run did not include a repository path; use crosscheckctl with an explicit run ID.");
  }
  let runRepository;
  try {
    runRepository = fs.realpathSync(recordedRepository);
  } catch {
    fail(`The latest crosscheck repository no longer exists: ${recordedRepository}`);
  }
  if (runRepository !== currentRepository) {
    fail(
      `The latest crosscheck run belongs to ${runRepository}, not ${currentRepository}. ` +
        "Refusing a cross-repository action; use crosscheckctl with the exact run ID."
    );
  }
  return runId;
}

function main() {
  const command = process.argv[2] || "";
  if (!COMMANDS.has(command)) fail(`Unsupported crosscheck plugin command: ${command || "(missing)"}`, 64);

  if (command === "plan") {
    const transcript = currentTranscript();
    // Pass the request via a 0600 temp file, never argv — argv is world-readable
    // in the process table for the lifetime of the crosscheckctl run.
    const stagingDir = fs.mkdtempSync(path.join(os.tmpdir(), "crosscheck-plan-"));
    fs.chmodSync(stagingDir, 0o700);
    const requestPath = path.join(stagingDir, "request.txt");
    fs.writeFileSync(requestPath, precedingUserRequest(transcript), { mode: 0o600 });
    let status = 1;
    try {
      const result = runController(
        ["plan", "--repo", process.cwd(), "--request-file", requestPath],
        { noExit: true }
      );
      status = result.status ?? 1;
    } finally {
      fs.rmSync(stagingDir, { recursive: true, force: true });
    }
    process.exit(status);
  }
  if (command === "status") {
    runController(["status", selectedRunId()]);
    return;
  }
  if (command === "result") {
    runController(["show", selectedRunId()]);
    return;
  }

  const runId = selectedRunId();
  if (command === "transfer") {
    runController([
      "transfer",
      runId,
      "--source",
      currentTranscript()
    ]);
    return;
  }
  runController([command, runId]);
}

main();
