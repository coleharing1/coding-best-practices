# Claude Code Folder Guide

> How to set up and use the `.claude/` folder to control Claude Code behavior across your projects. Covers rules, commands, skills, agents, and permissions.

---

## Why This Matters

Claude Code reads `CLAUDE.md` at session start — you already know that. But the `.claude/` folder goes much further. It lets you:

- **Split instructions into modular, path-scoped rules** instead of one giant CLAUDE.md
- **Create custom slash commands** that inject live shell output into prompts
- **Define skills** that auto-invoke when the conversation matches their description
- **Spawn specialized agents** with their own model, tool access, and persona
- **Control permissions** so Claude can run your scripts freely but never touch `.env` files

This guide covers every part of the folder, what it does, and when to add it.

---

## Two Folders, Not One

There are two `.claude/` directories:

| Location | Scope | Committed to Git? |
|---|---|---|
| `your-project/.claude/` | Team config — shared rules, commands, permissions | Yes |
| `~/.claude/` | Personal config — global preferences, session memory | No (machine-local) |

Project-level config takes priority for project-specific rules. Global config provides defaults that apply everywhere.

---

## The Full Structure

```
your-project/
├── CLAUDE.md                    # Team instructions (committed)
├── CLAUDE.local.md              # Personal overrides (gitignored)
│
└── .claude/
    ├── settings.json            # Permissions + config (committed)
    ├── settings.local.json      # Personal permission overrides (gitignored)
    │
    ├── commands/                # Custom slash commands
    │   ├── review.md            #   → /project:review
    │   ├── fix-issue.md         #   → /project:fix-issue
    │   ├── plan-feature.md      #   → /project:plan-feature
    │   ├── quality-gate.md      #   → /project:quality-gate
    │   └── codex-handoff.md     #   → /project:codex-handoff
    │
    ├── rules/                   # Modular instruction files
    │   ├── code-style.md        #   Always loaded
    │   ├── testing.md           #   Always loaded
    │   ├── api-conventions.md   #   Loaded only for src/api/** files
    │   └── security.md          #   Loaded only for auth/middleware files
    │
    ├── skills/                  # Auto-invoked workflows
    │   ├── security-review/
    │   │   └── SKILL.md
    │   └── deploy/
    │       └── SKILL.md
    │
    └── agents/                  # Specialized subagent personas
        ├── code-reviewer.md
        └── security-auditor.md

~/.claude/
├── CLAUDE.md                    # Global instructions (all projects)
├── settings.json                # Global permissions
├── commands/                    # Personal commands → /user:command-name
├── skills/                      # Personal skills (all projects)
├── agents/                      # Personal agents (all projects)
└── projects/                    # Session history + auto-memory
```

---

## CLAUDE.md — Best Practices

You already have a `CLAUDE.md` template. Key sizing guidance:

**Keep it under 200 lines.** Longer files eat context and reduce instruction adherence.

**What belongs in CLAUDE.md:**
- Build/test/lint commands
- Key architectural decisions
- Non-obvious gotchas and constraints
- Import conventions, naming patterns
- File and folder structure overview

**What does NOT belong:**
- Anything a linter or formatter handles
- Full documentation (link to it instead)
- Long explanatory paragraphs

**When CLAUDE.md gets crowded:** Split instructions into `.claude/rules/` files. Each rule file is loaded alongside CLAUDE.md automatically.

### CLAUDE.local.md — Personal Overrides

Create `CLAUDE.local.md` in your project root for preferences specific to you. It's auto-gitignored. Use it for:

- Personal coding style preferences
- Local environment differences (port numbers, package managers)
- Custom aliases ("when I say X, do Y")

---

## settings.json — Permissions

Controls what Claude can and can't do. Three tiers:

| Tier | Behavior |
|---|---|
| `allow` | Runs without asking |
| (not listed) | Claude asks for confirmation |
| `deny` | Blocked entirely |

