# Brownfield Adoption Guide

> Last updated: February 25, 2026
> Role in workflow: Phase 0.5 (Onboard Existing Repos) — between bootstrap and planning
> Audience: Solo developers adopting this workflow in an already-active codebase

---

## Goal

Adopt the multi-model workflow in an existing repository without disrupting shipping velocity or rewriting project conventions.

This guide is for projects where:
- The repo already has production code and history
- You cannot pause development for a full process migration
- You need a safe, incremental rollout

---

## Success Criteria

Brownfield adoption is successful when all of the following are true:
1. The repo has stable context files (`WORKLOG.md`, `CLAUDE.md`, `AGENTS.md`) with real project commands.
2. The quality gate runs reliably for normal changes.
3. At least one production-facing feature shipped using the full Plan -> Execute -> Review -> Gate loop.
4. Team habits changed without introducing process drag.

---

## Day 0: 45-Minute Baseline Audit

Before adding any AI workflow files, capture the current reality:

1. Repo state
- Default branch strategy (`main` direct push vs PR-only)
- Existing CI status (green/red/flaky)
- Known "do not touch" areas

2. Commands that actually work today
- Lint command
- Unit/integration test command
- Build command
- Optional E2E command
- Optional typecheck command

3. Risk map
- High-risk domains (auth, billing, migrations, webhooks, data deletion)
- Critical paths that must not regress

Write this into a short "Repo Baseline" section in `CLAUDE.md` and `AGENTS.md`.

---

## Day 1: Add Minimum Context Layer

Add these files without changing application logic:

1. `WORKLOG.md`
- Start with `Entry 001 — Workflow Adoption Baseline`
- Record verified commands, risk areas, and known flaky tests

2. `CLAUDE.md`
- Include stack, architecture constraints, and role split
- Include high-risk areas and required review expectations

3. `AGENTS.md`
- Include exact runnable commands
- Include hard constraints (no destructive commands, no secret commits, one phase at a time)

4. `.cursor/rules/` and `.claude/commands/` / `.claude/rules/` when relevant
- Keep rules short and enforce only non-controversial constraints first
5. Service bootstrap docs when the repo depends on hosted services
- Add `TESTING_AND_BROWSER_AUTOMATION.md`, runbooks, or a service handoff note before the next browser/auth-heavy task

Use `workflow/New-Project-Setup-Guide.md` plus the relevant files in `templates/` from this repo when possible.

---

## Day 2: Enable Quality Gate Safely

1. Run a dry run on a small branch:
- `scripts/review-diff.sh`
- `scripts/quality-gate.sh` (or the repo's equivalent if you have not adopted this script yet)

2. Fix command drift:
- If lint/test/build commands fail due to stale scripts, update commands in `AGENTS.md` and `CLAUDE.md` first.

3. Only then wire CI:
- Add `templates/.github/workflows/quality-gate.template.yml` to the target repo as its starting point
- Keep it non-blocking for one week if CI is currently unstable

---

## Day 3+: Rollout Levels

Choose one rollout level and upgrade later:

### Level A (Low Friction)
- Claude plans
- Codex builds
- Gemini review for medium/high-risk changes only
- Required gates: lint + test + build

### Level B (Standard)
- Gemini review on every non-trivial diff
- Risk tiers enforced (`workflow/Risk-Tier-Matrix.md`)
- Conditional checks (E2E + typecheck) enabled

### Level C (Strict)
- Automated review hooks/aliases
- CI gate is blocking for PR merge
- Weekly metrics + weekly retrospective required

---

## Brownfield Migration Strategy (Do Not Big-Bang)

Use the "one pilot feature" approach:
1. Pick a medium-risk feature (not auth/billing/migrations).
2. Run full workflow end-to-end on that feature.
3. Capture friction in `WORKLOG.md`.
4. Update docs/templates/scripts once.
5. Repeat for a high-risk feature.

Avoid "rewrite all process docs first." Adopt via real changes.

---

## Failure Modes and Fixes

1. "The workflow is too heavy"
- Usually caused by unclear risk thresholds.
- Fix: adopt risk tiers and skip heavy checks for T0/T1 changes.

2. "The AI keeps using wrong commands"
- Usually stale context files.
- Fix: centralize commands in `AGENTS.md` + `CLAUDE.md` and keep them current.

3. "CI blocks too often"
- Usually flaky tests treated as stable gates.
- Fix: classify flaky suites explicitly and move them to conditional/manual until stable.

4. "Reviews are noisy"
- Usually prompt drift.
- Fix: use `prompts/` templates and tighten review scope by risk tier.

---

## Brownfield Checklist

- [ ] Baseline commands verified locally
- [ ] `WORKLOG.md` created with adoption entry
- [ ] `CLAUDE.md` and `AGENTS.md` populated with real commands
- [ ] Cursor rules added for the current repo realities
- [ ] Service login / bootstrap path documented if the repo depends on hosted tools
- [ ] `scripts/review-diff.sh` works in repo
- [ ] `scripts/quality-gate.sh` runs end-to-end
- [ ] CI quality-gate workflow added
- [ ] Risk tiers documented and adopted
- [ ] Weekly metrics + retro loop started

---

## Exit Criteria (Adoption Complete)

You are done with brownfield adoption when:
1. New feature work naturally uses this workflow without reminders.
2. Contributors can onboard using docs/templates alone.
3. Quality gate failures are mostly real defects, not process noise.
