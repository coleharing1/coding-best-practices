# Work Log

A lightweight running log of what changed in this repo over time. Use this to preserve intent, decisions, and follow-ups that commits do not fully capture.

---

## Entry format rules

- Use entry numbers (`Entry 001`, `Entry 002`, ...).
- Keep entries in reverse order (newest first).
- Use one entry per logical unit of work.
- Include real file paths in `Changes`.

### Entry 001 -- Initial Project Setup

- **Goal**: Bootstrap [Project Name] with shared AI workflow context files and core rules.
- **Changes**:
  - `README.md` -- added project overview and setup commands
  - `WORKLOG.md` -- created worklog format and first entry
  - `CLAUDE.md` -- added planning/architecture context for Claude Code
  - `AGENTS.md` -- added implementation constraints for Codex
  - `.cursor/rules/000-core.mdc` -- added global project constraints
  - `.cursor/rules/050-worklog.mdc` -- enforced worklog updates for meaningful changes
- **Notes / decisions**:
  - Workflow: Claude Code (plan) -> Codex (build) -> Gemini (review) -> Jules (maintenance)
- **Follow-ups**:
  - Define first feature plan in `PLAN.md`
  - Add baseline tests and quality gate scripts

---

### Entry Template -- Copy This

- **Goal**:
- **Changes**:
  - `path/to/file` -- one-sentence summary
- **Notes / decisions**:
- **Follow-ups**:
