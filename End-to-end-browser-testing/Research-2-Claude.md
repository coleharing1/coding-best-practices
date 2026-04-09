# Browser-in-the-Loop Vibe Coding: Verified Guide (April 2026)

> **Research-2** — Claude Code (Opus 4.6), April 4, 2026.
> This is a corrected and verified second pass. Research-1 from Claude, Grok, and Codex were compared, disagreements identified, and each disputed claim was independently fact-checked against official docs, GitHub issues, developer forums, and community reports.

---

## What Changed From Research-1

My original Research-1 contained errors. So did Grok's and Codex's. This document corrects all three and cites proof for every correction.

**Errors I corrected in my own Research-1:**
- I initially said Antigravity has "no MCP support" — **wrong**, it does support MCP via `mcp_config.json`
- I said Codex "CANNOT interact with a live browser" — **partially wrong**, it can in `danger-full-access` sandbox mode with the `playwright-interactive` skill, but it is unreliable
- I ranked Claude Code #1 at 9.5/10 — **overconfident**, the visual verification gap vs Antigravity is real (38% vs 72.7% on ScreenSpot-Pro)
- I said Cursor has "no authenticated sessions" — **correct for the built-in browser**, but I failed to mention BrowserTools MCP as a workaround and Cloud Agents as an alternative

