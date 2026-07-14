from __future__ import annotations

import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

from crosscheck_council.adapters import (
    ClaudeAdapter,
    ProcessRegistry,
    ProcessResult,
    run_process,
    sanitized_environment,
)
from crosscheck_council.cli import build_parser
from crosscheck_council.controller import Controller, ControllerConfig
from crosscheck_council.errors import CancelledError, ProviderError, SafetyError
from crosscheck_council.repository import (
    capture_worktree_changes,
    commit_worktree_changes,
    create_worktree,
    redact_text,
    run_git,
)
from crosscheck_council.schemas import EVIDENCE_SCHEMA, RUN_SCHEMA, VERIFICATION_SCHEMA
from crosscheck_council.storage import atomic_write_json, atomic_write_text, read_json, sha256_file
from crosscheck_council.storage import Store


ROOT = Path(__file__).resolve().parents[1]


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=True,
        env={**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"},
    )


def initialize_repo(root: Path) -> str:
    git(root.parent, "init", "-q", "--initial-branch=main", str(root))
    (root / "tracked.txt").write_text("original\n", encoding="utf-8")
    git(root, "add", "tracked.txt")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "initial")
    return git(root, "rev-parse", "HEAD").stdout.strip()


def minimal_manifest(run_id: str, repository: Path, sha: str, *, status: str) -> dict:
    now = "2026-07-14T12:00:00Z"
    return {
        "schema": RUN_SCHEMA,
        "run_id": run_id,
        "status": status,
        "created_at": now,
        "updated_at": now,
        "repository": {
            "path": str(repository),
            "target_sha": sha,
            "dirty": False,
            "dirty_fingerprint": "0" * 64,
            "remote_config_sha256": "0" * 64,
        },
        "models": {"claude": {}, "codex": {}},
        "artifacts": {},
        "attempts": [],
    }


class TTY(io.StringIO):
    def isatty(self) -> bool:
        return True


