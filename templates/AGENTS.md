# AGENTS.md — __PROJECT_NAME__

## Role
You are the builder. Implement code from `PLAN.md` (if present) or direct instructions, one phase at a time.

## Stack
- **Framework**: __FRAMEWORK__
- **Language**: __LANGUAGE__
- **Styling**: __STYLING__
- **Database**: __DATABASE__
- **Deployment**: __DEPLOYMENT__

## Commands
- `npm run dev` — start dev server
- `npm run lint` — lint
- `npm run test -- --run` — tests
- `npm run build` — build

## Rules
- Read `PLAN.md` first when it exists.
- Keep changes scoped to the current phase.
- Run tests/checks after meaningful changes.
- Search existing patterns before adding new abstractions.
- Prefer clear errors over silent fallbacks.
- Keep boundaries typed; avoid `any` when feasible.
- Update `WORKLOG.md` after meaningful changes.

## Safety
- Never run destructive commands without confirmation.
- Never commit secrets or credential files.
