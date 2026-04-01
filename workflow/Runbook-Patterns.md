# Runbook Patterns

## Goal

Turn repeated operational tasks into short, explicit procedures that do not depend on memory.

## Good Candidates For Runbooks

- auth/access issues
- invite/onboarding flows
- service setup handoffs
- production health checks
- incident investigations
- manual recovery procedures

## What A Strong Runbook Includes

- purpose
- when to use it
- exact commands or URLs
- expected outcomes
- common failure modes
- next checks if the first check fails

## Where Runbooks Belong

Put them in `runbooks/` when they are operator-facing or procedural.

Keep them out of:

- `README.md` if they are too detailed
- `WORKLOG.md` if they are evergreen
- one-off plan files if they will be used again

## Naming Suggestions

- `access-operations-runbook.md`
- `incident-investigation-runbook.md`
- `service-setup-handoff.md`

## Recommendation

If the answer to "how do we check that?" is longer than two sentences, it should probably be a runbook.
