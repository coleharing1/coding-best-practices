# Failure Playbooks

> Fast recovery procedures for common multi-model workflow failures.

## 1) Context Rot In Long Sessions

**Trigger**
- the agent starts ignoring constraints, repeating failed patterns, or touching unrelated files

**Immediate Response**
1. stop the session
2. capture stable intent in `WORKLOG.md`
3. restart with only goal, constraints, touched files, and next phase

## 2) Quality Gate Failure Loop

**Trigger**
- `lint`, `test`, or `build` keeps failing

**Immediate Response**
1. capture exact failing command and error
2. make the smallest safe fix
3. rerun failed command, then rerun required gates

## 3) Migration / Schema Drift

**Trigger**
- runtime breaks after schema or contract changes

**Immediate Response**
1. stop feature work
2. verify every schema-sync layer that should have changed
3. run parity or contract checks before more edits

## 4) Production / Service Outage Confusion

**Trigger**
- app behavior looks broken, but the real issue may be upstream service instability

**Immediate Response**
1. separate app-side symptoms from project/service-side health
2. run direct health checks, not just UI checks
3. capture the result in `DEBUG-JOURNAL.md` or `WORKLOG.md`

## 5) Browser Harness Blocked

**Trigger**
- Playwright/browser MCP is blocked by auth, Chrome state, or local port conflicts

**Immediate Response**
1. switch to the documented fallback path
2. use isolated Playwright server or auth-bypass copy if available
3. capture artifacts from the failing path before changing strategy

## 6) Reviewer Disagreement

**Trigger**
- Gemini, Claude, or Codex give conflicting advice

**Immediate Response**
1. classify the conflict as correctness, security, architecture, or style
2. prioritize correctness/security
3. record the decision briefly in `WORKLOG.md`

## 7) Donor-Port Regression

**Trigger**
- a donor-repo port works in isolation but breaks because the receiving repo has different assumptions

**Immediate Response**
1. compare the donor assumptions directly
2. identify what is tenant-, auth-, or data-shape-specific
3. document intentional divergence before continuing

## 8) Flaky E2E Or CI Instability

**Trigger**
- E2E fails non-deterministically

**Immediate Response**
1. rerun once to confirm flake
2. capture screenshots/traces/logs
3. quarantine only if it blocks all progress
