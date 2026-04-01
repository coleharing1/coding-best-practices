# AI-First Service Setup And Login Handoff

> Front-load the service setup work that unlocks AI execution after your one human-only step.

## Goal

Set up databases, hosting, browser QA, and service auth early enough that the AI can keep working without sending you back into dashboards all day.

## Core Principle

When a service needs login, 2FA, org selection, or consent:

1. the AI should get you to the exact page or auth command
2. you complete the human-only step
3. the AI immediately resumes setup, verification, and documentation

This is the preferred startup flow across your repos.

## What To Front-Load In The First Project Hour

- a dedicated cloud project when the repo needs real data or hosted auth
- direct AI-usable database access, not just dashboard access
- hosting/project linking so env pulls and deploy commands work
- one documented browser QA path for the agent
- one short runbook for service handoff and follow-up commands
- the first repeatable setup commands or skills so the same bootstrap is not re-prompted forever

## Database Bootstrap Pattern

Use this when the repo depends on Supabase, Postgres, or another hosted database.

- Create a dedicated dev project early when the repo needs real remote state.
- Capture both app-safe and admin-safe connection paths early:
  - project URL
  - public/anon key
  - service/admin key
  - pooled DB URL
  - direct DB URL
- Put the variable names in `.env.local.example` immediately.
- Verify direct SQL access from the terminal, not just the dashboard.
- Prefer checked-in migrations over dashboard-only schema edits.
- If the project will grow, add explicit env-targeted push/parity scripts instead of depending forever on linked CLI state.
- If the platform supports it, connect MCP or OAuth database access so the AI can inspect the hosted project without dashboard clicking.

### Strong Patterns From Your Repos

- `coupler.io` and Texas Fowlers OS treat direct Postgres access as a first-class workflow, not an emergency tool.
- `fish-monkey-ad-creative-generator` uses explicit env-targeted DB push scripts for dev vs prod.
- `TodoList` uses separate hosted dev/prod projects plus MCP access and documents the exact project refs.

## Vercel Bootstrap Pattern

Use this when the app will deploy on Vercel or depends on Vercel envs, logs, or cron.

- Authenticate the CLI first so the AI can use `vercel` without stopping later.
- Link the repo early so `.vercel/project.json` exists.
- Record the Vercel `projectId` and `orgId` in repo docs or runbooks.
- Document required env var names and where each value comes from.
- Add env-pull or env-wire scripts if the repo will repeatedly sync Vercel configuration.
- Treat Vercel env state as external truth:
  - document names in the repo
  - keep values out of git

### Strong Patterns From Your Repos

- `TodoList` documents `projectId`, `orgId`, cron behavior, and env ownership.
- `TodoList/scripts/social/local-whisper-offload/vercel-wire.sh` is a good example of AI-finishing the configuration after auth/linking exist.
- `coupler.io` keeps auth redirects tied to the real deployed origin with `APP_URL`, which prevents broken invite flows.

## Browser QA Bootstrap Pattern

Do not wait until the first UI bug to decide how the agent can see the app.

- Pick the primary browser path on day one.
- Separate the human lane from the agent lane when auth or real-browser state matters.
- Keep one documented fallback path when the primary flow is blocked.

### The Best Recurring Pattern

- user lane: real Chrome profile for logged-in, extension-aware, cookie-aware behavior
- agent lane: isolated Playwright server or localhost auth-bypass copy for DOM, console, network, and repeatable inspection

This is the cleanest pattern in `coupler.io` and fits how you like to collaborate.

## Human-Only Handoff Loop

Use this for Supabase, Vercel, Shopify, Google, Meta, Clerk, OAuth providers, and any dashboard that the agent cannot fully access on its own.

1. AI opens the exact service page or runs the exact auth command.
2. You log in, complete 2FA, choose the org/project, or grant consent.
3. AI resumes the remaining configuration immediately.
4. AI records what was created and how to verify it.

## What The AI Must Record After A Handoff

- service name
- dev/preview/prod environment
- project ref, team ID, org ID, or account selected
- auth method now available to the AI
- local artifacts created
  - `.vercel/project.json`
  - `supabase/config.toml`
  - project-scoped MCP config
  - `.env.local.example` updates
- next verification commands
- any remaining human-only steps

## Platform Playbooks

### Codex

Best fit: browser-assisted setup plus terminal follow-through.

- In the desktop app, Codex can use browser automation and local tooling together.
- Preferred flow:
  - Codex opens the target page or browser route
  - you complete login or 2FA
  - Codex continues configuration, testing, and documentation
