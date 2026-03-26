# Multi-Model Workflow: Claude Code + Codex + Gemini + Cursor + Jules

> Last updated: February 24, 2026
> Primary tools: Claude Code Mac (Max) + Codex Mac (Max)
> Secondary tools: Cursor (Ultra), Gemini CLI, Jules (via MCP)

---

## Table of Contents

1. [Tool Stack and Roles](#1-tool-stack-and-roles)
2. [Project Lifecycle](#2-project-lifecycle)
3. [Task Router](#3-task-router)
4. [How Models Share Context](#4-how-models-share-context)
5. [When to Drop Into Cursor](#5-when-to-drop-into-cursor)
6. [Cost Optimization](#6-cost-optimization)
7. [Integration with Existing Conventions](#7-integration-with-existing-conventions)

---

## 1. Tool Stack and Roles

The workflow treats each tool as a team member with a specialized job. No single model handles everything well; the combination is what produces quality at speed.

| Tool | Role | Strengths | Daily Usage |
|------|------|-----------|-------------|
| **Claude Code Mac (Max)** | Architect | Deep reasoning, cross-file context, global constraint awareness, review synthesis | ~30% of time |
| **Codex Mac (Max)** | Builder | Fast terminal loops, test-run-fix cycles, highest Terminal-Bench scores (77.3%), cheap volume execution | ~50% of time |
| **Gemini CLI** | Reviewer | 1M token context for full-repo review, architectural/structural feedback, 7x cheaper than Opus | ~5% of time |
| **Cursor (Ultra)** | Bootstrapper / Debugger | Project setup, research docs, GitHub connection, plan mode, debug mode, Jules MCP access | ~10% of time |
| **Jules (via Cursor MCP)** | Maintenance Bot | Scheduled security/perf/test agents, dependency updates, overnight PRs | Runs async, review PRs each morning |

### Why This Ordering

Claude Opus 4.6 produces fewer architectural rewrites because its adaptive thinking spends tokens reasoning before writing. Codex 5.3 grinds through implementation faster because it's built for tool-using loops and tight compile-fail-fix cycles. Using a different model to review than the one that built catches ~60% more issues than single-model workflows (Reddit consensus, Feb 2026). Jules handles the tedious maintenance work asynchronously so it never blocks your dev environment.

---

## 2. Project Lifecycle

### Phase 0 — Bootstrap in Cursor

**When:** Starting a new project or connecting an existing repo.

**What happens:**
1. Create the project folder and open it in Cursor
2. Paste research docs, requirements, and reference materials into the project
3. Connect the project to a GitHub repo from Cursor
4. Set up initial structure following `New-Project-Setup-Guide.md`:
   - `WORKLOG.md` with Entry 001
   - `CLAUDE.md` (Claude Code context — Pattern A: focused, short)
   - `AGENTS.md` (Codex context — builder instructions and constraints)
   - `.cursor/rules/000-core.mdc` and `050-worklog.mdc`
   - `README.md`
   - `.env.local.example`
5. Push the initial commit

**No code is written in this phase.** Cursor's value here is its file management UI, GitHub integration, and the ability to write/organize research context in a visual editor.

### Phase 1 — Plan in Claude Code

**When:** Starting a new feature, major refactor, or architectural decision.

**What happens:**
1. Open the project in Claude Code
2. Use `/plan` mode — do not let it write code yet
3. Feed Claude the requirements, constraints, and relevant context from your research docs
4. Ask for output in this structure:
   - Short spec / interface definitions
   - Phased implementation plan (sequential, discrete steps)
   - Risk areas and design decisions called out explicitly
   - Acceptance criteria per phase
5. Save the plan to `PLAN.md` or capture the key decisions in your WORKLOG entry
6. **Get a second opinion (or two)** before executing: paste the plan into Codex `/plan` mode and/or Gemini CLI and ask them to poke holes. Look for missed edge cases, over-engineering, or steps that should be reordered. Revise the plan based on feedback worth keeping.

**Why Claude Code:** Opus 4.6 has an industry-low control flow error rate (55 errors per million lines) and maintains global constraints across designs. It catches contradictions and cross-file invariants early, which prevents expensive rework in Phase 2. The second-opinion step catches Opus's blind spots before any code is written.

**Tips:**
- Use `opusplan` model alias for day-to-day planning to save Opus tokens (plans with Opus, executes with Sonnet)
- Switch to full `opus` only for complex architecture decisions or high-risk logic
- Use `/compact` aggressively in long sessions to manage context
- For complex multi-step features, ask Claude to output a `tasks.json` with dependencies:

```json
[
  {"id": 1, "task": "Set up database schema", "status": "pending"},
  {"id": 2, "task": "Build API endpoints", "status": "pending", "depends_on": 1},
  {"id": 3, "task": "Add frontend forms", "status": "pending", "depends_on": 2}
]
```

### Early-Project Exception: UI/Visual Design Phase

**When:** Building a new app or website where the visual look matters. This replaces the standard Phase 1 → Phase 2 order until the design is established.

Opus produces better-looking websites and apps out of the gate — cleaner layouts, more cohesive styling, better visual hierarchy. For early-stage UI work, **flip the standard roles**: let Opus write the initial code and Codex refine it.

**The pattern:**
1. **Opus writes** — Use Claude Code to build the initial UI: pages, components, layouts, styling. Give it design direction (screenshots, references, descriptions) and let it generate the visual foundation.
2. **Codex edits** — Hand the code to Codex for refinement: fixing responsiveness, tightening interactions, cleaning up edge cases. Iterate with Codex until the general look matches what you're going for.
3. **Switch to standard flow** — Once the visual design is established, revert to the normal workflow: Opus plans, you get a second opinion or two from other models (Gemini, Codex in `/plan` mode), then Codex executes the plan and writes the code going forward.

**Why this works:** Opus has stronger aesthetic judgment and produces more cohesive first-attempt designs. But once the look is locked in, the remaining work is implementation — adding features, wiring up data, writing tests — and that's Codex's strength. The switch point is when you stop saying "make it look like X" and start saying "now build feature Y."

### Phase 2 — Execute in Codex

**When:** The plan is solid and it's time to write code. (Or, if you ran the UI design phase above, when the visual foundation is established and you're ready to build features on top of it.)

**What happens:**
1. Open the project in Codex
2. Start with `/plan` mode — paste the plan from Phase 1 and let Codex confirm it understands the approach
3. Switch to build mode and constrain Codex to **one phase at a time**
4. For each phase, Codex should:
   - Implement the code
   - Run tests
   - Fix failures
   - Report back
5. If Codex gets stuck on a design question, capture it and take it back to Claude Code for a targeted answer, then return to Codex

**Why Codex:** Built for tool-using loops. It scores highest on Terminal-Bench 2.0 (77.3%) because it thrives in tight feedback cycles — build, break, patch, repeat. It also produces the cleanest integration code (only 22 control flow errors per MLOC). This is where 70%+ of your code gets written.

**Tips:**
- Use `xhigh` reasoning mode for maximum accuracy on complex logic
- Keep sessions focused — Codex performance degrades after ~40% context utilization
- Start fresh sessions for each major phase rather than running one massive session
- If a `tasks.json` exists, tell Codex to read it and update task status as it works
- Let Codex write tests as part of implementation, not as an afterthought

### Phase 3 — Review

**When:** Before committing. After Codex has finished a phase or feature.

**What happens:**

**Standard review (every commit):**
1. Generate the diff: `git diff` or `git diff --staged`
2. Pipe it to Gemini CLI for an architectural/structural review:

```bash
git diff | gemini --model gemini-3-pro-preview -p "Review this diff for:
- Structural issues (functions doing too many things, missing separation of concerns)
- Cross-file invariant violations
- Race conditions or concurrency issues
- Patterns that deviate from the rest of the codebase
Be specific: cite file names and line ranges."
```

3. Fix anything Gemini flags that you agree with

**High-risk review (auth, payments, data models, large refactors):**
4. Additionally, paste the diff into Claude Code and ask for a logic/security audit:
   - Auth flows and permission checks
   - Input validation gaps
   - Failure states and edge cases
   - Missing error handling
5. Claude synthesizes its own findings with Gemini's — implements what it agrees with, flags disagreements for your decision

**Why this split:** Gemini catches structural/architectural issues (1M token context, opinionated about design). Codex catches concrete bugs (off-by-one errors, null handling). Claude synthesizes feedback and filters out noise. No single model catches everything.

**Tips:**
- Gemini review is cheap (free tier works) and takes ~30 seconds — do it on every commit
- Claude review is expensive — reserve it for changes that touch auth, payments, schemas, or span many files
- For full-repo health checks, dump the entire codebase into Gemini periodically

### Phase 4 — Quality Gate

**When:** After review, before `git add` / `commit` / `push`.

Follow the full `AI-QUALITY-GATE-SOP.md`. The mandatory steps:

```bash
# Required gates (always run)
npm run lint
npm run test -- --run
npm run build

# Conditional gates (based on changed paths)
PLAYWRIGHT_BASE_URL=http://127.0.0.1:3002 npm run test:e2e  # if UI changed
timeout 120 npx tsc --noEmit                                 # if types/schemas changed

# Secret scan
git diff | rg -n "API_KEY|SECRET|TOKEN|PRIVATE KEY" || true

# Stage explicitly (never blind git add .)
git add <file1> <file2> ...
```

Update `WORKLOG.md` before committing if behavior changed.

### Phase 5 — Push + Jules

**When:** After the quality gate passes.

**What happens:**
1. Push to GitHub
2. Jules scheduled agents run overnight and deliver PRs by morning:
   - **Sentinel** — security vulnerabilities
   - **Bolt** — performance optimizations
   - **Custom agents** — tests, documentation, dead code, type safety (see `Jules-Setup-Guide.md` for full setup)
3. Next morning: review Jules PRs, merge the good ones, close the rest
4. For ad-hoc Jules tasks, use Cursor's Jules MCP integration:

```
"Create a Jules session on sources/github/coleharing1/REPO_NAME
from branch main: [describe the task clearly]"
```

**Important:** Stagger scheduled agent run times to avoid merge conflicts. Merge Jules PRs one at a time. Never ask Jules to resolve its own merge conflicts.

---

## 3. Task Router

When you sit down to work, use this to decide which tool to open:

| Task | Open This | Why |
|------|-----------|-----|
| Architecture / system design | Claude Code (`/plan`) | Deep reasoning, maintains global constraints |
| Greenfield scaffolding (UI/visual) | Claude Code writes, Codex refines | Opus produces better-looking UIs; Codex edits until the look is dialed in, then switch to standard plan→execute flow |
| Greenfield scaffolding (backend/logic) | Claude Code plans, Codex builds | Standard flow — Opus for design, Codex for execution |
| Implementation / build loops | Codex (build mode) | Fastest iteration, best Terminal-Bench scores |
| Bug fixing (code-level) | Codex | Stays close to terminal, fast feedback loops |
| Bug fixing (visual/complex) | Cursor (debug mode) | Browser MCP, Playwright, visual inspection |
| Writing tests | Codex | Cheap iteration, good at boilerplate test coverage |
| Legacy refactoring | Claude Code | Global context awareness prevents cross-file breakage |
| Code review (architectural) | Gemini CLI | 1M token context, opinionated on structure |
| Code review (logic/security) | Claude Code | Catches auth issues, permission problems, failure states |
| Full-repo health check | Gemini CLI | Entire codebase in one prompt |
| Quick questions / small edits | Cursor | Already open, convenient, no context setup |
| Dependency updates / security | Jules (scheduled or ad-hoc) | Async, opens PRs, doesn't block you |
| Documentation / READMEs | Codex or Cursor | Commodity task, any model is fine |
| Project bootstrap / research | Cursor | File management UI, GitHub integration |
| DevOps / CI/CD tasks | Codex or Gemini CLI | Both score high on terminal benchmarks |

### The 30-Second Decision

```
Is it a planning or design question?     → Claude Code
Is it "write code and make tests pass"?  → Codex
Is it "review what I just built"?        → Gemini CLI (+ Claude Code for high-risk)
Is it a debug session?                   → Cursor
Is it maintenance/cleanup?               → Jules
Is it trivial?                           → Whatever's already open
```

---

## 4. How Models Share Context

As a solo developer, you don't need complex orchestration tooling. Manual coordination via shared files covers 90% of cases.

### Primary Method: Shared Files in the Repo

These files act as the coordination layer between all your tools:

| File | Written By | Read By | Purpose |
|------|-----------|---------|---------|
| `PLAN.md` | Claude Code (Phase 1) | Codex (Phase 2), You | Architecture spec, phased steps, risks |
| `tasks.json` | Claude Code (Phase 1) | Codex (Phase 2), You | Task queue with status tracking and dependencies |
| `WORKLOG.md` | Any tool (before commit) | All tools (session start) | Change history with intent, decisions, follow-ups |
| `CLAUDE.md` | You (Phase 0) | Claude Code (auto-loaded) | Persistent project memory — stack, rules, workflow role |
| `AGENTS.md` | You (Phase 0) | Codex (auto-loaded) | Builder instructions — commands, constraints, role |
| `README.md` | Any tool | All tools | Project overview, scripts, env vars |

### How Context Flows Between Tools

```
Cursor (research docs, project structure)
    ↓ push to GitHub
Claude Code (reads CLAUDE.md + WORKLOG.md, writes PLAN.md)
    ↓ you copy the plan or point Codex to PLAN.md
Codex (reads PLAN.md, builds code, updates tasks.json)
    ↓ you run git diff
Gemini CLI (reads the diff, returns review feedback)
    ↓ you fix issues
Quality Gate SOP (lint, test, build)
    ↓ push to GitHub
Jules (reads repo, opens PRs overnight)
```

### Manual Copy-Paste (The 90% Case)

For most tasks, you'll copy-paste between Claude Code and Codex:

- **Claude → Codex:** Copy the plan text or key interface definitions
- **Codex → Gemini:** Pipe the git diff directly to Gemini CLI
- **Codex → Claude:** Copy the diff or specific code sections for targeted review
- **Any → WORKLOG:** Summarize what changed before committing

**Warning from the community:** When summarizing multi-day conversations to pass between models, the receiving model may lose ~50% of detail. If transferring a complex plan, paste the full text rather than asking one model to "summarize for the other."

### Graduation Path: Automated Parallel Review

When manual copy-paste feels like a bottleneck (likely when working on larger codebases), consider:

1. **Gemini CLI one-liners** — Pre-commit hook or alias that pipes `git diff` to Gemini automatically
2. **Shell alias for dual review** — A bash function that sends the diff to Gemini and Claude Code CLI in parallel
3. **The drichelson CLAUDE.md pattern** — Configure Claude Code's global `~/.claude/CLAUDE.md` to automatically shell out to Gemini and Codex for parallel read-only review on significant changes (see `../research/Research-2-Multi-Model-Vibe-Coding.md`, Section 3, Level 3)
4. **Code Review Panel Skill** — Install the ecwilson skill that distributes review to 4+ models simultaneously (see `../research/Research-2-Multi-Model-Vibe-Coding.md`, Section 3, Level 4)

Start simple. Add automation only when the manual step becomes a real friction point.

---

## 5. When to Drop Into Cursor

Cursor is your secondary tool, not your primary one. Use it when its unique strengths justify opening it instead of Claude Code or Codex.

### Always Use Cursor For

- **Project bootstrap** — Creating the initial project structure, pasting research docs, connecting GitHub, setting up WORKLOG/CLAUDE.md/cursor rules. Cursor's file management UI and GitHub integration make this faster than CLI tools.
- **Debug mode** — When you need visual debugging with the browser MCP, Playwright integration, or the built-in visual editor (Cursor 2.2+). Claude Code and Codex are blind to what the UI looks like.
- **Jules MCP interactions** — Creating Jules sessions, checking status, approving plans, reviewing activities. The Jules MCP tools are connected through Cursor.

### Use Cursor When Convenient

- **Plan mode** — When you want Cursor's UI for reviewing or iterating on plans (though Claude Code's `/plan` mode is equally capable)
- **Quick edits** — When Cursor is already open and the change is small enough that spinning up Claude Code or Codex would be overkill
- **Research and docs** — Writing markdown docs, reviewing research, comparing files side-by-side

### Don't Use Cursor For

- **Heavy implementation** — Codex Max plan is more cost-effective for volume code generation
- **Extended build sessions** — Codex's terminal loop is purpose-built for this
- **Architecture decisions** — Claude Code Max plan gives you full Opus access with better context management

---

## 6. Cost Optimization

You're paying for three plans. Here's how to get maximum value from each.

### Current Stack Cost

| Plan | Monthly Cost | Primary Use |
|------|-------------|-------------|
| Claude Max | $100 or $200/mo | Architecture, planning, review synthesis |
| ChatGPT Pro/Plus | $20-$200/mo | Codex implementation volume |
| Cursor Ultra | Variable | Bootstrapping, debug, opportunistic use |
| Gemini CLI | Free (or $25/mo AI Ultra) | Architectural review |
| Jules | Free tier (15 tasks/day) | Scheduled maintenance |

### Token Spend Strategy

**Claude (most expensive: $15/$75 per 1M tokens via API)**
- Use `opusplan` alias for day-to-day work (plans with Opus, executes with Sonnet)
- Switch to full `opus` only for: architecture decisions, security-sensitive reviews, legacy refactors
- Use `/compact` aggressively to manage context in long sessions
- Never use Opus for commodity tasks (docs, tests, simple implementations)

**Codex (cheap volume: ~$2/$8 per 1M tokens)**
- This is your workhorse — don't be stingy with Codex sessions
- Use `xhigh` reasoning for complex logic; default for everything else
- Start fresh sessions per major phase to avoid context degradation

**Gemini (cheapest: $2/$12 per 1M tokens, free tier available)**
- Use liberally for review — it's 7x cheaper than Opus for the same task
- The 1M token context means you can send entire repos without retrieval tricks
- Free tier is sufficient for most solo developer review workflows

**Cursor (burn rate varies by model selection)**
- Don't burn Ultra credits on implementation that Codex handles better and cheaper
- Reserve Cursor for its unique strengths: debug mode, plan mode UI, Jules MCP, bootstrapping
- When using Cursor opportunistically, prefer Sonnet or Flash for quick tasks

### The Golden Rule

**Opus for brains, Codex for hands, Gemini for eyes, Cursor for coordination, Jules for overnight shifts.**

If you catch yourself using Opus to grind through implementation, stop and switch to Codex. If you catch yourself using Codex to review architecture, stop and switch to Gemini or Claude. If you catch yourself building in Cursor when Claude Code or Codex would be faster, stop and switch.

---

## 7. Integration with Existing Conventions

This workflow doesn't replace your existing docs — it sits on top of them and connects them.

| Existing Doc | Governs Which Phase | How It Plugs In |
|---|---|---|
| `New-Project-Setup-Guide.md` | Phase 0 (Bootstrap) | Follow the checklist when creating any new project in Cursor |
| `AI-QUALITY-GATE-SOP.md` | Phase 4 (Quality Gate) | Run the full SOP before every commit, regardless of which tool wrote the code |
| `Jules-Setup-Guide.md` | Phase 5 (Jules) | Reference for Jules setup, scheduled agents, MCP commands, and PR workflow |
| `../research/Research-2-Multi-Model-Vibe-Coding.md` | Phase 3 (Review) | Detailed community patterns for multi-model review automation when you're ready to graduate past manual copy-paste |

### What Stays the Same

- **WORKLOG.md** — Still updated before every commit. The "who" might change (Claude Code, Codex, or Cursor), but the format and discipline don't.
- **CLAUDE.md** — Still the persistent project memory for Claude Code. Now includes a "Workflow" section noting tool roles (see `New-Project-Setup-Guide.md` for the updated template).
- **AGENTS.md** — Codex context file. Builder instructions, commands, constraints. Created alongside CLAUDE.md in Phase 0.
- **Cursor rules** — `000-core.mdc` and `050-worklog.mdc` still apply whenever you work in Cursor. No changes needed.
- **Quality Gate SOP** — Still the pre-commit checklist. The only addition: run Gemini review (Phase 3) before the gate.

### What's New

- **`PLAN.md`** — Optional shared file written by Claude Code in Phase 1, read by Codex in Phase 2. Delete or archive after the feature ships.
- **`tasks.json`** — Optional task queue for complex multi-step features. Same lifecycle as PLAN.md.
- **Gemini CLI review step** — New pre-commit habit between Phase 2 (Execute) and Phase 4 (Quality Gate).

---

## Quick Reference

### Starting a New Project

```
Cursor: Create project → paste research → connect GitHub → set up WORKLOG/CLAUDE.md/rules → push
```

### Building a Feature (Standard)

```
Claude Code /plan → get 2nd opinions → Codex build mode → Gemini review → Quality Gate → push → Jules overnight
```

### Building a New UI (Early Project)

```
Claude Code writes UI → Codex refines look → once design is locked → switch to standard flow above
```

### Daily Morning Routine

```
Review Jules PRs from overnight → merge good ones → check WORKLOG for follow-ups → pick next task
```

### The Decision Shortcut

```
Planning?       → Claude Code
Building?       → Codex
Reviewing?      → Gemini CLI
Debugging?      → Cursor
Maintaining?    → Jules
Trivial?        → Whatever's open
```

---

## Sources

This workflow synthesizes findings from:

- `../research/Research-2-Multi-Model-Vibe-Coding.md` — Community consensus on multi-model workflows (Feb 2026)
- `../research/Gemini-R2-Opinion.md` — Gemini's synthesized opinion on the definitive workflow
- `../research/Grok4.2-R2-Opinion.md` — Grok's analytical opinion with task router and graduated complexity
- `Jules-Setup-Guide.md` — Jules setup, scheduled agents, MCP commands, and best practices
- Adaline Labs, Claire Vo / Lenny's Newsletter, drichelson gist, ecwilson skill — See Research-2 for full citations
