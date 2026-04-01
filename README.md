# Coding Best Practices

> Personal operating system for how Cole Haring likes to build with AI. This is not just prompt storage. It is a repo-level workflow library for planning, building, reviewing, debugging, and keeping project context durable.

## Current Status

This repo is now organized around the patterns that show up repeatedly in your live projects:

- plan-first execution with dual plans and a synthesized final plan
- durable repo memory through `WORKLOG.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, plans, and optional knowledgebases
- short context files that act as maps into deeper repo docs instead of trying to hold the whole truth alone
- risk-tiered review and deterministic quality gates
- browser QA as a first-class workflow, not a last-minute scramble
- environment parity and guarded production workflows
- safe fallbacks and operator runbooks for systems that touch real services
- a portable repeatable-actions layer through commands, skills, hooks, rules, and automations
- archetype starter kits for the project shapes you build most often

The canonical copy-ready assets in `templates/` now use the `*.template.*` naming pattern. Those files are the source of truth.

## The Workflow (TL;DR)

```text
Phase 0  Cursor          Bootstrap repo, paste research, connect GitHub, create context files
Phase 0.5 Services       Front-load DB/Vercel/browser auth so the AI can keep going after your login step
Phase 0.6 Workflow OS    Promote repeated prompts into commands, skills, hooks, and bounded automations
Phase 0.75 Brownfield    Audit existing repo reality, commands, risk map, and known sharp edges
Phase 1a Claude Code     Write Plan-XXX-CLAUDE.md as an owner-tagged checklist
Phase 1b Codex           Write Plan-XXX-Codex.md from the same prompt
Phase 1c Claude Code     Compare both and synthesize Plan-XXX-Final.md
Phase 1d You             Review and adjust the final plan
  -> UI  Claude first    For greenfield UI, let Opus set the look, then let Codex refine
