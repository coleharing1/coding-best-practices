from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import crosscheck_council.controller as controller_module
import crosscheck_council.repository as repository_module
from crosscheck_council.adapters import ProcessResult, ProviderAdapter, ProviderOutput
from crosscheck_council.controller import Controller, ControllerConfig
from crosscheck_council.errors import SafetyError
from crosscheck_council.storage import sha256_bytes, sha256_file


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=check,
        env={**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"},
    )


def initialize_repo(root: Path, *, seed: str = "SEEDED_FINDING") -> str:
    root.parent.mkdir(parents=True, exist_ok=True)
    git(root.parent, "init", "-q", "--initial-branch=main", str(root))
    (root / "tracked.txt").write_text("original\n", encoding="utf-8")
    (root / "seed.txt").write_text(seed + "\n", encoding="utf-8")
    git(root, "add", "tracked.txt", "seed.txt")
    git(
        root,
        "-c",
        "user.name=Workflow Test",
        "-c",
        "user.email=workflow@example.invalid",
        "commit",
        "-qm",
        "initial",
    )
    return git(root, "rev-parse", "HEAD").stdout.strip()


class TTY(io.StringIO):
    def isatty(self) -> bool:
        return True


class ScriptedProvider(ProviderAdapter):
    """In-process provider double that exercises controller orchestration only."""

    def __init__(self, provider: str) -> None:
        self.provider = provider
        self.binary = sys.executable
        self.primary_model = f"{provider}-primary"
        self.fallback_model = f"{provider}-fallback"
        self.effort = "test"
        self.calls: list[dict[str, Any]] = []
        self.review_verdicts: list[str] = []
        self.correction_count = 0
        self._mutex = threading.Lock()

    def build_argv(
        self,
        *,
        model: str,
        mode: str,
        run_dir: Path,
        repo: Path,
        worktree: Path | None,
    ) -> list[str]:
        return [self.binary, "fake-provider", self.provider, model, mode, str(run_dir), str(worktree or repo)]

    def build_qa_argv(self, command: list[str], *, worktree: Path, temp_dir: Path) -> list[str]:
        return [
            self.binary,
            "sandbox",
            "--permission-profile",
            ":workspace",
            "--cd",
            str(worktree),
            "--temp-dir",
            str(temp_dir),
            "--sandbox-state-disable-network",
            "--",
            *command,
        ]

    def run(
        self,
        prompt: str,
        *,
        mode: str,
        run_dir: Path,
        repo: Path,
        worktree: Path | None,
        registry: object,
        cancel_path: Path,
        timeout_seconds: int,
        label: str,
        independence_barrier: threading.Barrier | None = None,
    ) -> ProviderOutput:
        del registry, cancel_path, timeout_seconds
        if independence_barrier is not None:
            independence_barrier.wait(timeout=5)

        target = worktree or repo
        seed_path = target / "seed.txt"
        seed = seed_path.read_text(encoding="utf-8").strip() if seed_path.is_file() else "NO_SEED"
        with self._mutex:
            self.calls.append(
                {
                    "prompt": prompt,
                    "mode": mode,
                    "run_dir": run_dir,
                    "repo": repo,
                    "worktree": worktree,
                    "label": label,
                }
            )
            if mode == "review":
                verdict = self.review_verdicts.pop(0) if self.review_verdicts else "PASS"
            else:
                verdict = ""
            if mode == "correct":
                self.correction_count += 1
                correction_count = self.correction_count
            else:
                correction_count = self.correction_count

        if mode == "implement":
            if worktree is None:
                raise AssertionError("fake implementation did not receive an isolated worktree")
            (worktree / "tracked.txt").write_text("implemented locally\n", encoding="utf-8")
            (worktree / "implemented.txt").write_text("new untracked implementation\n", encoding="utf-8")
            text = "Implemented the approved plan in the isolated worktree.\n"
        elif mode == "correct":
            if worktree is None:
                raise AssertionError("fake correction did not receive an isolated worktree")
            (worktree / "corrections.txt").write_text(
                f"bounded corrections: {correction_count}\n", encoding="utf-8"
            )
            text = f"Applied correction {correction_count}.\n"
        elif mode == "review":
            text = f"Reviewed {seed}.\nCROSSCHECK_VERDICT: {verdict}\n"
        elif mode == "adversarial":
            text = f"Adversarial review retained finding {seed}.\n"
        elif mode == "synthesis":
            text = f"# Final fake plan\n\nResolve {seed} with local tests only.\n"
        else:
            text = f"# {self.provider} independent plan\n\nFinding: {seed}.\n"

        attempt = {
            "provider": self.provider,
            "attempt": 1,
            "requested_model": self.primary_model,
            "actual_model": self.primary_model,
            "status": "success",
            "output_sha256": sha256_bytes(text.encode("utf-8")),
        }
        return ProviderOutput(
            provider=self.provider,
            requested_model=self.primary_model,
            actual_model=self.primary_model,
            text=text,
            attempts=(attempt,),
        )


