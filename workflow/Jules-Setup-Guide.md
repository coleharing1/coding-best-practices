# Jules Setup Guide

> Last updated: February 24, 2026
> Role in workflow: Phase 5 (Maintenance) — see `Multi-Model-Workflow.md`

Jules is Google's autonomous coding agent. It runs in the cloud, reviews your code, and opens Pull Requests while you keep working. This doc covers everything you need to set up and use Jules effectively.

---

## Table of Contents

1. [What Jules Actually Is](#1-what-jules-actually-is)
2. [Jules Pricing and Limits](#2-jules-pricing-and-limits)
3. [How People Use Jules (Reddit Consensus, Feb 2026)](#3-how-people-use-jules)
4. [Jules Features You Should Be Using](#4-jules-features-you-should-be-using)
5. [Setting Up Jules for Your Workflow](#5-setting-up-jules-for-your-workflow)
6. [Using Jules from Cursor via MCP](#6-using-jules-from-cursor-via-mcp)
7. [Jules Scheduled Agents](#7-jules-scheduled-agents)
8. [Best Practices and Pitfalls](#8-best-practices-and-pitfalls)
9. [Quick Reference: Jules Commands](#9-quick-reference)

---

## 1. What Jules Actually Is

Jules is Google's **autonomous coding agent** powered by Gemini models. It does not run locally — it:

1. Clones your GitHub repo into a secure Google Cloud VM (20GB disk)
2. Reads the codebase, generates a plan
3. Writes code, runs tests, installs dependencies
4. Opens a Pull Request on GitHub when done

**Key distinction:** Jules is not a chat model. It's a background worker. You give it a task, walk away, and come back to a PR. This is what makes it ideal for maintenance — it doesn't block your local dev environment at all.

### What Jules Can Access

- Your GitHub repos (connected via the Jules GitHub App)
- Environment variables you configure per-repo
- The web (Jules can search documentation and code snippets)
- MCP server integrations (Linear, Supabase, Neon, Tinybird, etc.)

### What Jules Cannot Do

- Edit files outside of GitHub repos
- Access your local machine
- Run indefinitely (tasks have timeouts)
- Connect to arbitrary MCP servers (Google hand-vets each integration for security)

---

## 2. Jules Pricing and Limits

| Plan | Cost | Daily Tasks | Concurrent Tasks | Model |
|------|------|------------|-------------------|-------|
| **Jules (Free)** | $0/mo | 15 | 3 | Gemini 3 Flash |
| **Jules in Pro** | $19.99/mo (Google AI Pro) | 100 | 15 | Gemini 3 Pro (priority) |
| **Jules in Ultra** | $124.99/mo (Google AI Ultra) | 300 | 60 | Gemini 3 Pro (highest priority) |

**A "task" = one end-to-end session.** Jules spins up a VM, executes the work, and opens a PR. That entire lifecycle is a single task. Reddit users report the free tier (15/day) is more than enough for most solo developers using scheduled agents.

> *"I got 2 projects with 3 agent runs per day each. So total of 6, with 9 runs left. It's more than enough."* — u/mohamedhamad, r/google_antigravity

Paid plans require a Google AI subscription and are currently only available for @gmail.com accounts (not Workspace/business accounts yet).

---

## 3. How People Use Jules

Based on Reddit discussions from r/google_antigravity, r/ClaudeCode, r/ClaudeAI, and r/FlutterDev (February 2026):

### 1. Scheduled Maintenance Agents (Most Popular)

The single most talked-about Jules feature. You set up recurring tasks that run on a schedule and deliver PRs to your inbox every morning:

- **Sentinel** — finds and fixes security vulnerabilities
- **Bolt** — identifies and applies performance optimizations
- **Palette** — suggests UX/design improvements

People customize and add their own scheduled agents:

> *"I also expanded mine with more bots. One for improving CI, one for documentation, one for architecture improvements, and one for improving tests. So I have like 7 bots that run all night and give me PRs to improve my app every morning."* — u/AnalConnoisseur777

### 2. PR-Based Code Review Loop

Jules + Gemini Code Assist creates a feedback loop:
1. Jules opens a PR
2. Gemini Code Assist (GitHub integration) reviews the PR and adds comments
3. You reply to comments asking Jules to fix accordingly
4. Jules pushes a commit with the changes
5. You merge

> *"I can just reply asking Jules to fix accordingly and it does. And then I just merge the request."*

### 3. Phone-Based Task Delegation

Multiple Reddit users highlight using Jules from their phone — voice-dictate a task, Jules works in the background, review the PR when you're back at your desk.

> *"I take my kid for my morning coffee walk, I voice dictate a new task to Jules. By time I'm back I can once over the PR and merge."* — u/animflynny2012

### 4. Multi-Agent PR Pipelines (Advanced)

Power users build automated pipelines:
1. Jules creates 5 PRs overnight
2. Three separate code review agents comment on each PR
3. A custom agent in an E2B sandbox implements all the review comments
4. Human does final review and merges

> *"I've got a three pronged system... each PR has its own sandbox, destroyed once the agent is done."* — u/JustWuTangMe

### 5. Handling TODO Comments

Jules's "Suggested Tasks" feature scans your codebase for `#TODO` comments and proactively creates plans to resolve them. Available for Pro/Ultra users on up to 5 repos.

---

## 4. Jules Features You Should Be Using

### Memory (Settings → Knowledge)

Jules remembers your preferences, corrections, and patterns across sessions for a given repo. Toggle it on in repo settings.

> *"During a task, Jules will save your preferences, nudges, and corrections. The next time you run the same or similar task, Jules will reference its memory."* — Jules Docs

### Planning Critic

A secondary agent that reviews all auto-approved plans before execution. Resulted in a **9.5% reduction in task failure rates**. This runs automatically — no setup needed.

### CI Fixer (New, Feb 2026)

Jules now detects failed CI checks on its PRs and automatically fixes them in a loop — fix, commit, resubmit — without you intervening.

### Commit Authorship (New, Feb 2026)

Three modes: Jules-only, co-authored (Jules + You), or you-only. Set this in Settings → Commit Authoring to get GitHub contribution credit for Jules-initiated work.

### Image Upload

Upload screenshots, design mocks, or UI bugs when creating a task. Jules uses Gemini's multimodal capabilities to understand visual context.

### Interactive Plan Mode

Instead of Jules jumping straight to code, trigger "Interactive Plan" to have Jules ask clarifying questions first. Better for ambiguous or complex tasks.

### Web Search

Jules can proactively search the web for documentation, APIs, and code patterns while working on a task. No setup needed.

### File Selector

Pin specific files when creating a task so Jules focuses only on what matters. Reduces hallucination and tightens context.

### Environment Variables

Set per-repo env vars (API keys, config) in repo settings so Jules can run builds and tests that require them.

---

## 5. Setting Up Jules for Your Workflow

### Prerequisites

1. **Google account** with access to [jules.google](https://jules.google)
2. **GitHub repos** connected via the Jules GitHub App (done in Jules web UI)
3. **Jules API key** generated at [jules.google.com/settings#api](https://jules.google.com/settings#api)

### Step 1: Connect Your Repos

1. Go to [jules.google](https://jules.google)
2. Click "Add Repository" and install the Jules GitHub App
3. Select which repos to grant access to

### Step 2: Enable Memory

For each repo you work on regularly:
1. Go to the repo page in Jules
2. Settings → Knowledge → Toggle Memory ON

### Step 3: Set Up Scheduled Agents

Navigate to the **Scheduled** tab on your repo page:

**Recommended starter set (fits within free tier):**

| Agent | Schedule | Prompt |
|-------|----------|--------|
| Security | Daily, 2am | "Find and fix one security vulnerability. Focus on input validation, XSS, and dependency vulnerabilities." |
| Performance | Daily, 3am | "Identify and fix one performance issue. Focus on unnecessary re-renders, N+1 queries, and bundle size." |
| Tests | Daily, 4am | "Find one untested critical path and add comprehensive unit tests for it." |

You can edit, pause, and resume scheduled tasks without deleting/recreating them.

### Step 4: Configure Commit Authorship

Settings → Commit Authoring → Select "Co-authored (You + Jules)" so your GitHub contribution graph reflects Jules-initiated work.

### Step 5: Enable Suggested Tasks (Pro/Ultra only)

On your repo page, toggle "Suggested Tasks" to let Jules proactively scan for TODOs and improvements.

---

## 6. Using Jules from Cursor via MCP

Your Cursor is already connected to Jules via the MCP integration. Here's how to use it effectively:

### Available MCP Tools

| Tool | What It Does |
|------|-------------|
| `get_all_sources` | List all your connected GitHub repos |
| `get_source` | Get details about a specific repo (branches, etc.) |
| `create_session` | Create a new Jules task on a specific repo |
| `get_session` | Check the status of a running task |
| `list_sessions` | See all your recent/active sessions |
| `approve_session_plan` | Approve a plan when manual approval is required |
| `send_session_message` | Send follow-up instructions to an active session |
| `wait_for_session_completion` | Poll until a session finishes |
| `list_activities` / `list_all_activities` | See step-by-step what Jules did |
| `get_activity` | Get details on a specific activity (code changes, messages) |

### Workflow: Delegating Tasks from Cursor

After you've pushed your changes to GitHub:

1. In Cursor chat, tell the LLM:
   - *"Create a Jules session on `sources/github/coleharing1/REPO_NAME` from branch `main`: Review the latest changes, fix any issues found, add missing error handling, and improve test coverage."*
2. Jules spins up in the cloud, reviews your code, and opens a PR
3. Check progress: *"What's the status of my latest Jules session?"*
4. Review the PR on GitHub and merge

### Workflow: Repetitive/Tedious Tasks

Instead of doing repetitive work yourself:

- *"Create a Jules session on ad-matrix: Update all dependencies to latest versions, fix any breaking changes, and ensure tests pass."*
- *"Create a Jules session on Kingdom-react-testing: Find and fix all TypeScript strict mode errors."*
- *"Create a Jules session on texas-fowlers-shopify-theme: Add comprehensive unit tests for the cart module."*

### Workflow: Plan Approval

For sensitive tasks, require manual plan approval:

1. Create session with `require_plan_approval: true`
2. Jules generates a plan and pauses
3. Review the plan via `list_activities`
4. Approve with `approve_session_plan` or send feedback with `send_session_message`

---

## 7. Jules Scheduled Agents

### The Three Built-In Agents

These are pre-configured in Jules under the **Scheduled** tab:

**Sentinel (Security)**
- Scans for vulnerabilities
- Checks dependency CVEs
- Identifies input validation gaps

**Bolt (Performance)**
- Finds render bottlenecks
- Identifies unnecessary computations
- Suggests caching opportunities

**Palette (UX/Design)**
- Spots accessibility issues
- Suggests UI consistency improvements
- Identifies UX antipatterns

### Custom Scheduled Agents (What Reddit Users Add)

Based on Reddit discussions, power users add:

| Custom Agent | Prompt Template |
|-------------|----------------|
| **CI Improver** | "Review and improve CI/CD pipeline configuration. Reduce build time and improve reliability." |
| **Documentation** | "Find undocumented public functions and add JSDoc/docstring documentation." |
| **Architecture** | "Identify one architectural improvement. Focus on separation of concerns and module boundaries." |
| **Dead Code** | "Find and remove unused imports, dead code paths, and unreachable functions." |
| **Type Safety** | "Find one place where types could be stricter. Add proper TypeScript types and remove any `any` usage." |

### Important: Merge Conflict Handling

Reddit users flag this as Jules's biggest weakness. If multiple scheduled agents create PRs that touch the same files, merge conflicts are common.

**Mitigation:**
- Stagger scheduled agent run times (don't run them all at once)
- Merge one PR at a time
- If conflicts happen, resolve them manually — don't let Jules try to resolve its own conflicts (it sometimes reverts resolved commits)

---

## 8. Best Practices and Pitfalls

### Do

- **Use Jules for maintenance, not greenfield development.** Jules excels at incremental improvements to existing codebases, not building from scratch.
- **Keep prompts specific.** "Fix the authentication bug in `src/auth/login.ts` where special characters in passwords cause a 500 error" beats "fix bugs."
- **Use the file selector** to narrow Jules's focus. Less context = fewer hallucinations.
- **Enable Memory** for repos you work on repeatedly.
- **Review every PR.** Jules is good, not perfect.
- **Stagger scheduled agents** to avoid merge conflicts.
- **Use Interactive Plan** for complex or ambiguous tasks.
- **Set environment variables** for repos that need them for builds/tests.

### Don't

- **Don't use Jules to review its own PRs** — it sometimes reverts its own fixes.
- **Don't run too many concurrent tasks on the same repo** — creates merge conflict nightmares.
- **Don't skip the plan review step** for anything touching auth, payments, or data models.
- **Don't treat Jules output as production-ready without review** — same as any AI code.
- **Don't expect Jules to understand deep project context on first run** — Memory helps but takes a few sessions to build up.

### Common Pitfalls (from Reddit)

1. **"The PRs never good enough"** — Some users find automated PRs need too much human editing. Solution: use more specific prompts and enable the Planning Critic.
2. **Jules reverting resolved merge conflicts** — Known issue. Don't ask Jules to fix its own merge conflicts.
3. **Scheduled agents touching the same files** — Stagger times and merge sequentially.
4. **Context loss on large codebases** — Jules has the same context window limitations as any LLM. Use file selector and specific prompts to compensate.

---

## 9. Quick Reference

### Create a Jules Task from Cursor Chat

```
"Create a Jules session on sources/github/coleharing1/REPO_NAME 
from branch main: [describe the task clearly]"
```

### Check Task Status

```
"List my Jules sessions" or "Get the status of session [ID]"
```

### Approve a Plan

```
"Approve the plan for Jules session [ID]"
```

### Send Follow-Up Instructions

```
"Send a message to Jules session [ID]: [additional instructions]"
```

### See What Jules Did

```
"List all activities for Jules session [ID]"
```

### Jules API (curl, for scripting)

```bash
# List sources
curl -H "x-goog-api-key: $JULES_API_KEY" \
  https://jules.googleapis.com/v1alpha/sources

# Create a session
curl -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add unit tests for the auth module",
    "sourceContext": {
      "source": "sources/github/coleharing1/REPO_NAME",
      "githubRepoContext": { "startingBranch": "main" }
    },
    "title": "Add auth tests"
  }' \
  https://jules.googleapis.com/v1alpha/sessions
```

### Jules CLI (terminal)

```bash
# Install
npm install -g @google/jules

# Authenticate
jules login

# List repos
jules remote list --repo

# Create a task (auto-infers repo from cwd)
jules remote new --session "fix all lint errors"

# Pull results from a completed session
jules remote pull --session SESSION_ID

# Launch interactive TUI dashboard
jules
```

---

## Sources

- [Jules Official Docs](https://jules.google/docs/)
- [Jules API Reference](https://jules.google/docs/api/reference/overview/)
- [Jules CLI Reference](https://jules.google/docs/cli/reference/)
- [Jules Changelog](https://jules.google/docs/changelog/)
- [r/google_antigravity: Jules + Gemini Code Assist](https://www.reddit.com/r/google_antigravity/comments/1r4tluv/) — Feb 2026
- [r/ClaudeCode: Codex 5.3 vs Opus for implementation](https://www.reddit.com/r/ClaudeCode/comments/1r3snq2/) — Feb 2026
- [r/ClaudeAI: Opus 4.6 v Codex 5.3 w Extra High](https://www.reddit.com/r/ClaudeAI/comments/1r5xwe6/) — Feb 2026
- [r/ClaudeCode: Using Gemini + Codex as code reviewers](https://www.reddit.com/r/ClaudeCode/comments/1r9a4x2/) — Feb 2026
- [r/google_antigravity: Moving to an Engineered Stack](https://www.reddit.com/r/google_antigravity/comments/1r4iuqp/) — Feb 2026
