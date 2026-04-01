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
- **Risk Tier**: [T0/T1/T2/T3]
- **Constraints**: [Constraints]

## Current Evidence
- [Key repo findings]

## Working Assumptions
- [Assumption]

## Ownership Legend
- `[Cole]`, `[Codex]`, `[Claude]`, `[Gemini]`, `[Shared]`, `[Gate]`

## Blocking Gates
- [Gate list]

## Implementation Checklist

### Phase 1: [Name]
#### 1A. [Workstream]
- [ ] `[Owner]` [specific step]
- [ ] `[Owner]` [specific step]
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

Rules:
- Do NOT write implementation code — planning only.
- Be specific about file paths, function names, and data shapes.
- Call out unknowns and assumptions explicitly.
- Prefer minimal-change integration with existing patterns.
- Think independently — do not try to anticipate what Claude's plan will say.
- If a step needs a human login, 2FA, approval, or browser consent, mark it with the right owner tag.
