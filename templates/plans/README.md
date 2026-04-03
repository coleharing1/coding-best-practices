# Plans

> Dual-plan workflow: Claude and Codex each write a competing plan, then we synthesize a Final plan for implementation. Pair that with a permanent macro roadmap for the whole project.

## Structure

```text
plans/
├── MACRO-ROADMAP.md              # Permanent whole-project roadmap
├── active/                       # Current feature being planned/built
│   ├── Plan-001-CLAUDE.md        # Claude Code's plan
│   ├── Plan-001-Codex.md         # Codex's plan
│   └── Plan-001-Final.md         # Synthesized plan (this gets implemented)
├── archive/                      # Completed plans (moved here after implementation)
│   ├── Plan-000-CLAUDE.md
│   ├── Plan-000-Codex.md
│   └── Plan-000-Final.md
└── README.md
```

## Naming Convention

`Plan-XXX-[SOURCE].md` where:

- `XXX` = sequential number (000, 001, 002...)
- `SOURCE` = `CLAUDE`, `Codex`, or `Final`

## Workflow

1. Seed `plans/MACRO-ROADMAP.md` with the whole-project sequence.
2. Write the same planning prompt for both tools.
3. Claude reads the macro roadmap and writes `Plan-XXX-CLAUDE.md` to `plans/active/`.
4. Codex reads the macro roadmap and writes `Plan-XXX-Codex.md` to `plans/active/`.
5. Compare both plans and synthesize `Plan-XXX-Final.md`.
6. Make the Final plan an owner-tagged checklist with gates and `Macro Roadmap Alignment`.
7. Codex implements from `Plan-XXX-Final.md`.
8. After implementation is complete, move all three files to `plans/archive/` and update `plans/MACRO-ROADMAP.md` if the long-range sequence changed.

## What The Final Plan Should Look Like

- checklist-based
- aligned to the macro roadmap
- owner-tagged
- explicit about blockers and gates
- explicit about verification
- explicit about human-only login, approval, or consent steps

## Commands (Claude Code)

- `/project:dual-plan [feature]` -- Claude writes its plan to `plans/active/`
- `/project:compare-plans` -- Claude reads both plans and produces a comparison + draft Final
- `/project:archive-plan` -- Moves active plans to archive after implementation

See `workflow/Dual-Plan-Workflow.md` for the full guide.
