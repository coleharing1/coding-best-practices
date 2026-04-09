# Browser-in-the-Loop AI Coding Research, Round 2

Date: April 4, 2026

## What I did differently this time

I read all three first-round notes:
- `Research-1-Claude.md`
- `Research-1-Grok.md`
- `Research-1-Codex.md`

Then I re-checked the major claims against:
- official product docs and help centers
- official Playwright docs
- GitHub issues
- Reddit/community reports

I also checked X/Twitter search results, but the high-signal evidence was much stronger in official docs, GitHub issues, and Reddit than on X. So this version weights those higher.

The goal of this note is not to be the most flattering answer to any platform. It is to be the most defensible answer.

---

## 1. Where all three answers agreed

All three first-round answers were directionally right on the core workflow:

1. The best setup is not code-only. The agent needs codebase + terminal + browser + runtime signals.
2. The best loop is:
   - run the app
   - browse it like a user
   - inspect console/network/runtime failures
   - fix code
   - rerun
   - then turn the passing flow into Playwright tests
3. Playwright or a browser MCP is the most important add-on across the board.
4. Antigravity is unusually browser-native.
5. Codex is the weakest of the four for this specific browser-first QA loop.

That shared core was mostly correct.

---

## 2. Where the three answers diverged

The biggest disagreements were:

### Who should rank #1

- Claude ranked `Claude Code` first.
- Grok ranked `Antigravity` first.
- My first answer split the difference and said `Antigravity` had the most native browser feel, but `Cursor` was the safest default.

### How native Cursor's browser workflow is

- Grok treated Cursor like it already has a strong native browser tool flow.
- Claude treated Cursor as mostly MCP-driven.
- The official docs support Claude's framing more than Grok's.

### Whether Codex can really use a browser

- Claude said Codex is basically headless-only and fundamentally limited.
- Grok and my first answer said Codex can do browser testing through Playwright MCP, but it is less polished.
- The docs and community evidence support Grok/my first answer more than Claude's hard limitation claim.

### How production-ready Antigravity is in practice

- Grok emphasized the browser-first magic.
- Claude included many additional specifics about plans, context limits, agent counts, trace hooks, and quota issues.
- The official docs strongly support the browser-first design, but many of Claude's extra Antigravity specifics were not verifiable from primary sources I could confirm.

---

## 3. Verified findings by platform

## Cursor

### What is clearly verified

Cursor's official web development guide explicitly recommends using browser tooling through MCP, especially Browser Tools MCP, to bring console logs, network requests, and UI element data into the agent loop. It also says they are still working on making this easier to integrate natively, which means the strongest browser workflow is still MCP-centric rather than fully native today. Sources: [Cursor web development guide](https://docs.cursor.com/guides/tutorials/web-development), [Cursor MCP docs](https://docs.cursor.com/en/context/mcp).

Playwright's official MCP docs list Cursor as a supported MCP client and show it can install `@playwright/mcp` directly in Cursor settings. Source: [Playwright MCP docs](https://playwright.dev/docs/getting-started-mcp).

Cursor background agents are real remote agents with internet access running in isolated Ubuntu machines, but the official docs emphasize repo cloning, terminals, and remote execution; they do not document a first-class desktop-style computer-use capability comparable to Claude's screen control. Source: [Cursor background agents](https://docs.cursor.com/en/background-agents).

### What this means

The best verified Cursor workflow is:
- local or remote Cursor agent
- Browser Tools MCP for console/network/UI data
- Playwright MCP for actual browser interaction
- optionally Chrome DevTools MCP for deeper debugging

### What Grok got wrong about Cursor

Grok overstated Cursor's browser stack as a native built-in browser-first system. The official Cursor guide still tells users to wire in browser MCPs and says native integration is still being worked on. So Cursor is strong here, but not because the browser loop is already fully native. Source: [Cursor web development guide](https://docs.cursor.com/guides/tutorials/web-development).

### What Claude got right about Cursor

Claude was closer to the docs: Cursor is powerful here, but mainly because of MCP composition, not because it has a uniquely complete native browser stack.

---

## Claude Code

### What is clearly verified

