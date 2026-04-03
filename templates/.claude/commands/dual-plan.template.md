---
description: Create a competing plan — Claude writes its plan, then you give the same prompt to Codex
argument-hint: [feature-name]
---

## Dual Planning: $ARGUMENTS

You are creating a competing plan for **$ARGUMENTS**.

### Before You Start

1. Read the current codebase context: `CLAUDE.md`, `WORKLOG.md`, existing architecture
2. Read `plans/MACRO-ROADMAP.md` if it exists
3. Check `plans/active/` for the next plan number:

!`ls plans/active/ 2>/dev/null | grep -oP 'Plan-\K[0-9]+' | sort -rn | head -1 || echo "No existing plans — start with 000"`

### Your Task

Write a comprehensive implementation plan and save it to `plans/active/Plan-XXX-CLAUDE.md` (use the next sequential number).

### Plan Format

Use this structure:

```markdown
# Plan XXX — [Feature Name] (Claude)

## Context
- **Goal**: [One-sentence desired outcome]
- **Scope**: [What's in scope]
- **Out of Scope**: [Explicitly excluded]
- **Risk Tier**: [T0/T1/T2/T3]
- **Constraints**: [Performance/security/deadline constraints]

## Current Evidence
- [Repo findings that matter]

## Macro Roadmap Alignment
- [roadmap IDs this plan advances]
- [whether the roadmap needs a sync]

## Working Assumptions
- [Assumption]

## Ownership Legend
- `[Cole]`, `[Codex]`, `[Claude]`, `[Gemini]`, `[Shared]`, `[Gate]`

## Blocking Gates
- [Gate list]

## Implementation Checklist

### Phase 1: [Name]
#### 1A. [Workstream]
- [ ] `[Owner]` [step]
- [ ] `[Owner]` [step]
#### Phase 1 Verification
- [ ] `[Owner] [Gate]` [binary criterion]

### Phase 2: [Name]
[Same structure]

## Review Plan
- [ ] `[Gemini]` [structural review need]
- [ ] `[Claude]` [logic/security review need]

## Rollout / Backout
- [deployment notes]
- [rollback trigger]

## Definition Of Done
- [ ] [done item]
```

### Rules

- Do NOT write implementation code — planning only
- Be specific about file paths, function names, and data shapes
- Call out unknowns and assumptions explicitly
- Flag any phase that should require Gemini + Claude security review
- Mark human-only login, 2FA, approval, or browser-consent steps explicitly

### After Writing

Tell the user:
> "Claude plan written to `plans/active/Plan-XXX-CLAUDE.md`. Now give Codex the same feature prompt to write `Plan-XXX-Codex.md`. Once both plans exist, run `/project:compare-plans` to synthesize."
