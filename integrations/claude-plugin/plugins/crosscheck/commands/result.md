---
description: Show artifacts and results for the latest crosscheck run
disable-model-invocation: true
allowed-tools: Bash(node:*)
---

!`node "${CLAUDE_PLUGIN_ROOT}/scripts/crosscheck-command.mjs" result`

Present the controller output exactly as returned.
