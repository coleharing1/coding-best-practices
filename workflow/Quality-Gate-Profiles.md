# Quality Gate Profiles

> Stack-specific command profiles for Phase 4 quality gates.

Use this with `scripts/quality-gate.sh` by mapping each profile's commands to environment variables (`LINT_CMD`, `TEST_CMD`, `BUILD_CMD`, `E2E_CMD`, `TSC_CMD`).

---

## Profile Selection

1. Pick the profile closest to your project stack.
2. Set profile commands in your repo-level `AGENTS.md` and `CLAUDE.md`.
3. Run `scripts/quality-gate.sh` and override flags only when needed.

---

## 1) Node / Next.js / TypeScript

**Required Gates**
- `npm run lint`
- `npm run test -- --run`
- `npm run build`

**Conditional Gates**
- `PLAYWRIGHT_BASE_URL=http://127.0.0.1:3000 npm run test:e2e` when UI changes
- `npx tsc --noEmit` when schema/types/contracts change

**Suggested Env Mapping**

```bash
LINT_CMD="npm run lint"
TEST_CMD="npm run test -- --run"
BUILD_CMD="npm run build"
E2E_CMD="npm run test:e2e"
TSC_CMD="npx tsc --noEmit"
```

---

## 2) Python / FastAPI / Pytest

**Required Gates**
- `ruff check .`
- `pytest -q`
- `python -m compileall .`

**Conditional Gates**
- `pytest -m e2e -q` when API/UI integration paths change
- `mypy .` when typed contracts or models change

**Suggested Env Mapping**

```bash
LINT_CMD="ruff check ."
TEST_CMD="pytest -q"
BUILD_CMD="python -m compileall ."
E2E_CMD="pytest -m e2e -q"
TSC_CMD="mypy ."
```

---

## 3) Shopify Theme / Liquid + JS

**Required Gates**
- `npm run lint` (JS/CSS)
- `npm run test -- --run` (if test suite exists)
- `npm run build` (assets bundle)

**Conditional Gates**
- Theme check/lint (example): `shopify theme check`
- Playwright storefront smoke tests when templates/sections change

**Suggested Env Mapping**

```bash
LINT_CMD="npm run lint"
TEST_CMD="npm run test -- --run"
BUILD_CMD="npm run build"
E2E_CMD="npm run test:e2e"
TSC_CMD="shopify theme check"
```

---

## 4) Monorepo (pnpm / turbo)

**Required Gates**
- `pnpm lint`
- `pnpm test`
- `pnpm build`

**Conditional Gates**
- `pnpm --filter <app> test:e2e` for affected UI apps
- `pnpm typecheck` for shared types/contracts

**Suggested Env Mapping**

```bash
LINT_CMD="pnpm lint"
TEST_CMD="pnpm test"
BUILD_CMD="pnpm build"
E2E_CMD="pnpm --filter web test:e2e"
TSC_CMD="pnpm typecheck"
```

---

## 5) Minimal Script-Only Project

**Required Gates**
- `shellcheck scripts/*.sh` (if shell-heavy)
- Project-specific smoke test command
- Packaging/build command if applicable

**Conditional Gates**
- Integration smoke scripts against known fixtures

**Suggested Env Mapping**

```bash
LINT_CMD="shellcheck scripts/*.sh"
TEST_CMD="./scripts/test-smoke.sh"
BUILD_CMD="./scripts/build-check.sh"
E2E_CMD="./scripts/test-integration.sh"
TSC_CMD="echo 'No type gate for this profile'"
```

---

## Guardrails

- Keep required gates deterministic and fast enough for every commit.
- Move slow/expensive checks to CI only when they block daily flow.
- If you skip a conditional gate, document why in handoff or worklog.
