# Cole's Saved Prompts, AI Optimized

Rewritten versions of saved prompts, optimized for clearer execution, stronger outputs, and easier future conversion into slash commands.

## Optimized Prompt 1

```text
Read `README.md`, `WORKLOG.md`, `plans/MACRO-ROADMAP.md`, and the active plans first to understand the project and its current status. Then do a deep dive through the codebase to understand the architecture, current implementation state, completed work, gaps, and the highest-leverage next buildable chunk. After that, create `plans/active/Plan-XXX-Codex.md` as Codex's independent next-step plan. Make it a concrete checklist with scope, current evidence, macro-roadmap alignment, assumptions, risks, blockers, phased implementation steps, and verification commands. Explain why this should be the next plan and why the sequencing is appropriate. Do not read Claude's plan before writing Codex's plan.
```

## Optimized Prompt 1.2

```text
Read `README.md`, `WORKLOG.md`, `plans/MACRO-ROADMAP.md`, and the active plans first so you understand the product, current status, and how this request fits into the broader project. Then do a deep dive on everything related to `[TARGET PAGE, ROUTE, OR FEATURE]` across the codebase, including the UI structure, supporting components, state management, APIs, data flow, existing UX, current limitations, and any already-shipped or partially built capabilities. Treat this as a focused one-off improvement plan for an existing surface, not automatically the next core roadmap milestone, and explicitly call out whether it should stay standalone or change roadmap sequencing.

After you understand the current implementation, research the internet for relevant product patterns, interaction models, technical approaches, and strong reference examples that could improve this surface, especially around `[GOAL, INSPIRATION, OR COMPARABLE PRODUCT PATTERN]`. Then create `plans/active/Plan-XXX-Codex.md` for this focused improvement initiative. Make it a concrete checklist with the problem framing, current-state evidence, UX and product goals, proposed direction, dependencies, risks, tradeoffs, phased implementation steps, verification commands, browser QA expectations, and any human-only decisions. Explain why this is the right next move for this page or feature and why your proposed sequencing is the best balance of impact, scope, and implementation risk.
```

## Optimized Prompt 2

```text
Read `README.md`, `WORKLOG.md`, `plans/MACRO-ROADMAP.md`, and the active plans first to understand the project and its current status. Then do a deep dive through the codebase to understand the architecture, completed work, major risks, and likely next milestones. After that, create `plans/active/Plan-XXX-CLAUDE.md` as Claude's independent next-step plan. Make it a concrete owner-tagged checklist with scope, constraints, current evidence, macro-roadmap alignment, assumptions, risks, blockers, human-only decisions, phased tasks, and verification gates. Explain why this should be the next plan and what risks or edge cases drove your recommendations. Do not read Codex's plan before writing Claude's plan.
```

## Optimized Prompt 3

```text
Read both draft plans carefully and compare where they agree, where they differ, and what each one catches that the other misses. Then do any additional codebase research needed, and use internet research when current documentation or implementation details need verification. After reconciling the differences, write `plans/active/Plan-XXX-Final.md` as the best combined plan. Preserve the strongest ideas from each draft, cut unnecessary work, resolve disagreements explicitly, and produce one owner-tagged checklist with scope, current evidence, macro-roadmap alignment, assumptions, blockers, phased tasks, verification gates, and any human-only login, approval, or browser steps. Briefly explain the major decisions you made and why this final approach is stronger than either draft alone.
```

## Optimized Prompt 4

```text
Begin implementing `plans/active/Plan-XXX-Final.md`. Read the relevant docs and code before each phase, then execute the checklist one item at a time without skipping ahead. Update the checklist as items are completed. Use the browser whenever local app login, QA, or other browser interactions are needed, and ping me if you need me to complete a human-only login, consent, or 2FA step. Do additional codebase or internet research as needed for missing context or up-to-date documentation. Keep changes scoped, run the relevant verification commands after meaningful changes, fix failures before moving on, and report progress clearly.
```

## Optimized Prompt 5

```text
Read `README.md`, `WORKLOG.md`, the macro roadmap, active plans, and the most relevant project docs first. Then audit the repo against this coding-best-practices system and identify what is missing, outdated, duplicated, risky, or unclear across repo structure, planning, docs, testing, browser QA, service setup, safety practices, and repeatable workflow assets. Separate your output into highest-leverage priorities, quick wins, and deeper structural upgrades. Do not make edits yet unless explicitly asked.
```

## Optimized Prompt 6

```text
Audit the full repository structure before changing anything. Classify files and folders into current, historical, generated, duplicate, or misplaced. Then recommend a cleaner target structure, explain the reasoning, and produce a safe step-by-step cleanup plan that calls out dependency risks such as broken imports, scripts, docs links, CI paths, or developer workflow assumptions. Do not move files yet unless explicitly asked.
```

## Optimized Prompt 7

