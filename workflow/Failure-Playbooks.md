# Failure Playbooks

> Fast recovery procedures for common multi-model workflow failures.

---

## 1) Context Rot in Long Sessions

**Trigger**
- Agent starts ignoring constraints, repeats failed patterns, or edits unrelated files.

**Immediate Actions**
1. Stop current session.
2. Capture latest stable state in `WORKLOG.md`.
3. Start a fresh session with minimal context: goal, constraints, changed files, and next phase only.

**Recovery Checklist**
1. Regenerate or tighten `PLAN.md` for the current phase.
2. Re-run only required tests for touched files first.
3. Resume full gate once focused tests pass.

**Prevention**
1. Keep sessions phase-scoped.
2. Reset sessions after major milestones.
3. Prefer shared files (`PLAN.md`, `tasks.json`) over long conversational history.

---

## 2) Quality Gate Failure Loop

**Trigger**
- `lint`, `test`, or `build` fails repeatedly.

**Immediate Actions**
1. Record exact failing command and error snippet.
2. Apply the smallest safe fix.
3. Re-run the failed command, then re-run full required gates.

**Recovery Checklist**
1. If failure persists after 3 focused attempts, stop and isolate root cause.
2. Ask architect model (Claude) for targeted diagnosis only.
3. Resume implementation after root cause is confirmed.

**Prevention**
1. Build and test in smaller increments.
2. Add missing tests before extending functionality.
3. Avoid stacking unrelated refactors in one diff.

---

## 3) Migration / Schema Drift

**Trigger**
- Runtime errors after schema changes, type mismatches, or broken contracts.

**Immediate Actions**
1. Stop feature work.
2. Verify migration order and applied state.
3. Validate corresponding type/validator/API updates.

**Recovery Checklist**
1. Reconcile schema source of truth.
2. Add/repair migration with monotonic order.
3. Run targeted data-contract tests.
4. Re-run `build` and type checks.

**Prevention**
1. Treat schema changes as a standalone phase.
2. Require contract tests for migrations.
3. Keep runtime validators close to schema changes.

---

## 4) Reviewer Disagreement (Gemini vs Claude vs Codex)

**Trigger**
- Reviewers provide contradictory recommendations.

**Immediate Actions**
1. Classify disagreement: correctness, architecture, or style.
2. Prioritize correctness and security over style.
3. Escalate only unresolved correctness conflicts to human decision.

**Recovery Checklist**
1. Create a short decision note in `WORKLOG.md`.
2. Implement selected direction.
3. Re-run review with an explicit prompt anchored to chosen constraints.

**Prevention**
1. Use consistent review prompt structure.
2. Keep acceptance criteria explicit in `PLAN.md`.
3. Avoid vague goals like "clean this up".

---

## 5) Jules PR Merge Conflicts

**Trigger**
- Multiple Jules agents produce overlapping PRs.

**Immediate Actions**
1. Pause non-critical scheduled agents.
2. Merge the highest-priority PR first.
3. Rebase remaining PR branches and resolve conflicts manually.

**Recovery Checklist**
1. Validate conflict resolutions locally with full quality gate.
2. Close stale/conflicting low-value PRs.
3. Resume schedules with staggered run windows.

**Prevention**
1. Stagger scheduled agents by at least 30-60 minutes.
2. Limit concurrent agents touching same domain.
3. Keep each agent focused on a narrow responsibility.

---

## 6) Flaky E2E or CI Instability

**Trigger**
- E2E tests fail non-deterministically across runs.

**Immediate Actions**
1. Re-run failed suite once to confirm flake.
2. Capture failing test artifacts/logs.
3. Quarantine known flaky test with explicit tracking issue.

**Recovery Checklist**
1. Add deterministic waits/state setup.
2. Isolate external dependencies with mocks or fixtures.
3. Re-enable quarantined test once stabilized.

**Prevention**
1. Keep smoke E2E small and deterministic.
2. Use stable test data and controlled seeds.
3. Run periodic flake audits in maintenance windows.