Claude Code officially supports MCP and hooks. That matters a lot because hooks let you encode your verification loop into the product instead of relying on prompt memory. Sources: [Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/mcp), [Claude Code hooks guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide), [Claude Code hooks reference](https://docs.anthropic.com/en/docs/claude-code/hooks).

Claude in Chrome is officially available on paid plans and is explicitly documented as letting Claude read, click, and navigate websites. The help center also explicitly says Claude Code and the Chrome extension can work together for a build-test-verify workflow, including reading console errors, network requests, and DOM state directly. Source: [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome).

Computer use is also officially documented for Cowork and Claude Code inside the macOS Claude Desktop app. Anthropic says Claude can use the screen directly when no better connector exists, and that it prioritizes the fastest more precise method before falling back to screen interaction. Source: [Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork).

Playwright's official docs now make an important distinction:
- `playwright-cli` is best for coding agents when you want token efficiency.
- Playwright MCP is best for exploratory loops and persistent reasoning over page structure.
That distinction is especially valuable for Claude Code workflows. Source: [Playwright coding agents / CLI docs](https://playwright.dev/docs/getting-started-cli), [Playwright MCP docs](https://playwright.dev/docs/getting-started-mcp).

### What this means

Claude Code has the strongest verified browser-testing stack of the four:
- codebase access via Claude Code
- structured browser automation via Playwright MCP or `playwright-cli`
- real logged-in browser/session reuse via Claude in Chrome
- true fallback desktop control via Computer Use
- hooks to force verification after edits

That is not just "lots of tools." It is the best-documented combination of:
- browser control
- real-session access
- automation discipline
- deterministic reruns

### What Claude got right

Claude's first-round answer was strongest on process:
- hooks matter
- Playwright CLI vs MCP matters
- Claude in Chrome matters
- guardrails in `CLAUDE.md` matter

Those points are well-supported.

### What Claude got wrong or overclaimed

Claude included a "Claude Preview" / `.claude/launch.json` workflow that I could not verify in official docs.

Claude also stated a very specific automatic tool-priority order for Claude Code. Anthropic documents that kind of prioritization for computer use in Cowork, but I did not find a primary source proving Claude Code itself follows the exact same order in the exact same way.

So Claude's recommendation was directionally excellent, but it mixed verified facts with some unsupported product detail.

---

## Codex Mac desktop app

### What is clearly verified

OpenAI's official Codex app announcement says the app is a multi-agent command center and explicitly says the app uses configurable system-level sandboxing similar to the CLI. By default, agents can edit files in their working folder or branch and use cached web search; network access requires permission unless rules allow it. Source: [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/).

The same official launch post also says Codex validated one of its demo projects by "actually playing the game." That is not a full product-spec browser API doc, but it is direct evidence that the platform is not conceptually limited to "write test scripts only." Source: [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/).

More importantly, Playwright's official MCP docs explicitly list `Codex` as a supported MCP client. That directly contradicts any claim that Codex fundamentally cannot use Playwright MCP. Source: [Playwright MCP docs](https://playwright.dev/docs/getting-started-mcp).

Community evidence is mixed:
- some users report Codex + Playwright MCP works
- others report bugs, context churn, or flaky MCP behavior
- there are GitHub and Reddit reports describing difficulty, but not a universal hard product limitation
Sources: [openai/codex issue #3100](https://github.com/openai/codex/issues/3100), [Reddit: Codex can't run and test projects in a browser?](https://www.reddit.com/r/OpenaiCodex/comments/1rdzdfe/codex_cant_run_and_test_projects_in_a_browser/), [Reddit: Codex and Playwright MCP infinite autocompact bug](https://www.reddit.com/r/codex/comments/1r7zspi/codex_and_playwright_mcp_infinite_autocompact_bug/).

### What this means

The correct description of Codex is:

- It is not a no-browser platform.
- It can use Playwright MCP.
- It is meaningfully weaker and rougher than Claude Code and Cursor for this use case.
- Its strengths are agent orchestration, skills, parallel work, and long-running coding tasks more than polished browser-first QA.

### What Claude got wrong about Codex

Claude's first-round answer said Codex was basically headless-only and fundamentally could not do live browser interaction the way the others could. That is too strong and materially misleading.

Why it is wrong:
- Playwright's official docs list Codex as a supported MCP client.
- OpenAI's own product story describes Codex validating a project by actually using it.
- Community reports show that Codex browser testing is possible, but uneven.

So the real verdict is "possible but less polished," not "not possible."

### What Grok got right and wrong about Codex

Grok was right that Codex can be made to do this with Playwright MCP and that it is weaker than the top contenders.

Grok was too optimistic, though, about how smooth this is today. The community signal is much more "works, but expect setup and reliability friction" than "fully workable and comparable to the others out of the box."

---

## Google Antigravity

### What is clearly verified

Google's official launch post says Antigravity is designed around agents that plan, execute, and verify tasks across editor, terminal, and browser. Source: [Google Developers Blog: Build with Google Antigravity](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/).

Google's official codelab says Antigravity is an agent-first platform with "Mission Control" for agents that can plan, code, and browse the web. It also documents artifacts including screenshots and browser recordings, and describes the agent launching a browser to verify the app after coding. Source: [Google Codelab: Getting Started with Google Antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity).

That is the strongest official browser-first product framing of the four.

### What is supported by community reports

Reddit reports show repeated issues with:
- quota weirdness or abrupt exhaustion
- browser extension installation failures
- agents getting stuck in the browser verification stage

These are not official docs, but the pattern is consistent enough that they should influence practical ranking. Sources: [quota help thread](https://www.reddit.com/r/GoogleAntigravityIDE/comments/1rrollc/quota_help/), [browser extension fails to install](https://www.reddit.com/r/google_antigravity/comments/1q29ias/antigravity_extension_bug/), [agent gets stuck after opening browser](https://www.reddit.com/r/google_antigravity/comments/1pw7ifo/agent_gets_stuck_after_opening_browser/), [weekly quotas/issues thread](https://www.reddit.com/r/google_antigravity/comments/1s1bog2/weekly_quotas_known_issues_support_march_23/), [Antigravity has become unusable](https://www.reddit.com/r/google_antigravity/comments/1s8h0td/antigravity_has_become_unusable/).

### What this means

Antigravity has the strongest verified product design for this exact use case:
- agent manager
- browser involvement as a first-class concept
- screenshots/recordings as artifacts
- browser-based verification built into the narrative of how the product works

But it also has the weakest community reliability signal among the top three.

### What Grok got right

Grok correctly recognized that Antigravity is the most browser-native and most magical when it works.

### What Grok and Claude both overclaimed

Both first-round answers included additional very specific Antigravity details that I could not confidently verify from primary sources:
- exact model lineup claims
- exact pricing and tier behavior
- exact context-budget numbers
- exact "Browser Sub-Agent" and "trace hook" implementation details
- exact agent counts or AgentKit details

Some of those may be true in parts, but they were not well-supported enough for me to keep them in the corrected answer.

---

## 4. Corrected answer: the best workflow for each platform

## Cursor: best workflow

### Install

1. Cursor desktop app
2. Browser Tools MCP for console logs, network requests, and UI element data
3. Playwright MCP for browser interaction
4. Optional Chrome DevTools MCP for deeper browser debugging
5. Optional GitHub + Sentry/PostHog + Vercel connectors if relevant

### Use it like this

1. Start the app locally.
2. Use Cursor's local agent first for `localhost` work.
3. Prompt it to:
   - discover the main user flows
   - open the app in Playwright
   - browse like a user
   - inspect console/network/runtime failures
   - fix code
   - rerun the same flow
   - write or update Playwright tests for the passing path
4. Move to background agents only after the local loop is stable or if you want async branch/PR work.

### Best prompt pattern

```text
Use Playwright MCP and Browser Tools MCP against http://localhost:3000. Exercise the main user flows like a real user, inspect console errors and failed network requests, fix issues in the codebase, rerun until the flow passes cleanly, then convert the validated flow into Playwright tests.
```

### Verdict

Cursor is not the most browser-native product, but it is one of the best practical day-to-day setups once you add the right MCPs.

---

## Claude Code: best workflow

### Install

1. Claude Code
2. Playwright MCP
3. `@playwright/cli` for token-efficient reruns
4. Claude in Chrome
5. Enable Computer Use in Claude Desktop if you want fallback desktop/browser control
6. GitHub + runtime/error connectors as needed
7. Hooks for build/lint/test/smoke reruns

### Use it like this

1. Keep code editing in Claude Code.
2. Use Playwright MCP or `playwright-cli` for repeatable browser workflows.
3. Use Claude in Chrome when you want real logged-in session reuse and direct browser debugging.
4. Use Computer Use only when the task escapes browser tooling or needs broader desktop control.
5. Add hooks so Claude automatically reruns tests or smoke flows after edits.
6. Add explicit repo rules that prevent fake passes and require browser verification before stopping.

### Best prompt pattern

```text
Start the app, verify the main user journeys in the browser, inspect console/network/DOM issues, fix the code, rerun until the browser flow and tests both pass, and do not mark the task complete until the validated user path has been turned into Playwright coverage.
```

### Verdict

This is the strongest verified workflow overall because it combines:
- code access
- browser automation
- real authenticated browser sessions
- fallback desktop control
- enforceable verification hooks

---

## Codex desktop: best workflow

### Install

1. Codex desktop app
2. Playwright MCP
3. Optional Chrome DevTools MCP
4. GitHub
5. Runtime/error connectors if relevant

### Use it like this

1. Use Codex app for multi-threaded or multi-agent work.
2. Keep one thread focused on implementation and another focused on verification if needed.
3. Use Playwright MCP for browser checks against local or preview URLs.
4. Expect some extra setup and some MCP rough edges compared with Claude Code or Cursor.
5. As soon as a manual browser flow passes, promote it into Playwright tests.

### Best prompt pattern

```text
Run the app, verify the main browser flows with Playwright MCP, inspect visible failures plus console/network issues, fix the implementation, rerun until the browser flow passes, then save that success as Playwright regression coverage.
```

### Verdict

Codex can do this. It is just not the strongest platform for this exact style of work today.

---

## Antigravity: best workflow

### Install

1. Antigravity desktop app
2. Chrome
3. Antigravity browser extension
4. Minimal connector set at first

### Use it like this

1. Use Planning mode rather than only Fast mode for anything non-trivial.
2. Ask Antigravity to build, launch, verify, and produce artifacts.
3. Review screenshots and browser recordings, not just the code diff.
4. Comment directly on artifacts if the verification is too weak.
5. Once the browser flow is validated, require the agent to commit that learning into Playwright tests.

### Best prompt pattern

```text
Build and verify this app end to end. Start the dev server, use the browser to exercise the main user journeys like a real user, capture artifacts showing what happened, fix failures in code, rerun verification, and then save the validated path as Playwright smoke coverage.
```

### Verdict

If your only question is "which one feels most like the AI is literally using my app in a browser like a human," Antigravity has the best native product shape. If your question is "which setup do I trust the most to be my daily workflow right now," the community evidence makes that harder to recommend as the #1 default.

---

## 5. New ranking

## Overall ranking for this use case

### 1. Claude Code

Why:
- strongest verified browser stack
- real logged-in browser extension
- real desktop fallback via Computer Use
- hooks make the verification loop enforceable
- Playwright CLI vs MCP guidance is mature and well documented

### 2. Cursor

Why:
- very strong practical workflow once MCPs are added
- official docs explicitly support browser-in-the-loop development through MCP
- strong IDE ergonomics
- less browser-native than Claude, but more stable and mature-looking than Antigravity based on the sources I could verify

### 3. Google Antigravity

Why:
- best native browser-first product concept
- strongest artifact story
- most magical when it works
- but community reliability and quota complaints were too strong for me to rank it above Claude Code or Cursor as the default recommendation

### 4. Codex desktop

Why:
- definitely capable with Playwright MCP
- best at orchestration and multi-agent coding among the four
- weakest polished browser-verification story today

## Alternate ranking if you optimize for "wow factor" only

If you care less about maturity and more about "AI visibly uses the browser like a human," I would rank:

1. Antigravity
2. Claude Code
3. Cursor
4. Codex

That is the best way to reconcile the real disagreement between the first-round answers.

---

## 6. My response back to Claude

## What Claude got right

Claude's answer was best on workflow discipline.

Strong points Claude got right:
- hooks are a major advantage in Claude Code
- Playwright CLI vs Playwright MCP is an important distinction
- Claude in Chrome is a real strategic advantage for authenticated browser workflows
- Computer Use gives Claude a fallback path the others mostly lack
- Codex should not rank near the top for this use case

Those are the strongest parts of Claude's answer, and they are supported by official docs:
- [Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
- [Computer Use in Cowork / Claude Code](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- [Playwright CLI docs](https://playwright.dev/docs/getting-started-cli)

## What Claude got wrong

Claude's answer was too aggressive and too specific in places where the evidence was weaker.

Main problems:

1. It treated Codex like it is fundamentally headless-only or unable to interact with a real browser.
That is not supported by the evidence. Playwright's official docs list Codex as a supported MCP client, and community reports show it can work, even if it is rough. Sources: [Playwright MCP docs](https://playwright.dev/docs/getting-started-mcp), [openai/codex issue #3100](https://github.com/openai/codex/issues/3100).

2. It included a "Claude Preview" / `.claude/launch.json` setup that I could not verify in official docs.

3. It asserted an exact automatic tool-priority order for Claude Code that I could not fully verify as a Claude Code product guarantee.

4. It included many Antigravity specifics that were not well-supported from primary sources I could confirm, including exact product internals and plan behavior.

## Why this new answer is better than Claude's

This version keeps Claude's strongest insight, which is that Claude Code has the best verified browser-testing stack, but removes or downgrades the unsupported details.

In other words:
- Claude had the right top-line ranking.
- Claude did not have the cleanest evidence boundary.

This version is superior because it separates:
- verified product facts
- community-supported practical observations
- unsupported or weakly supported claims

---

## 7. My response back to Grok

## What Grok got right

Grok correctly saw several big things:

1. The best browser-testing workflow is codebase + browser + bug-fixing loop, not just test generation.
2. Antigravity is unusually strong for browser-native end-to-end verification.
3. Codex belongs below the top tier for this use case.
4. Playwright MCP is central to making these workflows actually work.

Those were solid calls.

## What Grok got wrong

Grok's answer was too rosy and too casual with product specifics.

Main problems:

1. It overstated Cursor's native browser tooling.
The official Cursor docs still point users toward Browser Tools MCP and say native integration is still being improved. Source: [Cursor web development guide](https://docs.cursor.com/guides/tutorials/web-development).

2. It blurred Claude Desktop, Claude Code, browser use, and Computer Use together without enough product-boundary precision.
The modern Anthropic stack is powerful, but the exact roles of Claude Code, Claude in Chrome, Cowork, and Computer Use need more careful separation than Grok gave them.

3. It made Codex sound smoother than the evidence supports.
Codex can do this with Playwright MCP, but the community evidence is much more mixed than Grok implied. Sources: [openai/codex issue #3100](https://github.com/openai/codex/issues/3100), [Reddit Codex browser testing thread](https://www.reddit.com/r/OpenaiCodex/comments/1rdzdfe/codex_cant_run_and_test_projects_in_a_browser/).

4. It treated Antigravity as nearly frictionless once installed.
The official story is very strong, but the community reports show real friction around extension setup, verification hangs, and quotas. Sources: [Google Codelab](https://codelabs.developers.google.com/getting-started-google-antigravity), [Reddit extension thread](https://www.reddit.com/r/google_antigravity/comments/1q29ias/antigravity_extension_bug/), [Reddit browser hang thread](https://www.reddit.com/r/google_antigravity/comments/1pw7ifo/agent_gets_stuck_after_opening_browser/).

## Why this new answer is better than Grok's

Grok's answer had good instincts, but it leaned too hard into the "magic" framing and not enough into what is actually documented and repeatable.

This version is better because it:
- keeps the useful high-level workflow advice
- corrects the product overstatements
- gives a more defensible ranking
- distinguishes "browser-first in theory" from "dependable daily driver in practice"

---

## 8. Final corrected answer

If you want the single best setup today for "AI uses my app in the browser like a user, finds bugs, fixes code, reruns, and turns that into repeatable coverage," the most defensible answer as of April 4, 2026 is:

### Best overall: Claude Code

Why:
- strongest verified browser stack
- best combination of structured browser automation, real-session access, and desktop fallback
- hooks let you force the verify-fix-rerun discipline instead of hoping the model remembers it

### Best traditional IDE choice: Cursor

Why:
- excellent with Browser Tools MCP + Playwright MCP
- probably the best "sit in an editor all day and iterate quickly" option

### Best browser-native concept: Antigravity

Why:
- the most agent-manager-plus-browser-native design
- but not the best reliability signal right now

### Best at orchestration but not this exact loop: Codex

Why:
- strongest multi-agent coding shape
- browser loop works, but is still rougher than the leaders

So if I were advising a real developer today:

- Choose `Claude Code` if you want the best full-stack browser-testing workflow.
- Choose `Cursor` if you want the best IDE-native daily-driver workflow.
- Choose `Antigravity` if you want the most exciting browser-first experience and can tolerate preview instability.
- Choose `Codex` if multi-agent coding/orchestration matters more to you than having the strongest browser QA loop.

---

## Sources

### Official docs

- Cursor MCP docs: <https://docs.cursor.com/en/context/mcp>
- Cursor web development guide: <https://docs.cursor.com/guides/tutorials/web-development>
- Cursor background agents: <https://docs.cursor.com/en/background-agents>
- Claude Code MCP docs: <https://docs.anthropic.com/en/docs/claude-code/mcp>
- Claude Code hooks guide: <https://docs.anthropic.com/en/docs/claude-code/hooks-guide>
- Claude Code hooks reference: <https://docs.anthropic.com/en/docs/claude-code/hooks>
- Claude in Chrome: <https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome>
- Let Claude use your computer in Cowork / Claude Code: <https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork>
- Playwright MCP docs: <https://playwright.dev/docs/getting-started-mcp>
- Playwright CLI docs: <https://playwright.dev/docs/getting-started-cli>
- OpenAI Codex app launch: <https://openai.com/index/introducing-the-codex-app/>
- Google Developers Blog on Antigravity: <https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/>
- Google Codelab for Antigravity: <https://codelabs.developers.google.com/getting-started-google-antigravity>

### GitHub issues and community

- Codex Playwright issue: <https://github.com/openai/codex/issues/3100>
- Reddit: Codex can't run and test projects in a browser?: <https://www.reddit.com/r/OpenaiCodex/comments/1rdzdfe/codex_cant_run_and_test_projects_in_a_browser/>
- Reddit: Codex Playwright MCP autocompact bug: <https://www.reddit.com/r/codex/comments/1r7zspi/codex_and_playwright_mcp_infinite_autocompact_bug/>
- Reddit: Google Antigravity quota help: <https://www.reddit.com/r/GoogleAntigravityIDE/comments/1rrollc/quota_help/>
- Reddit: Antigravity extension bug: <https://www.reddit.com/r/google_antigravity/comments/1q29ias/antigravity_extension_bug/>
- Reddit: Agent gets stuck after opening browser: <https://www.reddit.com/r/google_antigravity/comments/1pw7ifo/agent_gets_stuck_after_opening_browser/>
- Reddit: Weekly quotas / issues thread: <https://www.reddit.com/r/google_antigravity/comments/1s1bog2/weekly_quotas_known_issues_support_march_23/>
- Reddit: Antigravity has become unusable: <https://www.reddit.com/r/google_antigravity/comments/1s8h0td/antigravity_has_become_unusable/>

---

## Confidence note

High confidence:
- Claude Code ranking in the top tier
- Cursor's browser workflow being MCP-centric rather than fully native
- Codex being capable but clearly weaker than Claude/Cursor for this use case
- Antigravity being the most browser-native by design

Medium confidence:
- the exact ordering between Cursor and Antigravity, because that depends a lot on whether you optimize for reliability or for browser-first magic

Lower confidence:
- any exact plan, quota, or internal architecture claims for Antigravity or Claude that are not directly documented in official sources
