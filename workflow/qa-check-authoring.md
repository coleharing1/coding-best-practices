# Authoring `crosscheckctl verify --command` checks

Verification commands run inside `codex sandbox` (deny-by-default filesystem: worktree + private
temp only, network off). Two macOS-specific pitfalls, both discovered the hard way during the
2026-07-16 validation pilots (each one failed an otherwise-green run):

1. **No `/dev/null`.** The sandbox denies writes outside the granted roots, including `/dev/null`.
   A redirect like `1>/dev/null` fails the `open()`, and if stderr is being captured the shell's own
   error message is swallowed with it — the check dies silently with exit 1 and empty logs.
   *Instead:* capture output into a variable and ignore it, or pipe to `grep`/`tail`.

2. **`python3` is the xcrun shim.** Under the sandbox, `/usr/bin/python3` emits xcrun/xcodebuild
   noise (confstr warnings, cache-file errors, DVTFilePathFSEvents lines) on **stderr** before the
   real program runs. Any check that captures `2>&1` and does whole-string equality will fail even
   when the program's own output is exactly right.
   *Instead:* compare **stdout only** where possible; when stderr matters, match the **last line**
   (`… 2>&1 | tail -n1 | grep -qx "expected"`) or grep for the expected text — never whole-string
   equality over combined output.

Also by design: a failed verification command moves the run to `failed`, which is terminal — a bad
*check* kills a good run (both pilot-3 false failures required a fresh plan + a fresh human
approval). Dry-run every nontrivial check first, directly against the run's worktree:

    cd <run worktree> && codex sandbox -- sh -c '<your check>'; echo rc=$?

Derive checks from the final plan's locked-behavior section; keep them few and behavioral.
