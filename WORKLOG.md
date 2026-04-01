# Work Log

A lightweight running log of meaningful changes in this repo. This captures intent, decisions, and follow-ups that commit history alone will not preserve.

---

## Entry format rules

- Use entry numbers (`Entry 001`, `Entry 002`, ...).
- Keep entries in reverse chronological order (newest at top).
- Use one entry per logical unit of work.
- Include real file paths in `Changes`.

### Entry 004 -- Repo Dogfooding + Platform Guide Polish

- **Goal**: Finish the repo's "final pass" by making it dogfood its own workflow more directly and by giving Cursor and Gemini the same practical treatment Claude already had.
- **Changes**:
  - `.github/workflows/repo-self-check.yml`, `scripts/validate_repo.py` -- added a lightweight self-check workflow so the repo can validate its own docs/template structure, JSON/TOML files, and canonical-path expectations.
  - `workflow/Cursor-Workflow-Guide.md`, `workflow/Gemini-CLI-Workflow-Guide.md` -- added platform guides for Cursor and Gemini CLI to match the practical folder-usage style of the Claude guide.
  - `templates/.cursor/BUGBOT.template.md` -- added an explicit Cursor review-config template so bug review can be shaped as a first-class workflow surface.
  - `templates/.agents/skills/browser-verify/*`, `templates/.agents/skills/quality-gate/*` -- expanded the portable skill layer so service bootstrap is no longer the only reusable Codex/Gemini skill starter.
  - `prompts/README.md`, `README.md`, `templates/README.md` -- updated navigation so prompts are now clearly framed as one layer in the larger command/skill/hook stack.
- **Notes / decisions**:
  - I did not add a full golden example repo in this pass because that would be a separate mini-project; the highest ROI here was to strengthen the reusable system itself.
  - The repo now has a much better "practice what it preaches" posture without turning the reference library into a giant sample app.

### Entry 003 -- Repeatable Actions + Gemini/Cursor Workflow Upgrade

- **Goal**: Capture the newer April 1, 2026 cross-platform workflow patterns for commands, skills, hooks, rules, automations, and browser-login handoff so the repo better matches how modern agent tooling is actually being used.
- **Changes**:
  - `workflow/Repeatable-Actions-Stack.md` -- added a new guide for the prompt -> command -> skill -> hook/rule -> automation ladder, with platform mapping across Codex, Claude Code, Cursor, Gemini CLI, and Antigravity.
  - `workflow/Multi-Model-Workflow.md`, `workflow/New-Project-Setup-Guide.md`, `workflow/AI-First-Service-Setup-and-Login-Handoff.md` -- updated the core startup docs so they explicitly encode repeatable actions early and distinguish Gemini CLI's local workflow layer from Antigravity's browser-heavy operator role.
  - `README.md`, `templates/README.md`, `templates/AGENTS.template.md`, `templates/CLAUDE.template.md` -- pushed the portable repeatable-actions taxonomy into the main repo overview and canonical templates.
  - `templates/GEMINI.template.md`, `templates/.gemini/*`, `templates/.cursor/commands/*`, `templates/.agents/skills/*` -- added missing template scaffolding for Gemini CLI context/commands, Cursor commands, and portable Codex/Gemini skills.
  - `workflow/Workflow-Metrics.md`, `metrics/Workflow-Scorecard.md`, `templates/weekly-retro.md` -- upgraded the weekly measurement loop to track workflow-asset promotion and dashboard round-trips, not just speed/quality.
- **Notes / decisions**:
  - The preferred promotion ladder is now explicit: prompt -> command -> skill -> hook/rule -> automation.
  - Gemini CLI is now treated as more than a cheap reviewer. It is also a strong local commands/skills/hooks platform.
  - Antigravity remains the best fit when the browser itself is the work surface and the agent should resume after your login step.

### Entry 002 -- Startup Handoff + Checklist Planning Upgrade

