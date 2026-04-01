# Work Log

A lightweight running log of what changed in this repo over time. Use this to preserve intent, decisions, and follow-ups that commits do not fully capture.

---

## Entry format rules

- Use entry numbers (`Entry 001`, `Entry 002`, ...).
- Keep entries in reverse order (newest first).
- Use one entry per logical unit of work.
- Include real file paths in `Changes`.
- Include a `Verification` section when the work changed behavior, contracts, automation, or infrastructure assumptions.

### Entry 001 -- Initial Project Setup

- **Goal**: Bootstrap [Project Name] with shared AI workflow context files and the first linked service/setup paths.
- **Changes**:
  - `README.md` -- added project overview and setup commands
  - `WORKLOG.md` -- created worklog format and first entry
  - `CLAUDE.md` -- added planning/architecture context for Claude Code
  - `AGENTS.md` -- added implementation constraints for Codex
  - `.cursor/rules/` -- added repo-specific Cursor guidance
  - `.claude/commands/` and `.claude/rules/` -- added Claude Code workflow hooks
  - `.env.local.example` -- documented environment variable names and value sources
- **Notes / decisions**:
  - Workflow: Claude Code (plan) -> Codex (build) -> Gemini (review) -> Jules (maintenance)
  - Service setup uses the browser handoff pattern: AI opens the page, user logs in, AI finishes the rest
- **Verification**:
  - `npm run lint` -- [pass/fail]
  - `npm run build` -- [pass/fail]
- **Follow-ups**:
  - Define first feature plan in `plans/active/`
  - Add `knowledgebase/10-implementation-checklist.md` if the project is large enough
  - Add baseline tests and quality gate scripts

---

### Entry Template -- Copy This

- **Goal**:
- **Changes**:
  - `path/to/file` -- one-sentence summary
- **Notes / decisions**:
- **Verification**:
  - `[command]` -- [pass/fail or skipped + why]
- **Follow-ups**:
