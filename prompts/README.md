# Prompt Cookbook

> Reusable prompts for the multi-model workflow.
> Copy, fill placeholders, run.

---

## How To Use

1. Pick the prompt file for your phase.
2. Replace placeholders in brackets.
3. Keep prompts versioned so they evolve with your workflow.
4. For critical paths, prefer explicit constraints over "best effort" language.

---

## Prompt Files

| File | Use Case | Primary Tool |
|---|---|---|
| `plan-feature.md` | Create phased implementation plan with risks and acceptance criteria | Claude Code |
| `codex-plan-feature.md` | Codex's competing plan in the dual-plan workflow | Codex |
| `codex-execute-phase.md` | Constrained phase-by-phase implementation from Final plan | Codex |
| `review-diff-gemini.md` | Structural/architectural diff review | Gemini CLI |
| `review-diff-claude-high-risk.md` | Logic/security review for high-risk diffs | Claude Code |
| `jules-session-task.md` | High-quality task request for Jules sessions | Cursor/Jules |

---

## Usage Examples

Gemini review:

```bash
git diff | gemini --model gemini-3-pro-preview -p "$(cat prompts/review-diff-gemini.md)"
```

Codex competing plan (dual-plan workflow):

```text
Paste `prompts/codex-plan-feature.md` into Codex with the same feature prompt you gave Claude.
Codex writes its plan to plans/active/Plan-XXX-Codex.md.
```

Codex phase execution:

```text
Paste `prompts/codex-execute-phase.md` into Codex, then paste the relevant phase from plans/active/Plan-XXX-Final.md.
```
