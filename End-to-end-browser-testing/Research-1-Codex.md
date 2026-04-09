# End-to-End Browser Testing Research

Date: April 4, 2026

## Question

When vibecoding a new app, what is the best workflow to let the AI use the app in a real browser, click through features end to end like a user, inspect browser elements and errors, fix bugs in the codebase, and keep iterating until the app is genuinely working? How should this be set up in each of these four platforms with the best available connectors, MCPs, and tools as of April 2026?

Platforms covered:
- Cursor
- Claude Code Mac desktop app
- Codex Mac desktop app
- Google Antigravity

## Executive summary

The best general pattern across all four platforms is:

1. Give the agent local access to the codebase and terminal.
2. Give it a headed browser tool, not just screenshots.
3. Give it console logs, network requests, and deploy/runtime logs.
4. Let it do one exploratory browser pass like a user would.
5. Make it fix issues in code.
6. Make it rerun the same browser flow.
7. Convert the passing flow into Playwright tests so the success becomes repeatable.

The "best" platform depends on what you care about most:

- If you want the most native "AI actually uses the app in a browser like a user" experience, Google Antigravity appears strongest.
- If you want the safest and most practical daily-driver IDE workflow, Cursor is the best default recommendation.
- If you want the highest ceiling with heavy customization and strong workflow guardrails, Claude Code is excellent.
- If you want strong agent orchestration and parallel coding/test workers, Codex desktop is very good, but its browser loop still benefits from extra setup.

## The ideal workflow, regardless of platform

The most effective workflow is not "give the model total freedom and hope for the best." The reliable version is:

1. Start the app locally.
2. Have the agent inspect the codebase and determine the main user flows.
3. Have the agent open a real browser and execute those flows end to end.
4. Require the agent to inspect:
   - browser console errors
   - failed network requests
   - layout or interaction issues
   - server/runtime logs
   - auth/session/cookie problems
5. Let it patch the codebase.
6. Make it rerun the browser flow.
7. Once the flow passes, require it to create or update Playwright specs for the validated path.
8. Add one more verification pass before calling the task done.

The strongest stack is usually:

- Playwright MCP or equivalent browser controller
- GitHub connector
- deployment/runtime logs connector such as Vercel
- error/product analytics connector such as Sentry or PostHog
- docs/search connectors for framework and library lookup

## Cursor

### Best setup

Cursor is the best default IDE choice if you want a practical local build-test-fix loop with strong browser tooling.

Recommended stack:
- Cursor desktop app
- local Agent mode for localhost work
- Playwright MCP as the main browser automation layer
- optional GitHub connector
- optional Sentry/PostHog connector
- optional Vercel connector if you deploy there

Key takeaway from the docs and community reports:
- Cursor's built-in web/browser tooling is useful, but for serious browser-driven debugging the better workflow is to wire in Playwright MCP so the agent can click, inspect, and rerun deterministically.
- Background Agents are strong for cloud/offloaded coding tasks, but the best browser debugging loop for a new local app usually starts in the local agent with your dev server.

### Exact workflow

1. Open the repo in Cursor.
2. Start the app locally, or let Cursor start it.
3. Add Playwright MCP in Cursor's MCP/connectors settings.
4. Prompt Cursor with something like:

```text
Use Playwright against http://localhost:3000. Explore the signup, onboarding, dashboard, settings, and logout flows like a real user. Inspect console errors and failed network requests. Fix any bugs you find in the codebase, rerun the flow until it passes cleanly, then convert the successful flows into Playwright tests.
```

5. Let Cursor click through the product in a real browser session.
6. If auth or 2FA blocks the run, do that step manually, then return control.
7. After the flow passes, require Cursor to:
   - write Playwright tests
   - run those tests
   - summarize what was fixed

### What makes Cursor strong here

- Tight IDE integration.
- Mature MCP story.
- Good fit for local dev server plus browser plus code edits in one place.
- Strong community usage for "vibecoding and watch the agent fix it live."

### Weaknesses

- Some community reports noted friction or overlap between built-in browser tooling and external MCP browser tooling.
- Browser verification is excellent once configured, but not as natively "browser-first" as Antigravity.

### Best-practice rules to give Cursor

