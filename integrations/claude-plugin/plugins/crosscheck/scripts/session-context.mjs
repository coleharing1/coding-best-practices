#!/usr/bin/env node

// Modified from OpenAI's codex-plugin-cc 1.0.6 session lifecycle hook.
// This derivative retains only the SessionStart transcript-path export.

import fs from "node:fs";
import process from "node:process";

function shellEscape(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`;
}

function main() {
  const raw = fs.readFileSync(0, "utf8").trim();
  const input = raw ? JSON.parse(raw) : {};
  const transcriptPath = input.transcript_path;
  if (!process.env.CLAUDE_ENV_FILE || !transcriptPath) {
    return;
  }
  fs.appendFileSync(
    process.env.CLAUDE_ENV_FILE,
    `export CROSSCHECK_CLAUDE_TRANSCRIPT_PATH=${shellEscape(transcriptPath)}\n`,
    { encoding: "utf8", mode: 0o600 }
  );
}

try {
  main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
}
