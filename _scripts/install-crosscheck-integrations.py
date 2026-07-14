#!/usr/bin/env python3
"""Install verified skill caches and the private Claude plugin at user scope."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_ROOT = REPO_ROOT / "integrations" / "claude-plugin"
MARKETPLACE_NAME = "crosscheck-council-local"
PLUGIN_ID = f"crosscheck@{MARKETPLACE_NAME}"
LEGACY_PLUGIN_ID = f"crosscheck-council@{MARKETPLACE_NAME}"


def run(*argv: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=capture,
    )


def json_output(*argv: str) -> object:
    result = run(*argv, capture=True)
    return json.loads(result.stdout)


def main() -> int:
    run(sys.executable, str(REPO_ROOT / "_scripts" / "sync-crosscheck.py"), "--install", "--harness", "all")
    run("claude", "plugin", "validate", "--strict", str(MARKETPLACE_ROOT))

    marketplaces = json_output("claude", "plugin", "marketplace", "list", "--json")
    names = {item.get("name") for item in marketplaces if isinstance(item, dict)} if isinstance(marketplaces, list) else set()
    if MARKETPLACE_NAME in names:
        run("claude", "plugin", "marketplace", "update", MARKETPLACE_NAME)
    else:
        run("claude", "plugin", "marketplace", "add", "--scope", "user", str(MARKETPLACE_ROOT))

    installed = json_output("claude", "plugin", "list", "--json")
    ids = {item.get("id") for item in installed if isinstance(item, dict)} if isinstance(installed, list) else set()
    if LEGACY_PLUGIN_ID in ids:
        run("claude", "plugin", "uninstall", "--scope", "user", LEGACY_PLUGIN_ID)
        ids.remove(LEGACY_PLUGIN_ID)
    if PLUGIN_ID in ids:
        run("claude", "plugin", "update", "--scope", "user", PLUGIN_ID)
    else:
        run("claude", "plugin", "install", "--scope", "user", PLUGIN_ID)

    print(json.dumps({"ok": True, "plugin": PLUGIN_ID, "scope": "user"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
