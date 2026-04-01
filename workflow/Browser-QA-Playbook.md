# Browser QA Playbook

> A repeatable way to decide how AI agents and humans should validate browser behavior.

## Goal

Pick one reliable browser path per repo, one fallback path, and one clear human/agent handoff pattern.

## The Four Main Patterns

### 1. Isolated Playwright Server

Best for repos where agent-driven QA should not interfere with a normal dev server.

Use when:

- local dev server state is fragile
- you want clean artifacts
- browser automation should be reproducible

Typical shape:

- Playwright boots its own app instance
- uses a separate build dir if needed
- stores traces/screenshots/videos on failure

### 2. Existing Local App Target

Best for repos where the running local app already has seeded state.

Use when:

- the user already has the app running
- you need to test against known local data
- the app is easy to point Playwright at with `PLAYWRIGHT_BASE_URL`

### 3. Agent Bypass / Auth-Light QA Copy

Best for auth-heavy apps where the agent cannot reliably use the real protected route.

Use when:

- the user needs real Chrome on one port
- the agent needs a safe localhost-only bypass on another port
- protected flows otherwise block agent automation

### 4. Dual-Lane Browser QA

Best for projects where you want the human in a real browser while the agent inspects a controllable copy.

Use when:

- auth, cookies, or extensions matter in the user lane
- the agent still needs DOM, console, network, and screenshot access
- you want faster collaboration than screen-sharing every click

Typical shape:

- user lane: real Chrome profile
- agent lane: isolated Playwright or localhost bypass copy

## Browser Login Handoff Pattern

When setup or QA requires a real browser login:

1. the agent opens the relevant page
2. the user completes login, 2FA, consent, or org selection
3. the agent resumes setup or QA and records the result

Do not force the user to repeat the same browser setup later. Capture the path once in repo docs.

## What To Document In Each Repo

- the preferred browser QA path
- the fallback path
- the exact commands
- whether Playwright should use its own server or an existing one
- whether a real Chrome lane is part of the workflow
- where artifacts go on failure
- whether auth credentials or bypass env vars are required

## Good Defaults

- Prefer isolated Playwright for internal dashboards and smoke tests.
- Prefer an auth-bypass copy for protected SaaS dashboards.
- Prefer dual-lane QA when the user needs real login state and the agent still needs repeatable inspection.
- Prefer existing local app targeting when seeded state matters more than isolation.

## Artifact Policy

If a browser run can fail, keep:

- screenshots
- traces
- videos when practical
- one place in the repo docs that says where those artifacts land

## Recommendation

Every repo with UI should have a short `TESTING_AND_BROWSER_AUTOMATION.md` that answers:

- which browser path should I use right now?
- what should the agent use?
- when does the user need to log in manually?