Phase 2  Codex           Implement one phase at a time, run checks, fix failures, update docs
Phase 3  Review          Gemini for structural review, Claude for high-risk logic/security review
Phase 4  Quality Gate    Lint, test, build, E2E/type gates, secret scan, worklog/doc updates
Phase 5  Push + Ops      Push intentionally, run parity/health checks, let async maintenance tools help
```

## Project Structure

```text
├── README.md
├── WORKLOG.md
├── scripts/
│   ├── review-diff.sh
│   └── quality-gate.sh
├── templates/
│   ├── README.md
│   ├── AGENTS.template.md
│   ├── CLAUDE.template.md
│   ├── GEMINI.template.md
│   ├── CLAUDE.local.template.md
│   ├── PLAN.template.md
│   ├── WORKLOG.template.md
│   ├── DEBUG-JOURNAL.template.md
│   ├── TESTING_AND_BROWSER_AUTOMATION.template.md
│   ├── tasks.template.json
│   ├── knowledgebase/
│   ├── runbooks/
│   ├── plans/
│   ├── archetypes/
│   ├── .github/workflows/
│   ├── .claude/
│   ├── .cursor/
│   ├── .gemini/
│   └── .agents/skills/
├── workflow/
│   ├── Multi-Model-Workflow.md
│   ├── New-Project-Setup-Guide.md
│   ├── Repeatable-Actions-Stack.md
│   ├── Repo-Operating-System.md
│   ├── Worklog-2.0.md
│   ├── Browser-QA-Playbook.md
│   ├── AI-First-Service-Setup-and-Login-Handoff.md
│   ├── Cursor-Workflow-Guide.md
│   ├── Gemini-CLI-Workflow-Guide.md
│   ├── Environment-Parity-and-Prod-Safety.md
│   ├── Schema-Sync-Recipes.md
│   ├── Donor-Repo-Adaptation-Guide.md
│   ├── Runbook-Patterns.md
│   ├── Starter-Kits.md
│   ├── Dual-Plan-Workflow.md
│   ├── AI-QUALITY-GATE-SOP.md
│   ├── Quality-Gate-Profiles.md
│   ├── Failure-Playbooks.md
│   ├── Risk-Tier-Matrix.md
│   ├── Brownfield-Adoption-Guide.md
│   ├── Workflow-Metrics.md
│   ├── Source-Refresh-Policy.md
│   └── adjacent-tools/
├── metrics/
│   ├── Workflow-Scorecard.md
│   └── weekly-metrics.csv.template
└── research/
```

## How to Use

| Situation | Open This |
|---|---|
| Starting a new repo | `workflow/New-Project-Setup-Guide.md` + `workflow/Starter-Kits.md` |
| Setting up DB / Vercel / login handoff | `workflow/AI-First-Service-Setup-and-Login-Handoff.md` |
| Designing repeatable commands, skills, hooks, or automations | `workflow/Repeatable-Actions-Stack.md` |
| Setting up Cursor rules, commands, and Bugbot | `workflow/Cursor-Workflow-Guide.md` |
| Setting up Gemini CLI context, commands, hooks, and skills | `workflow/Gemini-CLI-Workflow-Guide.md` |
| Designing the repo operating system | `workflow/Repo-Operating-System.md` |
| Setting up core templates | `templates/README.md` |
| Planning a non-trivial feature | `workflow/Dual-Plan-Workflow.md` + `templates/plans/README.md` |
| Writing better worklogs | `workflow/Worklog-2.0.md` + `templates/WORKLOG.template.md` |
| Setting up browser QA | `workflow/Browser-QA-Playbook.md` + `templates/TESTING_AND_BROWSER_AUTOMATION.template.md` |
| Hardening prod/dev safety | `workflow/Environment-Parity-and-Prod-Safety.md` |
| Handling schema changes safely | `workflow/Schema-Sync-Recipes.md` |
| Porting from an existing donor repo | `workflow/Donor-Repo-Adaptation-Guide.md` |
| Building operator docs/runbooks | `workflow/Runbook-Patterns.md` + `templates/runbooks/` |
| About to commit/push | `scripts/quality-gate.sh` + `workflow/AI-QUALITY-GATE-SOP.md` |
| Recovering from workflow drift | `workflow/Failure-Playbooks.md` |
| Tracking whether the process is helping | `metrics/Workflow-Scorecard.md` + `workflow/Workflow-Metrics.md` |

## Core Repo Assets Per Project

| Asset | Purpose |
|---|---|
| `README.md` | Current product truth, setup, key paths, known limitations |
| `WORKLOG.md` | Durable implementation/change memory |
| `CLAUDE.md` | Planner/reviewer context for Claude Code |
| `AGENTS.md` | Builder instructions for Codex |
| `GEMINI.md` | Gemini CLI context and reviewer/workflow instructions when Gemini is in the loop |
| `plans/active/` + `plans/archive/` | Decision history and execution source of truth |
| `DEBUG-JOURNAL.md` | Investigation memory for bugs, dead ends, and root causes |
| `TESTING_AND_BROWSER_AUTOMATION.md` | One-stop browser/testing quick reference |
| `knowledgebase/` | Stable business, architecture, and decision context for larger systems |
| `knowledgebase/10-implementation-checklist.md` | Project-level owner-tagged execution checklist and gate tracker |
| `runbooks/` | Operator-facing procedures for auth, onboarding, incidents, and service setup |
| `.cursor/commands/`, `.claude/commands/`, `.gemini/commands/`, `.agents/skills/` | Repeatable action surfaces that turn stable prompts into reusable workflow assets |

## Best-Fit Project Archetypes

This repo now includes starter kits for the project shapes you keep returning to:

- `analytics-warehouse` -- multi-tenant dashboards, modeled marts, tenant scoping, warehouse health
- `dual-stack-platform` -- Python/Next or similar split-stack apps with API/schema sync
- `internal-ops-dashboard` -- workflow-heavy internal tools with queues, smoke tests, and safe fallback behavior
- `ai-media-saas` -- AI generation products with queues, parity checks, background jobs, and operator controls
