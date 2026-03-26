# New Project Setup Guide

> A reference for bootstrapping new projects for the multi-model workflow: Cursor (bootstrap) + Claude Code (plan) + Codex (build) + Gemini (review) + Jules (maintenance).

---

## How You Use WORKLOG.md

Across your projects (TodoList, MCPs-Project-Cursor, fish-monkey-ad-creative-generator, Oceans 6 Website, tripleaaa&j Ranch), a consistent WORKLOG.md pattern has emerged:

### Purpose

The worklog is a **lightweight running log of meaningful changes** designed to help future-you and AI tools regain context quickly after gaps, pivots, or returning to old branches. It is not a git log replacement — it captures *intent, decisions, and follow-ups* that commits alone don't preserve.

In the multi-model workflow, WORKLOG.md is the **shared memory** that every tool reads. Claude Code reads it at session start to understand recent context. Codex reads it to know what was just built. Gemini reads it during review to understand intent behind changes.

### Format (Standardized Across Projects)

```markdown
# Work Log

A lightweight running log of what changed in this repo over time. This is meant to help future-you (and AI tools) regain context quickly after gaps, pivots, or returning to old branches.

---

## Entry format rules

- Use **entry numbers** (e.g., `Entry 001`, `Entry 002`, ...).
- Keep entries in **reverse order**: newest entry is always at the top (right below this section).

### Entry XXX — Short title

- **Goal**:
- **Changes**:
  - `path/to/file` — what changed (1 sentence)
- **Notes / decisions**:
- **Follow-ups**:
```

### Your Conventions (Observed Across 5+ Projects)

| Convention | Detail |
|---|---|
| **Numbering** | Sequential entry numbers (`Entry 001`, `002`, ...), NOT dates as identifiers |
| **Ordering** | Reverse chronological — newest entry always at the top |
| **Entry scope** | One entry per logical unit of work. Don't combine unrelated work; don't split one feature across entries |
| **Changes section** | Always list real file paths with a one-sentence description per file. Grep-friendly |
| **When to write** | New feature, schema change, refactor, doc overhaul, integration change, config change, deployment fix, dependency upgrade, multi-file refactor |
| **When to skip** | Trivial single-line fixes, typo corrections, cosmetic-only changes |
| **Follow-ups** | Explicit about what's left undone — migration to run, env var to add, test to write |
| **Append-only** | Never remove or edit old entries. The worklog is a historical record |
| **Template at bottom** | Always include a copy/paste template at the end of the file |
| **Placement** | Root of repo (`WORKLOG.md`) or in a docs folder (`_Docs/worklog.md` or `docs/WORKLOG.md`) |

### What Makes Your Entries Good

Looking at your best entries (TodoList entries 017-028, fish-monkey entries 049-072, ranch entries 011-020):

1. **Goal is one sentence** — forces clarity about what you set out to do
2. **Changes list every file touched** — makes the entry searchable and verifiable
3. **Notes capture the "why"** — architectural decisions, tradeoffs, root causes
4. **Follow-ups are actionable** — "Run migration on prod", "Add CRON_SECRET to Vercel"
5. **Tests/verification section** (in larger projects) — what commands you ran to verify the work

### Scaling Pattern

| Project Size | Entry Detail Level |
|---|---|
| Small/prototype | Goal + Changes + Notes (3-5 lines per entry) |
| Medium app | Goal + Changes + Notes + Follow-ups (8-15 lines) |
| Large app (TodoList, fish-monkey) | Goal + Changes (every file) + Tests/verification + Notes + Follow-ups (15-40 lines) |

---

## AI Context Files

Your project needs context files for the two desktop apps that will do the real work: **CLAUDE.md** for Claude Code and **AGENTS.md** for Codex. These serve the same purpose (persistent project memory) but are read by different tools.

### CLAUDE.md — For Claude Code

Claude Code auto-loads `CLAUDE.md` from the project root at session start. This is your primary channel for telling Opus how the project works and what role it plays.

