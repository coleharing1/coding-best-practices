# Cursor Workflow Guide

> How to use Cursor's repo-level workflow surfaces without turning the repo into a pile of ad hoc prompts.

## Why This Matters

Cursor is strongest in your workflow when it acts like the project control room:

- repo bootstrap
- research and requirement organization
- GitHub and MCP setup
- rules and commands that multiple sessions can reuse
- background review or maintenance work once the repo is stable

The key is not to use Cursor as "the place I explain things again." Use it as the place where those explanations get promoted into repo assets.

## Core Surfaces

### Project Rules

Store persistent repo guidance in `.cursor/rules/`.

Use rules for:

- core code style and safety constraints
- browser QA expectations
- service-bootstrap reminders
- schema-sync and prod-safety guidance
- debug-journal expectations

Keep rules focused. A small set of strong rules beats one giant all-purpose file.

### Commands

Store invoked checklists in `.cursor/commands/`.

Best command candidates:

- `plan-feature`
- `final-plan-checklist`
- `review`
- `browser-verify`

Use commands when you want the same workflow on purpose, not automatically.

### Memories

Use Cursor Memories for recurring repo context that Cursor learns from repeated work, but do not treat memories as the source of truth. If a behavior matters to the team, promote it into a committed rule, command, runbook, or checklist.

### Background Agents And Automations

Use these only after the manual workflow is already reliable.

Good fits:

- review and triage loops
- stale-doc cleanup
- maintenance PRs
- bounded research summaries

Bad fits:

- first-run dashboard setup
- open-ended architecture work
- workflows that still require active human steering

### Bugbot

Treat review as its own config surface.

If Cursor review is part of the repo workflow, add `.cursor/BUGBOT.md` so Bugbot knows:

- risky paths
- what counts as a real bug
- migration, auth, and browser-flow expectations
- what noise to ignore

## Recommended Folder Shape

```text
.cursor/
├── rules/
│   ├── 000-core.mdc
│   ├── 050-worklog.mdc
│   ├── 100-browser-qa.mdc
│   ├── 110-service-bootstrap.mdc
│   ├── 150-prod-safety.mdc
│   ├── 200-schema-sync.mdc
│   └── 300-debug-journal.mdc
├── commands/
│   ├── plan-feature.md
│   ├── final-plan-checklist.md
│   ├── review.md
│   └── browser-verify.md
└── BUGBOT.md
```

## What To Add On Day One

Start with:

1. core rules
2. browser-qa rule
3. service-bootstrap rule
4. `plan-feature` command
5. `browser-verify` command if the repo has UI work

Add Bugbot config when review noise becomes a problem.

## How Cursor Fits Your Workflow

- **Phase 0**: create repo, paste research, connect GitHub, lay down repo OS
- **Phase 0.5**: help stage the browser-login handoff and MCP wiring
- **Phase 0.6**: create repeatable rules and commands from the first few recurring prompts
- **Later**: use Background Agents or Automations for bounded chores only

## What To Keep In Sync

When the workflow is shared across tools, keep these aligned:

- `.cursor/commands/plan-feature.md`
- `.claude/commands/plan-feature.md`
- `.gemini/commands/plan-feature.toml`

Do the same for:

- final-plan synthesis
- browser verify
- quality-gate or review flows

The prompts do not need to be identical, but the intent and outputs should line up.

## Common Mistakes

- using Memories as the only durable source of truth
- leaving review behavior undefined instead of configuring Bugbot
- automating before the manual workflow is reliable
- stuffing project truth into chat history instead of committed rules, commands, and runbooks

## Suggested Next Files

- `templates/.cursor/commands/README.template.md`
- `templates/.cursor/commands/plan-feature.template.md`
- `templates/.cursor/commands/final-plan-checklist.template.md`
- `templates/.cursor/commands/browser-verify.template.md`
- `templates/.cursor/BUGBOT.template.md`