**Template:**

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npx *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  }
}
```

**Adapt for your stack:**
- Python: `Bash(python -m pytest *)`, `Bash(pip install *)`
- Monorepo: `Bash(turbo run *)`, `Bash(pnpm *)`
- Shopify: `Bash(shopify theme *)`, `Bash(shopify app *)`

**settings.local.json** works the same way but is auto-gitignored for personal overrides.

---

## commands/ — Custom Slash Commands

Every `.md` file in `.claude/commands/` becomes a slash command. The filename is the command name.

| File | Command | Use Case |
|---|---|---|
| `dual-plan.md` | `/project:dual-plan auth-system` | Claude writes its competing plan to `plans/active/` |
| `compare-plans.md` | `/project:compare-plans` | Read both plans, synthesize Final plan |
| `archive-plan.md` | `/project:archive-plan` | Move completed plans to `plans/archive/` |
| `review.md` | `/project:review` | Pre-merge diff review |
| `fix-issue.md` | `/project:fix-issue 234` | Investigate and fix a GitHub issue |
| `plan-feature.md` | `/project:plan-feature auth-system` | Quick single-model plan (skip dual workflow) |
| `quality-gate.md` | `/project:quality-gate` | Run pre-commit checks |
| `codex-handoff.md` | `/project:codex-handoff 2` | Format a phase from Final plan for Codex |

### Key Features

**Shell interpolation:** Use `` !`command` `` to embed live shell output:

```markdown
## Files Changed
!`git diff --name-only main...HEAD`
```

Claude sees the actual output, not the command.

**Arguments:** Use `$ARGUMENTS` to pass text after the command:

```markdown
Look at issue #$ARGUMENTS
!`gh issue view $ARGUMENTS`
```

Running `/project:fix-issue 234` injects issue 234's content.

**Personal commands:** Put them in `~/.claude/commands/` — they show up as `/user:command-name` across all projects.

### How This Fits the Multi-Model Workflow

| Phase | Command | What It Does |
|---|---|---|
| Phase 1a (Claude plans) | `/project:dual-plan` | Claude writes `Plan-XXX-CLAUDE.md` |
| Phase 1b (Codex plans) | `prompts/codex-plan-feature.md` | Codex writes `Plan-XXX-Codex.md` |
| Phase 1c (Synthesize) | `/project:compare-plans` | Compare both, draft `Plan-XXX-Final.md` |
| Phase 2 (Handoff) | `/project:codex-handoff` | Format a phase from Final plan for Codex |
| Phase 3 (Review) | `/project:review` | Claude reviews the diff before commit |
| Phase 4 (Gate) | `/project:quality-gate` | Runs lint/test/build checks |
| Post-impl | `/project:archive-plan` | Move completed plans to archive |
| Bug fix | `/project:fix-issue` | Traces and fixes a GitHub issue |

---

## rules/ — Modular, Path-Scoped Instructions

Every `.md` file in `.claude/rules/` loads alongside CLAUDE.md. This is how you scale instructions without bloating CLAUDE.md.

### Unconditional Rules (Always Loaded)

Rules without a `paths` frontmatter load every session:

```markdown
---
description: Code style and naming conventions
---

# Code Style
- Prefer functional patterns; avoid classes
- One component per file; filename matches export
- Keep files under 500 lines
```

### Path-Scoped Rules (Loaded Conditionally)

Add `paths` to a rule and it only activates when Claude works on matching files:

```markdown
---
description: API design and handler conventions
paths:
  - "src/api/**"
  - "src/handlers/**"
  - "app/api/**"
---

