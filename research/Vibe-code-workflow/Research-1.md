All three research agents are done. Here's the full compiled report:

---

# Deep Dive: AI Coding Feedback Loops, Database Workflows, and What's New in 2026

---

## Part 1: How People Give AI Coding Tools Visual Feedback Loops

The core problem: AI coding agents are "blind" -- they write frontend code but can't see the result. The community has developed several approaches ranked by popularity:

### Tier 1: Playwright MCP (The Gold Standard)

The single most recommended approach across Reddit and the community. Microsoft's official Playwright MCP server gives AI agents a real browser they can control.

**Setup is one command:**
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

The AI navigates to `localhost:3000`, reads the accessibility tree (structured semantic page representation), takes screenshots, reasons about what it sees, and fixes issues. A real Chrome window opens so you can watch it work. Simon Willison's tip: say "use playwright mcp" the first time or Claude will try bash-based workarounds.

**Why it's #1:** 25 browser tools exposed, cookies persist (so you can log in manually and the AI keeps working), and it works with both Claude Code and Cursor.

### Tier 2: Round-Trip Screenshot Testing

Created by Tal Rotbart (Feb 2026) -- a custom Claude Code slash command (`/screenshot-test`) that:
1. Runs system tests with `SCREENSHOTS=1` to capture PNGs around every browser action
2. Has Claude visually examine every screenshot using its vision capabilities  
3. Claude flags broken layouts, overlapping elements, missing content
4. Claude fixes and re-runs

The key insight: encode the instructions in `CLAUDE.md` so Claude does this *automatically* during development, not just when asked.

### Tier 3: The Dev Browser Skill (Most Efficient)

Created by Sawyer Hood. He identified that Playwright MCP causes "context explosion" -- every step needs a screenshot or DOM snapshot, adding 33+ tools that confuse the agent.

His solution uses **persistent browser sessions** (browser runs as a server, survives between script executions) and **small atomic scripts** with tight feedback loops. Benchmarks vs Playwright MCP:
- 14% faster execution
- 39% less cost ($0.88 vs $1.45)
- 43% fewer turns (29 vs 51)

### Tier 4: The Ralph Wiggum Loop

Originally by Geoffrey Huntley, now has an **official Anthropic plugin**. Dead simple:
```bash
while :; do cat PROMPT.md | claude-code ; done
```

Each iteration: Claude works on a task, runs tests, updates a plan file, and when context fills, a fresh agent picks up where the last left off. Progress persists in files and git, not in the LLM's context. One developer claims they shipped 6 repos overnight; another completed a $50K contract for $297 in API costs.

**Note:** Ralph is text-based (tests/compilation as signals). For visual work, people combine it with Playwright MCP.

### Tier 5: Figma MCP + Playwright MCP Combo

The most sophisticated design-to-code loop:
- **Figma MCP** = what the UI *should* look like (design spec)
- **Playwright MCP** = what the UI *actually* looks like (live capture)
- Claude compares the two and closes the gap

### Other Notable Approaches

- **Claude Preview (built-in):** Claude Code desktop can launch dev servers and display running apps directly in the interface with element selection for feedback
- **Cursor's Built-in Visual Editor (2.2+):** Browser sidebar with visual sliders for moving/resizing/coloring elements, then Cursor translates visual changes into code edits
- **Hammerspoon Screenshot Workflow (macOS):** Bind Cmd+Shift+6 to capture a screen region and paste directly into the Claude Code terminal
- **viewpo-mcp:** Multi-viewport responsive testing -- captures a URL at multiple widths simultaneously and compares responsive layouts
- **Frontend Dev Plugin (8-agent system):** Coordinator, Frontend Tester, Frontend Validator, UX Specialist, etc. with quality gates (PASS 95-100 / ITERATE 65-84 / FAIL <65) and up to 5 automatic fix-and-retest iterations

### Key Takeaway

The industry is moving from raw screenshots toward **accessibility trees** as the primary representation. Screenshots cause context window explosion; accessibility trees are structured, semantic, and token-efficient. The best tools use both strategically -- accessibility tree for understanding, screenshots for visual verification.

---

## Part 2: Vibe Coder Database Preferences

### S-Tier: Supabase (The Default)

By far the #1 choice. It's the default database for v0, Lovable, and Bolt. The "vibe coder default stack" in 2026 is: **Next.js + Supabase + Drizzle + Vercel**.

**Why it dominates:**
- All-in-one: Postgres + auth + storage + realtime + edge functions
- Generous free tier: 500MB database, 50K MAU auth, 1GB storage
- Row Level Security lets your frontend talk directly to the DB safely (no middleware needed)
- Standard PostgreSQL under the hood -- no lock-in
- MCP integration with both Cursor and Claude Code

**Local dev workflow:**
```bash
supabase init
supabase start  # spins up full stack locally via Docker
```
Then `supabase db diff` captures schema changes as migration SQL files. Some devs skip local entirely and work against a free-tier cloud project.

**Pain points:** Docker dependency, confusing relation between `migration` and `db` commands, one dev titled their Medium post "My First Time Setting Up Supabase Locally (and Why It Almost Broke Me)."

### A-Tier: Neon (The Serverless Postgres)

Strong second choice, especially for CI/CD-heavy workflows.

**Killer feature: database branching.** Instant copies of production for dev/testing -- no local database needed. Branches spin up in <10 seconds, cost nothing when idle, cold starts under 1 second.

