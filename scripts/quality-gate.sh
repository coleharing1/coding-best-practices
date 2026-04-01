#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/quality-gate.sh [options]

Runs the AI quality gate in a deterministic order.

Options:
  --skip-review          Skip Gemini review step
  --skip-gemini          Alias for --skip-review
  --risk-tier TIER       Annotate the run as T0, T1, T2, or T3 (default: T1)
  --ui-changed           Force UI gate (E2E) on
  --types-changed        Force type gate (tsc --noEmit) on
  --base-url URL         Override PLAYWRIGHT_BASE_URL (default: http://127.0.0.1:3000)
  --help                 Show this help

Config via env vars (optional):
  LINT_CMD               Default: npm run lint
  TEST_CMD               Default: npm run test -- --run
  BUILD_CMD              Default: npm run build
  E2E_CMD                Default: npm run test:e2e
  TSC_CMD                Default: npx tsc --noEmit

Examples:
  scripts/quality-gate.sh
  scripts/quality-gate.sh --skip-review
  scripts/quality-gate.sh --ui-changed --base-url http://127.0.0.1:3002
USAGE
}

require_git_repo() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: this script must run inside a git repository." >&2
    exit 1
  fi
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

run_cmd() {
  local label="$1"
  local cmd="$2"
  echo
  echo "[$label] $cmd"
  bash -lc "$cmd"
}

collect_changed_files() {
  {
    git diff --name-only
    git diff --name-only --cached
  } | awk 'NF' | sort -u
}

matches_any() {
  local input="$1"
  shift
  local pattern
  for pattern in "$@"; do
    if [[ "$input" =~ $pattern ]]; then
      return 0
    fi
  done
  return 1
}

run_secret_scan() {
  local pattern='API_KEY|SECRET|TOKEN|PRIVATE KEY|BEGIN .*PRIVATE KEY|SERVICE_ROLE_KEY'
  local diff_data
  local staged_data
  local diff_exit=1
  local staged_exit=1

  echo
  echo "[secret-scan] Scanning diff for sensitive tokens"

  diff_data="$(git diff -- . ':(exclude)scripts/quality-gate.sh')"
  staged_data="$(git diff --cached -- . ':(exclude)scripts/quality-gate.sh')"

  if [[ -z "$diff_data" && -z "$staged_data" ]]; then
    echo "No diff content to scan after exclusions."
    return 0
  fi

  set +e
  if has_cmd rg; then
    if [[ -n "$diff_data" ]]; then
      printf '%s\n' "$diff_data" | rg -n "$pattern"
      diff_exit=$?
    fi
    if [[ -n "$staged_data" ]]; then
      printf '%s\n' "$staged_data" | rg -n "$pattern"
      staged_exit=$?
    fi
  else
    if [[ -n "$diff_data" ]]; then
      printf '%s\n' "$diff_data" | grep -nE "$pattern"
      diff_exit=$?
    fi
    if [[ -n "$staged_data" ]]; then
      printf '%s\n' "$staged_data" | grep -nE "$pattern"
      staged_exit=$?
    fi
  fi
  set -e

  if [[ $diff_exit -eq 0 || $staged_exit -eq 0 ]]; then
    echo "Potential secret-like pattern found in diff. Review before commit." >&2
    exit 1
  fi

  echo "No secret-like patterns detected in current diff."
}

resolve_timeout_wrapper() {
  if has_cmd timeout; then
    echo "timeout 120"
    return
  fi

  if has_cmd gtimeout; then
    echo "gtimeout 120"
    return
  fi

  echo ""
}

require_git_repo

