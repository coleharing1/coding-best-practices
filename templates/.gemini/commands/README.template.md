# Gemini CLI Commands

Gemini CLI custom commands live in `.gemini/commands/` and use TOML files.

Recommended starter pack:

- `plan-feature.toml`
- `final-plan-checklist.toml`
- `browser-verify.toml`

Gemini CLI appends the raw invoked command to the prompt by default when you do not use explicit argument placeholders, so these templates are written to parse the appended command safely.

Use commands for invoked checklists. Use `.agents/skills/` when the workflow needs bundled scripts, files, or stronger specialization.
