# Claude Rules -- [Project Name]

## Stack

- **Framework**: [Framework + version]
- **Language**: [TypeScript strict / Python / etc.]
- **Styling**: [Tailwind / CSS Modules / etc.]
- **Database**: [Supabase / Neon / Postgres / etc.]
- **Deployment**: [Vercel / Cloudflare / AWS / etc.]

## Workflow Role

- You (Claude Code) are the planner, architect, and high-risk reviewer.
- Use `/project:dual-plan [feature]` to write your competing plan to `plans/active/`.
- Codex independently writes its own plan from the same prompt.
- Use `/project:compare-plans` to read both plans, compare, and synthesize a Final plan.
- The Final plan (`plans/active/Plan-XXX-Final.md`) is what Codex implements.
- Use `/project:archive-plan` after implementation to move plans to `plans/archive/`.
- For high-risk diffs (auth, payments, schema), run security/logic audits before merge.

## Rules

- Provide complete, working code with no placeholders.
- Search existing patterns before creating new abstractions.
- Prefer functional/declarative patterns; avoid classes unless required.
- Prefer explicit, actionable errors over silent fallbacks.
- Avoid `any` when feasible; keep boundaries typed.
- Keep files under 500 lines when practical; split modules as needed.
- Update `WORKLOG.md` after meaningful behavior or architecture changes.

## Safety

- Never run destructive git or shell commands without explicit approval.
- Never commit secrets, `.env*`, private keys, or credential files.
- Never modify production config directly without a clear change request.

## Commands

- `npm run dev` -- start local development
- `npm run lint` -- lint checks
- `npm run test -- --run` -- unit/integration tests
- `npm run build` -- production build validation
- `scripts/quality-gate.sh` -- full pre-commit gate

## Current State

- [Add active branch, major constraints, and current milestone]
