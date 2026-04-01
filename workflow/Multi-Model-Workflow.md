# Multi-Model Workflow: Claude Code + Codex + Gemini + Cursor + Antigravity + Jules

> Last updated: April 1, 2026
> Primary loop: Claude plans, Codex builds, Gemini reviews, while Cursor and Antigravity handle the setup surfaces that unblock the rest.

---

## 1. Tool Stack And Roles

| Tool | Role | Best Use |
|---|---|---|
| Claude Code | Architect | system design, plan synthesis, high-risk review |
| Codex | Builder | implementation, test-run-fix loops, docs during execution |
| Gemini CLI | Reviewer + utility layer | structural diff review, portable commands, local skills/hooks |
| Cursor | Bootstrapper | repo setup, research organization, GitHub/MCP wiring, rules/commands control room |
| Google Antigravity | Browser-heavy operator | browser-first setup, computer-use validation, agentic browser tasks |
| Jules | Maintenance bot | scheduled cleanup, async PRs, dependency chores |

## 2. Project Lifecycle

### Phase 0: Bootstrap In Cursor

Use Cursor to:

1. create or open the repo
2. paste research and requirements
3. connect GitHub
4. add the repo OS
5. add starter docs, rules, and env templates

Follow `workflow/New-Project-Setup-Guide.md`.

### Phase 0.5: Front-Load Service Setup

Before meaningful build work, use `workflow/AI-First-Service-Setup-and-Login-Handoff.md`.

Front-load:

- database project and direct AI-usable access
- Vercel linking and env ownership
- browser QA path
- service handoff runbook

This is the key behavior across your best repos: do the one human-only login step early, then let the AI keep driving.

### Phase 0.6: Encode Repeatable Actions

Before the repo gets noisy, encode the first repeated behaviors as files:

1. keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` short and map-like
2. create project commands for stable checklists you will run on purpose
3. promote tool-heavy repeated flows into skills
4. use hooks or rules for guardrails you do not want to re-ask for
5. automate only bounded chores with reviewable output

See `workflow/Repeatable-Actions-Stack.md`.

### Phase 1: Dual Plan

Use the same feature prompt in both tools.

1. Claude writes `plans/active/Plan-XXX-CLAUDE.md`
2. Codex writes `plans/active/Plan-XXX-Codex.md`
3. Claude compares both and synthesizes `plans/active/Plan-XXX-Final.md`
4. You review the Final plan

The Final plan should be:

- a checklist, not loose prose
- tagged with owners like `[Cole]`, `[Codex]`, `[Claude]`, `[Shared]`, `[Gate]`
- explicit about login, approval, and browser-only steps

See `workflow/Dual-Plan-Workflow.md`.

### Early UI Exception

For early greenfield UI, let Claude write the first visual pass, then let Codex refine it. Once the look is established, switch back to the normal dual-plan -> Codex execution loop.

### Phase 2: Execute In Codex

Codex implements one phase at a time from `plans/active/Plan-XXX-Final.md`.

For each phase:

1. implement
2. run checks
3. fix failures
4. update docs that changed
5. report exact results

### Phase 3: Review

- Gemini review on every non-trivial diff
- Claude review on high-risk diffs
  - auth
  - payments
  - migrations
  - destructive jobs
  - large refactors

### Phase 4: Quality Gate

Run the full repo gate from `workflow/AI-QUALITY-GATE-SOP.md`.

Minimum pattern:

- lint
- tests
- build
- conditional browser/type/parity checks
- secret scan
- worklog/doc refresh

### Phase 5: Push + Jules

After the gate passes:

1. push intentionally
2. let Jules run async maintenance work
3. review those PRs separately

## 3. Task Router

| Task | Best Tool | Why |
|---|---|---|
| architecture or sequencing | Claude Code | strongest planner |
| build, fix, verify | Codex | best terminal execution loop |
| structural review | Gemini CLI | cheap second pair of eyes plus portable local utility commands |
| repo bootstrap, docs, MCP setup | Cursor | best control room |
| browser-first setup and validation | Antigravity | strongest browser-heavy posture |
| overnight cleanup | Jules | async maintenance |

## 4. What Becomes Repeatable Repo Code

Use this promotion ladder:

| If the behavior is... | Promote it to... |
|---|---|
| a one-off prompt or exploration | normal chat prompt |
| a stable checklist you invoke on purpose | command |
| a specialist workflow with scripts, tools, or assets | skill |
| a guardrail that should fire automatically | hook or rule |
| a narrow recurring maintenance task | automation / background agent |

Do not skip straight from "I said this twice" to automation. The normal progression is prompt -> command -> skill/hook -> automation.

## 5. How Tools Share Context

### Shared Repo Files

| File | Purpose |
|---|---|
| `plans/active/Plan-XXX-CLAUDE.md` | Claude's independent plan |
| `plans/active/Plan-XXX-Codex.md` | Codex's independent plan |
| `plans/active/Plan-XXX-Final.md` | implementation source of truth |
| `tasks.json` | optional queue with owner + dependency tracking |
| `WORKLOG.md` | durable implementation memory |
| `CLAUDE.md` | Claude-specific planning/review context |
| `AGENTS.md` | Codex-specific builder context |
| `GEMINI.md` | Gemini CLI context and review posture |
| `knowledgebase/10-implementation-checklist.md` | long-running project checklist and gate tracker |

### Context Flow

```text
Cursor -> repo OS + service bootstrap
Claude Code -> independent plan
Codex -> independent plan
Claude Code -> final checklist synthesis
Codex -> implementation
Gemini -> review
Quality gate -> verification
Jules -> async maintenance
```

## 6. Cursor, Gemini, And Antigravity

Use Cursor when you want the project-control-room workflow:

- repo creation
- GitHub connection
- research organization
- MCP wiring
- setup docs

Use Gemini CLI when you want the most flexible local repeatable-actions layer:

- `GEMINI.md` context hierarchy
- TOML custom commands
- local hooks
- skills and extensions
- lightweight review or utility passes from the terminal

Use Antigravity when the browser itself is the work surface:

- browser-first onboarding
- console configuration
- agent-driven browser validation
- computer-use tasks after login

## 7. Integration With Existing Conventions

This workflow plugs into the rest of the repo:

- `workflow/New-Project-Setup-Guide.md` governs bootstrap
- `workflow/AI-First-Service-Setup-and-Login-Handoff.md` governs setup that unlocks later AI work
- `workflow/Repeatable-Actions-Stack.md` governs when prompts should become commands, skills, hooks, or automations
- `workflow/Dual-Plan-Workflow.md` governs plan creation and synthesis
- `workflow/AI-QUALITY-GATE-SOP.md` governs pre-commit verification
- `workflow/Browser-QA-Playbook.md` governs the browser lanes
- `workflow/Worklog-2.0.md` governs durable memory

## Recommended Default

Use this as the default unless there is a strong reason not to:

```text
Cursor bootstrap -> service handoff -> commands/skills/hooks pack -> Claude plan -> Codex plan -> Claude final checklist -> Codex build -> Gemini review -> quality gate -> push
```
