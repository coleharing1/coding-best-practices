# Prompt Cookbook

> Reusable prompts for the multi-model workflow.
> Copy, fill placeholders, run.

---

## How To Use

1. Pick the prompt file for your phase.
2. Replace placeholders in brackets.
3. Keep prompts versioned so they evolve with your workflow.
4. For critical paths, prefer explicit constraints over "best effort" language.

## Prompt vs Command vs Skill

Use a raw prompt when the work is still exploratory or one-off.

Promote that prompt into a command when:

- you invoke the same checklist on purpose
- the output shape matters
- you want the workflow stored in the repo instead of memory

Promote the workflow into a skill when:

- it bundles scripts, files, or tool access
- it should work across Codex and Gemini
- it is more than a single prompt with placeholders

See `workflow/Repeatable-Actions-Stack.md`.

---

## Prompt Files

| File | Use Case | Primary Tool |
|---|---|---|
| `plan-feature.md` | Create an owner-tagged checklist plan with gates and verification | Claude Code |
| `codex-plan-feature.md` | Codex's competing checklist plan in the dual-plan workflow | Codex |
| `codex-execute-phase.md` | Constrained phase-by-phase implementation from Final plan | Codex |
| `project-audit-against-coding-best-practices.md` | Deep project audit prompt that compares a live repo against this reference repo before recommending upgrades | Codex |
| `project-structure-audit-and-cleanup-plan.md` | Generic deep-dive prompt for auditing a repo's current structure, classifying old vs current material, and recommending a cleaner layout before moving files | Codex |
| `review-diff-gemini.md` | Structural/architectural diff review | Gemini CLI |
| `review-diff-claude-high-risk.md` | Logic/security review for high-risk diffs | Claude Code |
| `jules-session-task.md` | High-quality task request for Jules sessions | Cursor/Jules |

---

## Usage Examples

Gemini review:

```bash
git diff | gemini --model gemini-3.1-pro-preview -p "$(cat prompts/review-diff-gemini.md)"
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

Project audit against this repo:

```text
Paste `prompts/project-audit-against-coding-best-practices.md` into a fresh Codex chat inside the target project repo.
Codex should read that repo first, then compare it against `/Users/coleharing/Cursor_Projects/coding best practices`, then report recommended upgrades before editing anything.
```

Generic project structure audit:

```text
Paste `prompts/project-structure-audit-and-cleanup-plan.md` into a fresh Codex chat inside the target repo.
Fill the bracket placeholders that matter for that project, then have Codex audit the whole repo, classify current vs historical vs generated material, and recommend a cleanup plan before moving anything.
```

## Related Repo Surfaces

- Cursor commands: `templates/.cursor/commands/`
- Claude commands: `templates/.claude/commands/`
- Gemini commands: `templates/.gemini/commands/`
- Portable skills: `templates/.agents/skills/`
