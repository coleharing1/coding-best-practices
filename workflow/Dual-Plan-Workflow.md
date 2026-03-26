# Dual-Plan Workflow

> Get competing plans from Claude Code and Codex, compare them, then synthesize a Final plan before implementation. Two perspectives catch more than one.

---

## Why Dual Planning

Single-model planning has blind spots. Claude Code (Opus) is strong at architecture and risk analysis but can over-engineer. Codex is strong at practical, buildable steps but can under-spec edge cases. Having both plan independently and then comparing produces a Final plan that is:

- **More robust** — risks caught by one model that the other missed
- **More practical** — implementation steps validated by the model that will build it
- **Better scoped** — two independent scope assessments surface disagreements early

---

## Folder Structure

```
plans/
├── active/                        # Plans for the current feature
│   ├── Plan-001-CLAUDE.md         # Claude Code's independent plan
│   ├── Plan-001-Codex.md          # Codex's independent plan
│   └── Plan-001-Final.md          # Synthesized plan → gets implemented
└── archive/                       # Completed plans (historical record)
    ├── Plan-000-CLAUDE.md
    ├── Plan-000-Codex.md
    └── Plan-000-Final.md
```

**Naming:** `Plan-XXX-[SOURCE].md`
- `XXX` = sequential number (000, 001, 002...)
- `SOURCE` = `CLAUDE`, `Codex`, or `Final`

**Active vs. Archive:**
- `active/` holds the plans for the feature currently being worked on (only one set at a time)
- `archive/` holds all completed plan sets — never delete these, they're your decision history

---

## The Workflow Step by Step

### Step 1: Write the Planning Prompt

Write one clear feature description that both tools will receive. Include:
- What the feature should do (user-facing behavior)
- Any technical constraints (stack, performance, backwards compatibility)
- What's explicitly out of scope

You can write this once and paste it into both tools, or keep it in a scratch file.

### Step 2: Claude Writes Its Plan

In **Claude Code**, run:

```
/project:dual-plan [feature-name]
```

Or paste your planning prompt directly. Claude writes its plan to `plans/active/Plan-XXX-CLAUDE.md`.

Claude's plan will emphasize:
- Architecture decisions with rationale
- Risk analysis and mitigation per phase
- Security and edge case considerations
- Interfaces and contracts

### Step 3: Codex Writes Its Plan

In **Codex**, paste the same planning prompt along with:

```
Write your plan to plans/active/Plan-XXX-Codex.md
```

Or use the prompt template from `prompts/codex-plan-feature.md`.

Codex's plan will emphasize:
- Practical step-by-step implementation
- Concrete file paths and function signatures
- Build/test commands for each phase
- Minimal-diff integration with existing code

### Step 4: Compare and Synthesize

Back in **Claude Code**, run:

```
/project:compare-plans
```

Claude reads both plans and produces:
1. **Agreement** — where both plans align
2. **Divergence** — where they disagree, with assessment of which is stronger
3. **Unique strengths** — ideas from one plan worth keeping
4. **Gaps** — things neither plan covered
5. **Draft Final plan** — `Plan-XXX-Final.md` synthesizing the best of both

### Step 5: Review and Finalize

Read `Plan-XXX-Final.md`. This is your decision point:
- Edit anything you disagree with
- Resolve any flagged open decisions
- Confirm the phase ordering and acceptance criteria

The Final plan is the single source of truth for implementation.

### Step 6: Implement from Final Plan

Hand off `Plan-XXX-Final.md` to **Codex** for implementation:

```
Implement Phase 1 from plans/active/Plan-XXX-Final.md
```

Or use `/project:codex-handoff` in Claude Code to format the handoff.

Codex implements one phase at a time, runs tests, reports back.

### Step 7: Archive After Completion

When all phases are implemented and the quality gate passes, archive the plans:

In **Claude Code**, run:

```
/project:archive-plan
```

This moves all `Plan-XXX-*.md` files from `active/` to `archive/`.

---

## How This Fits the Multi-Model Workflow

The dual-plan workflow replaces the single-plan Phase 1. Here's how the full lifecycle now looks:

```
Phase 0   Cursor          Bootstrap project, context files, plans/ folder
Phase 1a  Claude Code     /project:dual-plan → writes Plan-XXX-CLAUDE.md
Phase 1b  Codex           Same prompt → writes Plan-XXX-Codex.md
Phase 1c  Claude Code     /project:compare-plans → writes Plan-XXX-Final.md
Phase 1d  You             Review and finalize the plan
Phase 2   Codex           Implement from Plan-XXX-Final.md, one phase at a time
Phase 3   Gemini CLI      Pre-commit review of the diff
Phase 4   Quality Gate    Lint, test, build, E2E, secret scan
Phase 5   Jules           Push to GitHub, overnight agents
          Claude Code     /project:archive-plan → move plans to archive/
```

---

## Commands Reference

| Command | Tool | What It Does |
|---|---|---|
| `/project:dual-plan [feature]` | Claude Code | Claude writes its plan to `plans/active/` |
| `prompts/codex-plan-feature.md` | Codex | Prompt template for Codex to write its plan |
| `/project:compare-plans` | Claude Code | Reads both plans, produces comparison + draft Final |
| `/project:archive-plan` | Claude Code | Moves active plans to `plans/archive/` |
| `/project:codex-handoff [phase]` | Claude Code | Formats a phase from Final plan for Codex |

---

## Plan Format

Both Claude and Codex use the same format for consistency:

```markdown
# Plan XXX — [Feature Name] ([Source])

## Context
- **Goal**: [One-sentence desired outcome]
- **Scope**: [In scope]
- **Out of Scope**: [Explicitly excluded]
- **Constraints**: [Performance/security/deadline constraints]

## Technical Approach
- [Recommended architecture and patterns]
- [Key interfaces, contracts, data flow]
- [Why this approach over alternatives]

## Phased Implementation

### Phase 1 — [Name]
- **Deliverable**: [What this phase produces]
- **Steps**: [Numbered list]
- **Acceptance Criteria**: [Testable, binary pass/fail]
- **Risk**: [What can go wrong + mitigation]

## Test Plan
- Unit / Integration / E2E / Negative cases

## Risks and Tradeoffs
- [Risk → mitigation]

## Estimated Complexity
- [Low / Medium / High per phase]
```

The **Final plan** adds a `## Synthesis Notes` section at the top explaining what came from which plan and why.

---

## Tips

- **Don't bias the prompt.** Give both tools the same information. Don't tell Codex what Claude said or vice versa until the comparison step.
- **Disagreements are valuable.** When the two plans diverge, that's where the interesting architectural decisions live. Pay attention to those sections.
- **The Final plan is yours.** Claude drafts it, but you own it. Edit freely.
- **Keep archive plans.** They're a decision log. When you wonder "why did we build it this way?", the archived plans have the reasoning.
- **One active set at a time.** Don't start planning the next feature until the current one is archived. This prevents confusion about which plan is active.
- **Plan numbering is global.** Plan-000, Plan-001, Plan-002 across all features, not restarted per feature. Check `plans/archive/` for the latest number.
