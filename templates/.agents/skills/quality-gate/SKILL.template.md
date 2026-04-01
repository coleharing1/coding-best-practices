# Quality Gate

Use this skill when a change is approaching commit, deploy, or handoff and needs the repo's deterministic checks.

## Workflow

1. Read `README.md`, `WORKLOG.md`, and `workflow/AI-QUALITY-GATE-SOP.md` if available.
2. Run the repo's real checks:
   - lint
   - tests
   - build
   - browser/type/parity checks when relevant
   - secret scan or safety checks
3. Record exact commands and outcomes.
4. Report any skips explicitly with a reason.
5. Flag blockers before merge or deploy.

## Success Criteria

- the actual gate commands were run
- pass/fail state is explicit
- skipped checks are named, not implied away
