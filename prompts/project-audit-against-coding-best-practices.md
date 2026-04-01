You are working inside this project repo.

Your job is to deeply understand this project, then compare it against my reference repo at:

`/Users/coleharing/Cursor_Projects/coding best practices`

Do not make any code or doc changes yet. This phase is research, comparison, and recommendations only.

## Phase 1: Understand this project first

Read the project carefully to understand:

- what the product does
- current status / maturity
- stack and architecture
- how setup works
- how database access is handled
- how deploy / Vercel / env wiring is handled
- how browser testing / QA is handled
- how planning and execution are handled
- what AI workflow structure already exists
- where the project feels strong vs messy vs incomplete

Do not just read the README. Also inspect the files that shape how the repo actually works, including when present:

- `README.md`
- `WORKLOG.md`
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `plans/`
- `knowledgebase/`
- `runbooks/`
- `TESTING_AND_BROWSER_AUTOMATION.md`
- `DEBUG-JOURNAL.md`
- `.cursor/`
- `.claude/`
- `.gemini/`
- `.agents/skills/`
- `.github/workflows/`
- `scripts/`
- env templates
- package manifests
- DB config
- deployment config
- browser / Playwright config

Use fast repo inspection first, then read the most important files in depth.

## Phase 2: Deep dive the reference repo

Then do a deep dive of:

`/Users/coleharing/Cursor_Projects/coding best practices`

Learn how I like to run projects from it, especially around:

- repo operating system
- startup flow
- login handoff / browser handoff
- repeatable actions
- commands
- skills
- hooks / rules
- automations
- dual-plan workflow
- owner-tagged checklist plans
- quality gates
- worklog discipline
- browser QA
- mock mode
- schema sync
- prod safety
- runbooks
- Cursor / Claude / Codex / Gemini / Antigravity usage patterns

## Phase 3: Compare and think deeply

Based on what you learned from:

1. this project
2. the `coding best practices` repo
3. my overall vibe-coding style as reflected in repo structure and workflow files

figure out all the things this current project would benefit from.

I want you to think in terms of:

- improving vibe coding flow
- reducing re-explaining and repeated prompts
- making the AI more autonomous after one human login / approval step
- increasing speed without lowering quality
- improving planning clarity
- improving browser / DB / Vercel setup
- improving repeatable workflows
- improving review / verification / safety
- making context more durable across sessions

## Output requirements

Do not be generic.

Give me a detailed report in chat with these sections:

### 1. Current State Snapshot

Summarize:

- what this project already does well
- what workflow system it already has
- what feels missing or fragile
- biggest constraints or risks

### 2. Best Ideas To Add

List the specific things you think we should incorporate from `coding best practices`.

For each idea, include:

- **Idea**
- **Why it fits this project specifically**
- **Why it matches how I like to work**
- **Expected benefit**
- **Effort**: low / medium / high
- **Priority**: now / soon / later
- **Suggested files or areas to update**

### 3. Highest-ROI Changes

Give me the top changes you would do first if we only did a small first pass.

### 4. Gaps By Category

Break down recommendations by category:

- context / repo OS
- planning
- commands / skills / hooks / automations
- browser / login handoff
- database
- Vercel / deploy / envs
- testing / browser QA
- quality gate / review
- docs / worklog / runbooks
- prod safety / parity / schema sync

### 5. What Not To Add

Call out anything from `coding best practices` that you do NOT think belongs in this project yet, and why.

### 6. Suggested Rollout Plan

Give me a phased rollout:

- Phase 1 = easiest high-value wins
- Phase 2 = deeper workflow upgrades
- Phase 3 = nice-to-have polish

## Important instructions

- Be concrete and opinionated.
- Use real file references from this repo when possible.
- Reference exact files from `coding best practices` when helpful.
- Do not suggest changes that ignore this repo’s current architecture or maturity.
- Prefer practical workflow improvements over theoretical perfection.
- Do not edit files yet.
- Do not stop early after reading only a few files.
- Think like a senior engineer building a better operating system for this repo, based on how I actually like to work.

Once the audit is complete, report back in chat only and wait for my approval before making changes.
