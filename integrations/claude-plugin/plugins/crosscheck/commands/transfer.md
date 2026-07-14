---
description: Explicitly import this Claude session into a Codex Desktop thread
disable-model-invocation: true
allowed-tools: Bash(node:*)
---

!`node "${CLAUDE_PLUGIN_ROOT}/scripts/crosscheck-command.mjs" transfer`

Present the controller output exactly as returned. Preserve the thread ID and `codex resume` command.