- Keep `AGENTS.md` short and map-like, then put repeated setup flows into repo skills instead of overgrowing the context file.
- Use Codex skills for repeated setup tasks such as:
  - DB bootstrap
  - Vercel link + env documentation
  - browser smoke verification
  - service-handoff writeups
- Use Codex automations for bounded maintenance work after the repo is already configured, not for the first brittle bootstrap.
- For app QA, keep a real Chrome lane for your logged-in state and a separate agent-visible lane for Playwright or bypass QA.
- Codex is a strong default for finishing setup once auth exists:
  - link the project
  - wire env templates
  - verify direct DB access
  - run browser checks
  - write the worklog/runbook entry

### Claude Code

Best fit: planning, MCP auth setup, and high-risk setup review.

- Claude Code officially supports browser-based login on first launch.
- Remote MCP auth also uses a browser-login flow from `/mcp`, then stores refreshed tokens for reuse.
- Claude Code is the strongest current platform for turning startup habits into explicit workflow files:
  - `.claude/commands/` for invoked checklists
  - `.claude/rules/` for scoped instructions
  - hooks for automatic guardrails and notifications
  - subagents for specialized setup or review lanes
- For service setup, use Claude Code to:
  - plan the bootstrap steps
  - trigger CLI or MCP auth flows
  - resume terminal-side setup after you finish the browser step
- Promote a repeated startup prompt into a command first. Promote it into a skill only when it bundles real tooling or gets reused across projects. Use hooks for things you never want to remember manually.
- For browser-heavy setup beyond simple auth, pair Claude Code with its browser-capable surfaces when available, or let the relevant CLI/MCP open the auth window and continue from there.

### Cursor

Best fit: bootstrap control room, docs, repo wiring, and MCP/project setup.

- Cursor is excellent for creating the repo OS, pasting research, connecting GitHub, and organizing setup docs.
- Cursor's strong repeatable surfaces are:
  - Project Rules
  - Commands in `.cursor/commands/`
  - Memories for recurring repo context
  - Background Agents / Automations for bounded async chores
- In practice, treat Cursor as the place to prepare and finish setup around the browser step, not the default arbitrary-dashboard operator.
- Preferred flow in Cursor:
  - use Cursor to set up docs, rules, MCP config, and starter files
  - add the first project commands for plan, review, and browser verify
  - let provider CLIs or MCP auth open browser/OAuth windows when needed
  - you complete login/consent
  - Cursor continues from the linked or authenticated local state
- After the repo is configured, Background Agents or Automations are a good fit for review, triage, or cleanup loops. They are not a substitute for the first human-guided login handoff.
- This recommendation is partly an inference from Cursor's official rules/commands/security docs plus your repo patterns.

### Gemini CLI + Google Antigravity

Best fit: Gemini CLI for local reusable workflow assets, Antigravity for browser-heavy setup where the agent should actively drive the browser after login.

- Gemini CLI is strong when you want:
  - hierarchical `GEMINI.md` context
  - TOML custom commands
  - hooks
  - skills/extensions that bundle commands, context, and tool access
- Google says Antigravity agents have direct access to the editor, terminal, and browser.
- Google also says Antigravity is tightly coupled to Gemini Computer Use for browser control.
- Preferred flow:
  - Gemini CLI or Antigravity prepares the local repo command/skill context
  - Antigravity opens the dashboard or auth route
  - you complete login, org selection, or 2FA
  - Antigravity finishes the rest of the browser-side setup and validates the result
- This makes Antigravity a strong option for browser-first onboarding flows and cloud-console configuration.

## Recommended Startup Checklist

- [ ] repo OS files exist before real build work starts
- [ ] database project exists and the AI has direct access, not just dashboard screenshots
- [ ] hosting project is linked locally
- [ ] env var names and value sources are documented
- [ ] one browser QA lane for the user and one for the agent are documented
- [ ] one handoff runbook exists for service login/configuration
- [ ] the AI can resume work immediately after your login step

## Source Notes

Checked against official platform material on April 1, 2026:

- OpenAI Codex app: [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)
- Anthropic Claude Code: [Overview](https://docs.anthropic.com/en/docs/claude-code/overview), [Authentication](https://docs.anthropic.com/en/docs/claude-code/authentication), [MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)
- Cursor: [Rules](https://docs.cursor.com/context/rules), [Commands](https://docs.cursor.com/en/agent/chat/commands), [Agent Security](https://docs.cursor.com/account/agent-security)
- Gemini CLI: [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/), [Custom Commands](https://google-gemini.github.io/gemini-cli/docs/cli/custom-commands.html)
- Google Antigravity: [Gemini 3 announcement](https://blog.google/products-and-platforms/products/gemini/gemini-3/)