Post-Databricks acquisition (May 2025), storage pricing dropped from $1.75 to $0.35/GB-month. Free tier: 100 projects, 100 CU-hours.

**Trade-off:** Pure database only -- no built-in auth, storage, or functions. You pick your own tools for those.

### A-Tier: Turso / libSQL (The Edge Play)

Growing niche for edge computing and truly personal apps.

**Local workflow is unbeatable:** develop against a local SQLite file -- zero config, zero Docker, zero network. Push to Turso for production with global distribution. 5GB free storage, built-in vector search for AI/embedding use cases.

### B-Tier: PocketBase (The Self-Hoster's Dream)

Single Go executable containing DB + auth + file storage + realtime + admin dashboard. Uses SQLite under the hood. Deploy to a $6/month VPS and handle 10K+ concurrent connections. Same binary runs locally and in production.

**Trade-off:** Personal open-source project (no paid team/SLA), docs described as "kinda bad."

### B-Tier: Cloudflare D1 (The Edge Alternative)

Managed serverless SQLite on Cloudflare's edge. Compelling for developers already in the Cloudflare ecosystem. Community says the free tier is the best available.

### ORM Preferences

| ORM | Status | Why |
|-----|--------|-----|
| **Drizzle** | The vibe coder favorite, momentum clearly shifting here | ~57KB runtime vs Prisma's 2MB+, no codegen step, SQL-first, works everywhere |
| **Prisma** | Still the DX king | Better docs, larger community, Prisma 7 removed the Rust binary (now pure TS) |
| **Raw supabase-js** | Common for simpler apps | Skip the ORM entirely, use auto-generated REST APIs |

### The AI-Integrated Workflow

The real game-changer: **Supabase MCP** lets Cursor/Claude Code query, create tables, and modify schemas directly from the IDE. Developers describe what they want in natural language and the AI sets up the database connection and feature. One common setup: Claude Code + CLAUDE.md + GitHub MCP + Supabase MCP.

---

## Part 3: What's New and Interesting (Late 2025 - Feb 2026)

### Game-Changers

**Apple Xcode 26.3 -- Agentic Coding in Xcode (Feb 3, 2026)**
Apple integrated Claude Agent and OpenAI Codex directly into Xcode. Agents search docs, explore files, update project settings, and verify work visually by capturing Xcode Previews. Uses MCP, so any MCP-compatible agent can integrate. This legitimizes agentic coding as mainstream.

**GitHub Agent HQ -- Multi-Agent Platform (Feb 4, 2026)**
Run Claude, Codex, and Copilot simultaneously on the same task within GitHub. Compare how different agents approach the same problem. Available in public preview for Copilot Pro+ and Enterprise.

**Claude Code LSP Integration (Dec 2025)**
Native Language Server Protocol support -- go-to-definition, find references, hover docs across 11 languages. Navigating codebases in 50ms vs 45 seconds via text search. Closes a major gap with IDE-based tools.

**MCP Becoming the Universal Standard**
Apple adopted it for Xcode, GitHub supports it in Agent HQ, every major tool integrates it. MCP is now the USB-C of AI tool integration.

### Major Improvements

**Claude Code Task DAGs (Jan 2026):** Persistent tasks with directed acyclic graph dependencies. Tasks can block other tasks, coordinate across sessions and subagents, survive context resets.

**Claude Code Worktree Isolation (Jan 2026):** `--worktree` / `-w` flag creates isolated git worktrees per session. Combined with `--tmux`, fully isolated parallel agents on the same repo.

**Claude Code Plugin Ecosystem (Early 2026):** 9,000+ plugins available. Install via `/plugin marketplace add user-or-org/repo-name`.

**Claude Code Auto Memory (Feb 2026):** Automatically records patterns and conventions to `MEMORY.md`. First 200 lines loaded into system prompt every session.

**Cursor Subagents (Feb 2026):** Parallel execution -- one subagent researches, another writes code, a third runs terminal commands simultaneously. Benchmark: Next.js migration in 9 min parallel vs 17 min serial.

### Community Best Practices

**CLAUDE.md tips (community consensus):**
- Keep under 150 lines (bloated files get ignored)
- Use imperative language ("MUST use TypeScript strict mode" not "Prefer TypeScript")
- Include runnable commands (`npm run test`, `npm run build`)
- Document architecture patterns with file paths
- Tell Claude to plan before coding

**Advanced Claude Code tips:**
- Run Claude Code controlling another instance inside Docker via tmux for autonomous experimental work
- Use Gemini CLI as a subagent for second-opinion reasoning
- `/compact` aggressively in long sessions
- Multiple parallel sessions in Warp terminal
- Voice input (Whisper) with parallel sessions for speed

### Industry Stats

- AI writes ~30% of Microsoft's code and >25% of Google's code
- MIT named generative coding one of its 10 Breakthrough Technologies for 2026
- Developers integrate AI into 60% of their work but can only fully delegate 0-20% of tasks
- A Rakuten team pointed Claude Code at a 12.5M-line codebase; it worked autonomously for 7 hours and hit 99.9% numerical accuracy
- ~45% of AI-generated code fails security tests (Veracode report)

### The Big Picture

**2026 is the year AI coding moved from "assistant" to "agent."** The shift is from single-turn code generation to multi-agent orchestration, parallel execution, persistent task management, and autonomous multi-hour work sessions. The developer's role is increasingly about architecture, oversight, and orchestration rather than line-by-line implementation.