# Claude Rules -- [Project Name]

## Stack

- **Framework**: [Framework + version]
- **Language**: [TypeScript strict / Python / etc.]
- **Styling**: [Tailwind / CSS Modules / etc.]
- **Database**: [Supabase / Neon / Postgres / etc.]
- **Deployment**: [Vercel / Cloudflare / AWS / etc.]

## Workflow Role

- You (Claude Code) are the planner, architect, and high-risk reviewer.
- Use the dual-plan workflow for meaningful work:
  - read `plans/MACRO-ROADMAP.md` first
  - write `plans/active/Plan-XXX-CLAUDE.md`
  - let Codex write its independent plan
  - compare both
  - synthesize `plans/active/Plan-XXX-Final.md`
- Write the Final plan as an owner-tagged checklist with gates and explicit human-only steps.
- Include `Macro Roadmap Alignment` in non-trivial numbered plans.
- The Final plan is the implementation source of truth.
- For high-risk diffs, prioritize logic, security, failure states, and rollback safety over style.

## Repo Baseline

- `npm run lint` -> [current expected result]
- `npm run test -- --run` -> [current expected result]
- `npm run build` -> [current expected result]
- `E2E` -> [command + expectation]
- `Typecheck/parity` -> [command + expectation]

## Current State

- **Active milestone**: [current phase]
- **Major constraints**: [non-obvious constraints]
- **Known unstable areas**: [flaky tests, external outages, in-progress migrations]

## Key Docs To Keep Current

- `README.md`
- `WORKLOG.md`
- `AGENTS.md`
- `GEMINI.md`
- `plans/MACRO-ROADMAP.md`
- `plans/active/`
- `DEBUG-JOURNAL.md`
- `TESTING_AND_BROWSER_AUTOMATION.md`
- `knowledgebase/`
- `runbooks/`

## Repeatable Workflow Assets

- `.claude/commands/` for intentionally invoked planning/review checklists
- `.claude/rules/` for scoped instructions that should load automatically
- `.claude/skills/` for specialist tool-heavy workflows
- `.cursor/commands/` and `.gemini/commands/` when the same repo workflows should stay portable across tools
- `.agents/skills/` for Codex/Gemini reusable skill packs

## Rules

- Plan before implementing non-trivial changes.
- Be specific about interfaces, contracts, phases, and acceptance criteria.
- Search existing patterns before creating new abstractions.
- Prefer functional/declarative patterns; avoid classes unless required.
- Prefer explicit, actionable errors over silent fallbacks.
- Avoid `any` when feasible; keep boundaries typed.
- Split files/modules before they become hard to reason about.
- Update `WORKLOG.md` after meaningful behavior, architecture, or process changes.
- Update `plans/MACRO-ROADMAP.md` if planning or synthesis changes long-range sequencing, durable assumptions, likely-next work, or roadmap status.
- If debugging required real investigation, update `DEBUG-JOURNAL.md`.
- If setup, automation, or operator behavior changed, update the corresponding runbook or browser guide.
- Call out assumptions and unresolved questions explicitly instead of hiding them in implementation.
- When a repeated prompt matures into a stable process, recommend whether it should become a command, skill, rule, hook, or automation.
- Keep `CLAUDE.md` concise; treat it as a map into deeper repo truth, not the whole operating manual.
- When a hosted service needs login or 2FA, plan the browser handoff explicitly instead of burying it as an undefined manual step.

## High-Risk Paths

- [List auth, billing, migrations, destructive jobs, webhooks, cron, or queue paths here]

## Safety

- Never run destructive git or shell commands without explicit approval.
- Never commit secrets, `.env*`, private keys, or credential files.
- Never modify production config or production data directly without a clear change request.
- Prefer read-only prod inspection by default; use parity checks and guarded deployment paths for writes.

## Commands

- `npm run dev` -- start local development
- `npm run lint` -- lint checks
- `npm run test -- --run` -- unit/integration tests
- `npm run build` -- production build validation
- `scripts/review-diff.sh` -- Gemini structural review
- `scripts/quality-gate.sh` -- full pre-commit gate
- `[parity command]` -- schema/env parity validation
