"""Git evidence capture and local-only worktree operations."""

from __future__ import annotations

import hashlib
import base64
import contextlib
import os
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .errors import SafetyError, StateError
from .storage import canonical_json_bytes, sha256_bytes, sha256_file


SECRET_KEY_PATTERN = (
    r"(?:(?:[A-Za-z0-9]+[_-])*(?:api[_-]?key|access[_-]?token|service[_-]?role[_-]?key|private[_-]?key|"
    r"client[_-]?secret|database[_-]?url|redis[_-]?url|connection[_-]?string)|"
    r"token|auth(?:orization)?|password|passwd|secret|credentials?)"
)
QUOTED_SECRET_ASSIGNMENT_RE = re.compile(
    rf"(?i)(?P<prefix>[\"']?\b{SECRET_KEY_PATTERN}\b[\"']?\s*[:=]\s*)"
    r"(?P<quote>[\"'])(?P<value>[^\r\n]*?)(?P=quote)"
)
AUTHORIZATION_RE = re.compile(
    r"(?i)([\"']?\bauthorization\b[\"']?\s*[:=]\s*)"
    r"(?![\"'])(?:(?:bearer|basic)\s+[^\s,;#\"']+|[^\s,;#\"']+)"
)
SECRET_ASSIGNMENT_RE = re.compile(
    rf"(?i)([\"']?\b{SECRET_KEY_PATTERN}\b[\"']?\s*[:=]\s*)(?![\"'])([^\s,;#]+)"
)
URL_CREDENTIAL_RE = re.compile(
    r"(?i)((?:https?|postgres(?:ql)?|redis|rediss|mysql|mariadb|mongodb(?:\+srv)?)://[^@\s/]*:)"
    r"([^@\s/]+)(@)"
)
KNOWN_TOKEN_RE = re.compile(
    r"(?x)(?:"
    r"sk-[A-Za-z0-9_-]{8,}|"
    r"gh[pousr]_[A-Za-z0-9]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"AKIA[A-Z0-9]{16}|"
    r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"
    r")"
)
PEM_RE = re.compile(r"-----BEGIN [^-]+ PRIVATE KEY-----.*?-----END [^-]+ PRIVATE KEY-----", re.DOTALL)

POLICY_CANDIDATES = (
    "AGENTS.override.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".codex/config.toml",
    ".claude/settings.json",
    "scripts/quality-gate.sh",
)


def redact_text(text: str) -> str:
    text = PEM_RE.sub("[REDACTED PRIVATE KEY]", text)
    text = URL_CREDENTIAL_RE.sub(r"\1[REDACTED]\3", text)
    text = QUOTED_SECRET_ASSIGNMENT_RE.sub(
        lambda match: f"{match.group('prefix')}{match.group('quote')}[REDACTED]{match.group('quote')}",
        text,
    )
    text = AUTHORIZATION_RE.sub(r"\1[REDACTED]", text)
    text = SECRET_ASSIGNMENT_RE.sub(r"\1[REDACTED]", text)
    return KNOWN_TOKEN_RE.sub("[REDACTED TOKEN]", text)


def _git_env() -> dict[str, str]:
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin:/usr/sbin:/sbin"),
        "HOME": os.environ.get("HOME", str(Path.home())),
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
    }
    return env


