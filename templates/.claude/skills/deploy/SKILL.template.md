---
name: deploy-checklist
description: >
  Pre-deployment validation. Use when the user is about to deploy, push to
  production, create a release, or mentions "ship it" / "deploy" / "go live".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Deploy Checklist

Run through the pre-deployment checklist before pushing to production.

## Checks

1. **Quality Gate**
   - Run lint: `npm run lint`
   - Run tests: `npm run test -- --run`
   - Run build: `npm run build`
   - All must pass with zero errors

2. **Environment**
   - Verify all required env vars are documented in `.env.local.example`
   - Confirm no secrets are hardcoded in source files
   - Check that env vars referenced in code exist in the deployment platform

3. **Database**
   - Are there pending migrations? If so, flag them
   - Do migrations have rollback strategies?
   - Are there breaking schema changes that need coordination?

4. **Dependencies**
   - Are there any known vulnerable dependencies? (`npm audit`)
   - Are lock files (`package-lock.json` / `yarn.lock`) committed?

5. **WORKLOG.md**
   - Is the latest entry up to date?
   - Are follow-ups from previous entries resolved?

## Output

- List of checks with pass/fail status
- Any blockers that must be resolved before deploy
- Final verdict: `clear to deploy` or `blocked — fix required`