def controller_with_fakes(base: Path) -> tuple[Controller, ScriptedProvider, ScriptedProvider]:
    controller = Controller(
        ControllerConfig(
            home=base / "state",
            claude_bin=sys.executable,
            codex_bin=sys.executable,
            warn_disk_gib=0,
            block_disk_gib=0,
            timeout_seconds=10,
        )
    )
    claude = ScriptedProvider("claude")
    codex = ScriptedProvider("codex")
    controller._claude = claude
    controller._codex = codex
    return controller, claude, codex


def approve(controller: Controller, run_id: str) -> dict[str, Any]:
    manifest = controller.status(run_id)
    expected = manifest["artifacts"]["final_plan"]["sha256"][:12]
    return controller.approve(
        run_id,
        stdin=TTY(f"APPROVE {expected}\n"),
        stdout=TTY(),
    )


def fake_qa_result(calls: list[tuple[str, ...]]):
    def invoke(
        argv: list[str],
        *,
        cwd: Path,
        stdin_text: str,
        label: str,
        raw_dir: Path,
        registry: object,
        cancel_path: Path,
        timeout_seconds: int,
        env: dict[str, str],
    ) -> ProcessResult:
        del cwd, registry, cancel_path, timeout_seconds, env
        calls.append(tuple(argv))
        return ProcessResult(
            argv=tuple(argv),
            returncode=0,
            started_at="2026-07-14T12:00:00Z",
            ended_at="2026-07-14T12:00:01Z",
            duration_seconds=1.0,
            prompt=stdin_text.encode("utf-8"),
            stdout=b"local verification passed\n",
            stderr=b"",
            prompt_path=raw_dir / f"{label}.prompt.txt",
            stdout_path=raw_dir / f"{label}.stdout.log",
            stderr_path=raw_dir / f"{label}.stderr.log",
        )

    return invoke


class FakeProviderPlanningPilots(unittest.TestCase):
    def test_three_seeded_disposable_repository_pilots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for index, seed in enumerate(("SEED_ALPHA", "SEED_BRAVO", "SEED_CHARLIE"), start=1):
                with self.subTest(seed=seed):
                    pilot = base / f"pilot-{index}"
                    repo = pilot / "repo"
                    original_sha = initialize_repo(repo, seed=seed)
                    controller, claude, codex = controller_with_fakes(pilot)
                    run_id = f"seeded-pilot-{index}"

                    manifest = controller.plan(repo, f"Resolve {seed}", run_id=run_id)

                    self.assertEqual(manifest["status"], "awaiting_approval")
                    self.assertEqual(git(repo, "rev-parse", "HEAD").stdout.strip(), original_sha)
                    self.assertEqual(git(repo, "status", "--porcelain").stdout, "")
                    claude_plan = controller.show(run_id, "claude_plan")["content"]
                    codex_plan = controller.show(run_id, "codex_plan")["content"]
                    final_plan = controller.show(run_id, "final_plan")["content"]
                    self.assertIn(seed, claude_plan)
                    self.assertIn(seed, codex_plan)
                    self.assertIn(seed, final_plan)

                    claude_initial = [call for call in claude.calls if call["mode"] == "plan"]
                    codex_initial = [call for call in codex.calls if call["mode"] == "plan"]
                    self.assertEqual(len(claude_initial), 1)
                    self.assertEqual(len(codex_initial), 1)
                    self.assertEqual(claude_initial[0]["prompt"], codex_initial[0]["prompt"])
                    self.assertNotIn("# claude independent plan", codex_initial[0]["prompt"])
                    self.assertNotIn("# codex independent plan", claude_initial[0]["prompt"])
                    self.assertNotEqual(claude_initial[0]["run_dir"], codex_initial[0]["run_dir"])


