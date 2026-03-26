---
description: Run the full pre-commit quality gate
---

## Quality Gate — Pre-Commit Check

Run all checks sequentially. Stop and fix on first failure.

!`npm run lint 2>&1 || echo "GATE FAILED: lint"`

!`npm run test -- --run 2>&1 || echo "GATE FAILED: tests"`

!`npm run build 2>&1 || echo "GATE FAILED: build"`

## Post-Gate

If all checks passed:
1. Confirm no secrets in staged files: `git diff --cached --name-only | grep -E '\.(env|key|pem|secret)'`
2. Verify WORKLOG.md is updated for this change
3. Report: **Gate passed — ready to commit**

If any check failed:
1. Identify the root cause
2. Apply the smallest safe fix
3. Re-run the failing check
4. Do not attempt more than 3 fix cycles — escalate if stuck
