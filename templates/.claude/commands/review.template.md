---
description: Review the current branch diff before merging
---

## Files Changed

!`git diff --name-only main...HEAD`

## Full Diff

!`git diff main...HEAD`

Review the above changes for:

1. **Structural issues** — separation of concerns, module boundaries, cross-file invariants
2. **Security vulnerabilities** — auth gaps, input validation, exposed secrets, injection risks
3. **Missing test coverage** — new code paths without tests, edge cases unhandled
4. **Performance concerns** — N+1 queries, unnecessary re-renders, missing indexes
5. **Convention violations** — deviations from patterns established in this codebase

Output format:
- Severity-tagged findings (`critical`, `high`, `medium`, `low`)
- File path and line range for each finding
- One concrete fix recommendation per finding
- Final verdict: `safe to merge` or `needs fixes`

Ignore cosmetic/style-only issues unless they impact correctness or maintainability.