**Pattern A: Focused Rules File (Preferred for Real Projects)**

Used in: Kingdom-Shopify-Clone, Creative Management Platform, Ecom Scraping, alphaschool

```markdown
# Claude Rules — [Project Name]

## Answer style (non-negotiable)
- [How AI should communicate and format outputs]

## Project defaults (assume unless told otherwise)
- [Tech stack, framework versions, key patterns]

## Safety & limits
- [What NOT to do — destructive commands, config files to never touch]

## When to ask (rare)
- [Only ask when a decision blocks correctness]
```

**Characteristics:**
- Short (30-100 lines)
- Imperative language ("Provide complete code", "Never commit X")
- Project-specific constraints front and center
- Tells the AI what to assume so it doesn't ask

**Pattern B: Comprehensive Template (For Larger/Team Projects)**

Used in: TodoList templates, Starting-Documents

```markdown
# Project Conventions & Context

## Project Overview
## Architecture Decisions
### Tech Stack
### Design Patterns
## Code Conventions
### File Structure
### Naming Conventions
### Code Style Rules
## API Conventions
## Database Schema
## Testing Strategy
## Environment Variables
## Current Development Status
## Known Issues & Workarounds
## AI Assistant Instructions
## Useful Commands
```

**Characteristics:**
- Longer (100-200 lines)
- Serves as both AI context and human onboarding doc
- Includes runnable commands, env var lists, and file structure trees
- Has a "Recent Changes Tracker" section for session continuity

**Recommendation for New Projects:**
Start with Pattern A (focused, short). Expand to Pattern B only if the project grows past ~20 files, multiple AI tools need context, or the tech stack has non-obvious constraints.

### AGENTS.md — For Codex

Codex reads `AGENTS.md` from the project root. This tells Codex its role (builder), what commands to run, and what constraints to follow. Keep it short and imperative — Codex works best with direct instructions.

**Template:**

```markdown
# AGENTS.md — [Project Name]

## Role
You are the builder. Implement code based on the plan in PLAN.md (if it exists) or direct instructions. Run tests after every change. Fix failures before reporting back.

## Stack
- [Framework, language, styling, database, deployment — one line each]

## Commands
- `npm run dev` — start dev server
- `npm run build` — production build
- `npm run test -- --run` — run tests
- `npm run lint` — lint check
[Add project-specific commands]

## Rules
- Read PLAN.md before starting if it exists
- Implement one phase/task at a time — do not skip ahead
- Run tests after every meaningful change
- Prefer functional/declarative patterns; avoid classes
- Search existing code before creating new files or abstractions
- Prefer clear errors over silent fallbacks
- Avoid `any` when feasible; keep boundaries typed
- Files under 500 lines; split into modules if approaching the limit
- Update WORKLOG.md after completing a feature or significant change

## Safety
- Never run destructive commands without confirmation
- Never commit secrets, .env files, or credential files
- Never modify production config directly

## Testing
- Write tests alongside implementation, not as an afterthought
- Run the full test suite before reporting a phase as complete
- If tests fail, fix them before moving to the next phase
```

---

## Cursor Rules Patterns

Your cursor rules follow a numbered naming convention across projects. These apply when you work in Cursor (Phase 0 bootstrap, debug mode, quick edits).

### Naming Convention

```
.cursor/rules/
├── 000-core.mdc              # Project identity and global constraints
├── 010-safety.mdc            # Destructive command guards
├── 050-project-journals.mdc  # Worklog and debug journal rules
├── 100-frontend.mdc          # Frontend framework rules
├── 200-backend.mdc           # Backend/API rules
├── 300-testing.mdc           # Testing requirements
├── 400-docs.mdc              # Documentation maintenance
├── 900-context.mdc           # Project context and state
```

Lower numbers = higher priority. The 000-099 range is for project-wide rules, 100-499 for domain-specific rules, 900+ for context.

### The Two Rules That Always Exist

