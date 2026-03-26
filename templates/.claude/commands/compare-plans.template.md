---
description: Compare Claude and Codex plans, then draft a Final synthesis plan
---

## Plan Comparison and Synthesis

### Step 1: Find the Active Plans

!`ls -la plans/active/ 2>/dev/null || echo "No plans/active/ directory found"`

### Step 2: Read Both Plans

Read both the CLAUDE and Codex plans from `plans/active/`.

### Step 3: Compare

Analyze both plans and produce a structured comparison:

**Agreement** — Where both plans align (approach, phases, architecture)

**Divergence** — Where they disagree, with your assessment of which approach is stronger and why:
- Architecture differences
- Phase ordering differences
- Risk assessments that one caught and the other missed
- Scope differences (one plan covers more/less)

**Unique Strengths** — Ideas that only appear in one plan but should be kept:
- From Claude's plan: [list]
- From Codex's plan: [list]

**Gaps** — Things neither plan covers that should be addressed

### Step 4: Draft the Final Plan

Write `plans/active/Plan-XXX-Final.md` that synthesizes the best of both plans.

Use the same plan format but add a `## Synthesis Notes` section at the top explaining:
- Which plan's architecture was chosen and why
- Which phases were adopted from which plan
- What was added that neither plan had
- Any compromises or open decisions for the user

### Rules

- Be specific about what came from which plan
- Don't just average the two — pick the stronger approach for each section
- Flag any remaining disagreements that need the user's decision
- The Final plan must be implementable by Codex as-is

### After Writing

Tell the user:
> "Comparison complete. Final plan drafted at `plans/active/Plan-XXX-Final.md`. Review and edit, then hand off to Codex for implementation."
