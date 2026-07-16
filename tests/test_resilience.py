from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from crosscheck_council.adapters import (
    ProcessRegistry,
    ProcessResult,
    ProviderAdapter,
    run_process,
    sanitized_environment,
)
from crosscheck_council.controller import Controller, ControllerConfig, RAW_RETENTION_DAYS
from crosscheck_council.errors import CancelledError, ProviderError, StateError
from crosscheck_council.storage import (
    FileLock,
    Store,
    atomic_write_json,
    atomic_write_text,
    read_json,
    sha256_bytes,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]


FAKE_PROVIDER_SCRIPT = r"""
import json
import sys
import time

scenario, model = sys.argv[1:3]
# Keep the process alive long enough for the controller to bind its PID identity.
time.sleep(0.08)
if scenario == "fallback" and model == "fake-primary":
    print("429 capacity temporarily unavailable", file=sys.stderr)
    raise SystemExit(75)
if scenario == "auth":
    print("401 Unauthorized: authentication failed", file=sys.stderr)
    raise SystemExit(1)
if scenario == "malformed":
    print("{definitely-not-json")
    raise SystemExit(0)
print(json.dumps({"text": "fallback answer\n", "model": model}, sort_keys=True))
"""


class SubprocessJsonAdapter(ProviderAdapter):
    """Small same-vendor provider double that still exercises real subprocesses."""

    provider = "fake-vendor"

    def __init__(self, scenario: str) -> None:
        super().__init__(sys.executable, "fake-primary", "fake-fallback", "test")
        self.scenario = scenario
        self.build_calls: list[str] = []

    def build_argv(
        self,
        *,
        model: str,
        mode: str,
        run_dir: Path,
        repo: Path,
        worktree: Path | None,
    ) -> list[str]:
        del mode, run_dir, repo, worktree
        self.build_calls.append(model)
        return [self.binary, "-c", FAKE_PROVIDER_SCRIPT, self.scenario, model]

    def parse(self, result: ProcessResult, *, requested_model: str, mode: str) -> tuple[str, str]:
        del requested_model, mode
        try:
            payload = json.loads(result.stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderError("malformed provider JSON") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
            raise ProviderError("malformed provider JSON object")
        actual_model = payload.get("model")
        if not isinstance(actual_model, str) or not actual_model.startswith("fake-"):
            raise ProviderError("provider model attestation is missing or cross-vendor")
        return payload["text"], actual_model


class AtomicStorageTests(unittest.TestCase):
    def test_atomic_json_overwrite_is_private_and_failed_replace_preserves_previous_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private" / "nested" / "state.json"
            atomic_write_json(path, {"generation": 1})

            self.assertEqual(read_json(path), {"generation": 1})
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)

            atomic_write_json(path, {"generation": 2})
            self.assertEqual(read_json(path), {"generation": 2})
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

            with mock.patch("crosscheck_council.storage.os.replace", side_effect=OSError("simulated crash")):
                with self.assertRaisesRegex(OSError, "simulated crash"):
                    atomic_write_json(path, {"generation": 3})

            self.assertEqual(read_json(path), {"generation": 2})
            self.assertEqual(list(path.parent.glob(f".{path.name}.*")), [])

    def test_immutable_atomic_write_rejects_overwrite_without_changing_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            atomic_write_json(path, {"immutable": True}, overwrite=False)
            before = path.read_bytes()

            with self.assertRaisesRegex(StateError, "immutable"):
                atomic_write_json(path, {"immutable": False}, overwrite=False)

            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)


