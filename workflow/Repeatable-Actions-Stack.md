# Repeatable Actions Stack

> Last updated: April 1, 2026
> Purpose: Turn repeated prompts into portable repo assets instead of tribal chat habits.

## Why This Matters

The strongest April 2026 agent workflows are no longer built around better one-off prompts. They are built around versioned workflow assets:

- short context files
- reusable commands
- skills or subagents
- hooks or rules
- bounded automations

This keeps behavior portable across Codex, Claude Code, Cursor, Gemini CLI, and Antigravity.

## The Promotion Ladder

Use this ladder when a behavior repeats:

1. **Prompt**
   Use for one-off exploration, ambiguity, or fresh research.
2. **Plan / checklist**
   Use when the work spans multiple steps or owners.
3. **Command**
   Use when you want to run the same checklist or review prompt on purpose.
4. **Skill**
   Use when the workflow bundles tools, scripts, assets, or specialized judgment.
5. **Hook / rule**
   Use when the behavior should happen automatically or should always constrain the agent.
6. **Automation / background agent**
   Use when the task is narrow, recurring, and reviewable without live steering.

Do not jump from a repeated prompt straight to automation. Commands and skills are usually the right middle layer.

## When To Promote

Promote a prompt into a reusable asset when at least one is true:

- you have retyped it 3 or more times
- you keep reminding the AI about the same steps
- the workflow needs exact formatting or verification output
- the task has a recurring human-only handoff
- the workflow depends on tool access, browser state, or shell context
- the cost of doing it inconsistently is higher than the cost of storing it

## Platform Map

| Platform | Best Reusable Surfaces | What They Are Best At |
|---|---|---|
| Codex | `AGENTS.md`, skills, automations, worktrees | compact repo map, tool-heavy skills, bounded recurring maintenance |
| Claude Code | `CLAUDE.md`, `.claude/commands/`, `.claude/rules/`, hooks, skills, subagents | richest local workflow-as-code stack |
| Cursor | Project Rules, Commands, Memories, Background Agents, Automations, Bugbot | bootstrap control room, team-shared prompts, async review/triage |
| Gemini CLI | `GEMINI.md`, TOML commands, hooks, skills, extensions | portable local command/skill stack with strong context layering |
| Antigravity | browser-driven workflows and computer-use validation | setup or verification where the browser is the real work surface |

## What To Store Where

### Context Files

Keep always-loaded context short and map-like:

- `AGENTS.md` for Codex builder behavior
- `CLAUDE.md` for planning/review behavior
- `GEMINI.md` for Gemini CLI context

These should point to deeper truth in `knowledgebase/`, `runbooks/`, and plans.

### Commands

Use commands for stable invoked checklists such as:

- `plan-feature`
- `final-plan-checklist`
- `review`
- `browser-verify`
- `db-bootstrap`
- `vercel-bootstrap`

Commands are best when the workflow is explicit and you want to choose when it runs.

### Skills

Use skills when the workflow needs:

- scripts or shell helpers
- browser or MCP tooling
- shared assets or reference files
- specialized reviewer posture
- cross-project reuse

Good skill candidates in your workflow:

- service bootstrap
- schema sync audit
- browser smoke test
- deployment readiness
- structured code review

### Hooks And Rules

Use hooks or rules for things that should happen automatically:

- block secrets or destructive shell patterns
- remind the agent about browser lanes
- route API work to stricter conventions
- notify when the agent is blocked on login or approval
- load the right context for risky paths

### Automations

Only automate bounded chores with reviewable output:

- CI failure summaries
- daily issue triage
- stale-doc cleanup
- weekly shipped-work summary
- repetitive low-risk cleanup PRs

Avoid using automations for first-run setup, broad product design, or tasks that still need live human steering.

## Default Pack To Add Early

For most repos, add this small pack before feature churn starts:

- one `plan-feature` command
- one `review` command
- one `browser-verify` command if UI exists
- one service-bootstrap skill or command
- one core safety rule
- one browser-qa rule
- one weekly maintenance automation only after the repo is stable

## Browser-Login Handoff Rule

When login, 2FA, org selection, or consent is required:

1. the agent opens the exact page or auth command
2. the human completes the one human-only step
3. the agent resumes immediately
4. the repo records IDs, env names, and verification commands

If this happens more than once, it should have a named command, skill, or runbook entry.

## What Not To Do

- Do not stuff everything into one giant context file.
- Do not create commands for workflows that are still changing daily.
- Do not make a skill when a simple command would do.
- Do not build an automation before the manual workflow is already reliable.
- Do not leave browser setup as "someone clicks around later."

## Suggested Naming Pack

Keep names consistent across tools when possible:

- `plan-feature`
- `final-plan-checklist`
- `review`
- `quality-gate`
- `browser-verify`
- `db-bootstrap`
- `vercel-bootstrap`
- `service-handoff`

That makes the workflow easier to move between Claude, Cursor, Gemini, and Codex skills.

## Source Notes

Reviewed on April 1, 2026:

- OpenAI: [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/), [Harness engineering](https://openai.com/index/harness-engineering/), [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md), [Codex automations](https://developers.openai.com/codex/app/automations)
- Anthropic: [Claude Code slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands), [hooks](https://docs.anthropic.com/en/docs/claude-code/hooks), [subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents), [settings](https://docs.anthropic.com/en/docs/claude-code/settings)
- Cursor: [Rules](https://docs.cursor.com/context/rules), [Commands](https://docs.cursor.com/en/agent/chat/commands), [Memories](https://docs.cursor.com/en/context/memories), [Background Agents](https://docs.cursor.com/en/background-agents), [Bugbot](https://docs.cursor.com/en/bugbot), [Agent Security](https://docs.cursor.com/account/agent-security), [Automations announcement](https://forum.cursor.com/t/introducing-cursor-automations/153733)
- Gemini CLI / Google: [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/), [Custom Commands](https://google-gemini.github.io/gemini-cli/docs/cli/custom-commands.html), [Extension best practices](https://geminicli.com/docs/extensions/best-practices/), [Gemini 3 / Antigravity](https://blog.google/products-and-platforms/products/gemini/gemini-3/)
- Research baseline: [Configuring Agentic AI Coding Tools: An Exploratory Study](https://arxiv.org/abs/2602.14690)
