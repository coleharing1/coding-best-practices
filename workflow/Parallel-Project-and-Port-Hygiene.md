# Parallel Project And Port Hygiene

> Last updated: April 14, 2026
> Role in workflow: How to safely run multiple local projects, AI sessions, and dev servers without losing track of ports, processes, or repo context.

---

## Why This Matters

Running multiple things at once is normal in modern AI-assisted development:

- one repo may need a frontend, backend, database, and browser automation tool
- another repo may be open in a second editor window for planning or review
- Claude Code, Codex, and Cursor may each be helping with different parts of the workflow

The goal is not "only run one thing." The goal is:

1. one intentional task per context lane
2. one intentional server per repo by default
3. clear isolation when multiple agents or multiple repos are active

---

## Short Answer

Yes, it is okay to have multiple local projects and services running at the same time.

It is usually healthy to have:

- one or more app servers for different projects
- local infrastructure like Postgres or Redis
- browser automation or testing tooling while you are actively using it

It is usually unhealthy to have:

- duplicate app servers for the same repo with no clear purpose
- multiple agents editing the same branch or files at once
- random ports open that you cannot map back to a known project or tool

For most solo workflows, the best default is:

- multiple projects can be open
- only one active implementation lane per repo
- only one app server per repo unless you intentionally need a second copy

---

## The Four Collision Layers

Parallel work becomes confusing when you mix up which layer is colliding.

| Layer | What Collides | Best Isolation |
|---|---|---|
| repo context | instructions, plans, chat history, assumptions | separate chat/tab/window plus durable repo docs |
| code changes | files, branches, uncommitted edits | separate branch or git worktree |
| local runtime | ports, logs, CPU, RAM | fixed ports plus intentional shutdown habits |
| network exposure | who can reach the server | localhost by default, wider host binding only when needed |

If you isolate the right layer, running multiple things is usually fine.

---

## Healthy Default Posture

### 1. One Task Per Session

Use one chat, tab, or session per meaningful task.

Good examples:

- one Claude session for planning
- one Codex session for implementation
- one Cursor chat for repo setup or review

Bad example:

- one giant chat trying to plan feature A, debug feature B, and clean repo C at the same time

This reduces context bleed and makes it easier to tell which instructions belong to which task.

### 2. One Parallel Change Lane Per Repo

If two parallel efforts touch the same repo:

- use separate branches at minimum
- use `git worktree` if both efforts may be active at once

This is the cleanest way to let multiple AI tools or sessions work in parallel without trampling the same files.

### 3. One Intentional App Server Per Repo By Default

A good default is:

- one frontend or app server per repo
- one backend server per repo if the architecture requires it

Running two copies of the same app from the same repo is usually only worth it when you are:

- comparing two branches
- testing different env settings
- validating two ports or host modes on purpose

If you do not have a specific reason, duplicate servers mostly add noise, memory use, and log confusion.

### 4. Stable Ports Beat Random Ports

Pick predictable ports for repeat projects and document them.

Examples:

- project A frontend on `3000`
- project B frontend on `3002`
- project A API on `3030`
- Postgres on `5432`
- Redis on `6379`

When ports drift randomly, your machine becomes harder to understand and your AI tools become more likely to look at the wrong service.

### 5. Local Databases Are Usually Fine To Leave Running

Databases and caches such as Postgres and Redis are often long-lived local infrastructure, not session-specific clutter.

Keeping them running is usually fine when they are:

- bound to localhost only
- not consuming excessive resources
- part of your normal daily workflow

### 6. Prefer Localhost Unless You Need Device Testing

By default, expose local dev servers only to your own machine.

Open broader host access only when you intentionally need:

- phone or tablet testing
- LAN demos
- external browser automation that must reach your machine

This reduces accidental exposure and makes your setup easier to reason about.

---

## When Multiple Things Running Is Good

