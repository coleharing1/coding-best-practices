"""Fail-closed Claude and Codex subprocess adapters."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .errors import CancelledError, ProviderError, SafetyError
from .storage import FileLock, atomic_write_bytes, atomic_write_json, atomic_write_text, read_json, sha256_bytes


CLAUDE_ALLOWED_TOOLS = {"Read", "Grep", "Glob"}
CLAUDE_SECRET_DENIES = (
    "Read(**/.env)",
    "Read(**/.env.*)",
    "Read(**/*credentials*)",
    "Read(**/*.key)",
    "Read(**/keys/**)",
)
CODEX_READ_ITEM_TYPES = {"agent_message", "reasoning", "command_execution", "todo_list"}
CODEX_WRITE_ITEM_TYPES = CODEX_READ_ITEM_TYPES | {"file_change"}
CODEX_META_EVENT_TYPES = {"thread.started", "turn.started", "turn.completed"}
RETRYABLE_MARKERS = (
    "429",
    "529",
    "capacity",
    "model is overloaded",
    "overloaded",
    "rate limit",
    "temporarily unavailable",
)
CODEX_READ_PERMISSION_PROFILE = "crosscheck_read_only"
CODEX_WRITE_PERMISSION_PROFILE = "crosscheck_write"
CODEX_QA_PERMISSION_PROFILE = "crosscheck_qa"
CODEX_SECRET_DENY_GLOBS = (
    "**/*.env",
    "**/.env*",
    "**/*credentials*",
    "**/*.key",
    "**/keys",
    "**/keys/**",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sanitized_environment(extra: dict[str, str] | None = None) -> dict[str, str]:
    allowed = ("HOME", "PATH", "TMPDIR", "USER", "LOGNAME", "LANG", "LC_ALL", "SHELL", "TERM")
    env = {key: value for key in allowed if (value := os.environ.get(key)) is not None}
    env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin")
    env.setdefault("HOME", str(Path.home()))
    env["CI"] = "1"
    env["NO_COLOR"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_LAZY_FETCH"] = "1"
    if extra:
        env.update(extra)
    return env


def resolve_binary(binary: str) -> str:
    if os.path.sep in binary:
        path = Path(binary).expanduser().resolve()
        if not path.is_file() or not os.access(path, os.X_OK):
            raise SafetyError(f"provider binary is not executable: {path}")
        return str(path)
    resolved = shutil.which(binary)
    if not resolved:
        raise SafetyError(f"provider binary not found on PATH: {binary}")
    return str(Path(resolved).resolve())


def _toml_string(value: str | Path) -> str:
    """Return a safely escaped TOML basic string."""

    return json.dumps(str(value), ensure_ascii=True)


def _git_permission_paths(worktree: Path) -> tuple[Path, Path]:
    """Resolve the writable worktree Git dir and its readable common Git dir."""

    dot_git = worktree / ".git"
    if dot_git.is_dir():
        git_dir = dot_git.resolve()
    elif dot_git.is_file():
        try:
            marker = dot_git.read_text(encoding="utf-8", errors="strict").strip()
        except OSError as exc:
            raise SafetyError(f"cannot read worktree Git pointer: {dot_git}") from exc
        prefix = "gitdir: "
        if not marker.startswith(prefix) or "\n" in marker or "\x00" in marker:
            raise SafetyError(f"worktree Git pointer is malformed: {dot_git}")
        candidate = Path(marker[len(prefix) :])
        if not candidate.is_absolute():
            candidate = dot_git.parent / candidate
        git_dir = candidate.resolve(strict=False)
        if not git_dir.is_dir():
            raise SafetyError(f"worktree Git directory does not exist: {git_dir}")
    else:
        raise SafetyError(f"implementation worktree has no Git metadata: {worktree}")

    common_marker = git_dir / "commondir"
    if not common_marker.is_file():
        return git_dir, git_dir
    try:
        common_value = common_marker.read_text(encoding="utf-8", errors="strict").strip()
    except OSError as exc:
        raise SafetyError(f"cannot read worktree common Git pointer: {common_marker}") from exc
    if not common_value or "\n" in common_value or "\x00" in common_value:
        raise SafetyError(f"worktree common Git pointer is malformed: {common_marker}")
    common_dir = Path(common_value)
    if not common_dir.is_absolute():
        common_dir = git_dir / common_dir
    common_dir = common_dir.resolve(strict=False)
    if not common_dir.is_dir():
        raise SafetyError(f"worktree common Git directory does not exist: {common_dir}")
    return git_dir, common_dir


def _codex_filesystem_config(
    profile: str,
    grants: Sequence[tuple[Path, str]],
    *,
    secret_root: Path,
) -> str:
    rules = [
        "glob_scan_max_depth = 8",
        '":minimal" = "read"',
        f'{_toml_string(Path("/Users"))} = "deny"',
    ]
    home = Path.home().resolve(strict=False)
    if home != Path("/Users"):
        rules.append(f'{_toml_string(home)} = "deny"')
    seen: dict[Path, str] = {}
    for path, access in grants:
        seen[path.resolve(strict=False)] = access
    rules.extend(f'{_toml_string(path)} = "{access}"' for path, access in seen.items())
    for pattern in CODEX_SECRET_DENY_GLOBS:
        rules.append(f'{_toml_string(secret_root / pattern)} = "deny"')
    return f"permissions.{profile}.filesystem={{ {', '.join(rules)} }}"


@dataclass(frozen=True)
class ProcessResult:
    argv: tuple[str, ...]
    returncode: int
    started_at: str
    ended_at: str
    duration_seconds: float
    prompt: bytes
    stdout: bytes
    stderr: bytes
    prompt_path: Path
    stdout_path: Path
    stderr_path: Path

    def persist(self) -> None:
        atomic_write_bytes(self.prompt_path, self.prompt)
        atomic_write_bytes(self.stdout_path, self.stdout)
        atomic_write_bytes(self.stderr_path, self.stderr)


class ProcessRegistry:
    """Thread-safe live process list used by the external cancel command."""

    def __init__(self, path: Path, *, reset: bool = True) -> None:
        self.path = path
        self._mutex = threading.Lock()
        self._lock_path = path.with_name(f".{path.name}.lock")
        if reset:
            with self._mutex, FileLock(self._lock_path):
                atomic_write_json(path, {"schema": "active-processes/v1", "processes": []})

    def _read_unlocked(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"schema": "active-processes/v1", "processes": []}
        return read_json(self.path)

    def snapshot(self) -> list[dict[str, Any]]:
        with self._mutex, FileLock(self._lock_path):
            payload = self._read_unlocked()
            processes = payload.get("processes", [])
            if not isinstance(processes, list):
                raise SafetyError("active-process ledger is malformed")
            return [dict(item) for item in processes if isinstance(item, dict)]

    def add(self, record: dict[str, Any]) -> None:
        with self._mutex, FileLock(self._lock_path):
            payload = self._read_unlocked()
            payload.setdefault("processes", []).append(record)
            atomic_write_json(self.path, payload)

    def remove(self, pid: int) -> None:
        with self._mutex, FileLock(self._lock_path):
            payload = self._read_unlocked()
            payload["processes"] = [item for item in payload.get("processes", []) if item.get("pid") != pid]
            atomic_write_json(self.path, payload)


def process_identity(pid: int) -> str | None:
    """Return a stable token for one live process without trusting PID alone."""

    try:
        result = subprocess.run(
            ["/bin/ps", "-o", "uid=", "-o", "pgid=", "-o", "lstart=", "-p", str(pid)],
            capture_output=True,
            text=True,
            timeout=2,
            env=sanitized_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    fields = result.stdout.strip().split()
    if result.returncode != 0 or len(fields) < 7:
        return None
    uid, pgid = fields[:2]
    started = " ".join(fields[2:])
    return sha256_bytes(f"process-identity/v1\0{pid}\0{uid}\0{pgid}\0{started}".encode("utf-8"))


def validate_process_record(record: dict[str, Any]) -> tuple[bool, str]:
    pid = record.get("pid")
    pgid = record.get("pgid")
    uid = record.get("uid")
    identity = record.get("identity")
    if not isinstance(pid, int) or not isinstance(pgid, int) or pid <= 1 or pgid != pid:
        return False, "invalid pid/pgid"
    if uid != os.getuid() or not isinstance(identity, str):
        return False, "owner or identity mismatch"
    try:
        if os.getpgid(pid) != pgid:
            return False, "process-group mismatch"
    except (ProcessLookupError, PermissionError):
        return False, "process is no longer verifiable"
    if process_identity(pid) != identity:
        return False, "process identity changed"
    return True, "ok"


def _process_group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def terminate_process_group(pid: int, *, grace_seconds: float = 2.0) -> None:
    try:
        leader_group = os.getpgid(pid)
    except ProcessLookupError:
        leader_group = None
    except PermissionError as exc:
        raise SafetyError(f"cannot verify process group for pid {pid}") from exc
    if leader_group is not None and leader_group != pid:
        raise SafetyError(f"refusing to signal pid {pid}: it is not its process-group leader")
    if not _process_group_exists(pid):
        return
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.killpg(pid, signal.SIGTERM)
    deadline = time.monotonic() + grace_seconds
    while time.monotonic() < deadline:
        if not _process_group_exists(pid):
            return
        time.sleep(0.05)
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.killpg(pid, signal.SIGKILL)


def run_process(
    argv: Sequence[str],
    *,
    cwd: Path,
    stdin_text: str,
    label: str,
    raw_dir: Path,
    registry: ProcessRegistry,
    cancel_path: Path,
    timeout_seconds: int,
    env: dict[str, str],
    max_output_bytes: int = 64 * 1024 * 1024,
) -> ProcessResult:
    prompt_path = raw_dir / f"{label}.prompt.txt"
    stdout_path = raw_dir / f"{label}.stdout.jsonl"
    stderr_path = raw_dir / f"{label}.stderr.log"
    started_at = utc_now()
    started = time.monotonic()
    if cancel_path.exists():
        raise CancelledError(f"provider cancelled before start: {label}")
    try:
        process = subprocess.Popen(
            list(argv),
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            start_new_session=True,
            close_fds=True,
        )
    except OSError as exc:
        raise ProviderError(f"cannot start provider {label}: {exc}") from exc
    identity: str | None = None
    identity_deadline = time.monotonic() + 0.5
    while identity is None and time.monotonic() < identity_deadline:
        identity = process_identity(process.pid)
        if identity is None:
            time.sleep(0.01)
    if identity is None:
        terminate_process_group(process.pid)
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.communicate(timeout=3)
        raise SafetyError(f"cannot establish provider process identity: {label}")
    try:
        registry.add(
            {
                "pid": process.pid,
                "pgid": process.pid,
                "uid": os.getuid(),
                "identity": identity,
                "label": label,
                "started_at": started_at,
                "argv_sha256": sha256_bytes("\0".join(argv).encode()),
            }
        )
    except BaseException:
        terminate_process_group(process.pid)
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.communicate(timeout=3)
        raise
    prompt = stdin_text.encode("utf-8")
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    output_lock = threading.Lock()
    output_exceeded = threading.Event()
    stream_errors: list[BaseException] = []
    output_bytes = 0

    def drain(stream: Any, chunks: list[bytes]) -> None:
        nonlocal output_bytes
        try:
            while chunk := stream.read(64 * 1024):
                with output_lock:
                    remaining = max_output_bytes - output_bytes
                    if remaining > 0:
                        chunks.append(chunk[:remaining])
                    output_bytes += len(chunk)
                    if output_bytes > max_output_bytes:
                        output_exceeded.set()
        except BaseException as exc:  # surfaced on the controller thread
            stream_errors.append(exc)

    def feed() -> None:
        try:
            assert process.stdin is not None
            process.stdin.write(prompt)
            process.stdin.close()
        except BrokenPipeError:
            return
        except BaseException as exc:  # surfaced on the controller thread
            stream_errors.append(exc)

    assert process.stdout is not None and process.stderr is not None
    readers = [
        threading.Thread(target=drain, args=(process.stdout, stdout_chunks), daemon=True),
        threading.Thread(target=drain, args=(process.stderr, stderr_chunks), daemon=True),
    ]
    writer = threading.Thread(target=feed, daemon=True)
    for thread in readers:
        thread.start()
    writer.start()
    pending_error: BaseException | None = None
    try:
        while process.poll() is None:
            if output_exceeded.is_set():
                pending_error = ProviderError(f"provider output exceeded {max_output_bytes} byte safety limit: {label}")
                break
            if cancel_path.exists():
                pending_error = CancelledError(f"provider cancelled: {label}")
                break
            if time.monotonic() - started > timeout_seconds:
                pending_error = ProviderError(f"provider timed out after {timeout_seconds}s: {label}", retryable=False)
                break
            time.sleep(0.05)
        if pending_error is not None:
            terminate_process_group(process.pid, grace_seconds=0.2)
            with contextlib.suppress(subprocess.TimeoutExpired):
                process.wait(timeout=3)
        # The parent may have exited after forking children which inherited the
        # pipes. Drain that owned group before joining the readers.
        terminate_process_group(process.pid, grace_seconds=0.2)
        writer.join(timeout=3)
        for thread in readers:
            thread.join(timeout=3)
        if writer.is_alive() or any(thread.is_alive() for thread in readers):
            pending_error = pending_error or SafetyError(f"provider streams did not close: {label}")
        if output_exceeded.is_set():
            pending_error = pending_error or ProviderError(
                f"provider output exceeded {max_output_bytes} byte safety limit: {label}"
            )
        if stream_errors:
            pending_error = pending_error or ProviderError(f"provider stream failed: {label}: {stream_errors[0]}")
        if cancel_path.exists() and pending_error is None:
            pending_error = CancelledError(f"provider cancelled: {label}")
    finally:
        try:
            terminate_process_group(process.pid, grace_seconds=0.2)
            with contextlib.suppress(subprocess.TimeoutExpired):
                process.wait(timeout=3)
        finally:
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    with contextlib.suppress(OSError):
                        stream.close()
            registry.remove(process.pid)
    stdout = b"".join(stdout_chunks)
    stderr = b"".join(stderr_chunks)
    if pending_error is not None:
        raise pending_error
    return ProcessResult(
        argv=tuple(argv),
        returncode=int(process.returncode),
        started_at=started_at,
        ended_at=utc_now(),
        duration_seconds=round(time.monotonic() - started, 3),
        prompt=prompt,
        stdout=stdout,
        stderr=stderr,
        prompt_path=prompt_path,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
    )


@dataclass(frozen=True)
class ProviderOutput:
    provider: str
    requested_model: str
    actual_model: str
    text: str
    attempts: tuple[dict[str, Any], ...]


class ProviderAdapter:
    provider = "provider"

    def __init__(self, binary: str, primary_model: str, fallback_model: str, effort: str) -> None:
        self.binary = resolve_binary(binary)
        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self.effort = effort

    def build_argv(self, *, model: str, mode: str, run_dir: Path, repo: Path, worktree: Path | None) -> list[str]:
        raise NotImplementedError

    def parse(self, result: ProcessResult, *, requested_model: str, mode: str) -> tuple[str, str]:
        raise NotImplementedError

    def command_preview(self, *, mode: str, run_dir: Path, repo: Path, worktree: Path | None = None) -> list[dict[str, Any]]:
        return [
            {"provider": self.provider, "model": model, "argv": self.build_argv(model=model, mode=mode, run_dir=run_dir, repo=repo, worktree=worktree)}
            for model in (self.primary_model, self.fallback_model)
        ]

    def run(
        self,
        prompt: str,
        *,
        mode: str,
        run_dir: Path,
        repo: Path,
        worktree: Path | None,
        registry: ProcessRegistry,
        cancel_path: Path,
        timeout_seconds: int,
        label: str,
        independence_barrier: threading.Barrier | None = None,
    ) -> ProviderOutput:
        attempts: list[dict[str, Any]] = []
        results: list[ProcessResult] = []
        output: ProviderOutput | None = None
        pending_error: BaseException | None = None
        try:
            for index, model in enumerate((self.primary_model, self.fallback_model), start=1):
                argv = self.build_argv(model=model, mode=mode, run_dir=run_dir, repo=repo, worktree=worktree)
                result = run_process(
                    argv,
                    cwd=(worktree if mode in {"implement", "correct"} and worktree else run_dir),
                    stdin_text=prompt,
                    label=f"{label}-attempt-{index}",
                    raw_dir=run_dir / "raw",
                    registry=registry,
                    cancel_path=cancel_path,
                    timeout_seconds=timeout_seconds,
                    env=sanitized_environment(),
                )
                results.append(result)
                stderr = result.stderr.decode("utf-8", errors="replace")
                attempt = {
                    "provider": self.provider,
                    "attempt": index,
                    "requested_model": model,
                    "argv": list(result.argv),
                    "started_at": result.started_at,
                    "ended_at": result.ended_at,
                    "duration_seconds": result.duration_seconds,
                    "returncode": result.returncode,
                    "stdout": str(result.stdout_path),
                    "stdout_sha256": sha256_bytes(result.stdout),
                    "stderr": str(result.stderr_path),
                    "stderr_sha256": sha256_bytes(result.stderr),
                }
                if result.returncode != 0:
                    combined = (result.stdout.decode("utf-8", errors="replace") + "\n" + stderr).lower()
                    retryable = any(marker in combined for marker in RETRYABLE_MARKERS)
                    attempt["status"] = "retryable_failure" if retryable else "failure"
                    attempts.append(attempt)
                    if index == 1 and retryable:
                        continue
                    raise ProviderError(f"{self.provider} failed with exit {result.returncode}", retryable=retryable)
                try:
                    text, actual_model = self.parse(result, requested_model=model, mode=mode)
                except ProviderError:
                    attempt["status"] = "malformed_output"
                    attempts.append(attempt)
                    raise
                attempt.update({"status": "success", "actual_model": actual_model, "output_sha256": sha256_bytes(text.encode())})
                attempts.append(attempt)
                output = ProviderOutput(self.provider, model, actual_model, text, tuple(attempts))
                break
            if output is None:
                raise ProviderError(f"{self.provider} exhausted same-vendor fallbacks")
        except BaseException as exc:
            pending_error = exc
        finally:
            if independence_barrier is not None:
                try:
                    independence_barrier.wait(timeout=max(30, timeout_seconds * 3))
                except threading.BrokenBarrierError as exc:
                    pending_error = pending_error or SafetyError("independent provider barrier broke before both opinions completed")
        # No provider output or prompt touches disk until both independent processes
        # have exited and crossed the barrier.
        for result in results:
            result.persist()
        if pending_error is not None:
            # Carry the attempt records so the controller can journal failures
            # into the manifest (otherwise failed runs show "attempts": []).
            pending_error.attempts = tuple(attempts)
            raise pending_error
        assert output is not None
        return output


def _json_lines(payload: bytes, label: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for number, line in enumerate(payload.decode("utf-8", errors="strict").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ProviderError(f"malformed JSONL at {label}:{number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ProviderError(f"non-object JSONL event at {label}:{number}")
        events.append(value)
    if not events:
        raise ProviderError(f"provider emitted no JSON events: {label}")
    return events


class ClaudeAdapter(ProviderAdapter):
    provider = "claude"

    def build_argv(self, *, model: str, mode: str, run_dir: Path, repo: Path, worktree: Path | None) -> list[str]:
        target = worktree or repo
        return [
            self.binary,
            "--print",
            "--safe-mode",
            "--model",
            model,
            "--effort",
            self.effort,
            "--output-format",
            "stream-json",
            "--verbose",
            "--tools",
            "Read,Grep,Glob",
            "--disallowedTools",
            "Bash,Edit,Write,WebFetch,WebSearch,Task,Skill,NotebookEdit,EnterPlanMode,ExitPlanMode",
            "--permission-mode",
            "dontAsk",
            "--strict-mcp-config",
            "--mcp-config",
            '{"mcpServers":{}}',
            "--no-chrome",
            "--disable-slash-commands",
            "--no-session-persistence",
            "--setting-sources",
            "",
            "--settings",
            json.dumps({"hooks": {}, "permissions": {"allow": [], "deny": list(CLAUDE_SECRET_DENIES)}}),
            "--add-dir",
            str(target),
            "-",
        ]

    def parse(self, result: ProcessResult, *, requested_model: str, mode: str) -> tuple[str, str]:
        events = _json_lines(result.stdout, result.stdout_path)
        output = ""
        actual_models: list[str] = []
        saw_safe_init = False
        for event in events:
            event_type = str(event.get("type", ""))
            if event_type == "assistant":
                message = event.get("message", {})
                if isinstance(message, dict):
                    if isinstance(message.get("model"), str):
                        actual_models.append(message["model"])
                    content = message.get("content", [])
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "tool_use":
                                tool = str(block.get("name", ""))
                                if tool not in CLAUDE_ALLOWED_TOOLS:
                                    raise ProviderError(f"Claude emitted forbidden tool event: {tool or '<missing>'}")
            elif event_type == "result":
                if event.get("is_error"):
                    raise ProviderError(f"Claude result reported an error: {event.get('result', '')}")
                if isinstance(event.get("result"), str):
                    output = event["result"]
                usage = event.get("modelUsage") or event.get("model_usage")
                if isinstance(usage, dict):
                    actual_models.extend(str(key) for key in usage)
            elif event_type == "system":
                if event.get("subtype") == "init":
                    saw_safe_init = True
                    tools = event.get("tools", [])
                    if not isinstance(tools, list) or set(map(str, tools)) != CLAUDE_ALLOWED_TOOLS:
                        raise ProviderError("Claude init did not attest the exact read-only tool set")
                    for key in ("mcp_servers", "plugins", "hooks", "skills", "commands"):
                        value = event.get(key, [])
                        if value not in (None, [], {}):
                            raise ProviderError(f"Claude init attested unexpected {key}")
            elif event_type in {"user", "rate_limit_event"}:
                continue
            elif "mcp" in event_type.lower() or "tool" in event_type.lower():
                raise ProviderError(f"Claude emitted unexpected tool/MCP event: {event_type}")
        if not output.strip():
            raise ProviderError("Claude result did not contain non-empty text")
        if not saw_safe_init:
            raise ProviderError("Claude output omitted the safe init attestation")
        actual = actual_models[-1] if actual_models else requested_model
        if not actual.lower().startswith("claude"):
            raise ProviderError(f"Claude adapter reported a non-Claude model: {actual}")
        return output.strip() + "\n", actual


class CodexAdapter(ProviderAdapter):
    provider = "codex"

    _DISABLED_FEATURES = (
        "apps",
        "browser_use",
        "browser_use_external",
        "browser_use_full_cdp_access",
        "chronicle",
        "computer_use",
        "enable_fanout",
        "enable_mcp_apps",
        "hooks",
        "image_generation",
        "in_app_browser",
        "memories",
        "multi_agent",
        "multi_agent_v2",
        "network_proxy",
        "plugins",
        "remote_plugin",
        "shell_snapshot",
        "skill_mcp_dependency_install",
        "standalone_web_search",
        # web_search_cached / web_search_request intentionally omitted: current
        # Codex CLI (0.144+) deprecated those [features] sub-flags in favor of the
        # top-level `web_search` key (set to "disabled" below), and passing them
        # emits deprecation warnings as error-type item events that abort parsing.
        "workspace_dependencies",
    )

    def build_argv(self, *, model: str, mode: str, run_dir: Path, repo: Path, worktree: Path | None) -> list[str]:
        writable = mode in {"implement", "correct"}
        stage = run_dir.resolve(strict=False)
        if writable:
            if worktree is None:
                raise SafetyError(f"Codex {mode} mode requires an isolated worktree")
            target = worktree.resolve(strict=False)
            git_dir, common_git_dir = _git_permission_paths(target)
            profile = CODEX_WRITE_PERMISSION_PROFILE
            grants = [(common_git_dir, "read"), (target, "write"), (stage, "write"), (git_dir, "write")]
            cwd = target
        else:
            target = repo.resolve(strict=False)
            profile = CODEX_READ_PERMISSION_PROFILE
            grants = [(target, "read"), (stage, "read")]
            cwd = stage
        filesystem_config = _codex_filesystem_config(profile, grants, secret_root=target)
        argv = [
            self.binary,
            "exec",
            "--json",
            "--ephemeral",
            # The read/plan stage runs from the per-run staging dir, which is not a
            # git repository; without this flag `codex exec` aborts before inference.
            "--skip-git-repo-check",
            "--ignore-user-config",
            "--ignore-rules",
            "--strict-config",
            "--model",
            model,
            "--cd",
            str(cwd),
            "--config",
            'approval_policy="never"',
            "--config",
            f'default_permissions="{profile}"',
            "--config",
            filesystem_config,
            "--config",
            f"permissions.{profile}.network.enabled=false",
            "--config",
            f'model_reasoning_effort="{self.effort}"',
            "--config",
            'web_search="disabled"',
            "--config",
            "project_doc_max_bytes=0",
            "--config",
            "project_doc_fallback_filenames=[]",
            "--config",
            'shell_environment_policy.inherit="core"',
            "--config",
            "allow_login_shell=false",
            "--config",
            "shell_environment_policy.ignore_default_excludes=false",
            "--config",
            "shell_environment_policy.exclude=[]",
            "-",
        ]
        for feature in self._DISABLED_FEATURES:
            argv[2:2] = ["--disable", feature]
        return argv

    def build_qa_argv(self, command: Sequence[str], *, worktree: Path, temp_dir: Path) -> list[str]:
        target = worktree.resolve(strict=False)
        temporary = temp_dir.resolve(strict=False)
        git_dir, common_git_dir = _git_permission_paths(target)
        filesystem = _codex_filesystem_config(
            CODEX_QA_PERMISSION_PROFILE,
            [(common_git_dir, "read"), (git_dir, "read"), (target, "write"), (temporary, "write")],
            secret_root=target,
        )
        return [
            self.binary,
            "sandbox",
            "-c",
            f'default_permissions="{CODEX_QA_PERMISSION_PROFILE}"',
            "-c",
            filesystem,
            "-c",
            f"permissions.{CODEX_QA_PERMISSION_PROFILE}.network.enabled=false",
            "-P",
            CODEX_QA_PERMISSION_PROFILE,
            "--",
            *command,
        ]

    def parse(self, result: ProcessResult, *, requested_model: str, mode: str) -> tuple[str, str]:
        events = _json_lines(result.stdout, result.stdout_path)
        allowed_items = CODEX_WRITE_ITEM_TYPES if mode in {"implement", "correct"} else CODEX_READ_ITEM_TYPES
        messages: list[str] = []
        actual_model = requested_model
        for event in events:
            event_type = str(event.get("type", ""))
            if event_type in CODEX_META_EVENT_TYPES:
                model = event.get("model")
                if isinstance(model, str):
                    actual_model = model
                continue
            if event_type in {"error", "turn.failed"}:
                raise ProviderError(f"Codex emitted failure event: {event}")
            if not event_type.startswith("item."):
                raise ProviderError(f"Codex emitted unknown event type: {event_type or '<missing>'}")
            item = event.get("item")
            if not isinstance(item, dict):
                raise ProviderError(f"Codex item event missing object: {event_type}")
            item_type = str(item.get("type", ""))
            lowered = item_type.lower()
            if any(marker in lowered for marker in ("mcp", "app", "dynamic", "collaboration", "web_search", "image")):
                raise ProviderError(f"Codex emitted forbidden item event: {item_type}")
            if item_type not in allowed_items:
                raise ProviderError(f"Codex emitted unsupported item event: {item_type or '<missing>'}")
            if event_type == "item.completed" and item_type == "agent_message":
                text = item.get("text")
                if isinstance(text, str) and text.strip():
                    messages.append(text)
        if not messages:
            raise ProviderError("Codex result did not contain an agent_message")
        if not actual_model.lower().startswith(("gpt", "o")):
            raise ProviderError(f"Codex adapter reported a non-OpenAI model: {actual_model}")
        return messages[-1].strip() + "\n", actual_model
