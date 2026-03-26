# AI Coding Tool Rules: .cursor/rules/ vs CLAUDE.md vs AGENTS.md
## The Complete Guide to Giving Your AI Coding Tools Project Instructions

---

## Why This Matters

Every AI coding tool needs to understand your project before it can write good code. Without instructions, it doesn't know your stack, your conventions, your test commands, or how your codebase is organized. You end up repeating yourself every session.

Each of the three major AI coding tools solves this with a "rules" or "memory" file that the AI reads before doing any work. The file names are different, the formats are different, and the capabilities vary — but the goal is identical: **onboard the AI into your codebase so it writes code that fits.**

Here's how each one works.

---

## 1. Cursor: `.cursor/rules/` Directory

### What It Is

Cursor uses a directory of `.mdc` files (Markdown with YAML frontmatter) stored in `.cursor/rules/` at your project root. Each file is a standalone rule with metadata that controls when and how it gets applied. This replaced the old single `.cursorrules` file, which is now deprecated (still works, but Cursor recommends migrating).

### Where the Files Live

```
your-project/
├── .cursor/
│   └── rules/
│       ├── base.mdc              # Core conventions (always applied)
│       ├── frontend.mdc          # Only when working on frontend files
│       ├── api.mdc               # Only when working on API files
│       ├── supabase.mdc          # Only when touching DB-related code
│       └── personal.mdc          # Your local prefs (gitignored)
├── backend/
│   └── .cursor/
│       └── rules/
│           └── backend-api.mdc   # Scoped to backend/ subdirectory
└── src/
```

You can also nest `.cursor/rules/` directories inside subdirectories for scoped rules that only apply when working in that part of the codebase.

**Global rules** (applied to every project) are set in Cursor Settings > General > Rules for AI. These are plain text, not `.mdc` files.

### The .mdc File Format

Every rule file uses YAML frontmatter at the top followed by Markdown content:

```markdown
---
description: "React component conventions for the frontend"
globs:
  - "src/components/**"
  - "src/app/**"
alwaysApply: false
---

# Frontend Rules

- Use Server Components by default; only add 'use client' when needed
- Tailwind CSS for all styling — no inline styles or CSS modules
- shadcn/ui for primitives
- Named exports only, never default exports
- All async operations must use try/catch with our logger
```

### The Four Rule Types

The combination of `alwaysApply`, `globs`, and `description` in the frontmatter determines how the rule behaves:

| Rule Type | How It's Configured | When It Activates |
|-----------|-------------------|-------------------|
| **Always** | `alwaysApply: true` | Injected into every single AI request, no matter what |
| **Auto-Attached** | `globs` defined, `alwaysApply: false` | Only attached when you're working with files that match the glob pattern |
| **Agent-Requested** | `description` present, no `globs`, `alwaysApply: false` | The AI agent reads the description and decides whether the rule is relevant to the current task |
| **Manual** | No description, no globs, no alwaysApply | Never attached automatically — you invoke it explicitly with `@ruleName` in chat |

**Important behavior quirk:** If you set `alwaysApply: true` AND have `globs`, the globs are ignored — the rule is always applied regardless. They don't filter within "always apply" mode.

### How to Create Rules

Three ways:
1. **Command palette:** `Cmd + Shift + P` → "New Cursor Rule"
2. **From chat:** Use the `/Generate Cursor Rules` command during a conversation
3. **Manually:** Create `.mdc` files in `.cursor/rules/`

### Key Features

- **File pattern matching** via gitignore-style globs
- **Reference other files** using `@filename.ts` syntax inside a rule to include them as context
- **Chain rules together** by referencing other `.mdc` files with `@file`
- **Nested directory scoping** — subdirectory rules auto-attach when files in that directory are referenced
- **Version controlled** — the whole `.cursor/rules/` directory is meant to be committed to git
- **40-tool limit** — if you have many MCP servers + rules, you can hit Cursor's context ceiling

### Best Practices

- One concern per rule file — keep them small and focused
- Use `alwaysApply: true` sparingly (only for truly universal conventions)
- Use `globs` for tech-stack-specific rules (frontend, backend, database, tests)
- Use `description` (Agent-Requested) for situational rules the AI should decide about
- Keep rules under ~500 lines each
- Gitignore any personal/local rules you don't want shared with the team

---

## 2. Claude Code: `CLAUDE.md`

### What It Is

Claude Code uses a single `CLAUDE.md` file (standard Markdown, no special format) placed at your project root. Claude reads this file automatically at the start of every session — it becomes part of Claude's system prompt. Think of it as onboarding documentation written for an AI teammate.

### Where the Files Live

