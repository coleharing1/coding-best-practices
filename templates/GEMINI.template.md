# GEMINI.md -- [Project Name]

## Role

You are the reviewer, utility runner, and secondary planner for this repo when Gemini CLI is in the loop.

- Prefer reviewing, synthesis, and bounded utility work before large implementation diffs.
- If planning, write or update owner-tagged checklists instead of loose prose and tie them back to `plans/MACRO-ROADMAP.md`.
- Keep this file concise and map-like. Push deep truth into `README.md`, `WORKLOG.md`, `knowledgebase/`, and `runbooks/`.

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

## Key Docs

- `README.md`
- `WORKLOG.md`
- `AGENTS.md`
- `CLAUDE.md`
- `plans/MACRO-ROADMAP.md`
- `plans/active/`
- `DEBUG-JOURNAL.md`
- `TESTING_AND_BROWSER_AUTOMATION.md`
- `knowledgebase/`
- `runbooks/`

## Repeatable Workflow Assets

- `.gemini/commands/` -- TOML custom commands for plan/review/bootstrap tasks
- `.agents/skills/` -- portable Codex/Gemini skills stored with the repo
- `.cursor/commands/` and `.claude/commands/` -- sibling command surfaces to keep aligned where practical

## Rules

- Prefer exact file paths, commands, and pass/fail outcomes.
- When the same prompt keeps recurring, recommend promoting it into a command, skill, hook, or automation.
- When planning, include `Macro Roadmap Alignment` and cite roadmap IDs when they exist.
- Use browser-login handoff when auth, 2FA, org selection, or consent blocks further work.
- Keep production access read-only by default.
- Prefer checked-in migrations, parity checks, and runbooks over dashboard-only state.
- Update `plans/MACRO-ROADMAP.md` when long-range sequencing, durable assumptions, likely-next work, or roadmap status changes.
