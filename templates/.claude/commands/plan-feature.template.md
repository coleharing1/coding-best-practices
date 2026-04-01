---
description: Create a phased implementation plan for a feature
argument-hint: [feature-name]
---

## Planning: $ARGUMENTS

You are planning implementation for **$ARGUMENTS** in this project.

Read the current codebase context (CLAUDE.md, WORKLOG.md, existing architecture) before planning.

## Output Requirements

1. **Technical spec** — interfaces, contracts, data flow (keep it short)
2. **Working assumptions, ownership legend, and blocking gates**
3. **Phased implementation checklist** — discrete, sequential steps with owner tags. One phase = one Codex session.
4. **Risk analysis and verification per phase**
5. **Dual-review flags** — mark any phase that needs Gemini + Claude review (auth, payments, schema changes)

## Rules

- Do not write code yet — this is planning only.
- Call out unknowns explicitly.
- Prefer minimal-change integration with existing patterns.
- If you intentionally skip dual-plan workflow, output the quick plan to `PLAN.md`.
- Otherwise prefer the numbered plan set in `plans/active/`.
- Prefer the dual-plan workflow for non-trivial features; use `/project:dual-plan` when you want the full Claude-vs-Codex comparison loop.
- Mark human-only login, 2FA, approval, or browser-consent steps explicitly.

## Current Architecture

!`find . -type f -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" | head -40`
