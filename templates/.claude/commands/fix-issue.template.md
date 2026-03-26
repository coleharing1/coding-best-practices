---
description: Investigate and fix a GitHub issue
argument-hint: [issue-number]
---

## Issue Details

!`gh issue view $ARGUMENTS`

## Steps

1. Read the issue above and understand the reported problem.
2. Trace the root cause in the codebase — check related files, recent changes, and error paths.
3. Implement the minimal fix that resolves the issue without side effects.
4. Write or update a test that would have caught this bug.
5. Run the test suite to confirm the fix and no regressions.
6. Update WORKLOG.md with the fix details.

## Constraints

- Keep the diff scoped to the bug fix — no unrelated refactors.
- If the fix requires a schema or migration change, flag it explicitly.
- If the root cause is ambiguous, present options before implementing.
