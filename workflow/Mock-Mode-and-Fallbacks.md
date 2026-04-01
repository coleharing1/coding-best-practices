# Mock Mode And Fallbacks

## Goal

Keep development and testing moving even when third-party credentials, quotas, or upstream services are unavailable.

## Core Rule

Every external-service integration should have a predictable safe mode.

## Good Mock Mode Behaviors

- deterministic fake data
- realistic response shape
- explicit `isMock` metadata when helpful
- ability to force mock mode even when credentials exist

## Good Fallback Behaviors

- preserve last-known-good data when live refresh fails
- fail closed on auth/security problems
- surface clear operator messages instead of silent empty states

## What To Avoid

- random fake data that makes tests flaky
- hidden fallbacks that mask real outages
- production code paths that quietly downgrade behavior without any note

## Documentation

Document:

- which env vars enable live mode
- which env vars trigger mock mode
- what users should expect in mock mode
- whether fallback data is stale, partial, or synthetic

## Recommendation

Mock mode should be a first-class design choice, not a hack added after the API key runs out.