**1. Worklog Reminder Rule** (`alwaysApply: true`)

```markdown
---
description: Require worklog updates for meaningful changes
alwaysApply: true
---

# Worklog Discipline

When making meaningful project changes, update `WORKLOG.md` before final handoff.

## Update Required For
- Behavior changes (UI flow, route behavior, runtime behavior)
- Architecture or implementation pattern changes
- Process and governance changes

## Entry Expectations
- Add the newest entry at the top (reverse chronological)
- Include: Goal, Changes (with file paths), Notes/decisions, Follow-ups
- Keep entries specific and grep-friendly (use real file paths)

## Do Not Skip
If you changed code or process and did not update WORKLOG.md, stop and add the entry before concluding work.
```

**2. Core Project Rule** (`alwaysApply: true`)

```markdown
---
description: Core project identity, stack, and global constraints
alwaysApply: true
---

# Core — [Project Name]

## Stack
- [Framework, language, styling, database, deployment]

## Global Rules
- Search existing code before creating new files or abstractions
- Prefer minimal diffs; avoid cosmetic refactors unless requested
- Prefer functional/declarative patterns; avoid classes unless integrating external clients
- Prefer clear errors over silent fallbacks
- Avoid `any` when feasible; keep boundaries typed

## Safety
- Never run destructive commands without confirmation
- Never commit secrets or credential files
- Never modify production config directly
```

### Optional Rules (Add As Needed)

| Rule | When to Add |
|---|---|
| `040-docs-and-changelog.mdc` | When README accuracy matters (docs drift is a real problem) |
| `100-frontend.mdc` | React/Next.js projects with UI conventions |
| `100-shopify.mdc` / `100-wordpress.mdc` | Platform-specific projects |
| `200-backend.mdc` | Supabase/API projects with schema and RLS patterns |
| `300-testing.mdc` | When you have a real test suite |

---

## New Project Checklist

This is Phase 0 of the multi-model workflow. Everything here happens in Cursor.

### Step 1: Create the repo and initial files

```
project-root/
├── README.md                  # Project overview (see template below)
├── WORKLOG.md                 # Start with Entry 001
├── CLAUDE.md                  # Claude Code context (Pattern A to start)
├── CLAUDE.local.md            # Personal overrides (gitignored)
├── AGENTS.md                  # Codex context (builder instructions)
├── plans/                     # Dual-plan workflow (Claude + Codex competing plans)
│   ├── active/                #   Current feature plans
│   └── archive/               #   Completed plans (decision history)
├── .claude/
│   ├── settings.json          # Claude Code permissions (allow/deny)
│   ├── commands/              # Custom slash commands
│   │   ├── review.md          #   → /project:review (pre-merge diff review)
│   │   ├── fix-issue.md       #   → /project:fix-issue (GitHub issue fixer)
│   │   ├── dual-plan.md       #   → /project:dual-plan (Claude writes competing plan)
│   │   ├── compare-plans.md   #   → /project:compare-plans (synthesize Final)
│   │   ├── archive-plan.md    #   → /project:archive-plan (active → archive)
│   │   ├── quality-gate.md    #   → /project:quality-gate (pre-commit checks)
│   │   └── codex-handoff.md   #   → /project:codex-handoff (Final plan → Codex)
│   ├── rules/                 # Modular instructions (loaded with CLAUDE.md)
│   │   └── code-style.md      #   Start with one; add more as needed
│   ├── skills/                # Auto-invoked workflows (add later)
│   └── agents/                # Subagent personas (add later)
├── .cursor/
│   └── rules/
│       ├── 000-core.mdc       # Stack + global rules
│       └── 050-worklog.mdc    # Worklog discipline
├── .gitignore
├── .env.local.example         # Required env vars (never commit .env.local)
└── [project files]
```

### Step 2: Write Entry 001 in WORKLOG.md

Your first entry should capture the initial project setup:

