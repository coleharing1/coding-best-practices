# Incident Investigation Runbook

## Purpose

Use this when production or preview behavior looks broken and you need to separate app bugs from environment or service outages.

## First Checks

1. [health endpoint]
2. [service status or direct DB/API probe]
3. [recent deploy/build logs]

## Questions To Answer

- is the issue app-side or upstream-service-side?
- is it isolated to one environment?
- is there a rollback or fail-closed behavior?

## Evidence To Capture

- timestamps
- exact failing commands
- screenshots or traces
- relevant log excerpts
