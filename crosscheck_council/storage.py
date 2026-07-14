"""Private storage, canonical hashing, and advisory locking."""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any, Iterator

from .errors import SafetyError, StateError


RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$")


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_run_id(run_id: str) -> str:
    if not RUN_ID_RE.fullmatch(run_id):
        raise SafetyError(f"invalid run id: {run_id!r}")
    return run_id


def ensure_private_dir(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_symlink():
        raise SafetyError(f"refusing symlink directory: {expanded}")
    path = expanded.resolve(strict=False)
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not path.is_dir():
        raise SafetyError(f"not a directory: {path}")
    os.chmod(path, 0o700)
    return path


def atomic_write_bytes(path: Path, payload: bytes, *, mode: int = 0o600, overwrite: bool = True) -> None:
    parent = ensure_private_dir(path.parent)
    if not overwrite and path.exists():
        raise StateError(f"refusing to overwrite immutable file: {path}")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=parent)
    tmp = Path(tmp_name)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb", closefd=True) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if not overwrite and path.exists():
            raise StateError(f"refusing to overwrite immutable file: {path}")
        os.replace(tmp, path)
        os.chmod(path, mode)
        dir_fd = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        with contextlib.suppress(FileNotFoundError):
            tmp.unlink()


def atomic_write_text(path: Path, payload: str, *, mode: int = 0o600, overwrite: bool = True) -> None:
    atomic_write_bytes(path, payload.encode("utf-8"), mode=mode, overwrite=overwrite)


def atomic_write_json(path: Path, payload: Any, *, mode: int = 0o600, overwrite: bool = True) -> None:
    atomic_write_bytes(path, canonical_json_bytes(payload), mode=mode, overwrite=overwrite)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StateError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise StateError(f"expected JSON object in {path}")
    return value


def private_mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


class FileLock:
    """Exclusive process lock backed by flock; contents identify the holder."""

    def __init__(self, path: Path, *, blocking: bool = True) -> None:
        self.path = path
        self.blocking = blocking
        self._fd: int | None = None

    def __enter__(self) -> "FileLock":
        ensure_private_dir(self.path.parent)
        flags = os.O_RDWR | os.O_CREAT
        fd = os.open(self.path, flags, 0o600)
        os.fchmod(fd, 0o600)
        lock_flags = fcntl.LOCK_EX | (0 if self.blocking else fcntl.LOCK_NB)
        try:
            fcntl.flock(fd, lock_flags)
        except BlockingIOError as exc:
            os.close(fd)
            raise StateError(f"run is already active: {self.path.parent.name}") from exc
        os.ftruncate(fd, 0)
        os.write(fd, f"{os.getpid()}\n".encode("ascii"))
        os.fsync(fd)
        self._fd = fd
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._fd is None:
            return
        fcntl.flock(self._fd, fcntl.LOCK_UN)
        os.close(self._fd)
        self._fd = None


class Store:
    """Filesystem layout for controller state."""

    def __init__(self, home: Path) -> None:
        self.home = ensure_private_dir(home)
        self.runs = ensure_private_dir(self.home / "runs")
        self.worktrees = ensure_private_dir(self.home / "worktrees")

    def run_dir(self, run_id: str, *, create: bool = False) -> Path:
        validate_run_id(run_id)
        path = self.runs / run_id
        if path.is_symlink():
            raise SafetyError(f"refusing symlink run directory: {path}")
        if create:
            if path.exists():
                raise StateError(f"run already exists: {run_id}")
            ensure_private_dir(path)
            for child in ("artifacts", "raw", "receipts", "runtime"):
                ensure_private_dir(path / child)
        elif not path.is_dir():
            raise StateError(f"unknown run: {run_id}")
        return path

    def manifest_path(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "manifest.json"

    def load_manifest(self, run_id: str) -> dict[str, Any]:
        return read_json(self.manifest_path(run_id))

    def save_manifest(self, run_id: str, manifest: dict[str, Any]) -> None:
        atomic_write_json(self.manifest_path(run_id), manifest)

    def latest_run_id(self, repository: Path | None = None) -> str:
        expected_repository = repository.expanduser().resolve(strict=False) if repository is not None else None
        candidates: list[Path] = []
        for path in self.runs.iterdir():
            if path.is_symlink() or not path.is_dir() or not (path / "manifest.json").is_file():
                continue
            if expected_repository is not None:
                with contextlib.suppress(StateError, OSError, ValueError):
                    manifest = read_json(path / "manifest.json")
                    recorded = manifest.get("repository", {}).get("path")
                    if isinstance(recorded, str) and Path(recorded).expanduser().resolve(strict=False) == expected_repository:
                        candidates.append(path)
                continue
            candidates.append(path)
        if not candidates:
            suffix = f" for repository {expected_repository}" if expected_repository is not None else ""
            raise StateError(f"no crosscheck runs exist{suffix}")
        return max(candidates, key=lambda p: p.stat().st_mtime_ns).name

    def lock(self, run_id: str, *, blocking: bool = False) -> FileLock:
        return FileLock(self.run_dir(run_id) / "runtime" / "run.lock", blocking=blocking)

    def iter_manifests(self) -> Iterator[tuple[str, dict[str, Any]]]:
        for path in sorted(self.runs.iterdir()):
            if path.is_dir() and (path / "manifest.json").is_file():
                with contextlib.suppress(StateError):
                    yield path.name, read_json(path / "manifest.json")
