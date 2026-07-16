---
description: Start an independent Claude-Codex plan from the preceding user request
disable-model-invocation: true
allowed-tools: Bash(node:*)
---

!`node "${CLAUDE_PLUGIN_ROOT}/scripts/crosscheck-command.mjs" plan`

Present the controller output exactly as returned. Preserve the run ID and artifact paths.
