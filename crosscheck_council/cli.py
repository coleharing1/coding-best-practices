"""Command-line interface for crosscheckctl."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Sequence

from .controller import Controller, ControllerConfig, DEFAULT_HOME
from .errors import CrosscheckError, UsageError


def _json_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="emit machine-readable JSON")


def _run_selector(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("run_id", nargs="?", help="run id (defaults to latest with --latest)")
    parser.add_argument("--latest", action="store_true", help="select the most recently updated run")
    parser.add_argument("--repo", type=Path, help="restrict selection to this repository")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crosscheckctl", description="Local Claude/Codex crosscheck council")
    parser.add_argument("--home", type=Path, default=Path(os.environ.get("CROSSCHECK_HOME", DEFAULT_HOME)))
    parser.add_argument("--claude-bin", default=os.environ.get("CROSSCHECK_CLAUDE_BIN", "claude"))
    parser.add_argument("--codex-bin", default=os.environ.get("CROSSCHECK_CODEX_BIN", "codex"))
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("CROSSCHECK_TIMEOUT", "1800")))
    _json_flag(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="check binaries, disk, storage, and optional repository")
    doctor.add_argument("--repo", type=Path)
    doctor.add_argument("--prune", action="store_true", help="remove only raw logs older than 30 days")
    _json_flag(doctor)

    plan = sub.add_parser("plan", help="run two independent plans and synthesize a final plan")
    plan.add_argument("--repo", type=Path, required=True)
    request = plan.add_mutually_exclusive_group(required=True)
    request.add_argument("--request")
    request.add_argument("--request-file", type=Path)
    plan.add_argument("--run-id")
    plan.add_argument("--dry-run", action="store_true", help="write evidence and inspectable argv without invoking providers")
    _json_flag(plan)

    for name in ("status", "show", "result"):
        command = sub.add_parser(name, help="show run state" if name == "status" else "show a run artifact")
        _run_selector(command)
        if name != "status":
            command.add_argument("--artifact", help="artifact key from the manifest")
        _json_flag(command)

    cancel = sub.add_parser("cancel", help="request cancellation and terminate active provider process groups")
    cancel.add_argument("run_id")
    _json_flag(cancel)

    approve = sub.add_parser("approve", help="interactively approve the hash-bound final plan")
    approve.add_argument("run_id")
    _json_flag(approve)

    implement = sub.add_parser("implement", help="implement an approved plan in an isolated worktree")
    implement.add_argument("run_id")
    _json_flag(implement)

    review = sub.add_parser("review", help="Claude review with bounded Codex corrections")
    review.add_argument("run_id")
    review.add_argument("--max-corrections", type=int, default=5)
    _json_flag(review)

    verify = sub.add_parser("verify", help="run network-disabled local verification")
    verify.add_argument("run_id")
    verify.add_argument(
        "--command",
        dest="verification_commands",
        action="append",
        default=[],
        help="argv string; repeat for multiple checks",
    )
    _json_flag(verify)

    complete = sub.add_parser("complete", help="create the deterministic local-only commit after verification")
    complete.add_argument("run_id")
    _json_flag(complete)

    transfer = sub.add_parser("transfer", help="import an explicit Claude session transcript into Codex Desktop")
    transfer.add_argument("run_id")
    transfer.add_argument("--source", required=True, type=Path)
    transfer.add_argument("--helper", default=os.environ.get("CROSSCHECK_TRANSFER_HELPER", "crosscheck-import"))
    _json_flag(transfer)
    return parser


def _selected_run(args: argparse.Namespace) -> str | None:
    if args.latest and args.run_id:
        raise UsageError("provide either a run id or --latest, not both")
    if not args.latest and not args.run_id:
        raise UsageError("provide a run id or --latest")
    return None if args.latest else args.run_id


def _emit(value: Any, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2))
        return
    if isinstance(value, dict) and "content" in value:
        print(value["content"], end="" if str(value["content"]).endswith("\n") else "\n")
    else:
        print(json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2))


def main(argv: Sequence[str] | None = None) -> int:
    os.umask(0o077)
    parser = build_parser()
    args = parser.parse_args(argv)
    as_json = bool(getattr(args, "json", False))
    try:
        if args.timeout < 1:
            raise UsageError("timeout must be positive")
        controller = Controller(
            ControllerConfig(home=args.home, claude_bin=args.claude_bin, codex_bin=args.codex_bin, timeout_seconds=args.timeout)
        )
        if args.command == "doctor":
            result = controller.doctor(args.repo, prune=args.prune)
        elif args.command == "plan":
            request = args.request if args.request is not None else args.request_file.read_text(encoding="utf-8")
            result = controller.plan(args.repo, request, run_id=args.run_id, dry_run=args.dry_run)
        elif args.command == "status":
            result = controller.status(_selected_run(args), repository=args.repo)
        elif args.command in {"show", "result"}:
            result = controller.show(_selected_run(args), args.artifact, repository=args.repo)
        elif args.command == "cancel":
            result = controller.cancel(args.run_id)
        elif args.command == "approve":
            if as_json:
                raise UsageError("approve does not support --json; interactive confirmation must use a TTY")
            result = controller.approve(args.run_id)
        elif args.command == "implement":
            result = controller.implement(args.run_id)
        elif args.command == "review":
            result = controller.review(args.run_id, max_corrections=args.max_corrections)
        elif args.command == "verify":
            result = controller.verify(args.run_id, commands=args.verification_commands)
        elif args.command == "complete":
            result = controller.complete(args.run_id)
        elif args.command == "transfer":
            result = controller.transfer(args.run_id, source=args.source, helper=args.helper)
        else:
            raise UsageError(f"unknown command: {args.command}")
        _emit(result, as_json=as_json)
        return 0
    except CrosscheckError as exc:
        if as_json:
            print(json.dumps({"ok": False, "error": str(exc), "error_type": type(exc).__name__}), file=sys.stderr)
        else:
            print(f"crosscheckctl: {exc}", file=sys.stderr)
        return exc.exit_code
    except (OSError, ValueError) as exc:
        if as_json:
            print(json.dumps({"ok": False, "error": str(exc), "error_type": type(exc).__name__}), file=sys.stderr)
        else:
            print(f"crosscheckctl: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
