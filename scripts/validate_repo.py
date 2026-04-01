#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def add_error(errors: list[str], relpath: Path, message: str) -> None:
    errors.append(f"{relpath}: {message}")


def validate_json(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - validation script
            add_error(errors, rel, f"invalid JSON ({exc})")


def validate_toml(errors: list[str]) -> None:
    for path in ROOT.rglob("*.toml"):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - validation script
            add_error(errors, rel, f"invalid TOML ({exc})")


def validate_required_paths(errors: list[str]) -> None:
    required = [
        "README.md",
        "WORKLOG.md",
        "workflow/Repeatable-Actions-Stack.md",
        "workflow/Cursor-Workflow-Guide.md",
        "workflow/Gemini-CLI-Workflow-Guide.md",
        "workflow/Multi-Model-Workflow.md",
        "workflow/New-Project-Setup-Guide.md",
        "workflow/AI-First-Service-Setup-and-Login-Handoff.md",
        "metrics/Workflow-Scorecard.md",
        "templates/AGENTS.template.md",
        "templates/CLAUDE.template.md",
        "templates/GEMINI.template.md",
        "templates/.cursor/commands/README.template.md",
        "templates/.cursor/BUGBOT.template.md",
        "templates/.gemini/commands/README.template.md",
        "templates/.agents/skills/README.template.md",
    ]
    for relpath in required:
        path = ROOT / relpath
        if not path.exists():
            add_error(errors, Path(relpath), "required path is missing")


def validate_removed_duplicates(errors: list[str]) -> None:
    deprecated = [
        "templates/AGENTS.md",
        "templates/CLAUDE.md",
        "templates/PLAN.md",
        "templates/WORKLOG.md",
        "templates/.cursor/rules/000-core.mdc",
        "templates/.cursor/rules/050-worklog.mdc",
    ]
    for relpath in deprecated:
        path = ROOT / relpath
        if path.exists():
            add_error(errors, Path(relpath), "deprecated duplicate template still exists")


def validate_markdown_paths(errors: list[str]) -> None:
    prefixes = (
        "workflow/",
        "templates/",
        "prompts/",
        "metrics/",
        "research/",
        "scripts/",
        ".github/",
    )
    fenced_path_pattern = re.compile(r"`([^`\n]+)`")

    for md_path in ROOT.rglob("*.md"):
        if ".git" in md_path.parts:
            continue
        rel_md = md_path.relative_to(ROOT)
        if rel_md.name == "WORKLOG.md":
            continue
        text = md_path.read_text(encoding="utf-8")
        for raw in fenced_path_pattern.findall(text):
            candidate = raw.strip().rstrip(".,:)")
            if not candidate.startswith(prefixes):
                continue
            if " " in candidate:
                continue
            if any(token in candidate for token in ("XXX", "[", "]", "{", "}", "*")):
                continue
            if candidate in {"metrics/weekly-metrics.csv"}:
                continue
            path = ROOT / candidate
            if not path.exists():
                add_error(errors, rel_md, f"referenced path does not exist: `{candidate}`")


def main() -> int:
    errors: list[str] = []
    validate_json(errors)
    validate_toml(errors)
    validate_required_paths(errors)
    validate_removed_duplicates(errors)
    validate_markdown_paths(errors)

    if errors:
        print("Repo validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repo validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
