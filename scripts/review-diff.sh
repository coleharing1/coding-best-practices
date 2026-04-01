#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/review-diff.sh [options]

Review a git diff with Gemini CLI using the default architectural review prompt.

Options:
  --staged               Review staged diff only (default: unstaged diff)
  --model MODEL          Gemini model (default: gemini-3.1-pro-preview)
  --prompt-file PATH     Read prompt text from file instead of the repo default
  --help                 Show this help

Examples:
  scripts/review-diff.sh
  scripts/review-diff.sh --staged
  scripts/review-diff.sh --model gemini-3.1-pro-preview
USAGE
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: required command '$1' is not installed or not in PATH." >&2
    exit 1
  fi
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: this script must run inside a git repository." >&2
  exit 1
fi

MODE="unstaged"
MODEL="gemini-3.1-pro-preview"
PROMPT_FILE="prompts/review-diff-gemini.md"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --staged)
      MODE="staged"
      shift
      ;;
    --model)
      MODEL="${2:-}"
      if [[ -z "$MODEL" ]]; then
        echo "Error: --model requires a value." >&2
        exit 1
      fi
      shift 2
      ;;
    --prompt-file)
      PROMPT_FILE="${2:-}"
      if [[ -z "$PROMPT_FILE" ]]; then
        echo "Error: --prompt-file requires a value." >&2
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

require_cmd gemini

if [[ "$MODE" == "staged" ]]; then
  DIFF_CONTENT="$(git diff --staged)"
else
  DIFF_CONTENT="$(git diff)"
fi

if [[ -z "$DIFF_CONTENT" ]]; then
  echo "No ${MODE} changes found. Nothing to review."
  exit 0
fi

if [[ -n "$PROMPT_FILE" && -f "$PROMPT_FILE" ]]; then
  PROMPT="$(cat "$PROMPT_FILE")"
else
  if [[ -n "$PROMPT_FILE" ]]; then
    echo "Prompt file not found at $PROMPT_FILE; falling back to built-in review prompt."
  fi
  PROMPT=$'Review this diff for:\n- Structural issues (functions doing too many things, missing separation of concerns)\n- Cross-file invariant violations\n- Race conditions or concurrency issues\n- Error-handling gaps and failure-state behavior\n- Patterns that deviate from the rest of the codebase\nBe specific: cite file names and line ranges.'
fi

echo "Running Gemini review (${MODE} diff) with model: ${MODEL}"
printf '%s\n' "$DIFF_CONTENT" | gemini --model "$MODEL" -p "$PROMPT"
