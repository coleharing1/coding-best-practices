# Service Bootstrap

Use this skill when the repo needs first-run setup for databases, Vercel, browser QA, or other hosted services before normal implementation can proceed.

## Workflow

1. Read `README.md`, `WORKLOG.md`, `AGENTS.md`, `CLAUDE.md`, and any service handoff runbooks.
2. Identify which services still require:
   - login or 2FA
   - org/team selection
   - local linking
   - env wiring
   - direct DB or MCP access
3. Open the exact page or auth command for the human-only step when needed.
4. Resume immediately after the human step.
5. Record:
   - IDs, refs, org/team names
   - created local artifacts
   - exact verification commands
   - remaining blockers

## Success Criteria

- the AI can continue after the login step
- repo docs record the new access path
- direct verification commands exist
