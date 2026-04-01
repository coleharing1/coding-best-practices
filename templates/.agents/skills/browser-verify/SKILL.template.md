# Browser Verify

Use this skill when the repo needs real browser-visible verification instead of a code-only guess.

## Workflow

1. Read `TESTING_AND_BROWSER_AUTOMATION.md`, `README.md`, and any browser or service handoff runbooks.
2. Identify:
   - local URL
   - correct browser lane (`user` vs `agent`)
   - login expectations
   - whether this should hit an existing app or an isolated QA server
3. Open the target flow.
4. Check for:
   - page load failures
   - console errors
   - obvious network failures
   - broken UI path behavior
5. Report exact pass/fail outcomes and what was actually verified.

## Success Criteria

- the checked flow is named explicitly
- the browser lane is explicit
- verification is based on a real opened flow, not a guess from code alone