```text
Investigate this bug end to end. Read the relevant docs, plans, and code paths first, then reproduce the issue if possible, trace the likely root cause, identify plausible alternative explanations, and recommend the smallest safe fix. If browser interaction is needed, use it. If login, consent, or 2FA is required, pause and ask me for the human-only step. Summarize findings clearly before or alongside implementation.
```

## Optimized Prompt 8

```text
Review my staged diff like a high-signal senior reviewer. Focus first on logic bugs, regressions, edge cases, failure-state handling, schema or data risks, security concerns, and missing tests. Present findings first, ordered by severity, with specific file references and concise explanations of impact. Keep the summary brief and only mention style issues if they materially affect maintainability or correctness.
```

## Optimized Prompt 9

```text
Perform a security-focused review of the relevant code or diff. Look specifically for authentication and authorization gaps, insecure defaults, secrets exposure, injection risks, trust-boundary mistakes, unsafe browser or API flows, webhook validation issues, production-write risks, and any dangerous assumptions around environment or user input. Flag anything that should block merge and explain the risk clearly.
```

## Optimized Prompt 10

```text
Run the appropriate quality gate for this change. Determine which checks matter based on the files changed, then run them in a sensible order such as lint, tests, typecheck, build, browser or E2E checks, and any relevant parity or schema checks. Fix reasonable failures, rerun as needed, and report exactly what passed, what failed, what you changed, and what still needs human attention.
```

## Optimized Prompt 11

```text
Verify this feature in the browser from a real user perspective. Start the app if needed, open the correct page, exercise the main happy path plus obvious nearby failure states, watch for console errors, and report a clear pass or fail result. If authentication, consent, org selection, or 2FA is required, pause and ask me to complete the human-only step, then resume verification immediately after.
```

## Optimized Prompt 12

```text
Update the repo memory after this work. Read the diff and update `WORKLOG.md` plus any `README.md`, plan, runbook, testing doc, browser QA doc, or knowledgebase page that no longer matches reality. Keep updates concise, accurate, and tied to what actually changed, including verification status and any meaningful follow-up notes.
```

## Optimized Prompt 13

```text
Read `plans/MACRO-ROADMAP.md`, the active plans, `WORKLOG.md`, and the current codebase state. Then update the roadmap to reflect what is now complete, what sequencing has changed, which assumptions are stale, and what the most likely next numbered plans should be. Keep the roadmap durable and strategic rather than turning it into an implementation checklist.
```

## Optimized Prompt 14

```text
This workflow is repeating, so decide whether it should stay a prompt or be promoted into a command, skill, rule, hook, or automation. Recommend the right level based on frequency, complexity, tool usage, and risk. Explain why, and if appropriate create the first reusable version in the correct repo location with a clean structure and naming that fits the existing workflow system.
```

## Optimized Prompt 15

```text
Analyze this schema or database change before implementation. Identify the affected tables, queries, types, migrations, API contracts, validation layers, backfills, rollback concerns, environment-parity risks, and verification steps. Then write the safest implementation plan, including ordering, dependency risks, and how to confirm the change without creating data drift or breaking existing behavior.
```

## Optimized Prompt 16

```text
Prepare these changes for GitHub safely. Review the current branch and working tree, confirm the intended scope, stage only the relevant files, write a clean commit message, push the branch, and prepare a strong PR title and body that explains what changed, why it changed, and how it was validated. If the worktree is mixed or risky, pause and confirm scope before staging unrelated files.
```

## Optimized Prompt 17

```text
Fix responsive layout and visual polish for `[PAGE, ROUTE, OR FEATURE]` in the same session—do not stop at a findings-only report. Start the app if needed, then work in a tight loop: inspect in the browser, change the smallest reasonable code or style fix, reload or rely on hot reload, and re-inspect until the problem is resolved at that viewport. Repeat across viewports until the surface is in good shape.

Verify at least: a narrow mobile viewport (about 390px unless the project documents a canonical test width), a desktop viewport (about 1280px or wider), and an intermediate width if this UI has a tablet-specific layout or documented breakpoints. At each size, check: horizontal overflow or unwanted scroll; section, nav, and footer reflow; modals, drawers, and dropdowns; forms, tables, and dense content; images and media; spacing rhythm and alignment; typography hierarchy and line length; usable tap or click targets on narrow widths. Watch the console; fix errors you introduce and clear any straightforward pre-existing issues tied to this work.

Prioritize fixes that block usability first, then obvious layout bugs, then polish. Prefer project styling conventions and design tokens over one-off hacks. If something requires a real product or brand decision you cannot infer, stop that sub-issue and note it briefly—otherwise keep iterating until checks pass.

When finished, give a concise summary: files touched, what changed, and how you verified (viewports exercised). If authentication, consent, org selection, or 2FA is required, pause for the human-only step, then resume the same fix-and-verify loop immediately after.
```
