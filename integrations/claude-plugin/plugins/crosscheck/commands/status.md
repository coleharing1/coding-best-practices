---
description: Show status for the latest crosscheck run
disable-model-invocation: true
allowed-tools: Bash(node:*)
---

!`node "${CLAUDE_PLUGIN_ROOT}/scripts/crosscheck-command.mjs" status`

Present the controller output exactly as returned.
