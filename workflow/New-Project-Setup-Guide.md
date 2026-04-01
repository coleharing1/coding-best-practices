# New Project Setup Guide

> Bootstrap a new repo so it behaves like a project with an operating system, not just a code folder.

## Goal

Start from the nearest proven shape, establish durable context immediately, and front-load the service setup that unlocks AI execution later.

## Step 1: Choose A Starter Kit

Before copying files, choose the closest archetype from `workflow/Starter-Kits.md`:

- analytics warehouse
- dual-stack platform
- internal ops dashboard
- AI media SaaS

## Step 2: Create The Minimum Repo OS

Copy these first:

1. `README.md`
2. `WORKLOG.md`
3. `CLAUDE.md`
4. `AGENTS.md`
5. `GEMINI.md` when Gemini CLI is part of the loop
6. `plans/`
7. `.cursor/rules/` and `.cursor/commands/` when Cursor is part of the loop
8. `.claude/commands/`, `.claude/rules/`, and `.claude/skills/` if Claude Code is part of the loop
9. `.gemini/commands/` and optional `.gemini/settings.json` if Gemini CLI is part of the loop
10. `.agents/skills/` when you want portable Codex/Gemini skills in-repo
11. `.env.local.example`

## Step 3: Front-Load AI-Accessible Service Setup

Before feature work, use `workflow/AI-First-Service-Setup-and-Login-Handoff.md` to set up:

- database project and direct AI-usable access
- Vercel project linking and env ownership
- browser QA path
- login/2FA handoff runbook

If the AI will need the service later, do not leave the repo in a "dashboard only" state.

## Step 4: Verify Real Commands

Do not leave placeholder commands in context files.

Record:

- lint command
- test command
- build command
- E2E/browser QA command
- typecheck/parity command
- direct DB or MCP access check when relevant

## Step 5: Encode The First Repeatable Actions

Before the repo gets busy, add the first reusable workflow files:

- one plan command
- one review command
- one browser-verify command when UI work is expected
- one service-bootstrap skill or command when startup is multi-step
- one or two rules/hooks for non-negotiable guardrails

Use `workflow/Repeatable-Actions-Stack.md`.

## Step 6: Add High-Value Operating Layers

Add these when they match the project:

- `DEBUG-JOURNAL.md`
- `TESTING_AND_BROWSER_AUTOMATION.md`
- `knowledgebase/`
- `knowledgebase/10-implementation-checklist.md`
- `runbooks/`
- `.github/workflows/`

## Step 7: Capture Baseline Reality

In `CLAUDE.md` and `AGENTS.md`, record:

- repo baseline checks
- high-risk paths
- current milestone
- production posture
- service bootstrap status
- preferred browser path

## Step 8: Make The First Worklog Entry

`Entry 001` should capture:

- what repo OS files were added
- what services were linked or authenticated
- what commands were verified
- what commands, skills, hooks, or rules were added
- any remaining human-only blockers

## Step 9: Create The Project Checklist

Add `knowledgebase/10-implementation-checklist.md` for larger projects.

Use owner tags such as:

- `[Cole]`
- `[Codex]`
- `[Claude]`
- `[Shared]`
- `[Gate]`

## Step 10: Pick The First Real Feature

Run one real feature through:

1. dual plan
2. final checklist synthesis
3. phase-by-phase build
4. review
5. quality gate
6. worklog update

## Good Setup Outcome

The repo is ready when:

- a new AI session can understand the project quickly
- commands are real
- docs describe current truth
- the AI can continue after your login step
- repeated workflows already have a home in commands, skills, rules, or hooks
- the next feature can start without re-explaining the repo from scratch
