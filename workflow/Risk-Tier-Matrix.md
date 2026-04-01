# Risk Tier Matrix

> Last updated: April 1, 2026

## Goal

Classify every change before review and verification so the process matches the blast radius.

## Tier Definitions

| Tier | Typical Scope | Examples |
|---|---|---|
| `T0` | Docs/meta only | README edits, template wording, comments |
| `T1` | Localized low-risk code | small UI fix, minor refactor |
| `T2` | Multi-file behavior or contract change | new route, service refactor, validation change |
| `T3` | Security/data/critical runtime change | auth, billing, migrations, webhooks, destructive jobs |

## Review Requirements

| Tier | Gemini Review | Claude Logic/Security Review | Notes |
|---|---|---|---|
| `T0` | Optional | No | Keep diff scoped |
| `T1` | Recommended | No | Worklog if behavior changed |
| `T2` | Required | Recommended | Worklog required |
| `T3` | Required | Required | Worklog + rollback notes required |

## Gate Requirements

| Tier | Lint/Test/Build | E2E | Typecheck/Parity | Secret Scan |
|---|---|---|---|---|
| `T0` | Optional | No | No | Optional |
| `T1` | Required | Conditional | Conditional | Required |
| `T2` | Required | Conditional but likely | Required | Required |
| `T3` | Required | Required when a user-visible or route-level flow changed | Required | Required |

## Extra Requirements

### `T2`

- update `WORKLOG.md`
- update docs if operator/setup behavior changed

### `T3`

- update `WORKLOG.md`
- add rollback notes
- run parity checks if schema/capability surfaces changed
- update runbooks or browser docs if operator behavior changed

## Fast Rules

Default to the highest tier that applies.

1. migrations, auth, permissions, secrets, billing, destructive jobs, or webhooks -> `T3`
2. multi-file behavior/contract change -> `T2`
3. localized runtime change -> `T1`
4. docs/process-only -> `T0`
