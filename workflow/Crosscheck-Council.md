# Claude-Codex-Hermes Crosscheck Council

> A local, evidence-bound workflow for getting independent Claude and Codex opinions before implementation. The controller owns state and safety; integrations are thin command surfaces.

## What Is Installed

- `bin/crosscheckctl` is the canonical controller entrypoint. It runs with uv-managed Python 3.11 and has no third-party runtime dependencies.
- `.agents/skills/crosscheck-council` is the canonical shared skill. Copies in Claude, Codex, and Hermes are caches verified against `skills.lock.json`.
- `integrations/claude-plugin` exposes only `/crosscheck:plan`, `/crosscheck:review`, `/crosscheck:status`, `/crosscheck:result`, `/crosscheck:cancel`, and `/crosscheck:transfer`. It has no Stop hook, rescue path, reviewer MCP, or automatic implementation behavior.
- `integrations/hermes/crosscheck` is a manual, allowlisted wrapper. Hermes upgrades, Kanban mirroring, Telegram approval, and scheduled health checks remain gated until three real pilots pass.

Runtime records live outside repositories under:

```text
~/.local/share/crosscheck-council/
├── runs/<run-id>/
│   ├── manifest.json
│   ├── evidence.json
│   ├── artifacts/
│   ├── raw/
│   ├── receipts/
│   └── runtime/
└── worktrees/
```

Directories are `0700`; records and logs are `0600`. Raw provider logs expire after 30 days. Final plans and receipts are retained until explicitly removed.

## First-Run Checks

From this repository:

```bash
make council-test
make council-plugin-validate
make council-doctor
```

Install or refresh the controller and verified integration caches only after those checks pass, then verify the installed hashes:

```bash
uv tool install --force --python 3.11 /absolute/path/to/coding-best-practices
make council-sync-install
make council-sync-check
```

The controller warns below 30 GiB of free disk and refuses to start a new provider run below 20 GiB. The gate is intentional; do not bypass it by deleting chat histories or backups.

## Planning Workflow

Create one immutable evidence packet and dry-run the provider command plan first:

```bash
crosscheckctl plan \
  --repo /absolute/path/to/repository \
  --request "Describe the requested change and constraints" \
  --dry-run
```

Run the real planning council after reviewing `doctor` and the dry-run record:

```bash
crosscheckctl plan \
  --repo /absolute/path/to/repository \
  --request "Describe the requested change and constraints"
```

The sequence is bounded:

1. Claude and Codex independently receive the same evidence packet.
2. Neither provider receives the other's first opinion.
3. Claude synthesizes the two plans.
4. Codex performs one adversarial pass.
5. The controller writes the final plan and stops at `awaiting_approval`.

Planning can fingerprint a dirty repository. Implementation cannot start from one.

## Approval And Implementation

Inspect a run before approval:

```bash
crosscheckctl status <run-id>
crosscheckctl show <run-id>
crosscheckctl approve <run-id>
```

Approval requires an interactive TTY and is bound to the final-plan hash, evidence hash, and repository SHA. A stale or copied approval receipt is rejected.

After approval:

```bash
crosscheckctl implement <run-id>
crosscheckctl review <run-id>
crosscheckctl verify <run-id>
```

Implementation uses an isolated worktree and a clean, unchanged base. Review is pinned to the produced diff. Verification runs repository-specific commands and permits at most five bounded correction passes. Completion creates a deterministic local commit and receipt.

The controller never pushes, opens a pull request, deploys, migrates a database, changes an environment, or authorizes an external integration.

## Provider Isolation

Claude runs in safe mode without inherited settings, Chrome, skills, persistence, or MCP configuration. Its only available built-in tools are `Read`, `Grep`, and `Glob`; deny rules remove environment, credential, key, and similarly sensitive paths from those built-in file tools.

Codex planning and review use ephemeral, read-only `codex exec` sessions with strict path-scoped permission profiles. The user's home and unrelated run data are denied, target secret-file globs are denied, and network access is disabled. User config, project rules, repository instructions, apps, plugins, MCPs, hooks, memories, multi-agent behavior, web search, image generation, login shells, shell snapshots, and automatic skill instructions are disabled. The controller rejects forbidden JSONL events and repository drift. Implementation gets write access only to its isolated worktree, its Git administration path, and its private provider staging directory. QA gets only the worktree and a private per-run temporary directory.

The two first opinions are additionally isolated by a controller barrier: neither provider transcript nor output is persisted until both provider processes have exited; the shared immutable evidence packet is persisted beforehand by design. Later synthesis and adversarial stages receive earlier artifacts intentionally. Claude's built-in file-tool permissions are not a general VM boundary, so repositories themselves remain trusted data scope; use a VM for reviews that require whole-machine packet-only confidentiality.

Models are controller-managed and recorded in every attempt record. The record distinguishes the requested/invoked model from provider-reported model metadata when the provider supplies it:

- Claude primary: Opus 4.8; same-vendor fallback: Sonnet 4.6.
- Codex primary: GPT-5.6 Sol at high or xhigh effort; same-vendor fallback: GPT-5.5.

Fallback is explicit and never crosses vendors.

## Transfer

Ordinary council calls are ephemeral. Explicit transfer is the only persistence path:

```bash
crosscheckctl transfer <run-id> --source /absolute/path/to/claude-session.jsonl
```

The transfer importer accepts only a Claude JSONL session owned by the current user and stored below `~/.claude/projects`. It sends a `SESSIONS`-only migration to the normal Codex home, with empty plugin, MCP, hook, subagent, and command lists. The resulting thread ID and source hash are recorded so the task can be found and resumed in Codex Desktop.

## Cancellation And Recovery

```bash
crosscheckctl cancel <run-id>
crosscheckctl status <run-id>
```

Provider processes run in their own process groups. Timeout and cancellation terminate the group, not just the immediate child. Atomic records plus advisory locks make interrupted runs inspectable and prevent concurrent mutation.

## Gated Later Phases

Do not enable the following until three successful real pilots are recorded:

- Hermes side-by-side upgrade and profile cutover
- Kanban state mirroring
- Telegram approval
- Friday 6:30 AM CT health automation
- Crewplane or another orchestration dependency

Telegram approval additionally requires an authorized user/chat identity and a plan-hash-bound event. The Friday health check additionally requires passing Hermes rollback, timeout, approval, and unchanged-cron tests.
