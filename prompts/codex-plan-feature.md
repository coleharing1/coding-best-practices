You are creating a competing implementation plan for [FEATURE_NAME] in [PROJECT_NAME].

Context:
- Stack: [STACK]
- Constraints: [CONSTRAINTS]
- Read WORKLOG.md and AGENTS.md for current project state

This is a dual-plan workflow. Claude Code is independently writing its own plan. You are writing yours. After both plans are complete, they will be compared and a Final plan will be synthesized.

Write your plan to `plans/active/Plan-[NUMBER]-Codex.md`.

Plan format:

```markdown
# Plan [NUMBER] — [Feature Name] (Codex)

## Context
- **Goal**: [One-sentence desired outcome]
- **Scope**: [In scope]
- **Out of Scope**: [Explicitly excluded]
- **Constraints**: [Constraints]

## Technical Approach
- [Your recommended architecture and patterns]
- [Key interfaces, contracts, data flow]
- [Why this approach over alternatives]

## Phased Implementation

### Phase 1 — [Name]
- **Deliverable**: [What this phase produces]
- **Steps**: [Numbered list of specific steps]
- **Acceptance Criteria**: [Testable, binary pass/fail]
- **Risk**: [What can go wrong + mitigation]

### Phase 2 — [Name]
[Same structure]

## Test Plan
- Unit: [What to test]
- Integration: [What to test]
- E2E: [What to test]

## Risks and Tradeoffs
- [Risk/tradeoff → mitigation/rationale]

## Estimated Complexity
- [Low / Medium / High per phase]
```

Rules:
- Do NOT write implementation code — planning only.
- Be specific about file paths, function names, and data shapes.
- Call out unknowns and assumptions explicitly.
- Prefer minimal-change integration with existing patterns.
- Think independently — do not try to anticipate what Claude's plan will say.