```markdown
### Entry 001 — Initial Project Setup

- **Goal**: [What this project is and why it exists]
- **Changes**:
  - Created base project files: `.gitignore`, `README.md`, `WORKLOG.md`, `CLAUDE.md`, `AGENTS.md`
  - Added cursor rules: `000-core.mdc`, `050-worklog.mdc`
  - Scaffolded [framework] project with [key dependencies]
- **Notes / decisions**:
  - [Key tech stack choices and why]
  - Workflow: Claude Code (plan) → Codex (build) → Gemini CLI (review) → Jules (maintenance)
- **Follow-ups**:
  - [What to build first]
  - Connect Jules scheduled agents once repo is on GitHub
```

### Step 3: Write CLAUDE.md

```markdown
# [Project Name]

## Stack
- **Framework**: [e.g., Next.js 15 App Router]
- **Styling**: [e.g., Tailwind CSS + shadcn/ui]
- **Database**: [e.g., Supabase (Postgres + Auth + Storage)]
- **Deployment**: [e.g., Vercel]

## Workflow
- You (Claude Code) handle planning, architecture, and high-risk review
- Codex handles co-planning and implementation
- Gemini CLI handles pre-commit architectural review
- Jules handles overnight maintenance via scheduled agents
- Use `/project:dual-plan` to write your plan to `plans/active/`
- Codex writes its competing plan independently, then `/project:compare-plans` to synthesize

## Rules
- Provide complete, working code — no placeholders
- Search existing code before creating new files
- Prefer functional/declarative patterns
- Throw errors instead of silent fallbacks
- Avoid `any` when feasible; keep boundaries typed
- Update WORKLOG.md after meaningful changes

## Structure
[Paste your file tree here once scaffolded]

## Commands
- `npm run dev` — start dev server
- `npm run build` — production build
- `npm run test` — run tests
[Add project-specific commands]

## Current State
[Update this as the project evolves]
```

### Step 4: Write AGENTS.md

```markdown
# AGENTS.md — [Project Name]

## Role
You are the builder and co-planner.
- **Planning:** Write your independent plan to `plans/active/Plan-XXX-Codex.md` when given a planning prompt. Do not read Claude's plan first.
- **Building:** Implement from `plans/active/Plan-XXX-Final.md` (the synthesized plan) or direct instructions. Run tests after every change. Fix failures before reporting back.

## Stack
- **Framework**: [e.g., Next.js 15 App Router]
- **Styling**: [e.g., Tailwind CSS + shadcn/ui]
- **Database**: [e.g., Supabase (Postgres + Auth + Storage)]
- **Deployment**: [e.g., Vercel]

## Commands
- `npm run dev` — start dev server
- `npm run build` — production build
- `npm run test -- --run` — run tests
- `npm run lint` — lint check

## Rules
- Read PLAN.md before starting if it exists
- Implement one phase/task at a time — do not skip ahead
- Run tests after every meaningful change
- Search existing code before creating new files or abstractions
- Prefer functional/declarative patterns; avoid classes
- Prefer clear errors over silent fallbacks
- Avoid `any` when feasible; keep boundaries typed
- Files under 500 lines; split into modules if approaching the limit
- Update WORKLOG.md after completing a feature or significant change

## Safety
- Never run destructive commands without confirmation
- Never commit secrets, .env files, or credential files
- Never modify production config directly
```

### Step 5: Create cursor rules

Minimum viable rules for any project:

**`.cursor/rules/000-core.mdc`**
```markdown
---
description: Core project identity and global constraints
alwaysApply: true
---

# Core — [Project Name]

## Stack
[One line per technology]

## Global Rules
- Search existing code/patterns before creating new files or abstractions
- Prefer minimal diffs; avoid cosmetic refactors unless requested
- Prefer functional/declarative patterns; avoid classes
- Prefer clear errors over silent fallbacks; surface actionable error messages
- Avoid `any` when feasible; keep boundaries typed
- Files under 500 lines; split into modules if approaching the limit

## Safety
- Never run destructive commands without confirmation
- Never commit secrets, .env files, or credential files
- Never modify production config directly
```

