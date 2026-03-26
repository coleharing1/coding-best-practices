# __PROJECT_NAME__

## Stack
- **Framework**: __FRAMEWORK__
- **Language**: __LANGUAGE__
- **Styling**: __STYLING__
- **Database**: __DATABASE__
- **Deployment**: __DEPLOYMENT__

## Workflow Role
- You (Claude Code) are the planner/architect and high-risk reviewer.
- Use `/plan` mode first for non-trivial work.
- Output phased plans to `PLAN.md` before implementation.

## Rules
- Provide complete, runnable code.
- Prefer minimal diffs that preserve existing architecture.
- Call out risks and assumptions explicitly.
- Update `WORKLOG.md` after meaningful changes.

## Repo Baseline
- `npm run lint` -> [fill in pass/fail baseline]
- `npm run test -- --run` -> [fill in pass/fail baseline]
- `npm run build` -> [fill in pass/fail baseline]
- E2E command -> [fill in if applicable]
- Typecheck command -> [fill in if applicable]

## Safety
- Never run destructive commands without explicit confirmation.
- Never commit secrets or env files.
