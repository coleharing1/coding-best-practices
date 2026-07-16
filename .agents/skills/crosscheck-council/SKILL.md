---
name: crosscheck-council
description: Run or resume the local Claude-Codex crosscheck council for consequential repository planning, adversarial review, approved implementation, verification, cancellation, or explicit transfer into Codex Desktop. Use when the user asks for an independent second opinion, dual-model plan, crosscheck, council review, or the guarded Claude-Codex-Hermes workflow.
---

# Crosscheck Council

Use `crosscheckctl` as the only workflow authority. Do not call Claude or Codex directly, edit run manifests, forge approval receipts, or bypass a controller gate.

## Start safely

1. Resolve the target repository to an absolute path.
2. Run `crosscheckctl doctor --repo <repo>`.
3. Stop and report any blocking doctor finding.
4. Put substantial or untrusted request text in a private file and use `--request-file`; do not interpolate it into a shell command.

```bash
crosscheckctl plan --repo /absolute/repo --request-file /absolute/private-request.txt
```

Planning is read-only and may snapshot a dirty tree. Report the run ID and artifact paths returned by the controller.

## Inspect and control a run

```bash
crosscheckctl status --latest
crosscheckctl show --latest
crosscheckctl show <run-id> --artifact Plan-<id>-Final.md
crosscheckctl cancel <run-id>
```

Use the exact run ID for consequential actions. Prefer `--json` when another program must parse the response.

## Respect approval and write boundaries

- Ask the user to run `crosscheckctl approve <run-id>` in an interactive terminal. Never pipe confirmation, synthesize input, or claim approval from chat text alone.
- Run `implement`, `review`, or `verify` only when the user explicitly requested that stage and the controller accepts the bound receipt and repository SHA.
- Treat any stale SHA, dirty-tree block, missing receipt, provider mismatch, forbidden tool event, or disk gate as a hard stop.
- Never push, open a pull request, deploy, migrate a database, change a remote environment, or invoke an external write connector through this workflow.

```bash
crosscheckctl implement <run-id>
crosscheckctl review <run-id>
crosscheckctl verify <run-id> --command "<repository-owned check>"
```

## Transfer explicitly

Transfer only when the user requests a persistent Codex Desktop thread. Supply a genuine Claude Code session JSONL; never substitute a plan Markdown file.

```bash
crosscheckctl transfer <run-id> --source /absolute/path/to/claude-session.jsonl
```

Report the imported thread ID, resume command, source hash, and receipt path. Ordinary council runs remain ephemeral.

## Hermes boundary

In the initial Hermes integration, use only `plan`, `status`, `show`, `cancel`, and `transfer`. Do not approve, implement, review, verify, schedule health checks, alter gateways, or change Telegram/Kanban state until the staged Hermes gate is separately enabled and tested.