class GatedWorkflowTests(unittest.TestCase):
    def test_full_local_commit_flow_has_no_push_or_provider_logs_in_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / "repo"
            original_sha = initialize_repo(repo, seed="FLOW_SEED")
            remote = base / "remote.git"
            git(base, "clone", "-q", "--bare", str(repo), str(remote))
            git(repo, "remote", "add", "origin", str(remote))
            remote_before = git(remote, "for-each-ref", "--format=%(refname) %(objectname)").stdout

            controller, claude, codex = controller_with_fakes(base)
            run_id = "complete-local-flow"
            git_calls: list[tuple[str, ...]] = []
            qa_calls: list[tuple[str, ...]] = []
            real_run_git = repository_module.run_git

            def spy_run_git(path: Path, args: Any, **kwargs: Any):
                git_calls.append(tuple(args))
                return real_run_git(path, args, **kwargs)

            with mock.patch.object(repository_module, "run_git", side_effect=spy_run_git), mock.patch.object(
                controller_module,
                "run_process",
                side_effect=fake_qa_result(qa_calls),
            ):
                controller.plan(repo, "Implement the FLOW_SEED plan", run_id=run_id)
                approval = approve(controller, run_id)
                implemented = controller.implement(run_id)
                reviewed = controller.review(run_id)
                verification = controller.verify(run_id, commands=("python -m unittest",))
                completion = controller.complete(run_id)

            self.assertEqual(implemented["status"], "implemented")
            self.assertEqual(reviewed["status"], "reviewed")
            self.assertTrue(verification["success"])
            self.assertEqual(controller.status(run_id)["status"], "completed")
            self.assertFalse(completion["pushed"])
            self.assertEqual(completion["approval_sha256"], sha256_file(controller.store.run_dir(run_id) / "receipts" / "approval.json"))
            self.assertEqual(git(repo, "rev-parse", "HEAD").stdout.strip(), original_sha)
            self.assertEqual(git(remote, "for-each-ref", "--format=%(refname) %(objectname)").stdout, remote_before)
            self.assertFalse(any("push" in call or "fetch" in call for call in git_calls), git_calls)

            self.assertEqual(len(qa_calls), 1)
            self.assertIn("sandbox", qa_calls[0])
            self.assertIn("--sandbox-state-disable-network", qa_calls[0])
            self.assertEqual([call["mode"] for call in codex.calls].count("implement"), 1)
            self.assertEqual([call["mode"] for call in claude.calls].count("review"), 1)

            worktree = Path(controller.status(run_id)["worktree"]["path"])
            committed_files = set(
                git(worktree, "ls-tree", "-r", "--name-only", completion["commit_sha"]).stdout.splitlines()
            )
            self.assertEqual(committed_files, {"implemented.txt", "seed.txt", "tracked.txt"})
            self.assertFalse(any("raw" in name or "prompt" in name or "stdout" in name for name in committed_files))
            self.assertTrue((controller.store.run_dir(run_id) / "raw").is_dir())
            self.assertEqual(approval["plan_sha256"], controller.status(run_id)["artifacts"]["final_plan"]["sha256"])

    def test_approval_receipt_tamper_blocks_implementation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / "repo"
            initialize_repo(repo)
            controller, _, _ = controller_with_fakes(base)
            run_id = "approval-tamper"
            controller.plan(repo, "Plan", run_id=run_id)
            approve(controller, run_id)
            receipt_path = controller.store.run_dir(run_id) / "receipts" / "approval.json"
            receipt_path.write_text(receipt_path.read_text(encoding="utf-8") + " ", encoding="utf-8")

            with self.assertRaisesRegex(SafetyError, "approval receipt hash mismatch"):
                controller.implement(run_id)

            self.assertEqual(controller.status(run_id)["status"], "approved")
            self.assertFalse((controller.store.worktrees / run_id).exists())

    def test_repository_drift_blocks_implementation_before_worktree_creation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / "repo"
            initialize_repo(repo)
            controller, _, _ = controller_with_fakes(base)
            run_id = "repository-drift"
            controller.plan(repo, "Plan", run_id=run_id)
            approve(controller, run_id)
            (repo / "tracked.txt").write_text("unrelated user change\n", encoding="utf-8")

            with self.assertRaisesRegex(SafetyError, "clean repository"):
                controller.implement(run_id)

            self.assertEqual(controller.status(run_id)["status"], "approved")
            self.assertFalse((controller.store.worktrees / run_id).exists())

    def test_corrections_are_capped_at_five_across_review_retries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / "repo"
            initialize_repo(repo, seed="CORRECTION_SEED")
            controller, claude, codex = controller_with_fakes(base)
            run_id = "lifetime-correction-cap"
            controller.plan(repo, "Plan", run_id=run_id)
            approve(controller, run_id)
            controller.implement(run_id)
            claude.review_verdicts = ["CHANGES_REQUIRED"] * 8

            first = controller.review(run_id, max_corrections=3)
            second = controller.review(run_id, max_corrections=3)

            self.assertEqual(first["status"], "review_failed")
            self.assertEqual(first["correction_passes"], 3)
            self.assertEqual(second["status"], "review_failed")
            self.assertEqual(second["correction_passes"], 5)
            self.assertEqual(codex.correction_count, 5)
            correction_calls = [call for call in codex.calls if call["mode"] == "correct"]
            self.assertEqual(len(correction_calls), 5)
            self.assertTrue(all("APPROVED PLAN" in call["prompt"] for call in correction_calls))


if __name__ == "__main__":
    unittest.main()