| Situation | Healthy? | Why |
|---|---|---|
| one Next.js app for project A and one Vite app for project B | yes | separate repos, separate goals, separate ports |
| frontend + backend + Postgres + Redis for one project | yes | normal full-stack local stack |
| one browser automation server while actively testing UI | yes | tooling tied to current task |
| one planning session and one implementation session for different repos | yes | context separation is clear |
| multiple agents on the same repo using separate worktrees | yes | isolated file state |

---

## When One-At-A-Time Is Smarter

| Situation | Better To Reduce? | Why |
|---|---|---|
| two copies of the same app from the same repo | usually yes | duplicate memory use and log ambiguity |
| two agents editing the same branch | yes | easy to create collisions and accidental overwrites |
| many open sessions with unclear ownership | yes | context drift and instruction confusion |
| battery or RAM pressure on a laptop | yes | performance problems compound quickly |
| a debugging session that depends on deterministic logs | yes | fewer moving parts makes root-cause work easier |

---

## A Simple Rule For Beginners

If you are new to this, use this default:

1. keep at most two active app repos running at once
2. allow local infrastructure like Postgres and Redis to stay on
3. allow one browser automation tool while you are actively testing
4. shut down duplicate app servers when you finish with them

This is not a hard law. It is a low-stress starting point.

---

## Tool-Specific Guidance

### Claude Code

Use Claude Code as a planner, reviewer, and careful architect.

Best practices:

- keep `CLAUDE.md` short and map-like
- split large repo guidance into durable docs instead of one giant file
- use worktrees for parallel same-repo work
- remember that multiple instances and automations can add overhead and cost

Good fit for parallelism:

- planning one feature while another tool implements a different phase
- reviewing a diff while the build lane is separate

Bad fit for parallelism:

- two Claude sessions making overlapping edits in the same files

### Codex

Use Codex as the builder and terminal execution lane.

Best practices:

- keep `AGENTS.md` short and operational
- use isolated copies or worktrees when parallelizing the same repo
- prefer one active builder per branch
- let Codex own a bounded execution phase, then hand review back to another lane if needed

Good fit for parallelism:

- one Codex lane building feature A while another repo is only being planned elsewhere

Bad fit for parallelism:

- two Codex sessions applying overlapping edits to one branch with no clear ownership

### Cursor

Use Cursor as the project control room.

Best practices:

- keep persistent behavior in rules, commands, and committed docs
- use separate chats or tabs for separate tasks
- treat memories as helpful, but not as the source of truth
- automate only after the manual workflow is already reliable

Good fit for parallelism:

- one chat for setup
- one chat for code review
- one separate repo open for a different initiative

Bad fit for parallelism:

- one giant conversational thread mixing unrelated repos and goals

### Shared Rule Across All Three

Parallel sessions are fine.

Parallel ambiguity is the problem.

The fix is durable repo context:

- `README.md`
- `WORKLOG.md`
- `AGENTS.md`
- `CLAUDE.md`
- plans, checklists, and runbooks

---

## How To Audit What Is Running On Your Machine

These commands are enough for a fast local audit on macOS:

### 1. List TCP listeners

```bash
lsof -nP -iTCP -sTCP:LISTEN
```

Use this to answer:

- what ports are open
- which process owns each port
- whether the port is exposed on all interfaces or only localhost

### 2. List UDP listeners when needed

```bash
lsof -nP -iUDP
```

Use this mostly for:

- browser tooling
- local system services
- discovery protocols

### 3. See what a PID actually is

```bash
ps -p <PID> -o pid,ppid,user,command=
```

Use this to map a short process name like `node` back to the real command.

### 4. Find the working directory for a PID

```bash
lsof -a -p <PID> -d cwd
```

This is one of the highest-value commands in a multi-project machine. It tells you which repo launched the process.

### 5. Probe the port

```bash
curl -I http://127.0.0.1:<PORT>
```

Use this to learn whether the listener is:

- actually an HTTP app
- a Next.js dev server
- a Vite dev server
- an API or Express server
- just a tooling socket

---

## How To Interpret What You Find

Most local listeners fall into one of four buckets:

