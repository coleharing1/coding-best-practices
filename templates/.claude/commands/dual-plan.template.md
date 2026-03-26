---
description: Create a competing plan — Claude writes its plan, then you give the same prompt to Codex
argument-hint: [feature-name]
---

## Dual Planning: $ARGUMENTS

You are creating a competing plan for **$ARGUMENTS**.

### Before You Start

1. Read the current codebase context: `CLAUDE.md`, `WORKLOG.md`, existing architecture
2. Check `plans/active/` for the next plan number:

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
- **Constraints**: [Performance/security/deadline constraints]

## Technical Approach
- [Your recommended architecture and patterns]
- [Key interfaces, contracts, data flow]
- [Why this approach over alternatives]

## Phased Implementation

### Phase 1 — [Name]
- **Deliverable**: [What this phase produces]
- **Steps**: [Numbered list]
- **Acceptance Criteria**: [Testable, binary pass/fail]
- **Risk**: [What can go wrong + mitigation]

### Phase 2 — [Name]
[Same structure]

## Test Plan
- Unit: [What to test]
- Integration: [What to test]
- E2E: [What to test]

## Risks and Tradeoffs
- [Risk/tradeoff 1 → mitigation/rationale]
- [Any phase needing dual review (auth, payments, schema)]

## Estimated Complexity
- [Low / Medium / High per phase]
```

### Rules

- Do NOT write implementation code — planning only
- Be specific about file paths, function names, and data shapes
- Call out unknowns and assumptions explicitly
- Flag any phase that should require Gemini + Claude security review

### After Writing

Tell the user:
> "Claude plan written to `plans/active/Plan-XXX-CLAUDE.md`. Now give Codex the same feature prompt to write `Plan-XXX-Codex.md`. Once both plans exist, run `/project:compare-plans` to synthesize."
