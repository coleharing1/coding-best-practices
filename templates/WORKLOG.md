# Work Log

A lightweight running log of meaningful changes in this repo. This is for project continuity across sessions and tools.

---

## Entry format rules

- Use entry numbers (`Entry 001`, `Entry 002`, ...).
- Keep entries in reverse chronological order (newest at top).
- One entry per logical unit of work.

### Entry 001 — Initial Project Setup

- **Goal**: Bootstrap __PROJECT_NAME__ with workflow context and baseline conventions.
- **Changes**:
  - Created `README.md`, `WORKLOG.md`, `CLAUDE.md`, `AGENTS.md`
  - Added `.cursor/rules/000-core.mdc` and `.cursor/rules/050-worklog.mdc`
  - Documented stack and commands
- **Notes / decisions**:
  - Workflow: Claude (plan) -> Codex (build) -> Gemini (review) -> Quality Gate -> Push
- **Follow-ups**:
  - Add first feature plan to `PLAN.md`
  - Verify lint/test/build baseline

---

### Entry XXX — Short title

- **Goal**:
- **Changes**:
  - `path/to/file` — one-sentence summary
- **Notes / decisions**:
- **Follow-ups**:
