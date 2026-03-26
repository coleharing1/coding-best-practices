# Plans

> Dual-plan workflow: Claude and Codex each write a competing plan, then we synthesize a Final plan for implementation.

## Structure

```
plans/
├── active/                        # Current feature being planned/built
│   ├── Plan-001-CLAUDE.md         # Claude Code's plan
│   ├── Plan-001-Codex.md          # Codex's plan
│   └── Plan-001-Final.md          # Synthesized plan (this gets implemented)
├── archive/                       # Completed plans (moved here after implementation)
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

1. Write the same planning prompt for both tools
2. Claude writes `Plan-XXX-CLAUDE.md` to `plans/active/`
3. Codex writes `Plan-XXX-Codex.md` to `plans/active/`
4. Each tool reads the other's plan and provides comparison notes
5. You synthesize into `Plan-XXX-Final.md` (or have Claude do it after you review both)
6. Codex implements from `Plan-XXX-Final.md`
7. After implementation is complete, move all three files to `plans/archive/`

## Commands (Claude Code)

- `/project:dual-plan [feature]` — Claude writes its plan to `plans/active/`
- `/project:compare-plans` — Claude reads both plans and produces a comparison + draft Final
- `/project:archive-plan` — Moves active plans to archive after implementation

See `workflow/Dual-Plan-Workflow.md` for the full guide.