SKIP_REVIEW=false
FORCE_UI=false
FORCE_TYPES=false
BASE_URL="http://127.0.0.1:3000"
RISK_TIER="T1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-review)
      SKIP_REVIEW=true
      shift
      ;;
    --skip-gemini)
      SKIP_REVIEW=true
      shift
      ;;
    --risk-tier)
      RISK_TIER="${2:-}"
      if [[ ! "$RISK_TIER" =~ ^T[0-3]$ ]]; then
        echo "Error: --risk-tier must be T0, T1, T2, or T3." >&2
        exit 1
      fi
      shift 2
      ;;
    --ui-changed)
      FORCE_UI=true
      shift
      ;;
    --types-changed)
      FORCE_TYPES=true
      shift
      ;;
    --base-url)
      BASE_URL="${2:-}"
      if [[ -z "$BASE_URL" ]]; then
        echo "Error: --base-url requires a value." >&2
        exit 1
      fi
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown option '$1'." >&2
      usage >&2
      exit 1
      ;;
  esac
done

LINT_CMD="${LINT_CMD:-npm run lint}"
TEST_CMD="${TEST_CMD:-npm run test -- --run}"
BUILD_CMD="${BUILD_CMD:-npm run build}"
E2E_CMD="${E2E_CMD:-npm run test:e2e}"
TSC_CMD="${TSC_CMD:-npx tsc --noEmit}"

echo "[state] Branch + working tree"
git status --short --branch

echo
echo "[state] Risk tier: $RISK_TIER"

echo
echo "[state] Changed files"
CHANGED_FILES="$(collect_changed_files || true)"
if [[ -z "$CHANGED_FILES" ]]; then
  echo "No changed files detected (staged or unstaged)."
else
  printf '%s\n' "$CHANGED_FILES"
fi

RUN_UI_GATE=false
RUN_TYPES_GATE=false

if [[ -n "$CHANGED_FILES" ]]; then
  while IFS= read -r path; do
    matches_any "$path" '^app/' '^pages/' '^components/' '^src/' '^public/' '\.tsx$' '\.jsx$' '\.css$' '\.scss$' && RUN_UI_GATE=true
    matches_any "$path" '^types/' '^schemas?/' '^prisma/' '^supabase/' '^migrations?/' '^db/' '^contracts?/' '^validators?/' 'types?\.ts$' 'schema' && RUN_TYPES_GATE=true
  done <<< "$CHANGED_FILES"
fi

if [[ "$FORCE_UI" == true ]]; then
  RUN_UI_GATE=true
fi
if [[ "$FORCE_TYPES" == true ]]; then
  RUN_TYPES_GATE=true
fi

if [[ "$SKIP_REVIEW" == false ]]; then
  if [[ -x "scripts/review-diff.sh" ]]; then
    run_cmd "review" "scripts/review-diff.sh"
  else
    echo
    echo "[review] scripts/review-diff.sh not found/executable; skipping review step."
  fi
else
  echo
  echo "[review] Skipped by flag (--skip-review)."
fi

if [[ "$RISK_TIER" == "T3" ]]; then
  echo
  echo "[review] T3 change detected. Run a separate logic/security review and capture rollback notes."
fi

run_cmd "lint" "$LINT_CMD"
run_cmd "test" "$TEST_CMD"
run_cmd "build" "$BUILD_CMD"

if [[ "$RUN_UI_GATE" == true ]]; then
  run_cmd "e2e" "PLAYWRIGHT_BASE_URL=${BASE_URL} $E2E_CMD"
else
  echo
  echo "[e2e] Skipped (no UI-significant paths detected)."
fi

if [[ "$RUN_TYPES_GATE" == true ]]; then
  TIMEOUT_PREFIX="$(resolve_timeout_wrapper)"
  if [[ -n "$TIMEOUT_PREFIX" ]]; then
    run_cmd "types" "$TIMEOUT_PREFIX $TSC_CMD"
  else
    run_cmd "types" "$TSC_CMD"
  fi
else
  echo
  echo "[types] Skipped (no type/schema-significant paths detected)."
fi

run_secret_scan

echo

echo "[staging] Current staged files"
git diff --staged --name-only || true

echo
echo "Quality gate passed. Safe to stage explicit files and commit."
