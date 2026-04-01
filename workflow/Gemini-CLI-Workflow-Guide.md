# Gemini CLI Workflow Guide

> How to use Gemini CLI as a real workflow layer instead of only a cheap reviewer.

## Why This Matters

Gemini CLI is now strong enough to carry more than one job in your setup. It can be:

- a structural reviewer
- a utility runner from the terminal
- a command-driven checklist system
- a hook-enabled helper
- a skills/extensions platform

That makes it a strong fit for portable local workflow assets.

## Core Surfaces

### GEMINI.md

Use `GEMINI.md` as the always-loaded Gemini context file.

Keep it short and map-like:

- current commands
- risky paths
- review posture
- links to deeper repo docs

Do not try to cram the whole repo manual into it.

### Commands

Store Gemini commands in `.gemini/commands/` as TOML files.

Good starter commands:

- `plan-feature.toml`
- `final-plan-checklist.toml`
- `browser-verify.toml`

Gemini commands are good when:

- the workflow is explicit
- the output shape matters
- you want a reusable local command instead of another copied prompt

### Hooks

Use hooks for behavior that should happen automatically, such as:

- nudging the agent when browser-login handoff is required
- injecting extra context for risky paths
- reminding the agent about the correct QA lane

Start small. Hooks should reinforce a working workflow, not rescue a chaotic one.

### Skills And Extensions

Use `.agents/skills/` when the workflow needs:

- extra files or scripts
- stronger specialization
- cross-tool portability with Codex

Use extensions when the workflow depends on a larger reusable Gemini CLI package or connector surface.

## Recommended Folder Shape

```text
GEMINI.md
.gemini/
├── settings.json
├── commands/
│   ├── plan-feature.toml
│   ├── final-plan-checklist.toml
│   └── browser-verify.toml
└── hooks/
```

Portable skill pack:

```text
.agents/
└── skills/
    ├── service-bootstrap/
    ├── browser-verify/
    └── quality-gate/
```

## What To Add On Day One

Start with:

1. `GEMINI.md`
2. one plan command
3. one browser-verify command if UI exists
4. one shared portable skill if setup or QA is multi-step

Add hooks only after the manual workflow is already working well.

## How Gemini Fits Your Workflow

- **Review**: structural diff review, second-opinion passes
- **Utility**: run a command-driven plan or browser-verify checklist locally
- **Portable workflow layer**: share skill packs with Codex instead of rebuilding the same helper twice

It does not replace Claude for synthesis or Codex for execution. It makes the overall system more portable and cheaper to reuse.

## What To Keep In Sync

Where practical, keep these aligned with sibling tools:

- `.gemini/commands/plan-feature.toml`
- `.claude/commands/plan-feature.md`
- `.cursor/commands/plan-feature.md`

Also keep the same naming pack for:

- final-plan synthesis
- browser verify
- review
- quality gate

## Common Mistakes

- treating Gemini CLI as only a copy-paste review terminal
- overloading `GEMINI.md` with too much repo detail
- creating hooks before the workflow is stable
- forgetting that a portable skill may be better than another tool-specific prompt

## Suggested Next Files

- `templates/GEMINI.template.md`
- `templates/.gemini/commands/README.template.md`
- `templates/.gemini/hooks/README.template.md`
- `templates/.agents/skills/README.template.md`
