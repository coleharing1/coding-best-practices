# Coding Best Practices

> Personal knowledge base for how I (Cole Haring) use AI coding tools across projects. Not a codebase -- a reference library.

## The Workflow (TL;DR)

```
Phase 0  Cursor          Bootstrap project, paste research, connect GitHub, set up context files
Phase 1a Claude Code     /project:dual-plan → Claude writes Plan-XXX-CLAUDE.md
Phase 1b Codex           Same prompt → Codex writes Plan-XXX-Codex.md
Phase 1c Claude Code     /project:compare-plans → synthesize Plan-XXX-Final.md
Phase 1d You             Review and finalize the plan
  -> UI  Claude Code     For new apps: Opus writes the initial UI, Codex refines until the look is dialed in.
Phase 2  Codex           Implement from Plan-XXX-Final.md. One phase at a time, run tests, fix failures.
Phase 3  Gemini CLI      Pre-commit review. Pipe git diff to Gemini for architectural/structural feedback.
Phase 4  Quality Gate    Lint, test, build, E2E, secret scan, worklog update. No exceptions.
Phase 5  Jules           Push to GitHub. Scheduled agents run overnight. Review PRs each morning.
```

**Primary tools:** Claude Code Mac (Max) + Codex Mac (Max)
**Secondary:** Cursor (Ultra), Gemini CLI, Jules (free tier)

## Project Structure

```
├── README.md
├── scripts/                               # Automation scripts for review/gates
│   ├── review-diff.sh
│   └── quality-gate.sh
├── templates/                             # Copy-ready bootstrap templates
│   ├── WORKLOG.template.md
│   ├── CLAUDE.template.md
│   ├── CLAUDE.local.template.md           # Personal overrides (gitignored)
│   ├── AGENTS.template.md
│   ├── PLAN.template.md
│   ├── tasks.template.json
│   ├── plans/                             # Dual-plan workflow templates
│   │   ├── active/                        #   Current feature plans
│   │   ├── archive/                       #   Completed plans (decision history)
│   │   └── README.md                      #   Dual-plan workflow quick reference
│   ├── .claude/                           # Claude Code folder templates
│   │   ├── settings.template.json         #   Permissions (allow/deny)
│   │   ├── commands/                      #   Custom slash commands
│   │   │   ├── review.template.md         #     /project:review
│   │   │   ├── fix-issue.template.md      #     /project:fix-issue
│   │   │   ├── dual-plan.template.md      #     /project:dual-plan
│   │   │   ├── compare-plans.template.md  #     /project:compare-plans
│   │   │   ├── archive-plan.template.md   #     /project:archive-plan
│   │   │   ├── plan-feature.template.md   #     /project:plan-feature
│   │   │   ├── quality-gate.template.md   #     /project:quality-gate
│   │   │   └── codex-handoff.template.md  #     /project:codex-handoff
│   │   ├── rules/                         #   Modular path-scoped instructions
│   │   │   ├── code-style.template.md
│   │   │   ├── testing.template.md
│   │   │   ├── api-conventions.template.md
│   │   │   └── security.template.md
│   │   ├── skills/                        #   Auto-invoked workflows
│   │   │   ├── security-review/
│   │   │   └── deploy/
│   │   └── agents/                        #   Specialized subagent personas
│   │       ├── code-reviewer.template.md
│   │       └── security-auditor.template.md
│   └── .cursor/rules/*.template.mdc
├── metrics/
│   └── Workflow-Scorecard.md
├── workflow/                              # Core workflow playbooks
│   ├── Multi-Model-Workflow.md
│   ├── New-Project-Setup-Guide.md
│   ├── Claude-Code-Folder-Guide.md       # .claude/ folder anatomy & setup
│   ├── Dual-Plan-Workflow.md             # Competing plans from Claude + Codex
│   ├── AI-QUALITY-GATE-SOP.md
│   ├── Quality-Gate-Profiles.md
│   ├── Failure-Playbooks.md
│   ├── Jules-Setup-Guide.md
│   ├── Brownfield-Adoption-Guide.md
│   ├── Workflow-Metrics.md
│   ├── Risk-Tier-Matrix.md
│   ├── Source-Refresh-Policy.md
│   └── adjacent-tools/
│       └── nano-banana-pro-mcp-guide.md  # Optional/non-core tool guide
└── research/                              # Inputs that informed the workflow
    ├── Research-1.md
    ├── Research-2-Multi-Model-Vibe-Coding.md
    ├── Gemini-R2-Opinion.md
    └── Grok4.2-R2-Opinion.md
```

## How to Use

| Situation | Open This |
|---|---|
| Starting a new project | `workflow/New-Project-Setup-Guide.md` + `templates/README.md` |
| Setting up .claude/ folder | `workflow/Claude-Code-Folder-Guide.md` + `templates/.claude/` |
| Planning a new feature | `workflow/Dual-Plan-Workflow.md` + `templates/plans/` |
| Day-to-day "which tool do I use?" | `workflow/Multi-Model-Workflow.md` |
| About to commit/push | `scripts/quality-gate.sh` + `workflow/AI-QUALITY-GATE-SOP.md` |
| Different stack (not standard npm flow) | `workflow/Quality-Gate-Profiles.md` |
| If a workflow failure happens | `workflow/Failure-Playbooks.md` |
| Setting up Jules on a repo | `workflow/Jules-Setup-Guide.md` |
| Adopting this in an existing repo | `workflow/Brownfield-Adoption-Guide.md` |
| Tracking process quality over time | `metrics/Workflow-Scorecard.md` + `workflow/Workflow-Metrics.md` |
| Researching tools or approaches | `research/` folder |
| Optional adjacent tooling | `workflow/adjacent-tools/` |

## Context Files Created Per Project

| File | Read By | Purpose |
|---|---|---|
| `WORKLOG.md` | All tools | Reverse-chronological change log with intent, decisions, follow-ups |
| `CLAUDE.md` | Claude Code | Persistent project memory -- stack, rules, workflow role |
| `CLAUDE.local.md` | Claude Code | Personal overrides (gitignored) |
| `.claude/settings.json` | Claude Code | Permission allow/deny rules |
| `.claude/commands/` | Claude Code | Custom slash commands (review, plan, gate, fix-issue, codex-handoff) |
| `.claude/rules/` | Claude Code | Modular, path-scoped instruction files |
| `.claude/skills/` | Claude Code | Auto-invoked workflows (security review, deploy checklist) |
| `.claude/agents/` | Claude Code | Specialized subagent personas (code reviewer, security auditor) |
| `AGENTS.md` | Codex | Builder instructions -- commands, constraints, role |
| `.cursor/rules/000-core.mdc` | Cursor | Project identity and global constraints |
| `.cursor/rules/050-worklog.mdc` | Cursor | Enforce worklog discipline |
| `plans/active/` | Claude Code, Codex | Competing plans (CLAUDE + Codex) and synthesized Final plan |
| `plans/archive/` | Everyone | Completed plan sets — decision history, never delete |
| `tasks.json` | Claude Code, Codex | Optional task queue for phased implementation |
