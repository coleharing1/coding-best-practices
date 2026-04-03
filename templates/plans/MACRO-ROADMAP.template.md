# [Project Name] Macro Roadmap

> Permanent whole-project roadmap and checklist.
>
> Use this file for long-range direction and sequencing.
> Use `plans/active/Plan-XXX-Final.md` for the next buildable execution chunk.

## How To Use This File

1. Read this file when you need the whole-project picture or want to understand what comes after the current active plan.
2. Do not treat this file as the implementation source of truth for non-trivial work.
3. Pull the next actionable cluster into the normal numbered planning flow in `plans/active/`.
4. Implement from `Plan-XXX-Final.md`, not directly from the macro roadmap.
5. Every non-trivial numbered plan should include a `Macro Roadmap Alignment` section that cites the roadmap IDs it advances or changes.
6. When a numbered plan lands, update this roadmap, `WORKLOG.md`, and any affected docs.

## Maintenance Rules

- Update this file when whole-project sequencing, phase status, durable assumptions, or likely-next work changes.
- Keep this file strategic and durable. Put build-sized execution detail in `plans/active/Plan-XXX-Final.md`.
- If repo reality and this roadmap drift apart, update the roadmap before handoff instead of leaving the mismatch implicit.

## Roadmap Status Legend

- `Complete` means the phase is landed and no longer the active focus.
- `Mostly complete` means the foundation is real but notable gaps remain.
- `In progress` means the phase is an active supporting track with ongoing work.
- `Next` means it is the next major product phase to promote into the numbered planning flow.
- `Not started by design` means it is intentionally deferred until earlier foundations are explicit.
- `Later` means it is downstream and should not be pulled forward casually.

## Source Inputs For This Roadmap

This macro roadmap is synthesized from:

- current repo reality in `README.md`, `knowledgebase/`, `runbooks/`, `WORKLOG.md`, and the live codebase
- the active numbered plan in `plans/active/`
- completed plan history in `plans/archive/`
- durable project-level checkpoints in `knowledgebase/10-implementation-checklist.md` when present
- older project specs, research notes, and user direction that still matter

## Durable Decisions Carried Forward

- [decision that should survive many sessions]
- [architectural or business constraint]
- [deployment or safety posture]

## Current Status Snapshot

As of [date], [Project Name] is currently:

- [what is already real]
- [what maturity the project has reached]
- [what the biggest remaining gaps are]

## Macro Roadmap

Rename, merge, or split these phases to fit the project. The important part is preserving stable roadmap IDs and whole-project sequencing.

### MR-0 — Repo Operating System And Service Bootstrap

Status: [Complete / In progress / Next]

- [ ] Add the root workflow system, verified commands, and core context files
- [ ] Front-load hosted-service setup and browser/login handoff
- [ ] Make the repo easy to rehydrate in a fresh session

Exit criteria:

- the repo can be understood quickly from root docs
- commands and startup flows are real and verified

### MR-1 — Core Source Of Truth And Data Foundations

Status: [Mostly complete / In progress / Next]

- [ ] Define the real source-of-truth hierarchy
- [ ] Harden the primary ingestion or sync path
- [ ] Make freshness and provenance understandable to operators

Exit criteria:

- the team can explain where current truth comes from and how fresh it is

### MR-2 — First Usable Workflow Surface

Status: [Mostly complete / In progress / Next]

- [ ] Deliver the core user or operator workflow in the product
- [ ] Make the main path obvious without outside explanation
- [ ] Expose blockers, status, and manual controls where needed

Exit criteria:

- the primary journey is visible in the product, not only in docs

### MR-3 — Core Execution Loop Hardening

Status: [Next]

- [ ] Make the real execution or publish path explicit
- [ ] Track lifecycle state, auditability, and rollback expectations
- [ ] Reduce reliance on undocumented operator habits

Exit criteria:

- a real end-to-end workflow can be run with clear auditability and rollback

### MR-4 — Evidence, Durability, And Learnings

Status: [In progress / Later]

- [ ] Link outcomes back to exact inputs and evidence
- [ ] Track confidence, regression, and longer-term durability
- [ ] Surface reusable learnings and patterns

Exit criteria:

- the system can explain what it believes and what evidence supports it

### MR-5 — Testing, Verification, And Operational Confidence

Status: [In progress]

- [ ] Define the minimum verification bar
- [ ] Add browser or end-to-end coverage for the highest-value flows
- [ ] Capture durable investigation knowledge when incidents happen

Exit criteria:

- meaningful changes have a trusted verification path

### MR-6 — Auth, Deploy Posture, And Remote Ops Safety

Status: [Not started by design / Later]

- [ ] Decide where the system runs and who can access it
- [ ] Define read/write safety rules for remote environments
- [ ] Add release, rollback, and parity expectations only after the posture is explicit

Exit criteria:

- the team can clearly state where the app runs and what write rules apply

### MR-7 — Intelligence, Automation, Or Expansion

Status: [Later]

- [ ] Add heavier intelligence or automation only after the operator loop is mature
- [ ] Keep automation reviewable, attributable, and reversible
- [ ] Expand carefully based on real workflow needs, not novelty

Exit criteria:

- any automation is earned by operational reliability, not used to replace it

## Current Active Plan Alignment

Current active numbered plan: `[plans/active/Plan-XXX-Final.md or none yet]`

That plan primarily advances:

- `[MR-*]` [what it advances]
- `[MR-*]` [what it advances]

Macro roadmap sync:

- [whether the current active plan changed whole-project sequencing or not]

## Likely Next Numbered Plan Candidates

These are strong candidates for future `Plan-XXX-*` work, but they are not source of truth until promoted into `plans/active/`.

1. `[MR-*]` [next likely build chunk]
2. `[MR-*]` [next likely build chunk]
3. `[MR-*]` [next likely build chunk]

## End-State Definition

[Project Name] is "macro complete" when it is:

- [what success looks like at the whole-project level]
- [what operational maturity should exist]
- [what safety or durability bar should be met]
