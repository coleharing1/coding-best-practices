---
description: Create a phased implementation plan for a feature
argument-hint: [feature-name]
---

## Planning: $ARGUMENTS

You are planning implementation for **$ARGUMENTS** in this project.

Read the current codebase context (CLAUDE.md, WORKLOG.md, existing architecture) before planning.

## Output Requirements

1. **Technical spec** — interfaces, contracts, data flow (keep it short)
2. **Phased implementation plan** — discrete, sequential steps. One phase = one Codex session.
3. **Risk analysis per phase** — what can break, why, mitigation
4. **Acceptance criteria per phase** — testable, binary pass/fail
5. **Dual-review flags** — mark any phase that needs Gemini + Claude review (auth, payments, schema changes)

## Rules

- Do not write code yet — this is planning only.
- Call out unknowns explicitly.
- Prefer minimal-change integration with existing patterns.
- Output the plan to `PLAN.md` for Codex to execute.

## Current Architecture

!`find . -type f -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" | head -40`
