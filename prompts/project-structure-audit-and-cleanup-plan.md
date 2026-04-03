You are working inside `[PROJECT_NAME]`.

Your job is to do a deep structural audit of this entire project so we can clean up the repo layout for the current stage of the product.

Do not make any file moves or edits yet.
Phase 1 is research, classification, and recommendations only.

## Goal

Understand the full evolution of this repo, then recommend how to clean up and modernize the folder structure so the project is easier to navigate and build on going forward.

I want you to think specifically about:

- what is current and should stay prominent
- what is old but still valuable and should be archived
- what is redundant and should be merged or removed
- what folders or files should move
- what new folders or structure should exist now
- what generated, local-only, or runtime artifacts should be ignored and not treated as part of the real project structure

## Project-specific placeholders to fill before use

Replace these placeholders if they help the audit:

- `[PROJECT_NAME]`
- `[PRIMARY_APP_FOLDER if applicable]`
- `[SECONDARY_APP_OR_PACKAGE_FOLDERS if applicable]`
- `[KNOWN_OLDER_OR_HISTORICAL_FOLDERS if applicable]`
- `[KNOWN_DOCS_OR_WORKFLOW_FOLDERS if applicable]`
- `[OTHER_NOTES_ABOUT_CURRENT_PROJECT_STAGE if applicable]`

If a placeholder does not apply, remove it instead of forcing it into the prompt.

## Phase 1: Deep project audit

Read the project carefully to understand:

- what the product does today
- current product maturity and development posture
- what the active source of truth is
- how the repo appears to have evolved over time
- which docs are current vs historical
- which folders are core vs support vs legacy
- which files are duplicated, overlapping, or outdated
- where the current folder structure creates confusion or drag

### Start with the core repo-operating files first

Read these when present:

- `README.md`
- `WORKLOG.md`
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PLAN.md`
- `DEBUG-JOURNAL.md`
- `TESTING_AND_BROWSER_AUTOMATION.md`
- `plans/`
- `knowledgebase/`
- `runbooks/`
- `docs/`
- `specs/`
- `research/`
- `archive/`

Also inspect any platform and workflow surfaces when present:

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
- browser or Playwright config

### Then audit the full structure

Deep dive:

- all root folders
- all important markdown files
- the main app and package structure
- supporting docs folders
- scripts and workflow automation
- any research, planning, or historical folders
- any generated, local, cache, or build folders that should be classified separately from the real repo structure

Also inspect enough of the codebase to understand the real app boundaries:

- where the actual product code lives
- backend, frontend, worker, or package boundaries
- where product logic lives
- where docs directly support the live code vs reflect older project phases

Use fast repo inspection first, then read the most important files in depth.

## Phase 2: Classify everything

Classify the repo into categories.

For every important folder or file group, determine whether it is:

- **Core current structure** — should stay and maybe be made more prominent
- **Current but misplaced** — should move somewhere else
- **Historical but worth keeping** — should be archived into a clearer location
- **Redundant or overlapping** — should be merged or consolidated
- **Generated, local-only, or runtime-only** — should not drive repo structure decisions
- **Suspicious or unclear** — needs a recommendation or follow-up question

Be especially thoughtful about:

- older research folders
- old overview or planning docs
- duplicate docs across root and app subfolders
- old workflow files that may have been superseded
- whether historical planning or research should move into an archive area
- whether the main app layout is already fine and the real problem is only at the root level
- whether docs should be split into current product docs, workflow/repo docs, and historical material

## Phase 3: Recommend a cleaner target structure

After the audit, propose a cleaner target project structure for this repo as it exists today.

Your recommendation should cover:

- what the ideal root folder structure should be now
- what should remain at the root
- what should move into `archive/`, `history/`, or another dedicated historical area
- whether root docs should be consolidated
- whether docs need clearer boundaries between current product docs, repo workflow docs, and historical material
- whether there should be clearer separation between app code, repo operations, and historical context
- whether any new folders should exist for clarity

## Output requirements

Do not make changes yet.

Report back in chat with these sections:

### 1. Current Structure Assessment

Summarize:

- what the current structure is trying to do
- what is already good
- what is messy, mixed, or confusing
- what the biggest structural problems are

### 2. Evolution Read

Explain your understanding of how the repo evolved over time.
I want to know:

- what appears to be older project setup
- what appears to be newer operating-system structure
- what appears to be the current source of truth
- where older layers are still hanging around in ways that create confusion

### 3. Classification Map

Break the repo into categories:

- keep as core
- move
- archive
- merge or consolidate
- generated or local-only
- unclear or needs decision

Use real file and folder references.

### 4. Recommended Target Structure

Show the folder structure you recommend now.
Use a tree-style layout when helpful.

### 5. Recommended Changes

List the specific changes you think should happen.

For each recommendation, include:

- **Change**
- **Why**
- **Benefit**
- **Risk**
- **Suggested destination**
- **Whether it should be done now or later**

### 6. Archive Plan

Specifically call out:

- what should be archived
- where it should go
- why it should not stay in the active top-level structure

### 7. Things You Would Not Move

Tell me what you think should stay exactly where it is, and why.

### 8. Suggested Execution Plan

Give me a phased cleanup plan:

- Phase 1 = safest, highest-value structural cleanup
- Phase 2 = deeper consolidation
- Phase 3 = optional polish

## Important instructions

- Be concrete and opinionated.
- Use real file and folder references from this repo.
- Do not be generic in the analysis.
- Do not reorganize based on theory alone. Base it on the actual current repo.
- Distinguish between versioned project structure and local, generated, or runtime artifacts.
- Do not propose moving secrets or credential files into git-tracked locations.
- Do not make changes yet.
- Do not stop after reading only the README and worklog.
- Think like a senior engineer cleaning up a mature but layered repo that has grown through multiple phases.

When your audit is complete, stop and wait for approval before making any structural changes.