**`.cursor/rules/050-worklog.mdc`**
```markdown
---
description: Require worklog updates for meaningful changes
alwaysApply: true
---

# Worklog Discipline

When making meaningful project changes, update `WORKLOG.md` before final handoff.

## Update Required For
- Behavior changes (UI flow, route behavior, runtime behavior)
- Architecture or implementation pattern changes
- Process and governance changes (SOPs, rules, delivery policies)

## Entry Expectations
- Read the latest entry number before adding a new one
- Add the newest entry at the top (reverse chronological)
- Include: Goal, Changes (with real file paths), Notes/decisions, Follow-ups
- One entry per logical unit of work
- Keep entries specific and grep-friendly

## Do Not Skip
If you changed code or process and did not update WORKLOG.md, stop and add the entry before concluding work.
```

### Step 6: Set up .claude/ folder

Create `.claude/settings.json` with permission rules for your stack:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Read", "Write", "Edit", "Glob", "Grep"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(curl *)",
      "Bash(git push --force *)",
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  }
}
```

Add at least one custom command. Start with `/project:review` (pre-merge diff review) and `/project:quality-gate` (pre-commit checks). Copy templates from `templates/.claude/commands/`.

Optionally create `CLAUDE.local.md` for personal overrides (auto-gitignored).

See `Claude-Code-Folder-Guide.md` for the full setup reference including rules, skills, and agents.

### Step 7: Write README.md

See template in the next section.

### Step 8: Connect GitHub and push

1. Initialize the repo: `git init && git add . && git commit -m "chore: initial project setup"`
2. Create the GitHub repo and push
3. Connect Jules to the repo (see `Jules-Setup-Guide.md` for Jules setup)
4. Enable Jules Memory for the repo (Settings > Knowledge > Toggle Memory ON)
5. Set up Jules scheduled agents (Sentinel, Bolt, and custom agents as needed)

### Step 9: Start Phase 1 in Claude Code

Open the project in Claude Code. It auto-loads `CLAUDE.md` and `.claude/rules/`. Use `/plan` mode to begin architecture, or try `/project:plan-feature` for structured planning. From here, follow `Multi-Model-Workflow.md`.

---

## README.md Template

```markdown
# [Project Name]

> [One-line description]

## Current Status

[What works now, what doesn't, what's next — keep this honest]

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | [e.g., Next.js 15] |
| Language | [e.g., TypeScript (strict)] |
| Styling | [e.g., Tailwind CSS + shadcn/ui] |
| Database | [e.g., Supabase] |
| Deployment | [e.g., Vercel] |
| Testing | [e.g., Vitest + Playwright] |

## Getting Started

### Prerequisites
- Node.js [version]
- [Other requirements]

### Setup
[Copy-pasteable commands]

### Environment Variables
[List required vars with where to find each value]

## Project Structure

[File tree of key directories]

## Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run test` | Run tests |

## Documentation