class CoreCliTests(unittest.TestCase):
    def test_store_rejects_symlink_home_and_run_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "real"
            real.mkdir()
            linked = root / "linked"
            linked.symlink_to(real, target_is_directory=True)
            with self.assertRaises(SafetyError):
                Store(linked)
            store = Store(root / "state")
            outside = root / "outside-run"
            outside.mkdir()
            (store.runs / "linked-run").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(SafetyError):
                store.run_dir("linked-run")

    def test_verify_command_does_not_overwrite_subcommand(self) -> None:
        args = build_parser().parse_args(["verify", "run-1", "--command", "python -m unittest"])
        self.assertEqual(args.command, "verify")
        self.assertEqual(args.verification_commands, ["python -m unittest"])

    def test_source_tree_launcher_smoke(self) -> None:
        result = subprocess.run([str(ROOT / "bin/crosscheckctl"), "--help"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("transfer", result.stdout)

    def test_doctor_reports_missing_providers_and_disk_without_throwing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            controller = Controller(
                ControllerConfig(
                    home=Path(directory) / "home",
                    claude_bin="definitely-missing-claude",
                    codex_bin="definitely-missing-codex",
                )
            )
            with mock.patch.object(controller, "_disk_free_gib", return_value=10.0):
                result = controller.doctor()
            self.assertFalse(result["ok"])
            self.assertTrue(result["disk"]["blocked"])
            self.assertFalse(result["claude"]["available"])
            self.assertFalse(result["codex"]["available"])

    def test_latest_run_can_be_scoped_to_one_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            first_repo = base / "first"
            second_repo = base / "second"
            first_repo.mkdir()
            second_repo.mkdir()
            controller = Controller(ControllerConfig(home=base / "state"))
            for run_id, repository in (("first-run", first_repo), ("second-run", second_repo)):
                controller.store.run_dir(run_id, create=True)
                controller.store.save_manifest(
                    run_id,
                    minimal_manifest(run_id, repository, "0" * 40, status="dry_run"),
                )
                time.sleep(0.01)
            self.assertEqual(controller.status()["run_id"], "second-run")
            self.assertEqual(controller.status(repository=first_repo)["run_id"], "first-run")

    def test_plan_dry_run_writes_private_immutable_evidence_and_explicit_models(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            initialize_repo(repo)
            controller = Controller(
                ControllerConfig(
                    home=root / "state",
                    claude_bin=sys.executable,
                    codex_bin=sys.executable,
                    block_disk_gib=0,
                    warn_disk_gib=0,
                )
            )
            manifest = controller.plan(repo, "make a safe change", run_id="dry-run-test", dry_run=True)
            self.assertEqual(manifest["status"], "dry_run")
            self.assertEqual(manifest["models"]["claude"]["primary"], controller.config.claude_primary)
            self.assertEqual(manifest["models"]["codex"]["fallback"], controller.config.codex_fallback)
            evidence = Path(manifest["evidence"]["path"])
            self.assertEqual(stat.S_IMODE(evidence.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(evidence.parent.stat().st_mode), 0o700)
            self.assertEqual(sha256_file(evidence), manifest["evidence"]["sha256"])
            self.assertTrue((evidence.parent / "command-plan.json").is_file())


class RedactionAndApprovalTests(unittest.TestCase):
    def test_redacts_structured_assignments_urls_tokens_and_pem(self) -> None:
        secrets = [
            "json-secret",
            "toml secret",
            "dotenv-secret",
            "bearer-secret",
            "url-password",
            "db-password",
            "redis-password",
            "service-role-secret",
            "sk-abcdefgh12345678",
            "private-material",
        ]
        source = "\n".join(
            [
                '{"api_key": "json-secret"}',
                "token = 'toml secret'",
                "OPENAI_API_KEY=dotenv-secret",
                "Authorization: Bearer bearer-secret",
                "https://user:url-password@example.test/path",
                'DATABASE_URL="postgres://user:db-password@db/test"',
                "REDIS_URL=redis://:redis-password@cache",
                "SUPABASE_SERVICE_ROLE_KEY=service-role-secret",
                'const credential = "sk-abcdefgh12345678";',
                "-----BEGIN RSA PRIVATE KEY-----\nprivate-material\n-----END RSA PRIVATE KEY-----",
            ]
        )
        redacted = redact_text(source)
        for secret in secrets:
            self.assertNotIn(secret, redacted)
        self.assertIn("[REDACTED", redacted)

    def test_approval_is_interactive_hash_bound_and_show_accepts_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / "repo"
            sha = initialize_repo(repo)
            controller = Controller(ControllerConfig(home=base / "state"))
            run_id = "approval-test"
            run_dir = controller.store.run_dir(run_id, create=True)
            evidence = {
                "schema": EVIDENCE_SCHEMA,
                "run_id": run_id,
                "created_at": "2026-07-14T12:00:00Z",
                "request": "test",
                "repository": {},
                "constraints": [],
                "environment": {},
            }
            evidence_path = run_dir / "evidence.json"
            atomic_write_json(evidence_path, evidence, overwrite=False)
            final_path = run_dir / "artifacts" / f"Plan-{run_id}-Final.md"
            atomic_write_text(final_path, "approved plan\n", overwrite=False)
            manifest = minimal_manifest(run_id, repo, sha, status="awaiting_approval")
            manifest["evidence"] = {
                "path": str(evidence_path),
                "sha256": sha256_file(evidence_path),
                "bytes": evidence_path.stat().st_size,
            }
            manifest["artifacts"]["final_plan"] = {
                "path": str(final_path),
                "sha256": sha256_file(final_path),
                "bytes": final_path.stat().st_size,
            }
            controller.store.save_manifest(run_id, manifest)
            shown = controller.show(run_id, final_path.name)
            self.assertEqual(shown["artifact"], "final_plan")
            expected = sha256_file(final_path)[:12]
            receipt = controller.approve(run_id, stdin=TTY(f"APPROVE {expected}\n"), stdout=TTY())
            self.assertEqual(receipt["plan_sha256"], sha256_file(final_path))
            atomic_write_text(final_path, "tampered\n")
            with self.assertRaises(SafetyError):
                controller._verified_approval(run_id, controller.status(run_id))


class ProcessSafetyTests(unittest.TestCase):
    def test_provider_output_is_capped_while_process_is_running(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "raw"
            raw.mkdir()
            registry = ProcessRegistry(root / "active.json")
            script = "import os; os.write(1, b'x' * 65536)"
            with self.assertRaisesRegex(ProviderError, "output exceeded"):
                run_process(
                    [sys.executable, "-c", script],
                    cwd=root,
                    stdin_text="",
                    label="noisy-provider",
                    raw_dir=raw,
                    registry=registry,
                    cancel_path=root / "cancel",
                    timeout_seconds=10,
                    env=sanitized_environment(),
                    max_output_bytes=1024,
                )
            self.assertEqual(registry.snapshot(), [])

    def test_registry_add_failure_reaps_started_provider(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "raw"
            raw.mkdir()
            pid_path = root / "provider.pid"

            class FailingRegistry:
                def add(self, record: dict) -> None:
                    deadline = time.monotonic() + 1
                    while not pid_path.exists() and time.monotonic() < deadline:
                        time.sleep(0.01)
                    raise OSError("ledger unavailable")

                def remove(self, pid: int) -> None:
                    raise AssertionError("unregistered process must not be removed")

            script = "import os,pathlib,sys,time;pathlib.Path(sys.argv[1]).write_text(str(os.getpid()));time.sleep(30)"
            with self.assertRaisesRegex(OSError, "ledger unavailable"):
                run_process(
                    [sys.executable, "-c", script, str(pid_path)],
                    cwd=root,
                    stdin_text="",
                    label="ledger-failure",
                    raw_dir=raw,
                    registry=FailingRegistry(),  # type: ignore[arg-type]
                    cancel_path=root / "cancel",
                    timeout_seconds=30,
                    env=sanitized_environment(),
                )
            pid = int(pid_path.read_text())
            probe = subprocess.run(["/bin/ps", "-p", str(pid), "-o", "stat="], text=True, capture_output=True)
            self.assertTrue(probe.returncode != 0 or not probe.stdout.strip() or "Z" in probe.stdout)

    def test_idle_cancel_terminalizes_and_never_signals_stale_pid_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            controller = Controller(ControllerConfig(home=root / "state"))
            run_id = "cancel-test"
            run_dir = controller.store.run_dir(run_id, create=True)
            manifest = minimal_manifest(run_id, root, "a" * 40, status="awaiting_approval")
            controller.store.save_manifest(run_id, manifest)
            registry = ProcessRegistry(run_dir / "runtime" / "active-processes.json")
            registry.add(
                {
                    "pid": os.getpid(),
                    "pgid": os.getpid(),
                    "uid": os.getuid(),
                    "identity": "stale-token",
                    "label": "stale",
                }
            )
            result = controller.cancel(run_id)
            self.assertEqual(result["signalled_processes"], [])
            self.assertEqual(len(result["stale_processes"]), 1)
            self.assertEqual(controller.status(run_id)["status"], "cancelled")

    def test_shared_registry_tracks_both_parallel_processes_and_drains(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "raw"
            raw.mkdir()
            cancel = root / "cancel.requested"
            registry = ProcessRegistry(root / "active.json")
            outcomes: list[type[BaseException]] = []

            def invoke(label: str) -> None:
                try:
                    run_process(
                        [sys.executable, "-c", "import time; time.sleep(30)"],
                        cwd=root,
                        stdin_text="",
                        label=label,
                        raw_dir=raw,
                        registry=registry,
                        cancel_path=cancel,
                        timeout_seconds=30,
                        env=sanitized_environment(),
                    )
                except BaseException as exc:  # recorded for the assertion below
                    outcomes.append(type(exc))

            threads = [threading.Thread(target=invoke, args=(f"provider-{index}",)) for index in range(2)]
            for thread in threads:
                thread.start()
            deadline = time.monotonic() + 5
            snapshot: list[dict] = []
            while time.monotonic() < deadline:
                snapshot = registry.snapshot()
                if len(snapshot) == 2:
                    break
                time.sleep(0.025)
            self.assertEqual(len(snapshot), 2, snapshot)
            self.assertEqual(len({item["pid"] for item in snapshot}), 2)
            cancel.write_text("cancel\n", encoding="utf-8")
            for thread in threads:
                thread.join(8)
            self.assertTrue(all(not thread.is_alive() for thread in threads))
            self.assertEqual(outcomes.count(CancelledError), 2, outcomes)
            self.assertEqual(registry.snapshot(), [])

    def test_successful_provider_parent_cannot_leave_background_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "raw"
            raw.mkdir()
            child_file = root / "child.pid"
            script = (
                "import pathlib, subprocess, sys\n"
                "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'],"
                "stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\n"
                "pathlib.Path(sys.argv[1]).write_text(str(p.pid))\n"
            )
            registry = ProcessRegistry(root / "active.json")
            run_process(
                [sys.executable, "-c", script, str(child_file)],
                cwd=root,
                stdin_text="",
                label="forking-provider",
                raw_dir=raw,
                registry=registry,
                cancel_path=root / "cancel",
                timeout_seconds=10,
                env=sanitized_environment(),
            )
            child_pid = int(child_file.read_text())
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                probe = subprocess.run(["/bin/ps", "-p", str(child_pid), "-o", "stat="], text=True, capture_output=True)
                if probe.returncode != 0 or not probe.stdout.strip() or "Z" in probe.stdout:
                    break
                time.sleep(0.05)
            else:
                self.fail(f"background provider child survived: {child_pid}")
            self.assertEqual(registry.snapshot(), [])


class WorktreeCommitTests(unittest.TestCase):
    def test_raw_worktree_and_commit_bind_untracked_and_bypass_filters_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / "repo"
            sha = initialize_repo(repo)
            (repo / ".gitattributes").write_text("*.txt filter=trap eol=crlf\n", encoding="utf-8")
            git(repo, "add", ".gitattributes")
            git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "attributes")
            sha = git(repo, "rev-parse", "HEAD").stdout.strip()
            sentinel = base / "executed"
            trap = base / "trap.sh"
            trap.write_text(f"#!/bin/sh\ntouch {sentinel}\n/bin/cat\n", encoding="utf-8")
            trap.chmod(0o755)
            git(repo, "config", "filter.trap.clean", str(trap))
            git(repo, "config", "filter.trap.smudge", str(trap))
            hooks = repo / ".git/hooks"
            for name in ("post-checkout", "pre-commit", "post-commit"):
                hook = hooks / name
                hook.write_text(f"#!/bin/sh\ntouch {sentinel}\nexit 99\n", encoding="utf-8")
                hook.chmod(0o755)
            worktree = base / "worktree"
            create_worktree(repo, worktree, sha, "crosscheck/test-run")
            self.assertFalse(sentinel.exists())
            self.assertEqual(json.loads(capture_worktree_changes(worktree).payload)["changes"], [])
            self.assertEqual((worktree / "tracked.txt").read_bytes(), b"original\n")
            (worktree / "tracked.txt").write_text("changed\n", encoding="utf-8")
            (worktree / "new.txt").write_text("new file\n", encoding="utf-8")
            os.symlink("new.txt", worktree / "new-link")
            before = capture_worktree_changes(worktree)
            paths = {item["path"] for item in json.loads(before.payload)["changes"]}
            self.assertEqual(paths, {"tracked.txt", "new.txt", "new-link"})
            (worktree / "new.txt").write_text("tampered\n", encoding="utf-8")
            self.assertNotEqual(capture_worktree_changes(worktree).sha256, before.sha256)
            bound = capture_worktree_changes(worktree)
            result = commit_worktree_changes(
                worktree,
                bound,
                message="local only",
                commit_date="2026-07-14T12:00:00Z",
            )
            self.assertEqual(run_git(worktree, ["rev-parse", "HEAD"]).stdout.decode().strip(), result.commit_sha)
            self.assertEqual(json.loads(capture_worktree_changes(worktree).payload)["changes"], [])
            self.assertEqual(run_git(worktree, ["show", "HEAD:new.txt"]).stdout, b"tampered\n")
            self.assertFalse(sentinel.exists())


class ClaudeAttestationTests(unittest.TestCase):
    def test_argv_and_parser_require_safe_init(self) -> None:
        adapter = ClaudeAdapter(sys.executable, "claude-primary", "claude-fallback", "high")
        argv = adapter.build_argv(model="claude-primary", mode="plan", run_dir=ROOT, repo=ROOT, worktree=None)
        self.assertIn("--safe-mode", argv)
        settings = json.loads(argv[argv.index("--settings") + 1])
        self.assertIn("Read(**/.env)", settings["permissions"]["deny"])
        self.assertIn("Read(**/*.key)", settings["permissions"]["deny"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            events = [
                {"type": "system", "subtype": "init", "tools": ["Read", "Grep", "Glob"], "mcp_servers": []},
                {"type": "result", "result": "safe", "modelUsage": {"claude-primary": {}}},
            ]
            result = ProcessResult(
                argv=(sys.executable,),
                returncode=0,
                started_at="now",
                ended_at="now",
                duration_seconds=0,
                prompt=b"",
                stdout=("\n".join(json.dumps(item) for item in events) + "\n").encode(),
                stderr=b"",
                prompt_path=path / "prompt",
                stdout_path=path / "stdout",
                stderr_path=path / "stderr",
            )
            text, model = adapter.parse(result, requested_model="claude-primary", mode="plan")
            self.assertEqual(text, "safe\n")
            self.assertEqual(model, "claude-primary")
            missing_init = ProcessResult(**{**result.__dict__, "stdout": (json.dumps(events[-1]) + "\n").encode()})
            with self.assertRaises(ProviderError):
                adapter.parse(missing_init, requested_model="claude-primary", mode="plan")


if __name__ == "__main__":
    unittest.main()