- Never mark the task done until the browser flow passes twice.
- Always inspect console and network, not just screenshots.
- Never patch the app at runtime to fake passing tests.
- After every successful manual/browser-discovered fix, create or update a Playwright spec.

## Claude Code Mac Desktop App

### Best setup

Claude Code has one of the highest ceilings for this workflow because it combines MCP support with strong automation hooks and close integration with Claude Desktop.

Recommended stack:
- Claude Code on Mac
- Claude Desktop installed as well
- import or reuse Claude Desktop connectors/extensions where helpful
- Playwright MCP for browser control
- `playwright-cli` for cheap repeatable regression loops
- GitHub connector
- runtime/logging connector such as Vercel or Sentry
- strong `CLAUDE.md` rules file
- hooks enabled for auto-verification

Key takeaway:
- Claude Code becomes especially strong when you add process discipline.
- The browser loop itself is very capable, but the real differentiator is that you can codify guardrails in `CLAUDE.md` and hooks so Claude repeatedly runs the same verification sequence after edits.

### Exact workflow

1. Open the project in Claude Code.
2. Install or enable Playwright MCP.
3. If useful, import/connect relevant tools from Claude Desktop.
4. Add rules in `CLAUDE.md` such as:
   - do not call a task complete until browser flow and tests pass
   - always inspect console and network errors
   - never modify test harnesses or inject runtime shims to fake a pass
5. Add hooks so that after code edits Claude automatically reruns:
   - app build
   - lint
   - targeted tests
   - Playwright smoke path
6. Prompt Claude with something like:

```text
Start the app, open localhost in Playwright, use the product like a new user would, inspect errors and broken interactions, fix issues in code, and keep iterating until the main user flow passes in the browser and the Playwright tests are green.
```

7. Let Claude explore, fix, rerun, and codify the flow into tests.

### What makes Claude Code strong here

- Excellent extensibility via MCP.
- Hooks make it easier to institutionalize a reliable loop.
- Strong for teams that want repeatable process instead of pure one-off prompting.

### Weaknesses

- More setup than Cursor or Antigravity before it feels smooth.
- Community reports include warnings that if you do not constrain the workflow, an agent can take shortcuts, including brittle test-only patches or runtime hacks.

### Best-practice rules to give Claude

- Browser findings must map to real code fixes.
- No test-only hacks unless explicitly approved.
- Every fixed browser issue must produce either:
  - a new Playwright test, or
  - an update to an existing regression test.
- If a browser step needs manual intervention, Claude should pause and ask at that point instead of guessing.

## Codex Mac Desktop App

### Best setup

Codex desktop is strongest when you want coding agents and verifier agents working together. It is excellent at code work, worktrees, and multi-agent orchestration. For browser-heavy end-to-end testing, it becomes much better once you add the right browser connector and a reusable verification skill.

Recommended stack:
- Codex Mac desktop app
- Playwright MCP or Chrome DevTools MCP
- GitHub connector
- deployment/runtime connector such as Vercel
- error analytics connector such as Sentry or PostHog
- a reusable local skill for browser verification
- optional multiple agents or threads for implementer vs verifier

Key takeaway:
- Codex desktop can absolutely do this workflow well.
- The best version is not just one chat thread doing everything.
- The best version is one agent fixing the app and another agent or skill verifying the real browser path and feeding findings back.

### Exact workflow

1. Open the repo in Codex desktop.
2. Add Playwright MCP or Chrome DevTools MCP in Codex's connector/tooling setup.
3. Create or install a reusable browser verification skill with instructions like:
   - start the app if needed
   - browse main user flows
   - inspect console/network/runtime logs
   - report exact failure points
   - rerun after patches
   - convert successful flows into Playwright specs
4. Use a two-thread or two-agent pattern:
   - Agent 1: implementation/fixes
   - Agent 2: browser verification
5. Prompt the system with something like:

```text
Implement and verify the app end to end. Run the dev server, open the app in the browser tool, exercise the main user flows like a real user, inspect console and network failures, fix issues in code, rerun until clean, then capture the stable flow as Playwright tests.
```

6. Let the verifier report screenshots, DOM findings, broken requests, and visible UI issues.
7. Feed those results into the implementation agent until the loop stabilizes.

### What makes Codex strong here