| File | Purpose |
|---|---|
| `WORKLOG.md` | Running change log with decisions and follow-ups |
| `CLAUDE.md` | Claude Code context — stack, rules, workflow role |
| `AGENTS.md` | Codex context — builder instructions and constraints |
| `.cursor/rules/` | Cursor-specific AI behavior rules |
| `plans/` | Dual-plan workflow — competing plans from Claude + Codex, synthesized Final |
```

---

## Quick Reference: Files to Create for Every New Project

| File | Purpose | Read By | Priority |
|---|---|---|---|
| `WORKLOG.md` | Change history with intent and decisions | All tools | Required |
| `CLAUDE.md` | AI context for Claude Code — stack, rules, workflow role | Claude Code | Required |
| `AGENTS.md` | AI context for Codex — builder instructions, commands | Codex | Required |
| `.claude/settings.json` | Claude Code permissions — allow/deny rules | Claude Code | Required |
| `.claude/commands/review.md` | Pre-merge diff review (`/project:review`) | Claude Code | Recommended |
| `.claude/commands/quality-gate.md` | Pre-commit checks (`/project:quality-gate`) | Claude Code | Recommended |
| `.claude/commands/dual-plan.md` | Claude writes competing plan (`/project:dual-plan`) | Claude Code | Recommended |
| `.claude/commands/compare-plans.md` | Synthesize Final plan (`/project:compare-plans`) | Claude Code | Recommended |
| `.claude/commands/archive-plan.md` | Archive completed plans (`/project:archive-plan`) | Claude Code | Recommended |
| `.claude/commands/fix-issue.md` | GitHub issue fixer (`/project:fix-issue`) | Claude Code | Recommended |
| `.claude/commands/codex-handoff.md` | Final plan → Codex brief (`/project:codex-handoff`) | Claude Code | Recommended |
| `plans/active/` | Current feature plans (Claude + Codex + Final) | Claude Code, Codex | Required |
| `plans/archive/` | Completed plan sets (decision history) | Everyone | Required |
| `.claude/rules/code-style.md` | Code style conventions | Claude Code | When CLAUDE.md > 100 lines |
| `.claude/rules/testing.md` | Testing requirements | Claude Code | When tests exist |
| `.claude/rules/api-conventions.md` | API handler rules (path-scoped) | Claude Code | When API routes exist |
| `.claude/rules/security.md` | Security rules (path-scoped) | Claude Code | When auth/sensitive code exists |
| `.claude/skills/security-review/` | Auto-invoked security audit | Claude Code | When security reviews are frequent |
| `.claude/skills/deploy/` | Auto-invoked deploy checklist | Claude Code | When deploying regularly |
| `.claude/agents/code-reviewer.md` | Spawnable code review agent | Claude Code | When review quality matters |
| `.claude/agents/security-auditor.md` | Spawnable security audit agent | Claude Code | When touching auth/payments |
| `CLAUDE.local.md` | Personal Claude Code overrides (gitignored) | Claude Code | As needed |
| `.cursor/rules/000-core.mdc` | Project identity and global constraints | Cursor | Required |
| `.cursor/rules/050-worklog.mdc` | Enforce worklog discipline | Cursor | Required |
| `.cursor/rules/040-docs.mdc` | README/docs maintenance rules | Cursor | Recommended |
| `.cursor/rules/100-[domain].mdc` | Domain-specific rules (frontend, Shopify, etc.) | Cursor | As needed |
| `.cursor/rules/300-testing.mdc` | Testing requirements and patterns | Cursor | When tests exist |
| `README.md` | Human onboarding and project overview | Everyone | Required |
| `.env.local.example` | Document required environment variables | Everyone | Required (if any env vars) |
| `tasks.json` | Task queue with dependencies | Claude Code, Codex | Per feature (optional) |
| `_docs/` or `docs/` | Extended documentation (guides, plans) | Everyone | For larger projects |

---

## What Happens After Setup

Once Phase 0 is complete and the initial commit is pushed:

```
Phase 0  (done)  → Setup complete, context files and plans/ folder ready
Phase 1a         → Claude Code: /project:dual-plan → writes Plan-XXX-CLAUDE.md
Phase 1b         → Codex: same prompt → writes Plan-XXX-Codex.md
Phase 1c         → Claude Code: /project:compare-plans → writes Plan-XXX-Final.md
Phase 1d         → You: review and finalize the plan
Phase 2          → Codex: implement from Plan-XXX-Final.md, one phase at a time
Phase 3          → Gemini CLI: pre-commit review of the diff
Phase 4          → Quality Gate: lint, test, build, E2E, secret scan
Phase 5          → Jules: push to GitHub, overnight agents
                 → Claude Code: /project:archive-plan → move plans to archive
```

See `Multi-Model-Workflow.md` for the full lifecycle and `Dual-Plan-Workflow.md` for the competing plans process.
