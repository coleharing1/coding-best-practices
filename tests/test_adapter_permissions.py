from __future__ import annotations

import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

from crosscheck_council.adapters import (
    CODEX_QA_PERMISSION_PROFILE,
    CODEX_READ_PERMISSION_PROFILE,
    CODEX_WRITE_PERMISSION_PROFILE,
    CodexAdapter,
)
from crosscheck_council.errors import SafetyError


def config_values(argv: list[str]) -> dict[str, object]:
    values: dict[str, object] = {}
    for index, argument in enumerate(argv):
        if argument not in {"--config", "-c"}:
            continue
        key, raw_value = argv[index + 1].split("=", 1)
        values[key] = tomllib.loads(f"value = {raw_value}")["value"]
    return values


class CodexPermissionArgvTests(unittest.TestCase):
    def adapter(self) -> CodexAdapter:
        return CodexAdapter(sys.executable, "gpt-primary", "gpt-fallback", "xhigh")

    def assert_common_hardening(self, argv: list[str], *, profile: str, model: str) -> dict[str, object]:
        self.assertNotIn("--sandbox", argv)
        self.assertIn("--strict-config", argv)
        self.assertIn("--ignore-user-config", argv)
        self.assertIn("--ignore-rules", argv)
        # The plan/review stage launches from the non-git per-run staging dir;
        # without this flag codex exec aborts before inference (0/3 pilot bug).
        self.assertIn("--skip-git-repo-check", argv)
        self.assertEqual(argv[argv.index("--model") + 1], model)

        configs = config_values(argv)
        self.assertEqual(configs["approval_policy"], "never")
        self.assertEqual(configs["default_permissions"], profile)
        self.assertFalse(configs[f"permissions.{profile}.network.enabled"])
        self.assertEqual(configs["model_reasoning_effort"], "xhigh")
        self.assertEqual(configs["web_search"], "disabled")
        self.assertFalse(configs["allow_login_shell"])
        self.assertNotIn("--add-dir", argv)
        self.assertFalse(any(key.startswith("sandbox_") for key in configs))

        for feature in CodexAdapter._DISABLED_FEATURES:
            self.assertIn(["--disable", feature], [argv[index : index + 2] for index in range(len(argv) - 1)])
        # The deprecated web-search [features] sub-flags must NOT be passed — current
        # Codex CLI emits deprecation error-items for them that abort plan parsing;
        # top-level web_search="disabled" (asserted above) is the supported control.
        self.assertNotIn("web_search_cached", CodexAdapter._DISABLED_FEATURES)
        self.assertNotIn("web_search_request", CodexAdapter._DISABLED_FEATURES)
        self.assertNotIn("web_search_cached", argv)
        self.assertNotIn("web_search_request", argv)
        return configs

    def test_plan_and_review_use_exact_read_only_roots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            repo = root / "repo"
            stage = root / "provider-stage"
            repo.mkdir()
            stage.mkdir()

            for mode in ("plan", "review"):
                with self.subTest(mode=mode):
                    argv = self.adapter().build_argv(
                        model="gpt-primary",
                        mode=mode,
                        run_dir=stage,
                        repo=repo,
                        worktree=None,
                    )
                    configs = self.assert_common_hardening(
                        argv,
                        profile=CODEX_READ_PERMISSION_PROFILE,
                        model="gpt-primary",
                    )
                    filesystem = configs[f"permissions.{CODEX_READ_PERMISSION_PROFILE}.filesystem"]
                    self.assertEqual(filesystem[":minimal"], "read")
                    self.assertEqual(filesystem["/Users"], "deny")
                    self.assertEqual(filesystem[str(repo)], "read")
                    self.assertEqual(filesystem[str(stage)], "read")
                    self.assertNotIn("write", {value for value in filesystem.values() if isinstance(value, str)})
                    self.assertEqual(filesystem[str(repo / "**/.env*")], "deny")
                    self.assertEqual(filesystem[str(repo / "**/*credentials*")], "deny")
                    self.assertEqual(filesystem[str(repo / "**/*.key")], "deny")
                    self.assertEqual(filesystem[str(repo / "**/keys/**")], "deny")
                    self.assertEqual(argv[argv.index("--cd") + 1], str(stage))

    def test_implement_and_correct_write_only_worktree_git_and_stage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            repo = root / "source"
            common_git = repo / ".git"
            git_dir = common_git / "worktrees" / "isolated"
            worktree = root / "isolated"
            stage = root / "stage"
            git_dir.mkdir(parents=True)
            worktree.mkdir()
            stage.mkdir()
            (worktree / ".git").write_text(f"gitdir: {git_dir}\n", encoding="utf-8")
            (git_dir / "commondir").write_text("../..\n", encoding="utf-8")

            for mode in ("implement", "correct"):
                with self.subTest(mode=mode):
                    argv = self.adapter().build_argv(
                        model="gpt-primary",
                        mode=mode,
                        run_dir=stage,
                        repo=repo,
                        worktree=worktree,
                    )
                    configs = self.assert_common_hardening(
                        argv,
                        profile=CODEX_WRITE_PERMISSION_PROFILE,
                        model="gpt-primary",
                    )
                    filesystem = configs[f"permissions.{CODEX_WRITE_PERMISSION_PROFILE}.filesystem"]
                    self.assertEqual(filesystem[str(worktree)], "write")
                    self.assertEqual(filesystem[str(stage)], "write")
                    self.assertEqual(filesystem[str(git_dir)], "write")
                    self.assertEqual(filesystem[str(common_git)], "read")
                    self.assertNotIn(str(repo), filesystem)
                    self.assertEqual(filesystem[str(worktree / "**/.env*")], "deny")
                    self.assertEqual(filesystem[str(worktree / "**/*credentials*")], "deny")
                    self.assertEqual(filesystem[str(worktree / "**/*.key")], "deny")
                    self.assertEqual(filesystem[str(worktree / "**/keys/**")], "deny")
                    self.assertEqual(argv[argv.index("--cd") + 1], str(worktree))

    def test_command_preview_keeps_explicit_primary_and_fallback_models(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            repo = root / "repo"
            stage = root / "stage"
            repo.mkdir()
            stage.mkdir()
            preview = self.adapter().command_preview(mode="plan", run_dir=stage, repo=repo)

        self.assertEqual([item["model"] for item in preview], ["gpt-primary", "gpt-fallback"])
        self.assertEqual(
            [item["argv"][item["argv"].index("--model") + 1] for item in preview],
            ["gpt-primary", "gpt-fallback"],
        )

    def test_qa_profile_limits_writes_to_worktree_and_private_temp(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            common_git = root / "source/.git"
            git_dir = common_git / "worktrees/isolated"
            worktree = root / "isolated"
            temp_dir = root / "qa-tmp"
            git_dir.mkdir(parents=True)
            worktree.mkdir()
            temp_dir.mkdir()
            (worktree / ".git").write_text(f"gitdir: {git_dir}\n", encoding="utf-8")
            (git_dir / "commondir").write_text("../..\n", encoding="utf-8")
            argv = self.adapter().build_qa_argv(["python", "-m", "unittest"], worktree=worktree, temp_dir=temp_dir)
            configs = config_values(argv)
            filesystem = configs[f"permissions.{CODEX_QA_PERMISSION_PROFILE}.filesystem"]
            self.assertEqual(configs["default_permissions"], CODEX_QA_PERMISSION_PROFILE)
            self.assertFalse(configs[f"permissions.{CODEX_QA_PERMISSION_PROFILE}.network.enabled"])
            self.assertEqual(filesystem[str(worktree)], "write")
            self.assertEqual(filesystem[str(temp_dir)], "write")
            self.assertEqual(filesystem[str(git_dir)], "read")
            self.assertEqual(filesystem[str(common_git)], "read")
            self.assertEqual(filesystem["/Users"], "deny")
            self.assertEqual(argv[-3:], ["python", "-m", "unittest"])

    def test_write_mode_without_worktree_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with self.assertRaisesRegex(SafetyError, "requires an isolated worktree"):
                self.adapter().build_argv(
                    model="gpt-primary",
                    mode="implement",
                    run_dir=root,
                    repo=root,
                    worktree=None,
                )


if __name__ == "__main__":
    unittest.main()