def run_git(
    repo: Path,
    args: Iterable[str],
    *,
    check: bool = True,
    timeout: int = 60,
    input_bytes: bytes | None = None,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    argv = [
        "git",
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "core.fsmonitor=false",
        "-C",
        str(repo),
        *list(args),
    ]
    env = _git_env()
    if extra_env:
        env.update(extra_env)
    try:
        result = subprocess.run(argv, input=input_bytes, capture_output=True, check=False, timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise StateError(f"git command failed to start or timed out: {argv!r}: {exc}") from exc
    if check and result.returncode != 0:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise StateError(f"git command failed ({result.returncode}): {' '.join(argv)}: {error}")
    return result


def repository_root(path: Path) -> Path:
    candidate = path.expanduser().resolve()
    result = run_git(candidate, ["rev-parse", "--show-toplevel"])
    root = Path(result.stdout.decode("utf-8").strip()).resolve()
    if not root.is_dir():
        raise StateError(f"repository root does not exist: {root}")
    return root


def _untracked_paths(status: bytes) -> list[str]:
    fields = status.split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        if not field:
            index += 1
            continue
        text = field.decode("utf-8", errors="surrogateescape")
        code = text[:2]
        path = text[3:] if len(text) >= 4 else ""
        if code == "??":
            paths.append(path)
        if "R" in code or "C" in code:
            index += 1
        index += 1
    return sorted(set(paths))


def _hash_untracked(root: Path, paths: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative in paths:
        target = (root / relative).resolve(strict=False)
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise SafetyError(f"untracked path escapes repository: {relative}") from exc
        if target.is_symlink():
            value = os.readlink(target)
            records.append({"path": relative, "kind": "symlink", "sha256": sha256_bytes(value.encode())})
        elif target.is_file():
            records.append({"path": relative, "kind": "file", "bytes": target.stat().st_size, "sha256": sha256_file(target)})
        else:
            records.append({"path": relative, "kind": "missing"})
    return records


@dataclass(frozen=True)
class GitSnapshot:
    root: Path
    head: str
    branch: str
    dirty: bool
    fingerprint: str
    status: str
    diff_sha256: str
    diff_bytes: int
    redacted_diff: str
    tracked_files: tuple[str, ...]
    untracked: tuple[dict[str, Any], ...]
    remote_config_sha256: str

    def evidence(self) -> dict[str, Any]:
        return {
            "path": str(self.root),
            "target_sha": self.head,
            "branch": self.branch,
            "dirty": self.dirty,
            "dirty_fingerprint": self.fingerprint,
            "status": self.status,
            "diff": {
                "sha256": self.diff_sha256,
                "bytes": self.diff_bytes,
                "redacted_content": self.redacted_diff,
            },
            "tracked_files": list(self.tracked_files),
            "untracked_files": list(self.untracked),
            "remote_config_sha256": self.remote_config_sha256,
        }


@dataclass(frozen=True)
class WorktreeChanges:
    """Canonical, complete tracked + untracked working-tree change packet."""

    payload: bytes
    review_text: str
    sha256: str
    tracked_bytes: int
    untracked_count: int


@dataclass(frozen=True)
class LocalCommit:
    commit_sha: str
    tree_sha: str


def capture_worktree_changes(root: Path, *, max_bytes: int = 32 * 1024 * 1024) -> WorktreeChanges:
    """Capture raw files that differ from HEAD, bypassing diff and content filters."""

    root = repository_root(root)
    head = run_git(root, ["rev-parse", "HEAD"]).stdout.decode().strip()
    object_format = run_git(root, ["rev-parse", "--show-object-format"]).stdout.decode().strip()
    if object_format not in {"sha1", "sha256"}:
        raise SafetyError(f"unsupported Git object format: {object_format}")
    tree_raw = run_git(root, ["ls-tree", "-r", "-z", "--full-tree", "HEAD"]).stdout
    head_entries: dict[str, dict[str, str]] = {}
    for field in tree_raw.split(b"\0"):
        if not field:
            continue
        metadata, raw_path = field.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        try:
            relative = raw_path.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SafetyError("working-tree paths must be valid UTF-8") from exc
        head_entries[relative] = {"mode": mode, "kind": kind, "oid": oid}
    candidates_raw = run_git(root, ["ls-files", "-z", "--cached", "--others", "--exclude-standard"]).stdout
    try:
        candidates = {item.decode("utf-8") for item in candidates_raw.split(b"\0") if item}
    except UnicodeDecodeError as exc:
        raise SafetyError("working-tree paths must be valid UTF-8") from exc
    filemode_result = run_git(root, ["config", "--bool", "core.filemode"], check=False)
    filemode = filemode_result.stdout.decode().strip().lower() != "false"
    changes: list[dict[str, Any]] = []
    review_sections: list[str] = []
    total = 0
    tracked_bytes = 0
    untracked_count = 0
    for relative in sorted(set(head_entries) | candidates):
        target = root / relative
        try:
            target.parent.resolve(strict=False).relative_to(root)
        except ValueError as exc:
            raise SafetyError(f"working-tree path escapes repository: {relative}") from exc
        previous = head_entries.get(relative)
        raw: bytes | None
        if target.is_symlink():
            raw = os.readlink(target).encode("utf-8", errors="surrogateescape")
            mode, kind = "120000", "symlink"
            oid = hashlib.new(object_format, b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        elif target.is_file():
            raw = target.read_bytes()
            executable = bool(target.stat().st_mode & 0o111)
            mode = "100755" if executable else "100644"
            if not filemode and previous and previous["mode"] in {"100644", "100755"}:
                mode = previous["mode"]
            kind = "file"
            oid = hashlib.new(object_format, b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        elif target.is_dir() and previous and previous["mode"] == "160000":
            raw = None
            mode, kind = "160000", "gitlink"
            if (target / ".git").exists():
                oid = run_git(target, ["rev-parse", "HEAD"]).stdout.decode().strip()
            else:
                oid = previous["oid"]
        elif target.is_dir():
            raise SafetyError(f"unsupported untracked directory or nested repository: {relative}")
        else:
            raw = None
            mode, kind, oid = "0", "deleted", ""
        if previous and previous["mode"] == mode and previous["oid"] == oid:
            continue
        if raw is not None:
            total += len(raw)
            if total > max_bytes:
                raise SafetyError(f"working-tree change packet exceeds {max_bytes} bytes")
        record: dict[str, Any] = {
            "path": relative,
            "kind": kind,
            "mode": mode,
            "oid": oid,
            "previous_mode": previous["mode"] if previous else None,
            "previous_oid": previous["oid"] if previous else None,
        }
        if raw is not None:
            record.update(
                {
                    "bytes": len(raw),
                    "sha256": sha256_bytes(raw),
                    "content_base64": base64.b64encode(raw).decode("ascii"),
                }
            )
        changes.append(record)
        if previous is None:
            untracked_count += 1
        elif raw is not None:
            tracked_bytes += len(raw)
        label = json.dumps(relative, ensure_ascii=True)
        review_sections.append(
            f"=== {kind.upper()} {label}: {record['previous_mode'] or '<new>'} -> {mode}; "
            f"oid {record['previous_oid'] or '<new>'} -> {oid or '<deleted>'} ===\n"
        )
        if raw is not None:
            if b"\0" in raw:
                review_sections.append(f"[binary content: {len(raw)} bytes; sha256={sha256_bytes(raw)}]\n")
            else:
                review_sections.append(redact_text(raw.decode("utf-8", errors="replace")) + "\n")
    packet = {
        "schema": "worktree-changes/v1",
        "repository": str(root),
        "head": head,
        "object_format": object_format,
        "changes": changes,
    }
    payload = canonical_json_bytes(packet)
    return WorktreeChanges(
        payload=payload,
        review_text="".join(review_sections),
        sha256=sha256_bytes(payload),
        tracked_bytes=tracked_bytes,
        untracked_count=untracked_count,
    )


def commit_worktree_changes(
    root: Path,
    changes: WorktreeChanges,
    *,
    message: str,
    commit_date: str,
) -> LocalCommit:
    """Create a local commit from the bound raw packet without hooks or filters."""

    root = repository_root(root)
    packet = json.loads(changes.payload)
    head = run_git(root, ["rev-parse", "HEAD"]).stdout.decode().strip()
    if packet.get("schema") != "worktree-changes/v1" or packet.get("repository") != str(root) or packet.get("head") != head:
        raise SafetyError("working-tree change packet does not match this repository and HEAD")
    if capture_worktree_changes(root).sha256 != changes.sha256:
        raise SafetyError("working tree changed before local commit assembly")
    index_path_raw = run_git(root, ["rev-parse", "--git-path", "index"]).stdout.decode().strip()
    index_path = Path(index_path_raw)
    if not index_path.is_absolute():
        index_path = root / index_path
    index_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix="crosscheck-index-", dir=index_path.parent)
    os.close(fd)
    temporary_index = Path(temporary_name)
    temporary_index.unlink()
    index_env = {"GIT_INDEX_FILE": str(temporary_index)}
    try:
        run_git(root, ["read-tree", "HEAD"], extra_env=index_env)
        for record in packet.get("changes", []):
            if not isinstance(record, dict) or not isinstance(record.get("path"), str):
                raise SafetyError("working-tree change packet is malformed")
            relative = record["path"]
            if record.get("kind") == "deleted":
                run_git(root, ["update-index", "--force-remove", "--", relative], extra_env=index_env)
                continue
            mode = record.get("mode")
            oid = record.get("oid")
            if mode == "160000":
                if not isinstance(oid, str):
                    raise SafetyError("gitlink record is malformed")
            else:
                encoded = record.get("content_base64")
                if not isinstance(encoded, str):
                    raise SafetyError("file record omitted bound content")
                try:
                    raw = base64.b64decode(encoded, validate=True)
                except (ValueError, TypeError) as exc:
                    raise SafetyError("file record contains malformed base64") from exc
                written = run_git(
                    root,
                    ["hash-object", "--no-filters", "-w", "--stdin"],
                    input_bytes=raw,
                ).stdout.decode().strip()
                if written != oid:
                    raise SafetyError(f"Git object hash mismatch while staging: {relative}")
            run_git(root, ["update-index", "--add", "--cacheinfo", str(mode), str(oid), relative], extra_env=index_env)
        tree_sha = run_git(root, ["write-tree"], extra_env=index_env).stdout.decode().strip()
        identity_env = {
            "GIT_AUTHOR_NAME": "Crosscheck Council",
            "GIT_AUTHOR_EMAIL": "crosscheck@local.invalid",
            "GIT_COMMITTER_NAME": "Crosscheck Council",
            "GIT_COMMITTER_EMAIL": "crosscheck@local.invalid",
            "GIT_AUTHOR_DATE": commit_date,
            "GIT_COMMITTER_DATE": commit_date,
        }
        commit_sha = run_git(
            root,
            ["-c", "commit.gpgSign=false", "commit-tree", tree_sha, "-p", head],
            input_bytes=(message.rstrip() + "\n").encode("utf-8"),
            extra_env=identity_env,
        ).stdout.decode().strip()
        if capture_worktree_changes(root).sha256 != changes.sha256:
            raise SafetyError("working tree changed during local commit assembly")
        advanced = False
        try:
            run_git(root, ["update-ref", "-m", "crosscheck local completion", "HEAD", commit_sha, head])
            advanced = True
            run_git(root, ["read-tree", commit_sha])
            current = run_git(root, ["rev-parse", "HEAD"]).stdout.decode().strip()
            if current != commit_sha:
                raise SafetyError("local branch did not advance to the assembled commit")
            post = json.loads(capture_worktree_changes(root).payload)
            if post.get("changes"):
                raise SafetyError("local commit tree does not exactly match the verified working tree")
            return LocalCommit(commit_sha=commit_sha, tree_sha=tree_sha)
        except BaseException:
            if advanced:
                run_git(root, ["update-ref", "-m", "crosscheck completion rollback", "HEAD", head, commit_sha], check=False)
                run_git(root, ["read-tree", head], check=False)
            raise
    finally:
        with contextlib.suppress(FileNotFoundError):
            temporary_index.unlink()


def capture_snapshot(path: Path, *, max_diff_bytes: int = 2 * 1024 * 1024, max_files: int = 50_000) -> GitSnapshot:
    root = repository_root(path)
    head = run_git(root, ["rev-parse", "HEAD"]).stdout.decode().strip()
    branch_result = run_git(root, ["symbolic-ref", "--quiet", "--short", "HEAD"], check=False)
    branch = branch_result.stdout.decode().strip() if branch_result.returncode == 0 else "(detached)"
    changes = capture_worktree_changes(root)
    packet = json.loads(changes.payload)
    change_records = packet["changes"]
    tracked_raw = run_git(root, ["ls-files", "-z"]).stdout
    tracked = tuple(p.decode("utf-8", errors="surrogateescape") for p in tracked_raw.split(b"\0") if p)
    if len(tracked) > max_files:
        raise SafetyError(f"repository has {len(tracked)} tracked files; maximum evidence set is {max_files}")
    untracked = tuple(
        {
            "path": item["path"],
            "kind": item["kind"],
            "bytes": item.get("bytes", 0),
            "sha256": item.get("sha256", ""),
        }
        for item in change_records
        if item.get("previous_oid") is None
    )
    remote_config = run_git(root, ["config", "--local", "--get-regexp", r"^remote\..*"], check=False).stdout
    redacted = changes.review_text
    encoded = redacted.encode("utf-8")
    if len(encoded) > max_diff_bytes:
        suffix = f"\n[TRUNCATED: original redacted diff exceeded {max_diff_bytes} bytes]\n"
        redacted = encoded[:max_diff_bytes].decode("utf-8", errors="ignore") + suffix
    return GitSnapshot(
        root=root,
        head=head,
        branch=branch,
        dirty=bool(change_records),
        fingerprint=changes.sha256,
        status="\n".join(
            (
                "?? " if item.get("previous_oid") is None else " D " if item.get("kind") == "deleted" else " M "
            )
            + item["path"]
            for item in change_records
        ),
        diff_sha256=changes.sha256,
        diff_bytes=len(changes.payload),
        redacted_diff=redacted,
        tracked_files=tracked,
        untracked=untracked,
        remote_config_sha256=sha256_bytes(remote_config),
    )


def collect_policies(root: Path, *, max_each_bytes: int = 128 * 1024) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative in POLICY_CANDIDATES:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            continue
        raw = path.read_bytes()
        content = redact_text(raw[:max_each_bytes].decode("utf-8", errors="replace"))
        records.append(
            {
                "path": relative,
                "sha256": sha256_bytes(raw),
                "bytes": len(raw),
                "content": content,
                "truncated": len(raw) > max_each_bytes,
            }
        )
    return records


def assert_snapshot_unchanged(expected: GitSnapshot, path: Path | None = None) -> GitSnapshot:
    current = capture_snapshot(path or expected.root)
    if current.head != expected.head or current.fingerprint != expected.fingerprint:
        raise SafetyError(
            "repository drift detected: expected "
            f"{expected.head[:12]}/{expected.fingerprint[:12]}, got {current.head[:12]}/{current.fingerprint[:12]}"
        )
    return current


def assert_clean_base(root: Path, expected_sha: str) -> GitSnapshot:
    current = capture_snapshot(root)
    if current.head != expected_sha:
        raise SafetyError(f"repository HEAD changed: expected {expected_sha}, got {current.head}")
    if current.dirty:
        raise SafetyError("implementation requires a clean repository; planning snapshots may be dirty")
    return current


def _filter_overrides(root: Path) -> list[str]:
    result = run_git(
        root,
        ["config", "--local", "--name-only", "--get-regexp", r"^filter\..*\.(clean|smudge|process|required)$"],
        check=False,
    )
    drivers: set[str] = set()
    for line in result.stdout.decode("utf-8", errors="strict").splitlines():
        match = re.fullmatch(r"filter\.([A-Za-z0-9._-]+)\.(?:clean|smudge|process|required)", line.strip())
        if not match:
            raise SafetyError(f"unsupported Git filter configuration key: {line!r}")
        drivers.add(match.group(1))
    argv: list[str] = []
    for driver in sorted(drivers):
        for value in (
            f"filter.{driver}.clean=/bin/cat",
            f"filter.{driver}.smudge=/bin/cat",
            f"filter.{driver}.process=",
            f"filter.{driver}.required=false",
        ):
            argv.extend(["-c", value])
    return argv


def create_worktree(root: Path, target: Path, sha: str, branch: str) -> Path:
    if target.exists():
        raise StateError(f"worktree target already exists: {target}")
    reference = f"refs/heads/{branch}"
    if run_git(root, ["show-ref", "--verify", "--quiet", reference], check=False).returncode == 0:
        raise StateError(f"worktree branch already exists: {branch}")
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    run_git(root, ["worktree", "add", "--detach", "--no-checkout", str(target), sha], timeout=120)
    branch_created = False
    try:
        run_git(root, ["update-ref", reference, sha, ""])
        branch_created = True
        run_git(target, ["symbolic-ref", "HEAD", reference])
        tree = run_git(root, ["ls-tree", "-r", "-z", "--full-tree", sha]).stdout
        for field in tree.split(b"\0"):
            if not field:
                continue
            metadata, raw_path = field.split(b"\t", 1)
            mode, kind, oid = metadata.decode("ascii").split()
            if kind not in {"blob", "commit"}:
                raise SafetyError(f"unsupported Git tree entry type: {kind}")
            relative = raw_path.decode("utf-8", errors="surrogateescape")
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if mode == "120000":
                link = run_git(root, ["cat-file", "blob", oid]).stdout.decode("utf-8", errors="surrogateescape")
                os.symlink(link, destination)
            elif mode in {"100644", "100755"}:
                content = run_git(root, ["cat-file", "blob", oid]).stdout
                with destination.open("xb") as handle:
                    handle.write(content)
                os.chmod(destination, 0o755 if mode == "100755" else 0o644)
            elif mode == "160000":
                destination.mkdir(exist_ok=True)
            else:
                raise SafetyError(f"unsupported Git tree mode: {mode}")
        run_git(target, ["read-tree", sha])
        if json.loads(capture_worktree_changes(target).payload).get("changes"):
            raise SafetyError("raw worktree materialization did not reproduce the target tree")
    except Exception:
        run_git(root, ["worktree", "remove", "--force", str(target)], check=False)
        if branch_created:
            run_git(root, ["update-ref", "-d", reference], check=False)
        raise
    return target.resolve()