```
your-project/
├── CLAUDE.md                     # Main project instructions (committed to git)
├── CLAUDE.local.md               # Personal overrides (gitignored) — DEPRECATED
├── frontend/
│   └── CLAUDE.md                 # Frontend-specific instructions
├── backend/
│   └── CLAUDE.md                 # Backend-specific instructions
└── packages/
    └── shared/
        └── CLAUDE.md             # Package-specific instructions
```

**Loading hierarchy:**
- **Global:** `~/.claude/CLAUDE.md` — applies to all projects on your machine
- **Project root:** `./CLAUDE.md` — the primary project file, committed to git
- **Subdirectories:** Claude discovers `CLAUDE.md` files in subdirectories on-demand when it's working with files in those directories (great for monorepos)
- **Local overrides:** `CLAUDE.local.md` was previously supported but is now deprecated in favor of imports

### The Format

Plain Markdown. No frontmatter, no special syntax, no `.mdc` — just a standard `.md` file with whatever structure makes sense for your project:

```markdown
# Project: Oceans 6 AdMatrix

## Tech Stack
- React 18 + TypeScript + Vite
- Supabase (dev project: xyz, prod project: abc)
- Tailwind CSS + shadcn/ui

## Commands
- `npm run dev` — Start dev server (port 5173)
- `npm run build` — Production build
- `npm run test` — Vitest test suite
- `npx supabase db push` — Push migrations to dev

## Architecture
- `/src/app` — Route pages
- `/src/components/ui` — shadcn primitives (don't modify directly)
- `/src/lib` — Utilities, Supabase client, API helpers
- `/src/hooks` — Custom React hooks

## Code Style
- TypeScript strict mode, never use `any`
- Named exports only
- All async functions must use try/catch with our error logger
- Use Supabase RLS policies — never bypass with service_role in client code

## Important
- NEVER commit .env files
- Always run `npm run test` before committing
- The Stripe webhook at /api/webhooks/stripe MUST validate signatures
```

### How to Create It

- **`/init` command:** Run `/init` inside Claude Code and it analyzes your codebase and generates a starter `CLAUDE.md` automatically. Review and trim it — the auto-generated version tends to be verbose.
- **`#` shortcut:** During any session, press `#` to add an instruction to your CLAUDE.md on the fly. If Claude does something wrong, tell it to add the correction to CLAUDE.md so it sticks for future sessions.
- **Manually:** Just create and edit the file yourself.

### Key Features

- **Hierarchical loading** — global, project root, and subdirectory files are all merged
- **Progressive disclosure** — keep subdirectory CLAUDE.md files for module-specific context so Claude only loads what's relevant to the current task
- **Treated as system-level instructions** — Claude treats CLAUDE.md content with higher priority than your chat prompts. It's closer to "rules" than "suggestions"
- **Slash commands** — Separate from CLAUDE.md, stored in `.claude/commands/` as individual Markdown files you invoke with `/command-name`
- **Skills** — Custom agents stored in `.claude/agents/` as Markdown files with YAML frontmatter
- **MCP config** — Separate from CLAUDE.md, stored in `.mcp.json` or `.claude.json`
- **Settings** — `.claude/settings.json` for permissions, denied file paths, and tool behavior

### Best Practices

- Keep it under ~300 lines (shorter is better — general consensus is <60 lines is ideal for the root file)
- Focus on WHAT (your stack), WHY (project purpose), and HOW (commands, workflows)
- Don't use CLAUDE.md as a linter — use actual linters and formatters, then reference them in commands
- Use subdirectory CLAUDE.md files to keep the root file lean
- Point to documentation files rather than inlining long specs
- Commit to git so the whole team benefits
- Treat it as a living document — update it whenever Claude does something you don't like

---

## 3. OpenAI Codex: `AGENTS.md`

### What It Is

OpenAI Codex uses `AGENTS.md` files — standard Markdown files that provide project instructions, coding conventions, and workflow guidance. Codex reads these files before doing any work, building an "instruction chain" from global defaults down to directory-specific overrides.

### Where the Files Live

```
your-project/
├── AGENTS.md                     # Repo-wide conventions
├── AGENTS.override.md            # Temporary high-priority override (optional)
├── services/
│   └── payments/
│       ├── AGENTS.md             # Payment service-specific rules
│       └── AGENTS.override.md   # Temporary payment-specific override
└── frontend/
    └── AGENTS.md                 # Frontend-specific rules
```

**Loading hierarchy (built once per session):**

