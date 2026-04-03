# AGENTS.md -- [Project Name]

## Role

You are the builder and execution partner for this repo.

**Planning mode**
- When asked to plan non-trivial work, write an independent plan to `plans/active/Plan-XXX-Codex.md`.
- Do not read Claude's plan first. Plan independently, then compare later.
- Write plans as owner-tagged checklists with gates, not loose prose.

**Implementation mode**
- Implement from `plans/active/Plan-XXX-Final.md` when it exists.
- Execute one phase at a time.
- Run checks after meaningful changes.
- Fix failures before reporting completion.

## Stack

- **Framework**: [Framework + version]
- **Language**: [TypeScript strict / Python / etc.]
- **Styling**: [Tailwind / CSS Modules / etc.]
- **Database**: [Supabase / Neon / Postgres / etc.]
- **Deployment**: [Vercel / Cloudflare / AWS / etc.]

## Repo Baseline

- `npm run lint` -> [current expected result]
- `npm run test -- --run` -> [current expected result]
- `npm run build` -> [current expected result]
- `E2E` -> [command + expectation]
- `Typecheck/parity` -> [command + expectation]

## Current State

- **Active milestone**: [current phase or feature]
- **Known blockers**: [if any]
- **Production posture**: [dev only / preview safe / prod live]

## Commands

- `npm run dev` -- start dev server
- `npm run lint` -- lint checks
- `npm run test -- --run` -- tests
- `npm run build` -- build validation
- `scripts/review-diff.sh` -- Gemini diff review
- `scripts/quality-gate.sh` -- full pre-commit quality gate
- `[parity command]` -- dev/prod or schema parity check when relevant

## Key Docs

- `README.md` -- current repo truth
- `WORKLOG.md` -- durable implementation memory
- `CLAUDE.md` -- planner/reviewer context
- `GEMINI.md` -- Gemini CLI context when Gemini is part of the loop
- `plans/MACRO-ROADMAP.md` -- whole-project roadmap and sequencing memory
- `plans/active/` -- active plan set
- `plans/archive/` -- completed decision history
- `DEBUG-JOURNAL.md` -- investigation memory when debugging is non-trivial
- `TESTING_AND_BROWSER_AUTOMATION.md` -- browser/test quick reference
- `knowledgebase/` -- stable business/architecture context for larger repos
- `runbooks/` -- operator-facing procedures

## Repeatable Workflow Assets

- `.cursor/commands/` -- Cursor slash-command equivalents for stable prompts
- `.claude/commands/` and `.claude/rules/` -- Claude Code invoked checklists and scoped instructions
- `.claude/skills/` -- Claude Code auto-invoked specialist workflows
- `.gemini/commands/` -- Gemini CLI TOML commands for plan/review/bootstrap
- `.agents/skills/` -- portable Codex/Gemini skill packs stored with the repo

## Rules

- Read the active Final plan before implementation when one exists.
- Read `plans/MACRO-ROADMAP.md` before non-trivial planning or implementation work.
- Implement one phase/task at a time; do not skip ahead.
- Search existing patterns before creating new abstractions.
- Keep diffs minimal and scoped to the task.
- Prefer clear errors over silent fallbacks.
- Keep typed boundaries; avoid `any` when feasible.
- Update `WORKLOG.md` when behavior, architecture, process, or verification reality changes.
- Update `plans/MACRO-ROADMAP.md` when long-range phase status, sequencing, durable assumptions, or likely-next work changes.
- Update `README.md`, runbooks, or browser docs when they stop matching reality.
- Prefer mock mode or safe fallbacks when external-service credentials are unavailable.
- Prefer migrations and checked-in schema changes over ad hoc database edits.
- Keep production access read-only unless the user explicitly requests a confirmed write path.
- When the same prompt or checklist appears repeatedly, promote it into a command, skill, hook, or automation instead of relying on memory.
- Keep `AGENTS.md` concise and map-like; push deeper truth into runbooks, knowledgebase pages, and workflow assets.
- If setup requires login, 2FA, org selection, or consent, use the documented browser handoff pattern:
  - open the exact page or auth command
  - pause for the user
  - resume setup immediately after the human-only step
  - record IDs, env names, and verification commands in docs

## Browser QA

- Document the preferred local browser path for this repo.
- If auth blocks agent-driven QA, provide a safe local bypass or isolated Playwright server pattern.
- Capture whether Playwright should hit an existing user-run app or its own isolated dev server.
- When the user needs real login state, prefer a dual-lane setup:
  - user lane in real Chrome
  - agent lane in Playwright or a localhost bypass copy

## High-Risk Paths

- [List auth, billing, migrations, webhook, cron, queue, or destructive paths here]

## Safety

- Never run destructive commands without confirmation.
- Never stage or commit secrets, `.env*`, private keys, or credential files.
- Never stage unrelated changes.
- Never claim success unless the relevant checks were actually run.

## Delivery Contract

- Report exact commands run and pass/fail outcomes.
- If checks were skipped, say exactly which and why.
- If blocked after focused attempts, report the blocker and next best path.
- For high-risk changes, include risk notes and rollback notes in handoff.
