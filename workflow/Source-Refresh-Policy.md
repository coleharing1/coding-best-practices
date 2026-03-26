# Source Refresh Policy

> Last updated: February 25, 2026
> Role in workflow: Prevent stale guidance in this knowledge base

---

## Goal

This project references fast-moving tools, pricing, and benchmarks. This policy ensures docs remain accurate and clearly timestamped.

---

## Refresh Cadence

1. Monthly refresh (required)
- Run once per month in the first week.

2. Event-driven refresh (required)
- Refresh immediately after major product releases that affect your workflow:
  - Claude Code model/access/limits changes
  - Codex desktop/CLI policy or benchmark changes
  - Gemini CLI model, pricing, or context changes
  - Cursor/Jules workflow feature changes

3. Quarterly cleanup (recommended)
- Archive or rewrite docs that no longer influence real decisions.

---

## Source of Truth Rules

1. Prefer official docs/changelogs for product behavior, pricing, and limits.
2. Use community posts (Reddit/X/blogs) for workflow patterns, not hard product facts.
3. Every workflow doc with changing facts must include:
- `Last updated` date
- explicit date scope in claims (e.g., "as of February 2026")

---

## Refresh Checklist

For each monthly refresh, verify:

1. Models and plans
- Tool availability and plan names
- Usage limits / pricing assumptions

2. Commands and scripts
- CLI commands still valid
- Flags/options unchanged

3. Benchmarks and stats
- Keep only decision-relevant benchmark claims
- Remove stale leaderboard details if they no longer guide choices

4. Integrations
- MCP setup still correct
- GitHub Action references still valid

5. Docs consistency
- `README.md` file tree matches actual files
- cross-links between workflow docs are still valid

---

## Update Procedure

1. Create a dedicated docs branch.
2. Update affected docs in one pass:
- `README.md`
- `workflow/*.md`
- `research/*.md` (if source notes changed)

3. In each updated file:
- bump `Last updated`
- adjust date-sensitive claims

4. Add one `WORKLOG.md` entry in this repo (if you keep one) or your active governance doc elsewhere.

5. Run link and structure sanity checks (manual or script).

---

## Deprecation Policy

When a doc is no longer current but still useful historically:
1. Add a top banner: `Status: Archived`.
2. Keep the original date context.
3. Link to the replacement doc.

Do not silently delete material that informs past decisions.

---

## Ownership

Default owner: you (project maintainer).

If delegated, assign one "doc owner" per area:
- Workflow docs
- Research summaries
- Scripts/templates

Ownership must be explicit; stale docs happen when ownership is ambiguous.
