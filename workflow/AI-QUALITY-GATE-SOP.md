# AI Quality Gate SOP (Pre-`git add`, `commit`, `push`)

> Last updated: February 24, 2026
> Role in workflow: Phase 4 (Quality Gate) — see `Multi-Model-Workflow.md`
> Audience: Any coding LLM agent (Cursor, Claude Code, Codex, etc.)

## Goal

Prevent avoidable regressions by forcing a deterministic quality gate before any staging, commit, or push. This SOP applies regardless of which tool wrote the code.

## Non-Negotiable Rules

1. Do not run `git add`, `git commit`, or `git push` until all required checks pass.
2. Do not stage unrelated changes.
3. Do not stage secrets (`.env.local`, keys, tokens, private certs).
4. If a check fails, fix first, then rerun checks.
5. If a check is flaky or timing out, report it explicitly in the final handoff.

## Repo Baseline Template

Before relying on this SOP for a new project, establish the current baseline. Record these in your `CLAUDE.md` or `AGENTS.md`:

1. What lint command passes and its expected state.
2. What test command passes, how many files/tests.
3. What build command passes and any expected warnings.
4. Whether E2E tests exist and what base URL they expect.
5. Whether `tsc --noEmit` runs and how long it takes.

**Example baseline (fill in per project):**

```markdown
## Repo Baseline
- `npm run lint` passes.
- `npm run test -- --run` passes (X files, Y tests).
- `npm run build` passes (known warnings: [list any]).
- E2E: `PLAYWRIGHT_BASE_URL=http://127.0.0.1:3000 npm run test:e2e` passes Z tests.
- `npx tsc --noEmit` passes (may need timeout handling on large projects).
```

## Standard Workflow

### Step 0: Gemini Review (Recommended)

Before running the mechanical gates, pipe your diff through Gemini CLI for a structural review. This catches architectural issues that lint/test/build cannot:

```bash
git diff | gemini --model gemini-3-pro-preview -p "Review this diff for:
- Structural issues (functions doing too many things, missing separation of concerns)
- Cross-file invariant violations
- Race conditions or concurrency issues
- Patterns that deviate from the rest of the codebase
Be specific: cite file names and line ranges."
```

Fix anything worth fixing before proceeding. For high-risk changes (auth, payments, data models), also paste the diff into Claude Code for a logic/security audit. See `Multi-Model-Workflow.md` Phase 3 for the full review protocol.

### Step 1: Inspect Current State

Run:

```bash
git status --short --branch
git diff --name-only
git diff --name-only --cached
```

Then classify changed files by area (adapt to your project):

1. UI / pages / components / hooks
2. API / server logic
3. Database migrations / types
4. Config / CI / deployment
5. Docs only

### Step 2: Always-Run Required Gates

Run in this order:

```bash
npm run lint
npm run test -- --run
npm run build
```

If any command fails, stop and enter the fix loop (see Failure-Repair Loop below).

### Step 3: Diff-Aware Conditional Gates

Run extra checks based on changed paths:

1. **If UI/frontend files changed**, run E2E smoke tests:
```bash
PLAYWRIGHT_BASE_URL=http://127.0.0.1:3000 npm run test:e2e
```

2. **If auth-required E2E coverage is needed**, add credentials:
```bash
PLAYWRIGHT_TEST_EMAIL=... PLAYWRIGHT_TEST_PASSWORD=... PLAYWRIGHT_BASE_URL=http://127.0.0.1:3000 npm run test:e2e
```

3. **If types, validators, core API contracts, or large refactors changed**, run TypeScript check with timeout:
```bash
timeout 120 npx tsc --noEmit
```

If timeout is hit, note this explicitly in handoff and continue only if required gates already passed.

### Step 4: Migration/Schema Safety (When Relevant)

If database migration files changed:

1. Verify migration naming order and timestamp monotonicity.
2. Verify associated runtime/type updates (database types, API contracts, validators).
3. Verify tests cover the changed contract.

### Step 5: Worklog + Docs Update

Before staging, ensure worklog context is updated when behavior changed:

1. Add a new top entry in `WORKLOG.md` (single source of truth).
2. Keep entry format consistent (`Entry XXX`, goal, changes, notes, follow-ups).
3. Update README only if scripts/routes/env/checks changed.

### Step 6: Secret and Staging Hygiene

Run:

```bash
git diff | rg -n "API_KEY|SECRET|TOKEN|PRIVATE KEY|BEGIN .*PRIVATE KEY" || true
git status --short
```

Stage explicitly (never blind `git add .` for mixed changes):

```bash
git add <file1> <file2> ...
git diff --staged --name-only
git diff --staged
```

### Step 7: Commit Gate

Only commit when all apply:

1. Required gates are green.
2. Staged diff matches intended scope.
3. No secrets/sensitive data.
4. Worklog/doc updates done when required.

Commit with scoped message:

```bash
git commit -m "feat(auth): add password validation and session refresh"
```

### Step 8: Push Gate

Run final verification:

```bash
git show --name-only --stat HEAD
git push origin <branch>
```

If on `main` and project policy expects PR flow, push to feature branch and open PR instead.

## Failure-Repair Loop (Mandatory)

When any gate fails:

1. Capture failing command and exact error.
2. Make the smallest safe fix.
3. Rerun failed command.
4. Rerun all required gates (`lint`, `test`, `build`) before staging.
5. If still failing after 3 focused attempts, stop and report blocker clearly.

## LLM Execution Contract

When acting as the coding agent, follow this contract:

1. Announce what checks you will run.
2. Run commands and report concise pass/fail outcomes.
3. Never hide skips (state exactly what was skipped and why).
4. Never claim "all good" unless required gates were executed and passed.
5. Include exact commands used in final handoff.

## Tool-Specific Automation Pattern (Feb 2026)

Use these capabilities as a second layer, not a replacement for local gates:

1. **Cursor:**
   - Use `AGENTS.md`/Rules to enforce this SOP.
   - Use Cloud Agent/Bugbot for PR-level review and autofix workflows.
2. **Claude Code:**
   - Use hooks (`PreToolUse`, `PostToolUse`, `Stop`, etc.) to auto-run lint/test/build checks and block unsafe operations.
3. **Codex:**
   - Use `AGENTS.md` + Skills for local behavior.
   - Use `openai/codex-action` in CI for PR review automation with controlled sandbox/approval settings.

## Definition of Done

A change is ready to push only when:

1. Gemini review completed (or explicitly justified as skipped for trivial changes).
2. Required checks passed.
3. Conditional checks were either passed or explicitly justified as skipped.
4. Diff is scoped and secret-safe.
5. Commit message is clear and scoped.
6. Push target is correct for branch policy.

## References (External, Reviewed February 2026)

1. Cursor Rules + AGENTS docs: `https://cursor.com/docs/context/rules`
2. Cursor Cloud Agents docs: `https://cursor.com/docs/cloud-agent`
3. Cursor Bugbot docs: `https://cursor.com/docs/bugbot`
4. Cursor CLI docs: `https://cursor.com/docs/cli/overview`
5. Cursor changelog: `https://cursor.com/changelog`
6. Anthropic Claude Code hooks: `https://docs.anthropic.com/en/docs/claude-code/hooks`
7. Anthropic Claude Code settings: `https://docs.anthropic.com/en/docs/claude-code/settings`
8. Anthropic Claude Code memory: `https://docs.anthropic.com/en/docs/claude-code/memory`
9. Anthropic Claude Code GitHub Actions: `https://docs.anthropic.com/en/docs/claude-code/github-actions`
10. OpenAI Codex AGENTS guide: `https://developers.openai.com/codex/guides/agents-md`
11. OpenAI Codex security/sandbox: `https://developers.openai.com/codex/security`
12. OpenAI Codex skills: `https://developers.openai.com/codex/skills`
13. OpenAI Codex launch post (Feb 2, 2026): `https://openai.com/index/introducing-codex/`
14. Codex GitHub Action: `https://github.com/openai/codex-action`
