Perform a high-risk logic/security audit of this diff.

Focus areas:
- Authentication and authorization boundaries
- Input validation and trust boundaries
- Data integrity and schema/contract consistency
- Sensitive operations (billing, deletion, migration, webhooks)
- Failure states and rollback safety

Output:
1. Ranked findings with impact and exploitability/risk rationale
2. Exact file+line references
3. Minimal safe patch strategy for each finding
4. Final verdict: `safe to merge` or `needs fixes`

Ignore cosmetic issues.