1. **Global scope:** `~/.codex/AGENTS.md` (or `AGENTS.override.md` if it exists — override wins)
2. **Project scope:** Starting at the Git root, Codex walks down every directory from root to your current working directory
3. **At each directory level:** Checks for `AGENTS.override.md` first, then `AGENTS.md`, then any fallback filenames you've configured
4. **One file per directory** — Codex picks only the highest-priority file at each level
5. **Files are concatenated** from root down — deeper files appear later in the prompt and can override earlier guidance

### The Format

Plain Markdown, no special syntax required:

```markdown
# AGENTS.md

## Repository Expectations
- Run `npm run lint` before opening a pull request
- Document public utilities in `docs/` when you change behavior
- Use pnpm, not npm or yarn

## Tech Stack
- Next.js 15 App Router + TypeScript
- Supabase for database and auth
- Tailwind CSS + shadcn/ui

## Commands
- `pnpm dev` — Start dev server
- `pnpm test` — Run test suite
- `pnpm lint` — ESLint check
- `pnpm db:push` — Push Supabase migrations

## Code Style
- TypeScript strict mode
- Named exports only
- All error handling must use our custom logger
- Never use console.log in production code

## Architecture
- `/app` — Next.js App Router pages
- `/components/ui` — shadcn primitives (don't modify)
- `/lib` — Shared utilities
- `/supabase` — Migrations and config
```

### The Override System

`AGENTS.override.md` is a key differentiator. It's a temporary, higher-priority file that wins over `AGENTS.md` in the same directory without you having to edit the base file:

```markdown
# services/payments/AGENTS.override.md

## Payments Service Rules (Release Freeze)
- Use `make test-payments` instead of `npm test`
- Never rotate API keys without notifying the security channel
- All changes require manual review — no auto-merge
```

When the freeze is over, delete the override file and the base `AGENTS.md` takes over again. This is great for incident response, release freezes, or temporary workflow changes.

### Fallback Filenames

If your repo already uses a different convention (like `TEAM_GUIDE.md`), you can tell Codex to recognize it:

```toml
# ~/.codex/config.toml
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_doc_max_bytes = 65536
```

Codex then checks each directory in order: `AGENTS.override.md` → `AGENTS.md` → `TEAM_GUIDE.md` → `.agents.md`

### Skills System

