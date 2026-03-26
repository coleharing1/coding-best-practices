# Risk Tier Matrix

> Last updated: February 25, 2026
> Role in workflow: Decides review depth and gate strictness before commit
> Companion docs: `AI-QUALITY-GATE-SOP.md`, `Workflow-Metrics.md`

---

## Goal

Classify every change into a risk tier before implementation/review so checks are proportional to impact.

This prevents two failure modes:
1. Over-gating trivial changes (wasted time)
2. Under-gating sensitive changes (escaped regressions)

---

## Tier Definitions

| Tier | Name | Typical Scope | Blast Radius | Example Changes |
|---|---|---|---|---|
| `T0` | Docs/Meta | Docs, comments, non-runtime config text | None | README edits, typo fixes, SOP wording |
| `T1` | Low-Risk Code | Localized code with clear tests | Low | UI copy, minor refactor, small component fix |
| `T2` | Medium-Risk | Multi-file behavior changes | Medium | New API route, data transform changes, validation updates |
| `T3` | High-Risk | Security/data/critical runtime paths | High | Auth, billing, DB migrations, permissions, webhooks |

---

## Required Reviews by Tier

| Tier | Gemini Review | Claude Logic/Security Review | Human Notes Required |
|---|---|---|---|
| `T0` | Optional | No | Optional |
| `T1` | Recommended | No | Optional |
| `T2` | Required | Recommended | Yes (`WORKLOG.md`) |
| `T3` | Required | Required | Yes (`WORKLOG.md` + explicit risk notes) |

---

## Required Gates by Tier

| Tier | Lint | Unit/Integration Tests | Build | E2E Smoke | Typecheck (`tsc --noEmit`) | Secret Scan |
|---|---|---|---|---|---|---|
| `T0` | Optional | Optional | Optional | No | No | Optional |
| `T1` | Required | Required | Required | Conditional | Conditional | Required |
| `T2` | Required | Required | Required | Required if UI/API touched | Required | Required |
| `T3` | Required | Required | Required | Required | Required | Required |

---

## Fast Classification Rules

Default to the highest tier that applies:

1. If change touches any of these, mark `T3`:
- Auth/session/permission logic
- Payments/subscriptions/refunds
- DB schema migrations/data deletion jobs
- Security boundaries (RLS, ACL, secrets, token handling)

2. Else if change spans multiple modules or contracts, mark `T2`.

3. Else if runtime behavior changed in one area, mark `T1`.

4. Else docs/meta-only changes are `T0`.

If uncertain between two tiers, choose the higher one.

---

## Suggested Path-Based Heuristics

Use these as hints, not absolutes:

- Likely `T3`
  - `**/auth/**`
  - `**/billing/**`
  - `**/payments/**`
  - `**/migrations/**`
  - `**/policies/**`
  - `**/.github/workflows/**`

- Likely `T2`
  - `**/api/**`
  - `**/server/**`
  - `**/lib/**`
  - `**/validators/**`

- Likely `T1`
  - `**/components/**`
  - `**/pages/**`
  - `**/hooks/**`

- Likely `T0`
  - `**/*.md`
  - `docs/**`

---

## Commit Metadata Convention (Optional but Useful)

Add risk tier to commit body or PR description:

```text
Risk-Tier: T2
Why: Updates API validation and response shape across 3 handlers.
```

This improves post-merge analysis in weekly retros.

---

## Tier-to-Workflow Mapping

| Workflow Phase | T0 | T1 | T2 | T3 |
|---|---|---|---|---|
| Plan (Claude) | Optional | Recommended | Required | Required |
| Execute (Codex) | Optional | Required | Required | Required |
| Review (Gemini/Claude) | Optional | Gemini recommended | Gemini required | Gemini + Claude required |
| Quality Gate | Lightweight | Standard | Standard + conditional checks | Full strict |

---

## Definition of Done by Tier

### T0 Done
- Diff scoped and accurate.
- No runtime behavior changed.

### T1 Done
- Lint/test/build pass.
- Review completed or explicitly skipped with reason.

### T2 Done
- Gemini review complete.
- Typecheck complete.
- Worklog entry includes behavioral and contract notes.

### T3 Done
- Gemini + Claude reviews complete.
- Full gate (including E2E + typecheck + secret scan) complete.
- Worklog includes risk notes and rollback notes.
