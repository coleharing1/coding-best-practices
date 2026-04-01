# Environment Parity And Prod Safety

## Goal

Keep development fast without normalizing risky production behavior.

## Core Rules

1. Prefer read-only production inspection by default.
2. Use explicit parity checks between dev and prod when schema or capability surfaces matter.
3. Guard any production write path behind an explicit confirmation command or separate script.
4. Document environment IDs, hosts, and access posture in `AGENTS.md` or `CLAUDE.md`.

## What To Document Per Repo

- dev environment identifier
- prod environment identifier
- whether prod is read-only by default
- parity command
- guarded prod-write command

## Safe Patterns

- `schema:diff` between environments
- `schema:parity --strict` before release
- separate `db:push:dev` and `db:push:prod:confirm` scripts
- prod health checks that do not mutate state

## Unsafe Patterns

- one command that writes to whichever environment happens to be linked
- undocumented prod credentials in local shells
- migration flows that assume prod and dev drift is small

## Release Discipline

Before a risky release:

1. Run required local gates.
2. Run parity checks if schema/capability surfaces changed.
3. Confirm rollback path.
4. Update worklog and runbooks if operator behavior changed.

## Recommendation

Treat prod safety as a documented workflow, not a personal habit.
