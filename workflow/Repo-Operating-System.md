# Repo Operating System

> The repo operating system is the set of files, rules, and habits that let a project regain context quickly and stay stable across many AI sessions.

## Goal

Make the repo easy to rehydrate, safe to change, and readable by both humans and AI tools.

## Minimum Layer

Every serious repo should start with:

1. `README.md`
2. `WORKLOG.md`
3. `CLAUDE.md`
4. `AGENTS.md`
5. `plans/active/` and `plans/archive/`
6. `.cursor/rules/`
7. `.claude/commands/` and `.claude/rules/` when Claude Code is in the loop

## Optional But High-Value Layers

Add these when the repo grows in complexity:

- `DEBUG-JOURNAL.md`
  Use when debugging spans sessions, external services, or false starts.

- `TESTING_AND_BROWSER_AUTOMATION.md`
  Use when the repo has more than one QA path and people need to know which to use.

- `knowledgebase/`
  Use when business logic, donor architecture, or product direction should survive beyond one feature plan.

- `knowledgebase/10-implementation-checklist.md`
  Use when the project needs an owner-tagged checklist with gates across many phases.

- `runbooks/`
  Use when operators need explicit procedures for auth, onboarding, health checks, or setup.

## What Each File Does

| File/Folder | Job |
|---|---|
| `README.md` | Current product truth |
| `WORKLOG.md` | Durable implementation memory |
| `CLAUDE.md` | Planner/reviewer context |
| `AGENTS.md` | Builder instructions |
| `plans/` | Decision history and active execution source of truth |
| `DEBUG-JOURNAL.md` | Investigation memory |
| `TESTING_AND_BROWSER_AUTOMATION.md` | Browser/testing quick reference |
| `knowledgebase/` | Stable architecture/business context |
| `knowledgebase/10-implementation-checklist.md` | Cross-phase owner-tagged execution tracker |
| `runbooks/` | Operator procedures |

## Operating Principles

1. Docs are part of the product.
2. Update context during the work, not after memory fades.
3. Let `README.md` describe current reality, not aspirational roadmap.
4. Let `WORKLOG.md` record intent, verification, and follow-ups that git does not preserve.
5. Keep planning docs and operational docs separate.

## Healthy Repo Signals

- A new session can find the current milestone in under 2 minutes.
- Exact commands and expected outcomes are documented.
- High-risk areas are named explicitly.
- Browser QA path is documented.
- Service-login handoff path is documented.
- Production write paths are guarded and obvious.

## Unhealthy Repo Signals

- Commands only exist in chat history.
- Debugging knowledge lives only in one person's memory.
- `README.md` describes the repo six weeks ago.
- The AI tool keeps using the wrong paths because context files are stale.

## Recommendation

Treat repo operating-system work as foundational infrastructure, not documentation chores.