- Strong agent orchestration.
- Good fit for splitting implementation and verification responsibilities.
- Excellent when you want the agent to manage code, tests, docs, and deployment checks in parallel.

### Weaknesses

- Compared with Antigravity, the browser loop still feels more assembled than native.
- Compared with Cursor, it usually needs a bit more setup before the browser workflow feels turnkey.

### Best-practice rules to give Codex

- Separate implementer and verifier responsibilities.
- Do not trust code-only success; browser verification is required.
- Require the verifier to cite exact URLs, failing requests, and visible error states.
- Promote passing exploratory flows into tests immediately.

## Google Antigravity

### Best setup

Antigravity appears to be the most purpose-built platform for this exact problem as of April 2026: an agentic development environment that explicitly spans editor, terminal, and browser.

Recommended stack:
- Antigravity desktop app
- Chrome installed
- official Antigravity browser extension
- GitHub connector
- deployment/logging connector
- analytics/error connector
- keep the MCP set minimal at first

Key takeaway:
- If your goal is specifically "the AI should use the app in a browser like a human and fix it," Antigravity appears to have the most native experience for that loop.
- Community reports suggest keeping connector count modest at first because too many MCPs can reduce stability.

### Exact workflow

1. Open the project in Antigravity.
2. Install the Antigravity Chrome extension when prompted.
3. Use the manager surface to delegate the full task, for example:

```text
Build and verify this app end to end. Start the dev server, open the app in Chrome, use it like a new user would, inspect DOM, console, and failed requests, fix the code when something breaks, rerun the flow, and save the validated user path as Playwright smoke tests.
```

4. Let Antigravity orchestrate the editor, terminal, and browser together.
5. Review the artifacts it produces, such as screenshots, recordings, and walkthroughs.
6. Comment on the artifact trail if you want it to tighten the flow or broaden coverage.
7. Once stable, require it to codify the validated path as automated tests.

### What makes Antigravity strong here

- The browser is treated as a first-class part of the agent workflow.
- Strong artifact-based verification.
- Feels closest to "delegate the whole browser QA loop and supervise the evidence."

### Weaknesses

- Some community reports mention instability with too many MCPs.
- Some reports also raise caution around autonomy and automatic tool execution, so safety and approval boundaries should be reviewed carefully.

### Best-practice rules to give Antigravity

- Keep the connector set lean until the workflow is stable.
- Require artifact-backed claims.
- Require browser verification, not just DOM-level assertions.
- Turn successful flows into Playwright tests so you are not dependent on ad hoc agent exploration forever.

## Ranking for this exact use case

This ranking is based on the official docs I could verify plus community reports from Reddit, X/Twitter, and related discussions as of April 4, 2026. Where community evidence was mixed, I weighted native browser-first workflow highest.

### 1. Google Antigravity

Best for the purest version of this use case:
- browser-first
- artifact-heavy
- strongest "agent uses the app like a user" feel

Why it ranks first:
- It appears to be the most purpose-built for the editor-terminal-browser loop.
- The workflow is more natively aligned to browser verification than the others.

### 2. Cursor

Best all-around default for most people:
- very practical
- strong IDE integration
- strong MCP/connectors
- excellent once Playwright MCP is added

Why it ranks second:
- It feels more mature as a daily driver IDE for code plus browser verification.
- Slightly less magical than Antigravity for this exact use case, but arguably the safest default recommendation.

### 3. Claude Code

Best high-ceiling customizable workflow:
- powerful
- disciplined
- great if you want rules and hooks

Why it ranks third:
- It can be excellent, but it asks you to assemble a bit more process.
- With good rules and hooks, it can rival Cursor, but without them it is easier to drift into inconsistent verification.

### 4. Codex Mac desktop app

Best for orchestration-heavy teams:
- strong multi-agent thinking
- strong coding workflow
- very capable with the right browser MCP

Why it ranks fourth:
- It can definitely do the job well.
- Relative to the others, the browser-driven end-to-end loop still feels a bit more assembled than first-class-native.

## My practical recommendation

If I were setting this up for real in April 2026:

