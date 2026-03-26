# AGENTS.md -- [Project Name]

## Role

You are the builder and co-planner.

**Planning:** When given a planning prompt, write your independent plan to `plans/active/Plan-XXX-Codex.md`. Do not read Claude's plan first — plan independently.

**Building:** Implement code from `plans/active/Plan-XXX-Final.md` (the synthesized plan) or direct instructions. Execute one phase at a time, run tests after each meaningful change, and fix failures before reporting completion.

## Stack

- **Framework**: [Framework + version]
- **Language**: [TypeScript strict / Python / etc.]
- **Styling**: [Tailwind / CSS Modules / etc.]
- **Database**: [Supabase / Neon / Postgres / etc.]
- **Deployment**: [Vercel / Cloudflare / AWS / etc.]

## Commands

- `npm run dev` -- start dev server
- `npm run lint` -- lint checks
- `npm run test -- --run` -- tests
- `npm run build` -- build validation
- `scripts/review-diff.sh` -- Gemini diff review
- `scripts/quality-gate.sh` -- full pre-commit quality gate

## Rules

- Read `plans/active/Plan-XXX-Final.md` before implementation if it exists (the synthesized plan).
- Implement one phase/task at a time; do not skip ahead.
- Search existing code before creating files/abstractions.
- Keep diffs minimal and scoped to the task.
- Prefer clear errors over silent fallbacks.
- Avoid `any` when feasible; keep boundaries typed.
- Update `WORKLOG.md` for meaningful changes.

## Safety

- Never run destructive commands without confirmation.
- Never stage or commit secrets/credentials.
- Never stage unrelated changes.

## Delivery Contract

- Report exact commands run and pass/fail outcomes.
- If checks were skipped, say exactly which and why.
- If blocked after focused attempts, report blocker with next best path.