- **Goal**: Capture the newer project-start habits showing up in live repos: front-loading service setup so the AI can keep moving after a browser login, and turning Final plans into owner-tagged checklists with gates.
- **Changes**:
  - `workflow/AI-First-Service-Setup-and-Login-Handoff.md` -- added the service bootstrap pattern for database, Vercel, browser QA, and platform-specific login handoff across Codex, Claude Code, Cursor, and Antigravity.
  - `workflow/New-Project-Setup-Guide.md`, `workflow/Browser-QA-Playbook.md`, `workflow/Repo-Operating-System.md`, `workflow/Brownfield-Adoption-Guide.md` -- updated the startup docs so they explicitly front-load service access, browser lanes, and owner-tagged project checklists.
  - `workflow/Multi-Model-Workflow.md`, `workflow/Dual-Plan-Workflow.md`, `templates/plans/README.md` -- rewired the planning system around dual-plan synthesis into a Final checklist with owners and gates instead of loose `PLAN.md` prose.
  - `templates/PLAN.template.md`, `templates/knowledgebase/10-implementation-checklist.template.md`, `templates/tasks.template.json` -- upgraded the plan/checklist assets to match the Texas Fowlers style of ownership tags, blocking gates, and verification steps.
  - `templates/AGENTS.template.md`, `templates/CLAUDE.template.md`, `templates/TESTING_AND_BROWSER_AUTOMATION.template.md`, `templates/runbooks/service-setup-handoff.template.md`, `templates/.claude/rules/*`, `templates/.cursor/rules/*` -- pushed the browser handoff and service bootstrap expectations into the canonical reusable templates.
  - `prompts/plan-feature.md`, `prompts/codex-plan-feature.md`, `templates/.claude/commands/plan-feature.template.md`, `templates/.claude/commands/dual-plan.template.md`, `templates/.claude/commands/compare-plans.template.md` -- updated plan prompts and commands to request checklist plans with owner tags and explicit human-only steps.
- **Notes / decisions**:
  - The startup question is now: "what do we need to set up so the AI can keep going after my one login step?"
  - Cursor remains the main bootstrap control room, while Antigravity is now explicitly called out as a strong browser-first setup tool.
  - The Final plan format is now much closer to the TXF implementation-checklist style than the earlier narrative plan style.

### Entry 001 -- Repo Operating System Upgrade

- **Goal**: Evolve the `coding best practices` repo from a solid v1 into a fuller operating-system reference that better matches the patterns used in live projects like Coupler, Texas Fowlers OS, BanBox, LifeCurrent, Dropship, and Admatrix.
- **Changes**:
  - `README.md` -- rewrote the repo overview around canonical templates, starter kits, and the newer operations-oriented workflow.
  - `workflow/Repo-Operating-System.md`, `workflow/Worklog-2.0.md`, `workflow/Browser-QA-Playbook.md`, `workflow/Environment-Parity-and-Prod-Safety.md`, `workflow/Schema-Sync-Recipes.md`, `workflow/Donor-Repo-Adaptation-Guide.md`, `workflow/Runbook-Patterns.md`, `workflow/Mock-Mode-and-Fallbacks.md`, `workflow/Starter-Kits.md` -- added the missing higher-signal guides that now show up repeatedly in production repos.
  - `workflow/AI-QUALITY-GATE-SOP.md`, `workflow/Failure-Playbooks.md`, `workflow/Risk-Tier-Matrix.md`, `workflow/New-Project-Setup-Guide.md` -- refreshed core workflow docs so they point at the newer patterns instead of only the original v1 set.
  - `templates/AGENTS.template.md`, `templates/CLAUDE.template.md`, `templates/PLAN.template.md`, `templates/WORKLOG.template.md`, `templates/tasks.template.json`, `templates/README.md` -- upgraded the canonical templates to include repo baseline, high-risk paths, browser QA, parity, mock mode, and stronger worklog/verifications.
  - `templates/DEBUG-JOURNAL.template.md`, `templates/TESTING_AND_BROWSER_AUTOMATION.template.md`, `templates/knowledgebase/*`, `templates/runbooks/*`, `templates/.github/workflows/*`, `templates/archetypes/*` -- added reusable starter assets for knowledgebases, runbooks, CI, browser automation, and archetype-specific repo bootstraps.
  - `scripts/quality-gate.sh`, `scripts/review-diff.sh` -- tightened the generic automation scripts so they better reflect the current repo patterns used in live projects.
  - `templates/AGENTS.md`, `templates/CLAUDE.md`, `templates/PLAN.md`, `templates/WORKLOG.md`, `templates/.cursor/rules/000-core.mdc`, `templates/.cursor/rules/050-worklog.mdc` -- removed the duplicate lightweight template track so the repo has one clear canonical template set.
- **Notes / decisions**:
  - Canonical copy-ready assets now live in `*.template.*` files plus explicit archetype folders.
  - The repo now treats docs like a product surface, not background reference material.
  - Higher-signal operational assets won over generic placeholders because that is how the live repos actually behave.
- **Follow-ups**:
  - Add at least one example instantiated starter repo in a future pass if you want a fully copyable reference project.
  - Consider adding link-check or docs-lint automation if this repo starts changing more frequently.