- I would choose Cursor if I wanted the best balance of quality, daily usability, and low workflow risk.
- I would choose Antigravity if I specifically wanted the most native "AI uses the browser like a user" experience.
- I would choose Claude Code if I wanted to heavily customize the workflow with hooks and strict written rules.
- I would choose Codex desktop if I wanted a multi-agent implementation plus verification workflow and I was happy to add a good browser MCP and reusable skill.

## Connector and tool stack I would install first on each

### Cursor
- Playwright MCP
- GitHub
- Sentry or PostHog
- Vercel if relevant

### Claude Code
- Playwright MCP
- GitHub
- Vercel or Sentry
- hooks for verification
- `playwright-cli` for repeated smoke loops

### Codex desktop
- Playwright MCP or Chrome DevTools MCP
- GitHub
- Vercel
- Sentry or PostHog
- reusable browser verification skill

### Antigravity
- official Chrome extension
- GitHub
- one deployment/logging connector
- one error/analytics connector
- keep MCP count minimal until stable

## Sources

### Cursor
- Cursor MCP docs: <https://docs.cursor.com/en/context/mcp>
- Cursor MCP tools docs: <https://docs.cursor.com/en/tools/mcp>
- Cursor web development guide: <https://docs.cursor.com/guides/tutorials/web-development>
- Cursor Background Agents docs: <https://docs.cursor.com/en/background-agents>
- Cursor forum discussion on browser automation conflicts: <https://forum.cursor.com/t/browser-automation-interferes-with-other-mcp-tools-and-there-is-no-global-disable-for-it/143126>
- Reddit benchmark comparison thread: <https://www.reddit.com/r/AI_Agents/comments/1rg9cni/ai_coding_benchmark_with_claude_code_cursor_codex/>

### Claude Code
- Claude Code MCP docs: <https://docs.anthropic.com/en/docs/claude-code/mcp>
- Claude Code hooks guide: <https://docs.anthropic.com/en/docs/claude-code/hooks-guide>
- Claude Code hooks reference: <https://docs.anthropic.com/en/docs/claude-code/hooks>
- Claude connectors directory: <https://support.anthropic.com/en/articles/11724452-browsing-and-connecting-to-tools-from-the-directory>
- Claude custom remote MCP connectors: <https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp>
- Playwright CLI/getting started reference: <https://playwright.dev/docs/getting-started-cli>
- Reddit discussion on making Claude Code use the browser to test: <https://www.reddit.com/r/ClaudeAI/comments/1m89j9n/how_to_make_claude_code_use_the_browser_to_test/>
- Reddit warning about hidden test-time hacks: <https://www.reddit.com/r/ClaudeCode/comments/1rug14a/claude_wrote_playwright_tests_that_secretly/>

### Codex
- Introducing the Codex app: <https://openai.com/index/introducing-the-codex-app/>
- Codex use cases: <https://developers.openai.com/codex/use-cases>
- Codex cloud docs: <https://developers.openai.com/codex/cloud>
- OpenAI Docs MCP: <https://platform.openai.com/docs/docs-mcp>
- X post discussing the Codex app: <https://x.com/ajambrosino/status/2018385459936923656>
- Reddit discussion on browser testing in Codex: <https://www.reddit.com/r/OpenaiCodex/comments/1rdzdfe/codex_cant_run_and_test_projects_in_a_browser/>

### Antigravity
- Google Developers Blog launch post: <https://developers.googleblog.com/en/build-with-google-antigravity-our-new-agentic-development-platform/>
- Google Codelab getting started guide: <https://codelabs.developers.google.com/getting-started-google-antigravity>
- Reddit discussion on browser extension issues: <https://www.reddit.com/r/google_antigravity/comments/1pwfgdy/cant_get_the_antigravity_browser_to_work/>
- Reddit discussion raising caution about MCP auto-execution: <https://www.reddit.com/r/google_antigravity/comments/1p92k8e/warningquestion_google_antigravity_executes_mcp/>
- Reddit discussion on instability with too many MCPs: <https://www.reddit.com/r/google_antigravity/comments/1pij7kh/anyone_facing_issues_with_google_antigravity/>

## Confidence note

The official documentation was strongest for connector/MCP availability and workflow shape. The platform ranking itself is partly an inference from that documentation plus community reports. In other words, the install/setup recommendations are on firmer ground than the exact 1-to-4 ranking order.
