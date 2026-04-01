# Templates

Use this folder to bootstrap the repo operating system around a project, not just its code.

## Canonical Template Rule

The source-of-truth templates in this repo use `*.template.*` naming.

- `AGENTS.template.md`
- `CLAUDE.template.md`
- `GEMINI.template.md`
- `PLAN.template.md`
- `WORKLOG.template.md`
- `DEBUG-JOURNAL.template.md`
- `TESTING_AND_BROWSER_AUTOMATION.template.md`

If you copy a file into a live project, remove `.template` from the filename.

## Core Bootstrap Set

Start almost every repo with:

1. `README.md`
2. `WORKLOG.md`
3. `CLAUDE.md`
4. `AGENTS.md`
5. `GEMINI.md` when Gemini CLI is in the loop
6. `plans/`
7. `.cursor/rules/` and `.cursor/commands/` when Cursor is part of the workflow
8. `.claude/commands/`, `.claude/rules/`, and optional `.claude/skills/` when Claude Code is part of the workflow
9. `.gemini/commands/` and optional `.gemini/settings.json` when Gemini CLI is part of the workflow
10. `.agents/skills/` when you want portable Codex/Gemini skills
11. `.env.local.example`

## Repeatable Actions Layer

Treat repeatable actions as repo assets, not chat habits:

- commands for checklists you invoke on purpose
- skills for tool-heavy or cross-project workflows
- hooks/rules for guardrails and automatic behavior
- automations/background agents for bounded recurring chores
- review configuration files such as `.cursor/BUGBOT.md` when review noise needs shaping

See `workflow/Repeatable-Actions-Stack.md`.

## Add These When The Repo Needs More Operating Structure

- `DEBUG-JOURNAL.md`
  Use when debugging work routinely involves false starts, external outages, or multi-session investigations.

- `TESTING_AND_BROWSER_AUTOMATION.md`
  Use when the repo has multiple QA paths and you want one quick operator-facing reference.

- `knowledgebase/`
  Use for larger systems where business context, architecture direction, or open decisions need to survive across many sessions.

- `knowledgebase/10-implementation-checklist.md`
  Use when you want a long-running owner-tagged checklist with gates instead of a loose status doc.

- `runbooks/`
  Use when the system has operators, invite flows, onboarding, incidents, or service setup that should not live only in code comments.

- `.github/workflows/`
  Use when you want CI parity for quality gate, schema parity, or external health checks.

## Starter Kits

If you know the repo shape up front, start with an archetype kit in `templates/archetypes/`:

- `analytics-warehouse`
- `dual-stack-platform`
- `internal-ops-dashboard`
- `ai-media-saas`

Each kit explains what to copy first, what extra docs to add, and what safety/verification patterns matter most.
