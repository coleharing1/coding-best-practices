from __future__ import annotations

import importlib.util
import json
import os
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "_scripts" / "sync-crosscheck.py"
PLUGIN = ROOT / "integrations" / "claude-plugin" / "plugins" / "crosscheck"
PLUGIN_COMMAND = PLUGIN / "scripts" / "crosscheck-command.mjs"
TRANSFER_HELPER = PLUGIN / "scripts" / "crosscheck-import.mjs"


def run(*argv: str | Path, cwd: Path = ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(item) for item in argv],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def executable(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


class SkillSyncTests(unittest.TestCase):
    def test_install_check_and_drift_backup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            sentinel = home / ".codex" / "skills" / "unrelated" / "sentinel.txt"
            sentinel.parent.mkdir(parents=True)
            sentinel.write_text("preserve", encoding="utf-8")
            bin_sentinel = home / ".local/bin/unrelated"
            bin_sentinel.parent.mkdir(parents=True)
            bin_sentinel.write_text("preserve", encoding="utf-8")

            missing = run(sys.executable, SYNC, "--check", "--harness", "all", "--home", home)
            self.assertEqual(missing.returncode, 1)

            installed = run(sys.executable, SYNC, "--install", "--harness", "all", "--home", home)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")
            self.assertEqual(bin_sentinel.read_text(encoding="utf-8"), "preserve")
            for target in [
                home / ".claude/skills/crosscheck-council/SKILL.md",
                home / ".codex/skills/crosscheck-council/SKILL.md",
                home / ".hermes/skills/productivity/crosscheck-council/SKILL.md",
            ]:
                self.assertTrue(target.is_file(), target)
            for target in [
                home / ".local/bin/crosscheck-claude",
                home / ".local/bin/crosscheck-codex",
                home / ".local/bin/crosscheck-hermes",
                home / ".local/bin/crosscheck-import",
            ]:
                self.assertTrue(target.is_file(), target)
                self.assertTrue(os.access(target, os.X_OK), target)

            current = run(sys.executable, SYNC, "--check", "--harness", "all", "--home", home)
            self.assertEqual(current.returncode, 0, current.stderr)

            drifted = home / ".codex/skills/crosscheck-council/SKILL.md"
            drifted.write_text(drifted.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")
            drift = run(sys.executable, SYNC, "--check", "--harness", "codex", "--home", home)
            self.assertEqual(drift.returncode, 1)
            repaired = run(sys.executable, SYNC, "--install", "--harness", "codex", "--home", home)
            self.assertEqual(repaired.returncode, 0, repaired.stderr)
            payload = json.loads(repaired.stdout)
            backup = Path(payload["results"][0]["backup"])
            self.assertTrue((backup / "SKILL.md").is_file())
            self.assertIn("drift", (backup / "SKILL.md").read_text(encoding="utf-8"))

    def test_source_hash_mismatch_fails_closed(self) -> None:
        specification = importlib.util.spec_from_file_location("sync_crosscheck", SYNC)
        assert specification and specification.loader
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        lock = module.expected_lock()
        lock["skills"]["crosscheck-council"]["sha256"] = "0" * 64
        self.assertTrue(any("content does not match" in error for error in module.source_errors(lock)))


class WrapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.log = self.root / "calls.jsonl"
        self.fake = executable(
            self.root / "fake-crosscheckctl",
            """#!/usr/bin/env python3
import json, os, stat, sys
record = {'argv': sys.argv[1:], 'caller': os.environ.get('CROSSCHECK_CALLER')}
if '--request-file' in sys.argv:
    request_path = sys.argv[sys.argv.index('--request-file') + 1]
    record['request_file_content'] = open(request_path, encoding='utf-8').read()
    record['request_file_mode'] = stat.S_IMODE(os.stat(request_path).st_mode)
with open(os.environ['CALL_LOG'], 'a', encoding='utf-8') as handle:
    handle.write(json.dumps(record) + '\\n')
if sys.argv[1:] == ['--json', 'status', '--latest'] or sys.argv[1:3] == ['--json', 'status']:
    print(json.dumps({'run_id': 'run-test', 'repository': {'path': os.environ.get('STATUS_REPO', os.getcwd())}}))
else:
    print('ok')
""",
        )
        self.env = {
            **os.environ,
            "CROSSCHECKCTL_BIN": str(self.fake),
            "CALL_LOG": str(self.log),
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def calls(self) -> list[dict]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def test_harness_wrappers_enforce_initial_boundary(self) -> None:
        codex = run(ROOT / "integrations/codex/crosscheck", "approve", "run-1", env=self.env)
        self.assertEqual(codex.returncode, 0, codex.stderr)
        hermes = run(ROOT / "integrations/hermes/crosscheck", "implement", "run-1", env=self.env)
        self.assertEqual(hermes.returncode, 64)
        hermes_result = run(ROOT / "integrations/hermes/crosscheck", "result", "run-1", env=self.env)
        self.assertEqual(hermes_result.returncode, 64)
        claude = run(ROOT / "integrations/claude/crosscheck", "approve", "run-1", env=self.env)
        self.assertEqual(claude.returncode, 64)
        self.assertEqual(self.calls(), [{"argv": ["approve", "run-1"], "caller": "codex"}])

    def test_plugin_plan_passes_request_via_private_file_never_argv(self) -> None:
        transcript = self.root / "session.jsonl"
        request = 'Review this; $(touch /tmp/never) and "quotes" must stay text.'
        transcript.write_text(
            "\n".join(
                [
                    json.dumps({"type": "user", "message": {"content": [{"type": "text", "text": request}]}}),
                    json.dumps({"type": "user", "message": {"content": "/crosscheck:plan"}}),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        env = {**self.env, "CROSSCHECK_CLAUDE_TRANSCRIPT_PATH": str(transcript)}
        result = run("node", PLUGIN_COMMAND, "plan", cwd=self.root, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        call = self.calls()[0]
        self.assertEqual(call["argv"][:4], ["plan", "--repo", os.path.realpath(self.root), "--request-file"])
        # The request text must never appear in argv (argv is world-readable in
        # the process table); it travels via a 0600 temp file instead.
        self.assertNotIn(request, call["argv"])
        self.assertEqual(call["request_file_content"], request)
        self.assertEqual(call["request_file_mode"], 0o600)
        # The temp staging dir is removed once the controller returns.
        self.assertFalse(Path(call["argv"][4]).exists())
        self.assertEqual(call["caller"], "claude-plugin")

    def test_plugin_resolves_latest_for_cancel(self) -> None:
        run("git", "init", "-q", cwd=self.root)
        result = run("node", PLUGIN_COMMAND, "cancel", cwd=self.root, env=self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            [call["argv"] for call in self.calls()],
            [["--json", "status", "--latest", "--repo", os.path.realpath(self.root)], ["cancel", "run-test"]],
        )

    def test_plugin_refuses_cross_repository_consequential_action(self) -> None:
        run("git", "init", "-q", cwd=self.root)
        other = self.root / "other"
        other.mkdir()
        result = run(
            "node",
            PLUGIN_COMMAND,
            "review",
            cwd=self.root,
            env={**self.env, "STATUS_REPO": str(other)},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing a cross-repository action", result.stderr)
        self.assertEqual(
            [call["argv"] for call in self.calls()],
            [["--json", "status", "--latest", "--repo", os.path.realpath(self.root)]],
        )

    def test_plugin_validates_explicit_environment_run_id_repository(self) -> None:
        run("git", "init", "-q", cwd=self.root)
        result = run(
            "node",
            PLUGIN_COMMAND,
            "cancel",
            cwd=self.root,
            env={**self.env, "CROSSCHECK_RUN_ID": "run-other", "STATUS_REPO": str(self.root / "other")},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([call["argv"] for call in self.calls()], [["--json", "status", "run-other"]])

    def test_plugin_status_is_repository_bound(self) -> None:
        run("git", "init", "-q", cwd=self.root)
        result = run("node", PLUGIN_COMMAND, "status", cwd=self.root, env=self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            [call["argv"] for call in self.calls()],
            [["--json", "status", "--latest", "--repo", os.path.realpath(self.root)], ["status", "run-test"]],
        )

    def test_plugin_transfer_uses_the_installed_reviewed_helper(self) -> None:
        run("git", "init", "-q", cwd=self.root)
        transcript = self.root / "session.jsonl"
        transcript.write_text(json.dumps({"type": "user", "message": {"content": "transfer"}}) + "\n")
        result = run(
            "node",
            PLUGIN_COMMAND,
            "transfer",
            cwd=self.root,
            env={**self.env, "CROSSCHECK_CLAUDE_TRANSCRIPT_PATH": str(transcript)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [call["argv"] for call in self.calls()]
        self.assertEqual(calls[0], ["--json", "status", "--latest", "--repo", os.path.realpath(self.root)])
        self.assertEqual(calls[1], ["transfer", "run-test", "--source", os.path.realpath(transcript)])
        self.assertNotIn("--helper", calls[1])


class PluginStructureTests(unittest.TestCase):
    def test_plugin_namespace_is_crosscheck(self) -> None:
        marketplace = json.loads(
            (ROOT / "integrations/claude-plugin/.claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "crosscheck")
        self.assertEqual(marketplace["plugins"][0]["name"], "crosscheck")
        self.assertEqual(marketplace["plugins"][0]["source"], "./plugins/crosscheck")
        self.assertFalse((PLUGIN.parent / "crosscheck-council").exists())

    def test_command_and_hook_surface_is_narrow(self) -> None:
        commands = {path.stem for path in (PLUGIN / "commands").glob("*.md")}
        self.assertEqual(commands, {"plan", "review", "status", "result", "cancel", "transfer"})
        hooks = json.loads((PLUGIN / "hooks/hooks.json").read_text(encoding="utf-8"))["hooks"]
        self.assertEqual(set(hooks), {"SessionStart"})
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in PLUGIN.rglob("*") if path.is_file())
        self.assertNotIn("codex-companion", all_text)
        self.assertNotIn("stop-review-gate", all_text)
        self.assertTrue((PLUGIN / "NOTICE").is_file())
        self.assertTrue((PLUGIN / "LICENSE").is_file())

    def test_session_hook_shell_escapes_transcript_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env_file = root / "env"
            transcript = str(root / "project's transcript.jsonl")
            result = subprocess.run(
                ["node", str(PLUGIN / "scripts/session-context.mjs")],
                input=json.dumps({"transcript_path": transcript}),
                text=True,
                capture_output=True,
                env={**os.environ, "CLAUDE_ENV_FILE": str(env_file)},
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            exported = env_file.read_text(encoding="utf-8")
            self.assertIn("CROSSCHECK_CLAUDE_TRANSCRIPT_PATH=", exported)
            self.assertIn("'\"'\"'", exported)


class TransferHelperTests(unittest.TestCase):
    @staticmethod
    def process_exists(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False

    def wait_for_process_exit(self, pid: int, timeout: float = 3.0) -> bool:
        deadline = time.monotonic() + timeout
        while self.process_exists(pid) and time.monotonic() < deadline:
            time.sleep(0.025)
        return not self.process_exists(pid)

    def run_fake_import(self, home: Path, mode: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        source = home / ".claude/projects/project/session.jsonl"
        source.parent.mkdir(parents=True)
        source.write_text(json.dumps({"type": "user", "message": {"content": "hello"}}) + "\n", encoding="utf-8")
        codex_home = home / ".codex"
        codex_home.mkdir()
        log = home / "app-server-log.json"
        fake = executable(
            home / "fake-codex",
            """#!/usr/bin/env python3
import hashlib, json, os, pathlib, subprocess, sys
if sys.argv[1:] == ['mcp', 'list', '--json']:
    print(json.dumps([
        {'name': 'danger-one', 'enabled': True, 'transport': {
            'type': 'stdio', 'command': '/legacy/value', 'args': []
        }},
        {'name': 'danger-http', 'enabled': True, 'transport': {
            'type': 'streamable_http', 'url': 'https://example.invalid/mcp'
        }},
    ]))
    raise SystemExit(0)
if not sys.argv[1:] or sys.argv[1] != 'app-server':
    raise SystemExit(2)
child = subprocess.Popen(
    [sys.executable, '-c', 'import time; time.sleep(60)'],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
state = {
    'argv': sys.argv[1:],
    'parent_pid': os.getpid(),
    'parent_pgid': os.getpgrp(),
    'child_pid': child.pid,
    'child_pgid': os.getpgid(child.pid),
    'requests': [],
}
def save():
    pathlib.Path(os.environ['APP_SERVER_LOG']).write_text(json.dumps(state))
save()
requests = []
for raw in sys.stdin:
    message = json.loads(raw)
    requests.append(message)
    state['requests'] = requests
    save()
    if message.get('method') == 'initialize':
        print(json.dumps({'id': message['id'], 'result': {}}), flush=True)
    elif message.get('method') == 'externalAgentConfig/import':
        state['details'] = message['params']['migrationItems'][0]['details']
        save()
        print(json.dumps({'id': message['id'], 'result': {'accepted': True}}), flush=True)
        if os.environ.get('FAKE_IMPORT_MODE') == 'timeout':
            continue
        session = message['params']['migrationItems'][0]['details']['sessions'][0]
        source = pathlib.Path(session['path']).resolve()
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        ledger = pathlib.Path(os.environ['CODEX_HOME']) / 'external_agent_session_imports.json'
        ledger.write_text(json.dumps({'records': [{
            'source_path': str(source),
            'content_sha256': digest,
            'imported_thread_id': 'thread-test'
        }]}))
        print(json.dumps({'method': 'externalAgentConfig/import/completed', 'params': {}}), flush=True)
""",
        )
        env = {
            **os.environ,
            "HOME": str(home),
            "CODEX_HOME": str(codex_home),
            "CROSSCHECK_CODEX_BIN": str(fake),
            "CROSSCHECK_IMPORT_TIMEOUT_MS": "150" if mode == "timeout" else "120000",
            "APP_SERVER_LOG": str(log),
            "FAKE_IMPORT_MODE": mode,
        }
        argv = [
            "node",
            str(TRANSFER_HELPER),
            "--source",
            str(source),
            "--cwd",
            str(home),
            "--title",
            "Council transfer",
            "--json",
        ]
        proc = subprocess.Popen(
            argv,
            cwd=home,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        stdout, stderr = proc.communicate(timeout=10)
        result = subprocess.CompletedProcess(argv, proc.returncode, stdout, stderr)
        recorded = json.loads(log.read_text(encoding="utf-8"))
        recorded["helper_pid"] = proc.pid
        return result, recorded

    def assert_process_group_cleaned(self, recorded: dict) -> None:
        helper_pid = recorded["helper_pid"]
        parent_pid = recorded["parent_pid"]
        child_pid = recorded["child_pid"]
        try:
            # The controller starts the helper as the transfer group leader;
            # the helper must keep app-server and its descendants in that same
            # owned group so a controller timeout/cancel can reap the tree.
            self.assertEqual(recorded["parent_pgid"], helper_pid)
            self.assertEqual(recorded["child_pgid"], helper_pid)
            self.assertTrue(self.wait_for_process_exit(parent_pid), f"app-server parent survived: {parent_pid}")
            try:
                os.killpg(helper_pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            self.assertTrue(self.wait_for_process_exit(child_pid), f"app-server child survived: {child_pid}")
        finally:
            try:
                os.killpg(helper_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    def test_import_uses_empty_migration_and_cleans_forked_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result, recorded = self.run_fake_import(Path(directory), "success")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["thread_id"], "thread-test")
            self.assertEqual(payload["codex_binary"], os.path.realpath(Path(directory) / "fake-codex"))
            self.assertIn('mcp_servers."danger-one".enabled=false', recorded["argv"])
            self.assertIn('mcp_servers."danger-one".command="/usr/bin/false"', recorded["argv"])
            self.assertIn('mcp_servers."danger-http".url="http://127.0.0.1:9"', recorded["argv"])
            details = recorded["details"]
            self.assertEqual(details["plugins"], [])
            self.assertEqual(details["mcpServers"], [])
            self.assertEqual(details["hooks"], [])
            self.assertEqual(details["subagents"], [])
            self.assertEqual(details["commands"], [])
            self.assertEqual(details["sessions"][0]["title"], "Council transfer")
            self.assert_process_group_cleaned(recorded)

    def test_import_timeout_cleans_forked_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result, recorded = self.run_fake_import(Path(directory), "timeout")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Timed out waiting for Codex session import", result.stderr)
            self.assert_process_group_cleaned(recorded)


if __name__ == "__main__":
    unittest.main()