# API Conventions
- All handlers return { data, error } shape
- Validate request bodies with zod
- Never expose internal errors to clients
```

Claude won't load this when editing a React component. It only loads when working inside API directories.

### Recommended Rule Files

| File | Scope | When to Add |
|---|---|---|
| `code-style.md` | Global | Day 1 — establishes patterns |
| `testing.md` | Global | When you have a test suite |
| `api-conventions.md` | Path-scoped to API dirs | When you have API routes |
| `security.md` | Path-scoped to auth/middleware | When you have auth or sensitive handlers |

### Rules vs. Cursor Rules

Both serve the same purpose (modular AI instructions) for different tools:

| Feature | `.claude/rules/` | `.cursor/rules/` |
|---|---|---|
| Read by | Claude Code | Cursor |
| Format | Markdown with YAML frontmatter | MDC with YAML frontmatter |
| Path scoping | `paths:` in frontmatter | `globs:` in frontmatter |
| Auto-load | Yes (all rules load automatically) | Yes (`alwaysApply: true`) or on match |
| Naming | Any `.md` filename | Numbered convention (`000-core.mdc`) |

**Keep both in sync.** When you add a Claude rule, add the equivalent Cursor rule. The content can be identical — only the frontmatter format differs.

---

## skills/ — Auto-Invoked Workflows

Skills are like commands, but Claude triggers them automatically when the conversation matches the skill's description. You don't type a slash command — Claude recognizes the moment and invokes the skill.

Each skill lives in its own subdirectory with a `SKILL.md`:

```
.claude/skills/
├── security-review/
│   └── SKILL.md
└── deploy/
    └── SKILL.md
```

### SKILL.md Frontmatter

```yaml
---
name: security-review
description: >
  Comprehensive security audit. Use when reviewing code for vulnerabilities,
  before deployments, or when the user mentions security.
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

The `description` is what Claude matches against. Write it clearly — it determines when the skill fires.

The `allowed-tools` field restricts what the skill can do. A security review only needs read access. A deploy skill might need Bash too.

### When to Use Skills vs. Commands

| Feature | Commands | Skills |
|---|---|---|
| Trigger | You type `/project:name` | Claude auto-invokes based on context |
| Format | Single `.md` file | Directory with `SKILL.md` + supporting files |
| Best for | Workflows you run on demand | Workflows that should happen automatically |

**Start with commands.** Convert to skills once you find yourself repeatedly running the same command in the same situations.

### Skills in the Multi-Model Workflow

| Skill | Auto-triggers When |
|---|---|
| `security-review` | You mention security, review auth code, or prepare for deployment |
| `deploy-checklist` | You say "deploy", "ship it", "go live", or push to production |

---

## agents/ — Specialized Subagent Personas

Agents are specialized personas that Claude spawns in isolated context windows. They do focused work without cluttering your main session.

Each agent is a `.md` file in `.claude/agents/`:

```markdown
---
name: code-reviewer
description: Expert code reviewer. Use when reviewing PRs or diffs.
model: sonnet
tools:
  - Read
  - Grep
  - Glob
---

You are a senior code reviewer...
```

### Key Fields

| Field | Purpose |
|---|---|
| `name` | How you reference the agent |
| `description` | When Claude should spawn this agent |
| `model` | Which model to use (`haiku` for cheap reads, `sonnet` for focused work, `opus` for deep reasoning) |
| `tools` | What the agent can access (restrict to minimum needed) |

### Cost Optimization with Agents

This aligns with the multi-model cost strategy:

| Agent | Model | Why |
|---|---|---|
| `code-reviewer` | Sonnet | Good balance of quality and speed for review |
| `security-auditor` | Sonnet | Security analysis needs strong reasoning but not Opus-level |
| Read-only explorers | Haiku | Cheap and fast for codebase exploration |

### Agents vs. Multi-Model Workflow

Your workflow already uses different models for different jobs (Opus for planning, Codex for building, Gemini for review). Agents extend this within Claude Code itself:

- **Cross-tool**: Opus (Claude Code) plans → Codex builds → Gemini reviews
- **Within Claude Code**: Main session delegates to reviewer agent → security agent reports back

Both patterns serve the same goal: use the right model at the right cost for the right job.

---

## Global ~/.claude/ Folder

Your global config applies across all projects:

| File/Folder | Purpose |
|---|---|
| `~/.claude/CLAUDE.md` | Personal coding principles — loaded in every session |
| `~/.claude/settings.json` | Global permission defaults |
| `~/.claude/commands/` | Personal commands available everywhere (`/user:name`) |
| `~/.claude/skills/` | Personal skills available everywhere |
| `~/.claude/agents/` | Personal agents available everywhere |
| `~/.claude/projects/` | Auto-saved session transcripts and memory per project |

### What to Put in Global CLAUDE.md

Things that apply regardless of project:

```markdown
# Global Preferences

- Always write tests alongside implementation
- Prefer explicit error handling over silent fallbacks
- Update WORKLOG.md after meaningful changes
- When planning, output phased plans to PLAN.md
- When in doubt, ask rather than assume
```

### Auto-Memory

Claude Code automatically saves notes to `~/.claude/projects/` as it works — commands it discovers, patterns it observes, architecture insights. These persist across sessions.

Browse and edit with `/memory`. Wipe a project's memory to start fresh if Claude has stale context.

---

## Setup Progression

### Day 1 — Minimum Viable Setup

1. Run `/init` in Claude Code to generate a starter CLAUDE.md
2. Edit it down to essentials (under 200 lines)
3. Create `.claude/settings.json` with allow/deny rules for your stack

### Week 1 — Add Commands

4. Create `.claude/commands/review.md` for pre-merge review
5. Create `.claude/commands/quality-gate.md` for pre-commit checks
6. Add any workflow-specific commands (fix-issue, plan-feature, codex-handoff)

### Month 1 — Scale with Rules

7. When CLAUDE.md gets crowded, split instructions into `.claude/rules/`
8. Add path-scoped rules for API conventions, security, etc.
9. Keep both `.claude/rules/` and `.cursor/rules/` in sync

### When Needed — Skills and Agents

10. Convert frequently-used commands into skills for auto-invocation
11. Add agents for specialized tasks (code review, security audit)
12. Set up `~/.claude/CLAUDE.md` with your personal global preferences

---

## Checklist: Files to Create Per Project

| File | Purpose | Priority |
|---|---|---|
| `CLAUDE.md` | Team instructions for Claude Code | Required |
| `.claude/settings.json` | Permission allow/deny rules | Required |
| `.claude/commands/review.md` | Pre-merge diff review | Recommended |
| `.claude/commands/quality-gate.md` | Pre-commit checks | Recommended |
| `.claude/rules/code-style.md` | Code style conventions | When CLAUDE.md > 100 lines |
| `.claude/rules/testing.md` | Testing requirements | When you have tests |
| `.claude/rules/api-conventions.md` | API handler rules (path-scoped) | When you have API routes |
| `.claude/rules/security.md` | Security rules (path-scoped) | When you have auth/sensitive code |
| `.claude/skills/security-review/` | Auto-invoked security audit | When security reviews are frequent |
| `.claude/skills/deploy/` | Auto-invoked deploy checklist | When deploying regularly |
| `.claude/agents/code-reviewer.md` | Spawnable code review agent | When review quality matters |
| `.claude/agents/security-auditor.md` | Spawnable security audit agent | When touching auth/payments |
| `CLAUDE.local.md` | Personal overrides (gitignored) | As needed |
| `.claude/settings.local.json` | Personal permission overrides | As needed |

---

## Templates

All templates are in the `templates/.claude/` directory of this repo. Copy them into your project and customize:

```bash
# Copy the entire .claude/ structure
cp -r templates/.claude/ your-project/.claude/

# Copy CLAUDE.local.md template
cp templates/CLAUDE.local.template.md your-project/CLAUDE.local.md

# Remove .template from filenames and customize
cd your-project/.claude/
for f in $(find . -name "*.template.*"); do
  mv "$f" "${f/.template/}"
done
```

Then fill in project-specific details (stack, commands, path patterns).
