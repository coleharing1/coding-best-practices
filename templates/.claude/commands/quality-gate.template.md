---
description: Run the full pre-commit quality gate
---

## Quality Gate — Pre-Commit Check

Prefer the repo script so review, conditional gates, and secret scan stay consistent.

!`scripts/quality-gate.sh --risk-tier T2 2>&1 || echo "GATE FAILED"`

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
