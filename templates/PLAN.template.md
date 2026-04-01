# Plan XXX -- [Feature Name] ([Source])

## Context

- **Goal**: [one-sentence desired outcome]
- **Scope**: [in scope]
- **Out of Scope**: [explicitly excluded]
- **Risk Tier**: [T0/T1/T2/T3]
- **Constraints**: [performance, security, deadline, compatibility]

## Current Evidence

- [Current repo state, existing patterns, or live-system findings that the plan should respect]

## Working Assumptions

- [Assumption]
- [Assumption]

## Ownership Legend

- `[Cole]` = human-only login, approval, business decision, or credential handoff
- `[Codex]` = repo changes, terminal work, tests, documentation updates
- `[Claude]` = architecture, synthesis, or high-risk review work
- `[Gemini]` = structural diff review
- `[Shared]` = mostly AI-owned work that still needs one human step
- `[Gate]` = blocker that later work should not skip

## Blocking Gates

| Gate | Must Be Complete Before | Required Outcome |
| --- | --- | --- |
| Gate 0 | Phase 1 implementation | [Required baseline or decision] |
| Gate 1 | Phase 2 implementation | [Required verified dependency] |

## Implementation Checklist

### Phase 1: [Name]

#### 1A. [Workstream]

- [ ] `[Owner]` [step]
- [ ] `[Owner]` [step]

#### Phase 1 Verification

- [ ] `[Owner] [Gate 0]` [binary verification target]

### Phase 2: [Name]

#### 2A. [Workstream]

- [ ] `[Owner]` [step]
- [ ] `[Owner]` [step]

#### Phase 2 Verification

- [ ] `[Owner] [Gate 1]` [binary verification target]

## Review Plan

- [ ] `[Gemini]` Structural diff review for T2/T3 changes
- [ ] `[Claude]` Logic/security review for auth, payments, migrations, or destructive flows

## Rollout / Backout

- [rollout notes]
- [migration or release order]
- [operator/runbook updates]
- [rollback trigger]

## Definition Of Done

- [ ] Code implemented for this plan
- [ ] Required docs and runbooks updated
- [ ] Required checks passed
- [ ] Risk notes and follow-ups captured
