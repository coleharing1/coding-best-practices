#!/usr/bin/env python3
"""Hash-lock, check, and atomically install the canonical council skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / ".agents" / "skills"
LOCK_PATH = REPO_ROOT / "skills.lock.json"
TARGET_SUFFIXES = {
    "claude": Path(".claude/skills"),
    "codex": Path(".codex/skills"),
    "hermes": Path(".hermes/skills/productivity"),
}
LOCK_TARGETS = {
    "claude": "~/.claude/skills",
    "codex": "~/.codex/skills",
    "hermes": "~/.hermes/skills/productivity",
}
WRAPPER_SOURCES = {
    "claude": Path("integrations/claude/crosscheck"),
    "codex": Path("integrations/codex/crosscheck"),
    "hermes": Path("integrations/hermes/crosscheck"),
}
WRAPPER_TARGETS = {
    "claude": "~/.local/bin/crosscheck-claude",
    "codex": "~/.local/bin/crosscheck-codex",
    "hermes": "~/.local/bin/crosscheck-hermes",
}
HELPER_SOURCES = {
    "crosscheck-import": Path("integrations/claude-plugin/plugins/crosscheck/scripts/crosscheck-import.mjs"),
}
HELPER_TARGETS = {
    "crosscheck-import": "~/.local/bin/crosscheck-import",
}


def skill_dirs() -> dict[str, Path]:
    if not SOURCE_ROOT.is_dir():
        raise SystemExit(f"missing canonical skill root: {SOURCE_ROOT}")
    return {
        path.name: path
        for path in sorted(SOURCE_ROOT.iterdir())
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        if "__pycache__" in item.parts or item.name == ".DS_Store":
            continue
        relative = item.relative_to(path).as_posix().encode()
        data = item.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_lock() -> dict:
    return {
        "schema_version": "skills-lock/v1",
        "canonical_root": ".agents/skills",
        "skills": {name: {"sha256": tree_hash(path)} for name, path in skill_dirs().items()},
        "targets": LOCK_TARGETS,
        "wrappers": {
            name: {
                "source": source.as_posix(),
                "target": WRAPPER_TARGETS[name],
                "sha256": file_hash(REPO_ROOT / source),
            }
            for name, source in WRAPPER_SOURCES.items()
        },
        "helpers": {
            name: {
                "source": source.as_posix(),
                "target": HELPER_TARGETS[name],
                "sha256": file_hash(REPO_ROOT / source),
            }
            for name, source in HELPER_SOURCES.items()
        },
    }


def load_lock() -> dict:
    if not LOCK_PATH.is_file():
        raise SystemExit(f"missing lock file: {LOCK_PATH}")
    try:
        return json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"invalid lock file {LOCK_PATH}: {error}") from error


def source_errors(lock: dict) -> list[str]:
    actual = expected_lock()
    errors: list[str] = []
    if lock.get("schema_version") != actual["schema_version"]:
        errors.append("unsupported or missing lock schema")
    if lock.get("canonical_root") != actual["canonical_root"]:
        errors.append("canonical skill root does not match")
    if lock.get("targets") != actual["targets"]:
        errors.append("installed-cache targets do not match the cross-harness contract")
    if lock.get("skills") != actual["skills"]:
        errors.append("canonical skill content does not match skills.lock.json; run --write-lock intentionally")
    if lock.get("wrappers") != actual["wrappers"]:
        errors.append("canonical wrapper content does not match skills.lock.json; run --write-lock intentionally")
    if lock.get("helpers") != actual["helpers"]:
        errors.append("canonical helper content does not match skills.lock.json; run --write-lock intentionally")
    return errors


def selected_targets(home: Path, harness: str) -> dict[str, Path]:
    targets = {name: home / suffix for name, suffix in TARGET_SUFFIXES.items()}
    return targets if harness == "all" else {harness: targets[harness]}


def check(lock: dict, home: Path, harness: str) -> tuple[list[dict], bool]:
    errors = source_errors(lock)
    rows: list[dict] = []
    ok = not errors
    for target_name, target_root in selected_targets(home, harness).items():
        for skill_name, details in sorted(lock.get("skills", {}).items()):
            target = target_root / skill_name
            observed = tree_hash(target) if target.is_dir() and not target.is_symlink() else None
            matches = observed == details.get("sha256")
            rows.append(
                {
                    "harness": target_name,
                    "skill": skill_name,
                    "path": str(target),
                    "expected_sha256": details.get("sha256"),
                    "observed_sha256": observed,
                    "status": "current" if matches else ("missing" if observed is None else "drift"),
                }
            )
            ok = ok and matches
        wrapper_details = lock.get("wrappers", {}).get(target_name, {})
        wrapper_target = home / ".local/bin" / f"crosscheck-{target_name}"
        wrapper_observed = (
            file_hash(wrapper_target)
            if wrapper_target.is_file() and not wrapper_target.is_symlink()
            else None
        )
        wrapper_executable = wrapper_target.is_file() and os.access(wrapper_target, os.X_OK)
        wrapper_matches = wrapper_observed == wrapper_details.get("sha256") and wrapper_executable
        rows.append(
            {
                "kind": "wrapper",
                "harness": target_name,
                "path": str(wrapper_target),
                "expected_sha256": wrapper_details.get("sha256"),
                "observed_sha256": wrapper_observed,
                "executable": wrapper_executable,
                "status": "current" if wrapper_matches else ("missing" if wrapper_observed is None else "drift"),
            }
        )
        ok = ok and wrapper_matches
    for helper_name, helper_details in sorted(lock.get("helpers", {}).items()):
        helper_target = home / ".local/bin" / helper_name
        helper_observed = (
            file_hash(helper_target)
            if helper_target.is_file() and not helper_target.is_symlink()
            else None
        )
        helper_executable = helper_target.is_file() and os.access(helper_target, os.X_OK)
        helper_matches = helper_observed == helper_details.get("sha256") and helper_executable
        rows.append(
            {
                "kind": "helper",
                "path": str(helper_target),
                "expected_sha256": helper_details.get("sha256"),
                "observed_sha256": helper_observed,
                "executable": helper_executable,
                "status": "current" if helper_matches else ("missing" if helper_observed is None else "drift"),
            }
        )
        ok = ok and helper_matches
    return rows, ok


def private_mkdir(path: Path) -> None:
    # mkdir's mode only applies to the leaf (and is umask-subject); parents=True
    # creates intermediates (backup timestamp dirs) world-traversable. Track every
    # missing component and chmod the whole created chain to 0700.
    missing: list[Path] = []
    probe = path
    while not probe.exists():
        missing.append(probe)
        if probe.parent == probe:
            break
        probe = probe.parent
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    for created in missing:
        created.chmod(0o700)


def install(lock: dict, home: Path, harness: str) -> list[dict]:
    errors = source_errors(lock)
    if errors:
        raise SystemExit("; ".join(errors))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = home / ".local/share/crosscheck-council/backups" / timestamp / "skills"
    sources = skill_dirs()
    rows: list[dict] = []
    for target_name, target_root in selected_targets(home, harness).items():
        target_root.mkdir(parents=True, exist_ok=True)
        for skill_name, source in sources.items():
            target = target_root / skill_name
            expected_hash = lock["skills"][skill_name]["sha256"]
            if target.is_dir() and not target.is_symlink() and tree_hash(target) == expected_hash:
                rows.append({"harness": target_name, "skill": skill_name, "path": str(target), "status": "current"})
                continue
            backup = None
            if target.exists() or target.is_symlink():
                backup = backup_root / target_name / skill_name
                private_mkdir(backup.parent)
                shutil.move(str(target), str(backup))
            temporary = Path(tempfile.mkdtemp(prefix=f".crosscheck-{skill_name}-", dir=target_root))
            try:
                staged = temporary / skill_name
                shutil.copytree(source, staged, symlinks=False)
                os.replace(staged, target)
            finally:
                shutil.rmtree(temporary, ignore_errors=True)
            observed = tree_hash(target)
            if observed != expected_hash:
                raise SystemExit(f"post-install hash mismatch: {target}")
            rows.append(
                {
                    "harness": target_name,
                    "skill": skill_name,
                    "path": str(target),
                    "status": "installed",
                    "backup": str(backup) if backup else None,
                }
            )
        wrapper_source = REPO_ROOT / WRAPPER_SOURCES[target_name]
        wrapper_target_root = home / ".local/bin"
        wrapper_target_root.mkdir(parents=True, exist_ok=True)
        wrapper_target = wrapper_target_root / f"crosscheck-{target_name}"
        expected_wrapper_hash = lock["wrappers"][target_name]["sha256"]
        if (
            wrapper_target.is_file()
            and not wrapper_target.is_symlink()
            and file_hash(wrapper_target) == expected_wrapper_hash
            and os.access(wrapper_target, os.X_OK)
        ):
            rows.append({"kind": "wrapper", "harness": target_name, "path": str(wrapper_target), "status": "current"})
            continue
        wrapper_backup = None
        if wrapper_target.exists() or wrapper_target.is_symlink():
            wrapper_backup = backup_root / "wrappers" / target_name / wrapper_target.name
            private_mkdir(wrapper_backup.parent)
            shutil.move(str(wrapper_target), str(wrapper_backup))
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{wrapper_target.name}-", dir=wrapper_target_root)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(wrapper_source.read_bytes())
                handle.flush()
                os.fsync(handle.fileno())
            temporary.chmod(0o755)
            os.replace(temporary, wrapper_target)
        finally:
            temporary.unlink(missing_ok=True)
        if file_hash(wrapper_target) != expected_wrapper_hash or not os.access(wrapper_target, os.X_OK):
            raise SystemExit(f"post-install wrapper mismatch: {wrapper_target}")
        rows.append(
            {
                "kind": "wrapper",
                "harness": target_name,
                "path": str(wrapper_target),
                "status": "installed",
                "backup": str(wrapper_backup) if wrapper_backup else None,
            }
        )
    helper_target_root = home / ".local/bin"
    helper_target_root.mkdir(parents=True, exist_ok=True)
    for helper_name, helper_source_relative in sorted(HELPER_SOURCES.items()):
        helper_source = REPO_ROOT / helper_source_relative
        helper_target = helper_target_root / helper_name
        expected_helper_hash = lock["helpers"][helper_name]["sha256"]
        if (
            helper_target.is_file()
            and not helper_target.is_symlink()
            and file_hash(helper_target) == expected_helper_hash
            and os.access(helper_target, os.X_OK)
        ):
            rows.append({"kind": "helper", "path": str(helper_target), "status": "current"})
            continue
        helper_backup = None
        if helper_target.exists() or helper_target.is_symlink():
            helper_backup = backup_root / "helpers" / helper_target.name
            private_mkdir(helper_backup.parent)
            shutil.move(str(helper_target), str(helper_backup))
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{helper_target.name}-", dir=helper_target_root)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(helper_source.read_bytes())
                handle.flush()
                os.fsync(handle.fileno())
            temporary.chmod(0o755)
            os.replace(temporary, helper_target)
        finally:
            temporary.unlink(missing_ok=True)
        if file_hash(helper_target) != expected_helper_hash or not os.access(helper_target, os.X_OK):
            raise SystemExit(f"post-install helper mismatch: {helper_target}")
        rows.append(
            {
                "kind": "helper",
                "path": str(helper_target),
                "status": "installed",
                "backup": str(helper_backup) if helper_backup else None,
            }
        )
    return rows


def atomic_write_lock(payload: dict) -> None:
    data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    descriptor, temporary_name = tempfile.mkstemp(prefix=".skills.lock.", dir=REPO_ROOT)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, LOCK_PATH)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--check", action="store_true")
    actions.add_argument("--install", action="store_true")
    actions.add_argument("--write-lock", action="store_true")
    parser.add_argument("--harness", choices=["all", *TARGET_SUFFIXES], default="all")
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.write_lock:
        atomic_write_lock(expected_lock())
        print(json.dumps({"ok": True, "status": "written", "path": str(LOCK_PATH)}, indent=2))
        return 0

    lock = load_lock()
    if args.install:
        rows = install(lock, args.home.expanduser().resolve(), args.harness)
        print(json.dumps({"ok": True, "results": rows}, indent=2))
        return 0

    errors = source_errors(lock)
    rows, ok = check(lock, args.home.expanduser().resolve(), args.harness)
    print(json.dumps({"ok": ok, "source_errors": errors, "results": rows}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