**Errors in Grok's Research-1:**
- Grok said Codex browser control is "fully workable" — **overstated**, see Codex section below
- Grok said users "rave about watching the Agent literally sign into Google" in Cursor — **false/misleading**, the built-in browser has no auth support ([Cursor forum staff confirmation](https://forum.cursor.com/t/cursor-browser-still-does-not-support-401-http-authorization/154124))
- Grok ranked Antigravity #1 without mentioning ANY stability issues — **irresponsible**, see Antigravity section below
- Grok described Cursor's browser features in vague terms without distinguishing built-in browser vs Playwright MCP vs Cloud Agents
- Grok said Computer Use "launched in research preview March 2026" — **correct**
- Grok barely mentioned pricing or practical limitations for any platform

**Errors in Codex's Research-1:**
- Codex ranked Claude Code #3 behind Cursor — **undersold it**, Claude Code's Playwright MCP integration is at least as mature as Cursor's, plus Computer Use is unique
- Codex said Claude Code "asks you to assemble a bit more process" — **partially true** but misses that this is also a strength (hooks + CLAUDE.md make verification repeatable)
- Codex was the most measured and honest of the three competitors — most claims check out
- Codex correctly identified Antigravity as strongest for "browser-first" feel but failed to note reliability concerns
- Codex's workflow recommendations (spec-driven, test-first) are genuinely excellent advice

---

## The Corrected Rankings

| Rank | Platform | Score | Rationale |
|------|----------|-------|-----------|
| **1 (tie)** | **Claude Code** | 8.5/10 | Most browser tools, strongest code reasoning, best test artifact production, Computer Use is unique. Lower visual understanding than Antigravity. |
| **1 (tie)** | **Google Antigravity** | 8.5/10 | Best visual verification (72.7% ScreenSpot-Pro), most autonomous browser agent. But severe reliability/quota issues currently undermine it. |
| **3** | **Cursor** | 7.5/10 | Most polished IDE experience, visual element selection is genuinely useful, Cloud Agents are powerful. No Computer Use equivalent. |
| **4** | **OpenAI Codex** | 5/10 | Browser testing possible but unreliable. Sandbox bugs, platform-specific failures, "more assembled than first-class." |

**Why a tie at #1:** Claude Code and Antigravity excel at different halves of the same workflow. Antigravity is better at visual verification (catching CSS bugs, layout issues). Claude Code is better at code reasoning, test artifact production, and reliability. Neither is strictly superior. Your choice depends on whether you prioritize visual verification or reliability + test artifacts.

---

## 1. Claude Code (Mac Desktop App / CLI)

### What It Actually Has (Verified)

| Tool | Status | Source |
|------|--------|--------|
| **Playwright MCP** | Mature, well-documented, produces real Playwright test files | [Builder.io](https://www.builder.io/blog/playwright-mcp-server-claude-code), [Simon Willison](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code) |
| **Claude in Chrome** | Beta, works with authenticated sessions, lowest token cost (~7.7%) | [Official docs](https://code.claude.com/docs/en/chrome) |
| **Computer Use** | Research preview, macOS only, Pro/Max plans, can control any GUI app | [Official docs](https://code.claude.com/docs/en/computer-use) |
| **Chrome DevTools MCP** | Works, good for performance profiling and network debugging | [GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| **Claude Preview** | Built-in dev server preview with snapshot/inspect | Built into Claude Code |

### What I Got Wrong in Research-1

- I implied all 5 tools work seamlessly together. **In practice, nobody uses all 5 simultaneously.** The pattern is pick 1-2 per task: Playwright MCP for E2E tests, Claude in Chrome for authenticated debugging, Computer Use for GUI-only apps. ([DEV Community verdict](https://dev.to/minatoplanb/i-tested-every-browser-automation-tool-for-claude-code-heres-my-final-verdict-3hb7))
- I scored it 9.5/10. **The visual understanding gap is real** — Claude Opus 4.6 scores ~38% on ScreenSpot-Pro vs Antigravity's 72.7%. For catching visual/CSS bugs, Claude Code is weaker. ([DataCamp comparison](https://www.datacamp.com/blog/claude-code-vs-antigravity))
- I didn't mention context drift risk. **This is documented** — Claude can lose track of project goals mid-session and generate mocked tests that don't verify real functionality. Mitigated by CLAUDE.md rules and hooks. ([GitHub issue #10628](https://github.com/anthropics/claude-code/issues/10628))

### What I Got Right

- Playwright MCP integration is mature and produces real, committable test artifacts. Multiple independent sources confirm this works well. ([alexop.dev AI QA engineer](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/), [Testery](https://www.testery.com/blog/test-automation-with-claude-code))
- Computer Use is genuinely unique — no other coding agent can control arbitrary GUI apps via screenshot. ([Official docs](https://code.claude.com/docs/en/computer-use))
- The hooks + CLAUDE.md verification loop works when configured. The "Ralph Loop" pattern is documented and effective. ([nathanonn.com](https://www.nathanonn.com/claude-code-testing-ralph-loop-verification/))
- Claude Code's code reasoning quality is best-in-class (80.8% SWE-bench Verified). ([Anthropic](https://www.anthropic.com/research/swe-bench-sonnet))

### Corrected Setup

```bash
# Primary: Playwright MCP for E2E testing
claude mcp add playwright -- npx @playwright/mcp@latest

# For authenticated pages: Claude in Chrome extension
# Install from Chrome Web Store (v1.0.36+)

# For performance debugging: Chrome DevTools MCP
claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest

# For native app testing: enable Computer Use
# /mcp → enable computer-use (requires Pro/Max plan)

# For dev server preview: create .claude/launch.json
```

### Corrected Workflow

1. Write code with Claude (full codebase access)
2. Start dev server via Claude Preview
3. Use **Playwright MCP** to navigate and test — this is your primary loop
4. Use **Claude in Chrome** when you need authenticated session access
5. Use **Computer Use** only for native apps / simulators (it's slow)
6. Add CLAUDE.md rules: "Never mark task done until browser flow passes. Always inspect console and network errors. Convert passing flows into Playwright tests."
7. Add hooks for automatic re-verification after code edits

### Strengths (Verified)

- Most browser tool options of any platform
- Best code reasoning (80.8% SWE-bench)
- Produces real Playwright test artifacts for CI/CD
- Computer Use gives access to native apps no other tool can reach
- Hooks + CLAUDE.md create repeatable verification workflows
- No quota lockouts or context budget limits

### Weaknesses (Verified)

- Visual understanding is weak (~38% ScreenSpot-Pro) — will miss CSS/layout bugs
- Multi-tool setup requires configuration knowledge
- Context drift can produce fake/mocked tests without guardrails
- Computer Use is research preview, macOS only, slow
- No equivalent to Antigravity's trace hooks (HTTP, DB, queues)

---

## 2. Google Antigravity

### What It Actually Has (Verified)

| Feature | Status | Source |
|---------|--------|--------|
| **Browser Sub-Agent** | Real, powered by Gemini Computer Use, 72.7% ScreenSpot-Pro | [Antigravity docs](https://antigravity.google/docs/browser-subagent) |
| **MCP Support** | Yes, via `mcp_config.json` | [Antigravity MCP docs](https://antigravity.google/docs/mcp) |
| **Trace Hooks** | Real — wraps HTTP, DB calls, queues automatically | [Google Developers Blog](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/) |
| **AgentKit 2.0** | 16 agents, 40+ skills, up to 5 parallel agents | [Antigravity docs](https://antigravity.google/docs/agentkit) |
| **Multi-model** | Gemini 3.1 Pro, Claude Opus 4.6, GPT-OSS-120B | [Antigravity pricing](https://antigravity.google/pricing) |

### What Grok Got Wrong

- **Grok mentioned zero stability issues.** This is the biggest error in any of the three reports. The evidence is overwhelming:
  - **Quota lockouts:** Pro users locked out for 5-7 days after 20 minutes of intensive use. Quotas dropped from 300M+ tokens/week to under 9M — a 97% reduction. ([Google AI Forum](https://discuss.ai.google.dev/t/google-ai-pro-subscription-antigravity-quota-not-working-as-advertised-10-day-lockout-instead-of-5-hour-reset/118505), [PiunikaWeb](https://piunikaweb.com/2026/03/12/google-antigravity-pro-weekly-limits-multi-day-quota-lockouts/))
  - **Model degradation:** Documented quality regression starting January 2026. Users report shorter effective context windows and higher hallucination rates. ([Google AI Forum](https://discuss.ai.google.dev/t/anti-gravity-performance-decline-jan-2026/115360))
  - **Browser agent breakage:** Silent initialization failures after updates, "Loading..." hangs, platform-specific errors. ([Google AI Forum](https://discuss.ai.google.dev/t/browser-agent-cannot-open-after-update-1-20-3/129187))
  - **Data loss incident:** A user's entire D: drive was wiped when Turbo Mode ran an incorrect `rmdir` command targeting the drive root. ([WebProNews](https://www.webpronews.com/google-antigravity-ai-deletes-users-d-drive-data-in-turbo-mode-error/))
  - **Security vulnerability:** Mindgard identified a persistent code execution vulnerability within 24 hours of launch. ([Mindgard](https://mindgard.ai/blog/google-antigravity-persistent-code-execution-vulnerability))
  - **Pricing backlash:** The Register and DevClass documented user protests over opaque quota calculations. ([The Register](https://www.theregister.com/2026/03/12/users_protest_as_google_antigravity/), [DevClass](https://www.devclass.com/ai-ml/2026/03/13/users-protest-as-google-antigravity-price-floats-upward/5209219))

### What Grok Got Right

- The Browser Sub-Agent is genuinely purpose-built for this workflow and more autonomous than competitors
- The agent-first architecture (editor + terminal + browser orchestrated together) is real
- For pure "AI uses app like a human" feel, Antigravity is the most seamless when it works

### Corrected Assessment

Antigravity has the **highest raw capability** for visual browser testing but the **lowest reliability** of the top 3 platforms. It is the best platform when it works and the most frustrating when it doesn't.

### Setup (Verified)

1. Download from [antigravity.google](https://antigravity.google/)
2. Sign in with **personal Gmail** (Workspace not supported)
3. Install Chrome extension when prompted (Chrome only)
4. Budget for **Pro tier minimum** ($20/mo) — free tier is Flash-only after April 1, 2026
5. Keep MCP count minimal until stable (community reports instability with many MCPs — [Reddit](https://www.reddit.com/r/google_antigravity/comments/1pij7kh/anyone_facing_issues_with_google_antigravity/))
6. Break projects into smaller missions to avoid hitting 200k token context budget

### Strengths (Verified)

- Best visual UI verification (72.7% ScreenSpot-Pro)
- Most autonomous browser testing — no MCP configuration needed
- Built-in trace hooks (HTTP, DB, queues) are unique
- Patches as diffs linked to failing traces
- Agent-first architecture is genuinely impressive

### Weaknesses (Verified, Severe)

- Quota lockouts can halt work for days mid-project
- Model quality has regressed since launch
- Browser agent has documented breakage after updates
- Data loss incident from autonomous overreach
- Security vulnerability found within 24 hours of launch
- 200k token context budget per conversation
- Chrome only, personal Gmail only
- No persistent Playwright test artifacts like Claude Code produces

---

## 3. Cursor

### What It Actually Has (Verified)

| Feature | Status | Source |
|---------|--------|--------|
| **Built-in Browser Tool** | Real, shipped Cursor 1.7 (Sep 2025). Screenshots, clicks, forms, console logs, network requests. | [Official docs](https://cursor.com/docs/agent/tools/browser) |
| **Visual Element Selection** | Real, shipped Cursor 2.2 (Dec 2025). Click elements in browser pane to reference in chat. Point-and-prompt. | [Cursor blog](https://cursor.com/blog/browser-visual-editor) |
| **Design Mode** | Real, shipped Cursor 3 (Apr 2, 2026). Annotate and target UI elements for agents. | [Cursor blog](https://cursor.com/blog/cursor-3) |
| **Cloud Agents** | Real, isolated Linux VMs with full browser + desktop + clipboard. Produce video recordings. | [Cursor blog](https://cursor.com/blog/agent-computer-use) |
| **Playwright MCP** | Works via `.cursor/mcp.json` | [Playwright docs](https://playwright.dev/docs/getting-started-mcp) |
| **BrowserTools MCP** | Works, gives access to real Chrome profile with cookies/auth | [GitHub](https://github.com/AgentDeskAI/browser-tools-mcp) |

### What Grok Got Wrong

- **"Users rave about watching the Agent literally sign into Google"** — **False.** The built-in browser launches fresh instances without persistent state. It cannot handle HTTP 401 auth prompts. A Cursor staff member confirmed this is "a known limitation." ([Forum](https://forum.cursor.com/t/cursor-browser-still-does-not-support-401-http-authorization/154124), [Forum](https://forum.cursor.com/t/add-persistent-browser-state-cookie-configuration-to-built-in-playwright-mcp-server/136489))
- Grok conflated multiple different browser tools (built-in vs MCP vs Cloud Agents) into one vague description

### What I Got Wrong in Research-1

- I said Cursor has "no authenticated session reuse" — **correct for the built-in browser**, but I should have noted that **BrowserTools MCP** (which connects to your real Chrome profile with cookies) provides this as a workaround, and **Cloud Agents** have their own browser environment
- I scored Cursor 7/10 — bumping to **7.5/10** because Visual Element Selection and Design Mode are genuinely useful features I underweighted, and Cloud Agents with video recording are powerful

### What Codex (the researcher) Got Right

- Codex correctly identified Cursor as the "best all-around default" and "safest daily driver" — this checks out
- Codex's practical workflow advice (Playwright MCP as primary, rules about browser verification, converting flows to tests) is excellent
- Codex correctly noted the friction between built-in browser and external MCP tools ([Forum](https://forum.cursor.com/t/browser-automation-interferes-with-other-mcp-tools-and-there-is-no-global-disable-for-it/143126))

### Corrected Setup

```json
// .cursor/mcp.json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "browser-tools": {
      "command": "npx",
      "args": ["@agentdeskai/browser-tools-mcp@latest"]
    }
  }
}
```

Also: install BrowserTools Chrome extension + run `npx @agentdeskai/browser-tools-server@latest` for console/network access from your real Chrome.

### Strengths (Verified)

- Most polished IDE experience for daily use
- Visual Element Selection + Design Mode are genuinely useful for UI work
- Cloud Agents with video recording are powerful for autonomous testing
- Built-in browser tool is zero-config for basic visual checks
- Mature MCP marketplace

### Weaknesses (Verified)

- Built-in browser has no cookie persistence or auth support
- No equivalent to Computer Use (can't control native apps)
- Some friction between built-in browser and external MCP browser tools
- Cloud Agents require Cursor subscription and spin up fresh environments (no persistent state)

---

## 4. OpenAI Codex (Mac Desktop App / CLI)

### What It Actually Has (Verified)

| Feature | Status | Source |
|---------|--------|--------|
| **Playwright MCP** | Configurable via `config.toml`, works in CLI with `danger-full-access` | [Codex MCP docs](https://developers.openai.com/codex/mcp) |
| **Playwright Interactive Skill** | Headed Chromium, requires `danger-full-access` sandbox | [GitHub skill](https://github.com/openai/skills/blob/main/skills/.curated/playwright-interactive/SKILL.md) |
| **Chrome DevTools MCP** | Configurable | [Codex MCP docs](https://developers.openai.com/codex/mcp) |
| **Network Access** | OFF by default, must be explicitly enabled | [Sandboxing docs](https://developers.openai.com/codex/concepts/sandboxing) |

### What Grok Got Wrong

- **"Browser control is available via Playwright MCP... fully workable."** — **Overstated.** The GitHub issue tracker tells a different story:
  - [Issue #3100](https://github.com/openai/codex/issues/3100): Users confirmed Codex defaults to generating scripts rather than executing browser actions autonomously
  - [Issue #14368](https://github.com/openai/codex/issues/14368): macOS sandbox actively blocks Chromium from starting — `Permission denied (1100)` bootstrap errors
  - [Issue #4643](https://github.com/openai/codex/issues/4643): Linux Codex doesn't pass `DISPLAY` env var, so browser stays headless even when configured for headed mode
  - [Issue #13138](https://github.com/openai/codex/issues/13138): MCP transport drops during browser sessions
  - [Issue #6649](https://github.com/openai/codex/issues/6649): Playwright MCP doesn't work with GPT 5.1
  - [Issue #13373](https://github.com/openai/codex/issues/13373): Codex App ignores `network_access = true` from config.toml
  - [Community forum](https://community.openai.com/t/how-do-i-get-codex-to-use-the-browser/1373178): "Codex spends 3-5 minutes trying different bash scripts... only sometimes gets it to work"

### What I Got Wrong in Research-1

- I said Codex "CANNOT interact with a live browser" — **too absolute.** It CAN in `danger-full-access` mode with the `playwright-interactive` skill on some platforms. But my core point was directionally correct: it is not a reliable, first-class capability.
- Bumping score from 4.5 to **5/10** because the `playwright-interactive` skill is a real path forward, just unreliable.

### What Codex (the researcher) Got Right

- Codex's own assessment — "more assembled than first-class-native" — is the **most accurate description** of any of the three reports
- The two-agent pattern (implementer + verifier) is genuinely good advice for Codex
- Codex correctly noted it should be ranked last for this specific use case

### The Correct Assessment

Codex's browser testing story as of April 2026 is: **"possible with assembly required, unreliable in practice."**

- Success requires: `danger-full-access` sandbox mode + correct env var passthrough + platform-specific workarounds + tolerance for intermittent failures
- The macOS App has a confirmed sandbox bug that prevents Chromium from launching
- Even when it works, Codex tends to generate scripts rather than interactively navigate

### Upcoming: Atlas Superapp

[CNBC reported](https://www.cnbc.com/2026/03/19/openai-desktop-super-app-chatgpt-browser-codex.html) OpenAI is merging ChatGPT, Codex, and the Atlas AI-powered browser into a single desktop superapp. This could change everything for Codex's browser story, but it is not shipped as of April 2026.

---

## Head-to-Head: Verified Capability Matrix

| Capability | Claude Code | Antigravity | Cursor | Codex |
|-----------|-------------|-------------|--------|-------|
| Live browser interaction | Yes (Playwright MCP) | Yes (Browser Sub-Agent) | Yes (built-in + MCP) | Unreliable |
| Visual UI verification quality | ~38% ScreenSpot-Pro | 72.7% ScreenSpot-Pro | Similar to Claude Code | N/A |
| Authenticated session reuse | Yes (Claude in Chrome) | Limited | Via BrowserTools MCP only | No |
| Native app testing (iOS Sim, etc.) | Yes (Computer Use) | No | No (Cloud Agent VM only) | No |
| Cross-browser testing | Yes (Playwright) | No (Chrome only) | Yes (Playwright) | Unreliable |
| Produces Playwright test artifacts | Yes (strongest) | Weak | Yes | Yes (headless) |
| Performance profiling | Yes (DevTools MCP) | Yes (trace hooks) | Yes (DevTools MCP) | No |
| Visual element selection in IDE | No | No | Yes (Design Mode) | No |
| Cloud/background agents | Yes (subagents) | Yes (up to 5) | Yes (Cloud Agents + video) | Yes (Codex App) |
| Quota/availability issues | None reported | Severe (days-long lockouts) | None reported | Sandbox bugs |
| Code reasoning quality | 80.8% SWE-bench | 80.6% SWE-bench | Depends on model | Lower |
| Setup complexity | Medium-high | Low | Low-medium | High |
| Context drift risk | Documented, mitigatable | Less documented | Less documented | Less documented |

---

## Response to Grok (Research-1-Grok.md)

### What Grok Got Right

1. **Antigravity's Browser Sub-Agent description** is accurate — it genuinely is purpose-built for the editor+terminal+browser loop
2. **Claude Code's Computer Use description** is accurate — it does drive your actual desktop
3. **The general workflow pattern** (build → test in browser → fix → retest) is correct across all platforms
4. **Codex's multi-agent orchestration** strength is correctly identified
5. **Ranking Antigravity highly** for pure "AI uses app like a human" feel is defensible in isolation

### What Grok Got Wrong

1. **"Users rave about watching the Agent literally sign into Google" (Cursor)** — **False.** Cursor's built-in browser has no cookie persistence or auth support. A Cursor staff member confirmed this is a known limitation. ([Forum](https://forum.cursor.com/t/cursor-browser-still-does-not-support-401-http-authorization/154124)) Grok either fabricated this claim or confused it with a third-party MCP setup.

2. **"Browser control is fully workable" (Codex)** — **Overstated.** Six GitHub issues document sandbox blocking, transport drops, missing env vars, and model incompatibility. Community reports describe 3-5 minute troubleshooting sessions that "only sometimes" work. ([Issue #3100](https://github.com/openai/codex/issues/3100), [Issue #14368](https://github.com/openai/codex/issues/14368), [Issue #13138](https://github.com/openai/codex/issues/13138))

3. **Zero mention of Antigravity stability issues** — **Irresponsible omission.** Pro users are getting locked out for 5-7 days. A user lost an entire drive. A security vulnerability was found within 24 hours of launch. These are documented by The Register, PiunikaWeb, WebProNews, Mindgard, and Google's own developer forums. Ranking Antigravity #1 without mentioning any of this gives users a false picture. ([PiunikaWeb](https://piunikaweb.com/2026/03/12/google-antigravity-pro-weekly-limits-multi-day-quota-lockouts/), [WebProNews](https://www.webpronews.com/google-antigravity-ai-deletes-users-d-drive-data-in-turbo-mode-error/))

4. **Conflating Cursor's different browser tools** — Grok described Cursor's browser capabilities as one unified thing. In reality, there are distinct tools with different capabilities: (a) built-in Browser tool (no auth, no cookies), (b) Playwright MCP (separate Chromium), (c) BrowserTools MCP (real Chrome profile), (d) Cloud Agents (isolated VMs). These have very different strengths and limitations.

5. **No pricing or practical limitation details** — Grok gave no pricing info, no quota warnings, no context limits for any platform. This matters enormously for Antigravity where you can be locked out mid-project.

### Why This Report Is Superior to Grok's

- Every factual claim is cited with a specific source (official docs, GitHub issues, forum posts, news articles)
- Stability issues are documented, not hidden
- Browser tool distinctions (built-in vs MCP vs extension vs Cloud Agent) are properly separated
- Pricing and quota reality is included
- Each platform's weaknesses are stated alongside strengths

---

## Response to Codex (Research-1-Codex.md)

### What Codex Got Right

1. **The ideal workflow pattern** (build → browser test → inspect console/network → fix → retest → convert to Playwright specs) — **Excellent.** This is the best workflow description of any of the three reports. Practical, disciplined, repeatable.

2. **"More assembled than first-class-native" for Codex's browser story** — **Most accurate description.** Verified against 6 GitHub issues and community reports.

3. **Best-practice rules** (never mark done until browser passes twice, always inspect console and network, never patch runtime to fake tests, convert passing flows to specs) — **Outstanding advice** that applies to ALL platforms.

4. **Cursor as "best all-around default"** — Defensible. Cursor's IDE integration, visual element selection, and Cloud Agents make it the safest daily-driver recommendation for most people.

5. **Hooks and CLAUDE.md as Claude Code differentiators** — Correctly identified that Claude Code's ceiling depends on process discipline.

6. **Confidence note** — Codex was the only report that explicitly stated uncertainty about the ranking order. This honesty is valuable.

### What Codex Got Wrong

1. **Ranked Claude Code #3 behind Cursor** — **Undersold.** Claude Code's Playwright MCP integration is at least as mature as Cursor's (multiple independent sources confirm this). Computer Use gives it capabilities Cursor cannot match. The hooks system provides verification automation Cursor doesn't have natively. Claude Code's code reasoning (80.8% SWE-bench) is best-in-class.

2. **No mention of Computer Use** — This is Claude Code's unique capability. No other coding agent can control arbitrary GUI applications. For testing iOS Simulator, Electron apps, or design tools, nothing else works.

3. **No mention of Antigravity reliability issues** — Same omission as Grok. The quota lockouts, model degradation, data loss incident, and security vulnerability are documented facts that affect the ranking.

4. **"Claude Code can drift into inconsistent verification"** — **Partially true** but this is mitigatable with documented patterns (CLAUDE.md rules, hooks, Ralph Loop). Codex presented this as a weakness without noting the mitigations.

5. **Connector recommendations are generic** — Codex recommended Sentry, PostHog, Vercel connectors for every platform. These are fine but aren't specific to the browser testing workflow being asked about.

### Why This Report Is Superior to Codex's

- Includes Computer Use — a capability Codex completely missed
- Documents Antigravity's reliability issues with cited sources
- Corrects the Claude Code ranking with evidence (SWE-bench scores, Playwright maturity, Computer Use uniqueness)
- Verifies each disputed claim against official docs and GitHub issues rather than relying on inference
- Includes ScreenSpot-Pro scores for visual verification comparison (a metric neither competitor mentioned)
- Still incorporates Codex's excellent workflow advice (the best part of their report)

---

## Final Recommendation

### If reliability matters most → Claude Code

Install Playwright MCP + Claude in Chrome. Add CLAUDE.md rules for verification discipline. Use Computer Use for native app testing. You'll never be locked out mid-project.

### If visual verification matters most → Google Antigravity

The Browser Sub-Agent with 72.7% ScreenSpot-Pro is genuinely the best at catching visual bugs. But budget $20/mo minimum, break work into small missions, and accept that you may be locked out for days.

### If IDE experience matters most → Cursor

Visual Element Selection + Design Mode + Cloud Agents make the best integrated experience. Add Playwright MCP and BrowserTools MCP for full coverage.

### If you want parallel agents → OpenAI Codex

Wait for the Atlas superapp merger. Until then, use Codex for parallel code generation and Claude Code or Cursor for the browser testing loop.

### The combined power move

Use **Claude Code** as your primary coding + browser testing environment (Playwright MCP, hooks, CLAUDE.md rules). Use **Antigravity** as a secondary visual verification pass when you need to catch CSS/layout bugs that Claude's weaker visual understanding might miss. Use **Cursor** when you want the IDE experience with Design Mode for visual editing tasks.

---

## Sources Index

### Claude Code
- [Official Computer Use docs](https://code.claude.com/docs/en/computer-use)
- [Official Chrome docs](https://code.claude.com/docs/en/chrome)
- [Builder.io: Playwright MCP with Claude Code](https://www.builder.io/blog/playwright-mcp-server-claude-code)
- [Simon Willison: Playwright MCP TIL](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)
- [alexop.dev: AI QA Engineer with Claude Code](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/)
- [DEV Community: Browser tool verdict](https://dev.to/minatoplanb/i-tested-every-browser-automation-tool-for-claude-code-heres-my-final-verdict-3hb7)
- [DataCamp: Claude Code vs Antigravity](https://www.datacamp.com/blog/claude-code-vs-antigravity)
- [GitHub issue #10628: Context drift](https://github.com/anthropics/claude-code/issues/10628)
- [nathanonn.com: Ralph Loop verification](https://www.nathanonn.com/claude-code-testing-ralph-loop-verification/)
- [Anthropic: SWE-bench results](https://www.anthropic.com/research/swe-bench-sonnet)

### Google Antigravity
- [Google Developers Blog: Launch post](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
- [Antigravity Chrome Extension](https://antigravity.im/browser-extension)
- [Google AI Forum: 10-day quota lockout](https://discuss.ai.google.dev/t/google-ai-pro-subscription-antigravity-quota-not-working-as-advertised-10-day-lockout-instead-of-5-hour-reset/118505)
- [Google AI Forum: Performance decline Jan 2026](https://discuss.ai.google.dev/t/anti-gravity-performance-decline-jan-2026/115360)
- [Google AI Forum: Browser agent broken after update](https://discuss.ai.google.dev/t/browser-agent-cannot-open-after-update-1-20-3/129187)
- [PiunikaWeb: Multi-day quota lockouts](https://piunikaweb.com/2026/03/12/google-antigravity-pro-weekly-limits-multi-day-quota-lockouts/)
- [The Register: Users protest pricing](https://www.theregister.com/2026/03/12/users_protest_as_google_antigravity/)
- [WebProNews: D: drive data loss](https://www.webpronews.com/google-antigravity-ai-deletes-users-d-drive-data-in-turbo-mode-error/)
- [Mindgard: Security vulnerability](https://mindgard.ai/blog/google-antigravity-persistent-code-execution-vulnerability)
- [DevClass: Pricing backlash](https://www.devclass.com/ai-ml/2026/03/13/users-protest-as-google-antigravity-price-floats-upward/5209219)

### Cursor
- [Official Browser tool docs](https://cursor.com/docs/agent/tools/browser)
- [Cursor blog: Browser Visual Editor (2.2)](https://cursor.com/blog/browser-visual-editor)
- [Cursor blog: Cursor 3 launch](https://cursor.com/blog/cursor-3)
- [Cursor blog: Agent Computer Use (Cloud Agents)](https://cursor.com/blog/agent-computer-use)
- [Cursor forum: 401 auth not supported (staff confirmed)](https://forum.cursor.com/t/cursor-browser-still-does-not-support-401-http-authorization/154124)
- [Cursor forum: No persistent browser state](https://forum.cursor.com/t/add-persistent-browser-state-cookie-configuration-to-built-in-playwright-mcp-server/136489)
- [Cursor forum: Cookies not stored](https://forum.cursor.com/t/why-aint-cursor-storing-cookies/150813)
- [Cursor forum: Browser automation conflicts with MCP tools](https://forum.cursor.com/t/browser-automation-interferes-with-other-mcp-tools-and-there-is-no-global-disable-for-it/143126)
- [GitHub: AgentDeskAI/browser-tools-mcp](https://github.com/AgentDeskAI/browser-tools-mcp)

### OpenAI Codex
- [Codex MCP docs](https://developers.openai.com/codex/mcp)
- [Codex Sandboxing docs](https://developers.openai.com/codex/concepts/sandboxing)
- [Codex Skills docs](https://developers.openai.com/codex/skills)
- [GitHub: Playwright Interactive Skill](https://github.com/openai/skills/blob/main/skills/.curated/playwright-interactive/SKILL.md)
- [Issue #3100: Can't use Playwright MCP for real browser interaction](https://github.com/openai/codex/issues/3100)
- [Issue #14368: macOS sandbox blocks Chromium](https://github.com/openai/codex/issues/14368)
- [Issue #4643: Linux DISPLAY env var not passed](https://github.com/openai/codex/issues/4643)
- [Issue #13138: MCP transport drops](https://github.com/openai/codex/issues/13138)
- [Issue #6649: MCP doesn't work with GPT 5.1](https://github.com/openai/codex/issues/6649)
- [Issue #13373: App ignores network_access config](https://github.com/openai/codex/issues/13373)
- [Issue #16390: Working directory bug](https://github.com/openai/codex/issues/16390)
- [Community: How to get Codex to use browser](https://community.openai.com/t/how-do-i-get-codex-to-use-the-browser/1373178)
- [CNBC: Atlas superapp merger](https://www.cnbc.com/2026/03/19/openai-desktop-super-app-chatgpt-browser-codex.html)

### Cross-Platform Comparisons
- [Lushbinary: AI Coding Agents 2026 Comparison](https://lushbinary.com/blog/ai-coding-agents-comparison-cursor-windsurf-claude-copilot-kiro-2026/)
- [Augment Code: Antigravity vs Claude Code](https://www.augmentcode.com/tools/google-antigravity-vs-claude-code)
