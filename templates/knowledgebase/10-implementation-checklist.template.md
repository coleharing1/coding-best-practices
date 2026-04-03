# 10. Implementation Checklist

> Use this alongside `plans/MACRO-ROADMAP.md` for project-level execution order, owner tags, and blocking gates.

## Working Assumptions

- [business or product assumption]
- [data or auth assumption]
- [deployment assumption]

## How To Use This Checklist

- Check `plans/MACRO-ROADMAP.md` first for the whole-project sequence and current likely-next work.
- Use this file for durable gates and cross-cutting execution checkpoints that support that roadmap.
- Work in order unless an item is explicitly marked optional.
- Do not start later phases before their gates are complete.
- When a major phase starts, create or refresh the active plan set in `plans/active/`.
- When a major phase ends, update `plans/MACRO-ROADMAP.md`, `WORKLOG.md`, `README.md`, and any affected runbooks.

## Ownership Legend

- `[Cole]` means human-only login, credentials, approval, or business decision.
- `[Codex]` means repo work, terminal work, testing, and documentation.
- `[Claude]` means planning, synthesis, or high-risk review.
- `[Shared]` means the AI can prepare most of it but still needs one human step.
- `[Gate]` means later work should not start until the item is complete.

## Blocking Gates

| Gate | Must Be Complete Before | Required Outcome |
| --- | --- | --- |
| Gate 0 | Feature implementation | Repo operating system and real commands are in place |
| Gate 1 | Real data modeling or remote auth work | Cloud service setup is linked locally and verified |
| Gate 2 | Browser-heavy or user-facing QA | Preferred user lane and agent lane are documented |

## Phase 0: Repo Operating System

### 0A. Repo Rules And Memory

- [ ] `[Codex]` Add `README.md`, `WORKLOG.md`, `CLAUDE.md`, and `AGENTS.md`
- [ ] `[Codex]` Add `plans/active/` and `plans/archive/`
- [ ] `[Codex]` Add `.cursor/rules/` and `.claude/commands/` / `.claude/rules/` if relevant
- [ ] `[Codex]` Add `.env.local.example`

### 0B. Workflow Conventions

- [ ] `[Shared] [Gate 0]` Confirm dual-plan workflow for non-trivial work
- [ ] `[Shared] [Gate 0]` Confirm quality-gate commands
- [ ] `[Shared] [Gate 0]` Confirm browser QA posture

### Phase 0 Verification

- [ ] `[Codex] [Gate 0]` A new session can understand the repo quickly
- [ ] `[Codex] [Gate 0]` Commands in context files are real

## Phase 1: AI-Accessible Service Bootstrap

### 1A. Database And Auth

- [ ] `[Cole]` Log in or create the hosted database/auth project
- [ ] `[Codex]` Add config, migrations, env template, and DB tooling files
- [ ] `[Shared]` Capture URL, public key, admin key, pooled URL, and direct URL
- [ ] `[Codex] [Gate 1]` Verify direct DB access or MCP access actually works

### 1B. Hosting / Vercel

- [ ] `[Cole]` Complete Vercel or hosting auth if the CLI/browser requires it
- [ ] `[Codex]` Link the project locally and document project/team IDs
- [ ] `[Codex]` Document required env vars and their value sources

### 1C. Browser QA

- [ ] `[Shared] [Gate 2]` Decide the preferred user lane and agent lane
- [ ] `[Codex]` Add `TESTING_AND_BROWSER_AUTOMATION.md`
- [ ] `[Codex]` Add a service handoff runbook if browser login is part of setup

### Phase 1 Verification

- [ ] `[Codex] [Gate 1]` The AI can continue work after the human login step
- [ ] `[Codex] [Gate 2]` Browser QA path is documented and runnable

## Phase 2: Backbone And First Usable Surface

- [ ] `[Codex]` [task]
- [ ] `[Shared]` [task]
- [ ] `[Claude]` [high-risk review or synthesis task]

## Phase 3: Reliability And Operations

- [ ] `[Codex]` Add parity, health-check, or migration safety workflows
- [ ] `[Codex]` Add runbooks for onboarding, incidents, or service setup
- [ ] `[Gemini]` Review high-risk diffs structurally when needed
