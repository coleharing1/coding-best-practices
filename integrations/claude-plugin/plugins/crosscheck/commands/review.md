---
description: Run the guarded review stage for the latest crosscheck run
disable-model-invocation: true
allowed-tools: Bash(node:*)
---

!`node "${CLAUDE_PLUGIN_ROOT}/scripts/crosscheck-command.mjs" review`

Present the controller output exactly as returned. Do not make fixes outside the controller.
