# AI Quality Gate SOP (Pre-`git add`, `commit`, `push`)

> Last updated: April 1, 2026
> Role in workflow: Phase 4 (Quality Gate)

## Goal

Prevent avoidable regressions by forcing a deterministic gate before staging, commit, or push.

## Non-Negotiable Rules

1. Do not stage or commit until required checks pass.
2. Do not stage unrelated changes.
3. Do not hide skipped checks.
4. Do not commit secrets or credential material.
5. Do not treat production write paths as normal local verification.

## Step 0: Classify Risk

Pick a tier from `workflow/Risk-Tier-Matrix.md`.

- `T0` -- docs/meta only
- `T1` -- localized low-risk runtime change
- `T2` -- multi-file behavior/contract change
- `T3` -- security/data-critical/high-blast change

## Step 1: Review Before Mechanical Gates

- Run Gemini structural review on non-trivial diffs.
- For `T3`, also run a logic/security review in Claude.

## Step 2: Inspect Current State

Run:

```bash
git status --short --branch
git diff --name-only
git diff --name-only --cached
```

## Step 3: Run Required Gates

Standard baseline:

```bash
npm run lint
npm run test -- --run
npm run build
```

Or use:

```bash
scripts/quality-gate.sh --risk-tier T2
```

## Step 4: Run Conditional Gates

Use path- and change-aware checks:

- browser/E2E when UI or critical flows changed
- typecheck when contracts, schema, or large refactors changed
- parity checks when schema or capability surfaces changed

See:

- `workflow/Browser-QA-Playbook.md`
- `workflow/Environment-Parity-and-Prod-Safety.md`
- `workflow/Schema-Sync-Recipes.md`

## Step 5: Update Context Files

Before staging:

1. Add or update the top `WORKLOG.md` entry when meaningful behavior/process changed.
2. Update `README.md` if setup, routes, env, or status claims changed.
3. Update `DEBUG-JOURNAL.md` if significant debugging/investigation happened.
4. Update runbooks/browser docs if operator workflows changed.

## Step 6: Secret And Staging Hygiene

Run:

```bash
git status --short
git diff --staged --name-only
git diff --staged
```

Stage explicitly:

```bash
git add <file1> <file2> ...
```

## Step 7: Commit Gate

Commit only when:

1. required checks passed
2. conditional checks were passed or explicitly skipped
3. docs are current
4. staged diff matches intended scope
5. no secrets are present

## Step 8: Push Gate

Before push:

1. inspect `git show --name-only --stat HEAD`
2. confirm branch target
3. for `T3`, confirm rollback notes and any operator/runbook updates

## Failure-Repair Loop

When any gate fails:

1. capture the exact failing command
2. make the smallest safe fix
3. rerun the failed command
4. rerun the required baseline gates
5. after 3 focused attempts, stop and isolate root cause

## Definition Of Done

A change is ready to push only when:

1. review happened at the right depth for the risk tier
2. required gates passed
3. conditional gates/parity checks were handled correctly
4. context docs reflect reality
5. the staged diff is scoped and safe
