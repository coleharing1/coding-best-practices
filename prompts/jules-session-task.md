Create a Jules session for repo [REPO_SOURCE] from branch [BRANCH].

Task:
[DESCRIBE TASK CLEARLY]

Constraints:
- Limit changes to: [TARGET_PATHS]
- Do not modify: [EXCLUDED_PATHS]
- Keep diff scoped to one objective
- Run tests/checks: [COMMANDS]
- If a plan is ambiguous, stop and request clarification

Output expectations:
- Open a PR with clear title and summary
- Include command results in PR description
- List risks or follow-up items explicitly
