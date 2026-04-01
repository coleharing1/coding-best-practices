# BUGBOT.md -- [Project Name]

Use this file to teach Cursor Bugbot what matters in review for this repo.

## Prioritize

- correctness regressions
- auth and permission mistakes
- migration and schema-sync issues
- browser-visible workflow failures
- missing verification on high-risk changes

## Treat As High Risk

- auth
- payments
- migrations
- destructive jobs
- webhooks
- browser onboarding or invite flows

## Ignore Or Downrank

- purely cosmetic style nits
- naming preferences already enforced by lint rules
- broad refactor suggestions that are unrelated to the diff

## Review Notes

- The project uses owner-tagged checklist plans with gates.
- Work that changes setup, operator behavior, or browser flows should update docs and runbooks.
- Prefer findings that can name a concrete file, failure mode, and fix path.
