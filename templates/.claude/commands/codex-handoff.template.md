---
description: Prepare a Final-plan handoff for Codex execution
argument-hint: [phase-number]
---

## Codex Handoff — Phase $ARGUMENTS

Read the active `plans/active/Plan-XXX-Final.md` and extract Phase $ARGUMENTS.

Prepare a focused execution brief:

1. **Objective** — one sentence describing what this phase delivers
2. **Files to create/modify** — explicit list with expected changes
3. **Commands to run after** — test, lint, build commands for verification
4. **Acceptance criteria** — copy from the Final plan, must be binary pass/fail
5. **Do-not-touch list** — files outside scope that must not change

Format the output so it can be pasted directly into Codex as a task prompt.