| Bucket | Typical Examples | Usually Okay To Leave Running? |
|---|---|---|
| app servers | Next.js, Vite, Express, Python API | yes, if actively used and intentional |
| local infra | Postgres, Redis | yes, often |
| tooling | Playwright MCP, language servers, editor helpers | yes, while in use |
| system/app services | OS services, Drive, Loom, editor internals | usually yes, but they are not your build stack |

When auditing your machine, the important question is not "is every process tiny?"

The important question is:

"Can I explain why this process exists, what repo owns it, and whether I still need it?"

---

## Generalized Lessons From A Real Local Audit

A real-world local audit often looks like this:

- one Vite app on one port
- one Express or Node app on another port
- local Postgres and Redis on localhost
- browser tooling on a utility port
- one or more Next.js dev servers

That can be perfectly healthy.

The most common anti-pattern is more specific:

- the same repo has two copies of the same Next.js dev server running on different ports, without an intentional compare/test reason

That pattern is not dangerous, but it is usually wasteful and confusing.

If you see that, the best cleanup step is usually to keep the one you want and stop the duplicate.

---

## Recommended Repo-Level Habits

### Document Ports

Add port notes to the repo when the project is non-trivial.

Best places:

- `README.md`
- `TESTING_AND_BROWSER_AUTOMATION.md`
- a runbook if the service layout is more complex

### Keep Context Files Short

Do not bury runtime facts inside long AI instruction files.

Instead:

- keep `AGENTS.md` and `CLAUDE.md` short
- point to deeper docs for runtime setup and QA

### Name Ownership Clearly

If parallel lanes are active, define who owns what:

- Claude owns planning
- Codex owns implementation phase 2
- Cursor owns setup docs and repo control room

This sounds simple, but it prevents a lot of duplicated work.

### Close Stale Servers At Decision Boundaries

Good moments to shut things down:

- after switching projects
- after merging a feature branch
- before running a clean browser QA pass
- before debugging a flaky port issue

---

## Warning Signs That Your Setup Is Drifting

- you cannot explain which repo owns a port
- the same app is running on multiple ports by accident
- you are reading logs from the wrong process
- multiple chats are giving conflicting instructions to the same repo
- the laptop feels slow and you do not know what is costing RAM
- your local stack only works because of invisible state you cannot describe

When that happens, stop and do a short audit before adding more automation.

---

## Practical Beginner Defaults

If you want a simple standard operating posture:

1. one repo per window
2. one main task per chat
3. one app server per repo by default
4. one worktree per concurrent same-repo build lane
5. local databases may stay on
6. browser tooling stays on only while testing
7. document repeat ports in the repo

This gives you most of the upside of parallel vibe coding without the chaos.

---

## Source Notes

As of April 2026, this guidance aligns with the direction of the official docs:

- OpenAI recommends maximizing a single agent before adding extra orchestration complexity, while still supporting structured multi-agent patterns when they are justified.
- OpenAI's Codex app explicitly supports multiple agents in parallel and isolated worktrees.
- Anthropic documents that multiple instances and automation can affect usage and cost.
- Next.js now treats AI-agent instructions as a first-class repo concern through `AGENTS.md` and `CLAUDE.md`.
- Vite and Next.js both support explicit dev-port configuration, which makes stable local layouts easier.

Official references:

- [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [OpenAI: Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)
- [OpenAI: AGENTS.md and the Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/)
- [Anthropic: Manage costs effectively](https://code.claude.com/docs/en/costs)
- [Anthropic: Memory and project instructions](https://code.claude.com/docs/en/memory)
- [Next.js: How to set up your project for AI coding agents](https://nextjs.org/docs/app/guides/ai-agents)
- [Vite: Server options](https://vite.dev/config/server-options)

Where this guide goes beyond the docs, it does so intentionally as workflow inference for solo development on a real machine:

- use one task per session
- treat duplicate app servers as suspicious unless intentional
- prefer one active implementation lane per repo
- keep port ownership easy to explain