Beyond AGENTS.md, Codex also has a Skills system (similar to Claude Code's slash commands):

- Skills are directories containing a `SKILL.md` file plus optional scripts
- Stored in `.agents/skills/` directories
- Invoked explicitly with `$skill-name` in your prompt or implicitly when the task matches the description
- Codex only loads the full SKILL.md content when it decides to use a skill (progressive disclosure)

### PLANS.md for Complex Tasks

Codex has an additional convention: `PLANS.md` — a structured template for multi-step execution plans. You reference it from AGENTS.md and use it for complex features or refactors:

```markdown
# In your AGENTS.md:

## ExecPlans
When writing complex features or significant refactors, use an ExecPlan
(as described in .agent/PLANS.md) from design to implementation.
```

Plans include sections for purpose, progress checkboxes, decision logs, interfaces, testing criteria, and rollback paths. They're designed so a stateless agent can pick up and continue work across sessions.

### Key Features

- **Cascading hierarchy** — the most granular of the three tools. Global → repo root → every subdirectory down to your working directory
- **Override files** — `AGENTS.override.md` for temporary high-priority rules without editing the base
- **Fallback filenames** — configure Codex to recognize your existing docs
- **Size limit** — `project_doc_max_bytes` (default 32KB) caps total instruction size; raise it or split across directories if needed
- **Shared config** — `~/.codex/config.toml` is shared between Codex CLI and the Codex VS Code extension
- **Skills + Plans** — additional structured systems beyond the base instructions

### Best Practices

- Keep a root `AGENTS.md` for repo-wide conventions
- Use subdirectory files for team/service-specific overrides
- Use `AGENTS.override.md` for temporary states (incidents, freezes, sprints)
- Put global defaults in `~/.codex/AGENTS.md` so every repo inherits your working agreements
- Your explicit prompt still overrides any file — AGENTS.md sets defaults, not hard locks

---

## Side-by-Side Comparison

| Feature | Cursor `.cursor/rules/` | Claude Code `CLAUDE.md` | OpenAI Codex `AGENTS.md` |
|---------|------------------------|------------------------|-------------------------|
| **File Format** | `.mdc` (Markdown + YAML frontmatter) | Plain Markdown | Plain Markdown |
| **Location** | `.cursor/rules/*.mdc` | Project root `CLAUDE.md` | Project root `AGENTS.md` |
| **Global Config** | Cursor Settings > Rules for AI | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| **Subdirectory Scoping** | Nested `.cursor/rules/` dirs | Subdirectory `CLAUDE.md` files | Subdirectory `AGENTS.md` files |
| **Cascading/Inheritance** | Glob-based pattern matching | Parent → child directory loading | Full directory walk, root to CWD |
| **Temporary Overrides** | No built-in mechanism | N/A (deprecated `CLAUDE.local.md`) | `AGENTS.override.md` |
| **Conditional Activation** | 4 types: Always, Auto-Attached, Agent-Requested, Manual | All-or-nothing per directory level | All-or-nothing per directory level |
| **File Pattern Matching** | Yes (gitignore-style `globs`) | No (directory-level only) | No (directory-level only) |
| **Auto-Generation** | `/Generate Cursor Rules` in chat | `/init` command | No built-in generator |
| **Quick-Add from Chat** | Yes (via `/Generate Cursor Rules`) | Yes (`#` shortcut) | No |
| **Companion Systems** | Memories, @file references | Slash commands, Skills/Agents, Hooks | Skills (`SKILL.md`), Plans (`PLANS.md`) |
| **Max Size** | No documented limit | ~300 lines recommended | 32KB default (`project_doc_max_bytes`) |
| **Legacy Format** | `.cursorrules` (deprecated) | N/A | Configurable fallback filenames |
| **Version Controlled** | Yes (commit `.cursor/rules/`) | Yes (commit `CLAUDE.md`) | Yes (commit `AGENTS.md`) |

---

## Using All Three in the Same Project

If you're using Cursor, Claude Code, and Codex on the same codebase (or switching between them), you need all three files. The content should be largely the same — your stack, conventions, and commands don't change just because the tool does.

Here's what your project root looks like:

```
your-project/
├── .cursor/
│   └── rules/
│       ├── base.mdc              # Cursor: always-applied core rules
│       ├── frontend.mdc          # Cursor: glob-scoped to frontend files
│       └── supabase.mdc          # Cursor: glob-scoped to DB files
├── CLAUDE.md                     # Claude Code: project instructions
├── AGENTS.md                     # OpenAI Codex: project instructions
├── .claude/
│   ├── commands/                 # Claude Code: slash commands
│   └── settings.json             # Claude Code: permissions
├── .codex/
│   └── config.toml               # Codex: project-scoped config (if needed)
├── .mcp.json                     # Shared MCP server config
├── .env                          # App env vars (public, committed)
├── .env.local                    # App secrets (NEVER committed)
└── src/
```

### Keeping Them in Sync

One practical approach: maintain your canonical instructions in one file (say `CLAUDE.md` since it's plain Markdown with no special format), then reference or mirror it:

- **AGENTS.md** can be nearly identical to CLAUDE.md since both are plain Markdown
- **Cursor's `.mdc` files** require the YAML frontmatter, so you'll need to adapt the content into the `.mdc` format with proper `globs` and `alwaysApply` settings

Some developers create a shared `docs/ai-instructions.md` and have each tool's config file reference it, but this only works with tools that support file references (Cursor's `@file` syntax, Claude's import system).

---

## Quick-Start Template

Here's a minimal starting point you can adapt for any tool. The content is the same — only the file format differs.

### For Cursor (`.cursor/rules/base.mdc`):
```markdown
---
description: "Core project conventions"
alwaysApply: true
---

# Project: [Your Project Name]

## Stack
- [Framework] + [Language]
- [Database]
- [Styling]

## Commands
- `npm run dev` — Start dev server
- `npm run test` — Run tests
- `npm run lint` — Lint check

## Code Style
- [Your conventions here]

## Important
- NEVER commit .env files
- [Your warnings here]
```

### For Claude Code (`CLAUDE.md`):
```markdown
# Project: [Your Project Name]

## Stack
- [Framework] + [Language]
- [Database]
- [Styling]

## Commands
- `npm run dev` — Start dev server
- `npm run test` — Run tests
- `npm run lint` — Lint check

## Code Style
- [Your conventions here]

## Important
- NEVER commit .env files
- [Your warnings here]
```

### For OpenAI Codex (`AGENTS.md`):
```markdown
# Project: [Your Project Name]

## Stack
- [Framework] + [Language]
- [Database]
- [Styling]

## Commands
- `npm run dev` — Start dev server
- `npm run test` — Run tests
- `npm run lint` — Lint check

## Code Style
- [Your conventions here]

## Important
- NEVER commit .env files
- [Your warnings here]
```

Yes — `CLAUDE.md` and `AGENTS.md` are literally the same format. The only one that's structurally different is Cursor's `.mdc` with its YAML frontmatter.

---

*Last updated: March 2026*