class LockingTests(unittest.TestCase):
    def test_nonblocking_flock_rejects_concurrent_process_then_recovers_stale_metadata(self) -> None:
        child_code = """
import sys
from pathlib import Path
from crosscheck_council.errors import StateError
from crosscheck_council.storage import FileLock

try:
    with FileLock(Path(sys.argv[1]), blocking=False):
        raise SystemExit(0)
except StateError:
    raise SystemExit(23)
"""
        with tempfile.TemporaryDirectory() as directory:
            lock_path = Path(directory) / "state" / "runtime" / "run.lock"
            env = {**os.environ, "PYTHONPATH": str(ROOT)}
            with FileLock(lock_path, blocking=False):
                contender = subprocess.run(
                    [sys.executable, "-c", child_code, str(lock_path)],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                self.assertEqual(contender.returncode, 23, contender.stderr)

            # A dead holder's PID text is not authority; only the kernel flock is.
            lock_path.write_text("999999\n", encoding="ascii")
            lock_path.chmod(0o644)
            with FileLock(lock_path, blocking=False):
                self.assertEqual(lock_path.read_text(encoding="ascii"), f"{os.getpid()}\n")
                self.assertEqual(stat.S_IMODE(lock_path.stat().st_mode), 0o600)


class RetentionTests(unittest.TestCase):
    def test_raw_retention_removes_only_expired_raw_logs_and_preserves_plans_and_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            controller = Controller(
                ControllerConfig(
                    home=Path(directory) / "state",
                    claude_bin=sys.executable,
                    codex_bin=sys.executable,
                    warn_disk_gib=0,
                    block_disk_gib=0,
                )
            )
            run_dir = controller.store.run_dir("retention-run", create=True)
            expired_raw = run_dir / "raw" / "provider" / "expired.log"
            current_raw = run_dir / "raw" / "provider" / "current.log"
            final_plan = run_dir / "artifacts" / "Plan-retention-run-Final.md"
            approval = run_dir / "receipts" / "approval.json"
            for path, content in (
                (expired_raw, "expired raw\n"),
                (current_raw, "current raw\n"),
                (final_plan, "final plan\n"),
                (approval, "{}\n"),
            ):
                atomic_write_text(path, content)

            expired_at = datetime.now(timezone.utc) - timedelta(days=RAW_RETENTION_DAYS + 1)
            old_timestamp = expired_at.timestamp()
            for path in (expired_raw, final_plan, approval):
                os.utime(path, (old_timestamp, old_timestamp))

            self.assertEqual(controller._prune_raw_logs(), 1)
            self.assertFalse(expired_raw.exists())
            self.assertTrue(current_raw.is_file())
            self.assertTrue(final_plan.is_file())
            self.assertTrue(approval.is_file())
            self.assertEqual(stat.S_IMODE(final_plan.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(approval.stat().st_mode), 0o600)


class ProviderResilienceTests(unittest.TestCase):
    def run_adapter(self, adapter: SubprocessJsonAdapter) -> tuple[Path, object]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        workspace = root / "provider"
        workspace.mkdir(mode=0o700)
        registry = ProcessRegistry(root / "runtime" / "active-processes.json")
        output = adapter.run(
            "same evidence packet",
            mode="plan",
            run_dir=workspace,
            repo=root,
            worktree=None,
            registry=registry,
            cancel_path=root / "cancel.requested",
            timeout_seconds=3,
            label="fake-plan",
        )
        self.assertEqual(registry.snapshot(), [])
        return root, output

    def test_retryable_primary_uses_same_vendor_fallback_and_attests_model_and_hashes(self) -> None:
        adapter = SubprocessJsonAdapter("fallback")
        root, output = self.run_adapter(adapter)

        self.assertEqual(adapter.build_calls, ["fake-primary", "fake-fallback"])
        self.assertEqual(output.provider, "fake-vendor")
        self.assertEqual(output.requested_model, "fake-fallback")
        self.assertEqual(output.actual_model, "fake-fallback")
        self.assertEqual(output.text, "fallback answer\n")
        self.assertEqual(len(output.attempts), 2)

        first, second = output.attempts
        self.assertEqual(
            (first["provider"], first["attempt"], first["requested_model"], first["status"]),
            ("fake-vendor", 1, "fake-primary", "retryable_failure"),
        )
        self.assertEqual(
            (second["provider"], second["attempt"], second["requested_model"], second["actual_model"], second["status"]),
            ("fake-vendor", 2, "fake-fallback", "fake-fallback", "success"),
        )
        self.assertEqual(second["output_sha256"], sha256_bytes(output.text.encode("utf-8")))
        for attempt in output.attempts:
            self.assertEqual(Path(attempt["stdout"]).parent, root / "provider" / "raw")
            self.assertEqual(attempt["stdout_sha256"], sha256_file(Path(attempt["stdout"])))
            self.assertEqual(attempt["stderr_sha256"], sha256_file(Path(attempt["stderr"])))
            self.assertEqual(Path(attempt["stdout"]).stat().st_mode & 0o777, 0o600)
            self.assertEqual(Path(attempt["stderr"]).stat().st_mode & 0o777, 0o600)
            self.assertEqual(Path(attempt["argv"][0]).resolve(), Path(adapter.binary))

    def test_auth_like_failure_is_nonretryable_and_never_invokes_fallback(self) -> None:
        adapter = SubprocessJsonAdapter("auth")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "provider"
            workspace.mkdir()
            registry = ProcessRegistry(root / "runtime" / "active-processes.json")
            with self.assertRaisesRegex(ProviderError, "failed with exit") as raised:
                adapter.run(
                    "prompt",
                    mode="plan",
                    run_dir=workspace,
                    repo=root,
                    worktree=None,
                    registry=registry,
                    cancel_path=root / "cancel.requested",
                    timeout_seconds=3,
                    label="auth",
                )

            self.assertFalse(raised.exception.retryable)
            self.assertEqual(adapter.build_calls, ["fake-primary"])
            self.assertIn("401 Unauthorized", (workspace / "raw" / "auth-attempt-1.stderr.log").read_text())
            self.assertFalse((workspace / "raw" / "auth-attempt-2.stderr.log").exists())
            self.assertEqual(registry.snapshot(), [])
            # Failed attempts must ride the exception so the controller can
            # journal them into the manifest (failed runs used to show []).
            failed_attempts = getattr(raised.exception, "attempts", ())
            self.assertEqual(len(failed_attempts), 1)
            self.assertEqual(failed_attempts[0]["status"], "failure")
            self.assertEqual(failed_attempts[0]["requested_model"], "fake-primary")

    def test_malformed_provider_json_fails_closed_without_fallback(self) -> None:
        adapter = SubprocessJsonAdapter("malformed")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "provider"
            workspace.mkdir()
            registry = ProcessRegistry(root / "runtime" / "active-processes.json")
            with self.assertRaisesRegex(ProviderError, "malformed provider JSON"):
                adapter.run(
                    "prompt",
                    mode="plan",
                    run_dir=workspace,
                    repo=root,
                    worktree=None,
                    registry=registry,
                    cancel_path=root / "cancel.requested",
                    timeout_seconds=3,
                    label="malformed",
                )

            self.assertEqual(adapter.build_calls, ["fake-primary"])
            self.assertEqual(
                (workspace / "raw" / "malformed-attempt-1.stdout.jsonl").read_text().strip(),
                "{definitely-not-json",
            )
            self.assertEqual(registry.snapshot(), [])

    def test_timeout_and_prestart_cancel_are_nonretrying_terminal_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "raw"
            raw.mkdir()
            registry = ProcessRegistry(root / "runtime" / "active-processes.json")
            with self.assertRaisesRegex(ProviderError, "timed out") as raised:
                run_process(
                    [sys.executable, "-c", "import time; time.sleep(30)"],
                    cwd=root,
                    stdin_text="",
                    label="timeout",
                    raw_dir=raw,
                    registry=registry,
                    cancel_path=root / "cancel.requested",
                    timeout_seconds=0,
                    env=sanitized_environment(),
                )
            self.assertFalse(raised.exception.retryable)
            self.assertEqual(registry.snapshot(), [])

            cancel_path = root / "cancel.requested"
            cancel_path.write_text("cancel\n", encoding="utf-8")
            with self.assertRaisesRegex(CancelledError, "before start"):
                run_process(
                    [sys.executable, "-c", "raise SystemExit(0)"],
                    cwd=root,
                    stdin_text="",
                    label="cancelled",
                    raw_dir=raw,
                    registry=registry,
                    cancel_path=cancel_path,
                    timeout_seconds=3,
                    env=sanitized_environment(),
                )
            self.assertEqual(registry.snapshot(), [])


if __name__ == "__main__":
    unittest.main()
