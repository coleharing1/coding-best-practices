# Cole's Saved Prompts

Ongoing place to save favorite prompts before turning them into slash commands.

## Prompt 1

```text
"please read the readme and worklog and plans to understand the project and its current status, then do a deep dive of the project codebase to understand it all, then create plan-xx-Codex.md of the next plan based on what all u think we should do next and why."
```

## Prompt 2

```text
"please read the readme and worklog and plans to understand the project and its current status, then do a deep dive of the project codebase to understand it all, then create plan-xx-Claude.md of the next plan based on what all u think we should do next and why."
```

## Prompt 3

```text
"Please read both plan-xx's to see how they differ then do additional research of the codebase and internet to confirm anything additional, then write plan-xx-final based on what you think is the best combined approach."
```

## Prompt 4

```text
"please begin implementing plan-xx-final for me. Use the browser to log into the app locally or anything else in the browser if u need to. ping me if you need me to log in to a browser. Feel free do additional research of the project codebase or internet for additional context as u need it. Make sure u check things off of the checklist as they are completed."
```

## Prompt 5

```text
Please read the README, WORKLOG, plans, key docs, and the codebase to understand the current project. Then audit the repo against our coding best practices system and tell me what is missing, outdated, duplicated, risky, or unclear. Prioritize the highest-leverage improvements first and separate quick wins from deeper structural work. Do not edit anything yet unless I ask.
```

## Prompt 6

```text
Please read the whole repo and classify what is current, historical, generated, duplicate, or misplaced. Then recommend a cleaner target structure and a safe step-by-step cleanup plan before moving any files. Call out any moves that could break imports, scripts, docs, or developer workflows.
```

## Prompt 7

```text
Please investigate this bug end to end. Read the relevant docs, plans, and code paths, reproduce the issue if possible, trace the likely root cause, identify alternative explanations, and recommend the smallest safe fix. Use the browser if needed, and tell me if you need me for a login or human-only step.
```

## Prompt 8

```text
Please review my staged diff like a senior reviewer. Focus on logic bugs, regressions, missing edge cases, failure-state behavior, security concerns, schema/data risks, and missing tests. Give findings first, ordered by severity, with file references. Keep summary brief.
```

## Prompt 9

```text
Please perform a security-focused review of the relevant code or diff. Look for auth gaps, insecure defaults, secrets exposure, injection risks, access-control mistakes, unsafe browser or API flows, webhook trust issues, and production-write risks. Flag anything that should block merge.
```

## Prompt 10

```text
Please run the appropriate quality gate for this change. Figure out which checks matter based on the files changed, run them in the right order, fix reasonable failures, and tell me exactly what passed, what failed, what you changed, and what still needs human attention.
```

## Prompt 11

```text
Please verify this feature in the browser from a real user perspective. Start the app if needed, open the correct page, check the main happy path, look for obvious UI issues and console errors, and report pass/fail clearly. If login or consent is required, pause and ping me for the human-only step.
```

## Prompt 12

```text
Please update the repo memory after this work. Read the diff and update WORKLOG.md plus any README, plan, runbook, testing doc, or knowledgebase file that no longer matches reality. Keep the updates concise, accurate, and grounded in what actually changed.
```

## Prompt 13

```text
Please read the macro roadmap, active plans, worklog, and current codebase state, then update the roadmap to reflect what is complete, what changed in sequencing, what assumptions are now outdated, and what the most likely next numbered plans should be.
```

## Prompt 14

```text
This workflow is repeating. Please decide whether it should become a prompt, command, skill, rule, hook, or automation. Recommend the right level, explain why, and if appropriate create the first version in the correct repo location with a clean reusable structure.
```

## Prompt 15

```text
Please analyze this schema or database change before implementation. Identify affected tables, queries, types, API contracts, migrations, backfills, rollback concerns, environment-parity risks, and verification steps. Then write the safest implementation plan.
```

## Prompt 16

```text
Please prepare these changes for GitHub safely. Review the current branch and working tree, confirm the intended scope, stage only the relevant files, write a clean commit message, push the branch, and prepare a strong PR title and body with validation notes.
```

## Prompt 17

```text
Please fix responsive layout and visual polish for this page or feature in one continuous pass—not just a report. Use the browser at a narrow mobile width and a comfortable desktop width (and tablet if it matters). After you spot a problem, edit the code or styles, reload or hot-refresh, and re-check the same viewports until the issues are gone or you hit a genuine product or design decision you cannot resolve without me. Keep iterating: look, change, verify, repeat. Watch the console for errors and fix any you caused or can reasonably clear. When you are done, give a short summary of what you changed and how you confirmed it. If login or consent is required, pause and ping me for the human-only step, then continue the same fix-and-verify loop.
```
