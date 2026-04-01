# Worklog 2.0

> Your best worklogs behave more like compact change reports than journals.

## Goal

Preserve enough implementation memory that a future session can answer:

- what changed
- why it changed
- how it was verified
- what still needs attention

## Standard Entry Shape

Use this order:

1. `Goal`
2. `Changes`
3. `Notes / decisions`
4. `Verification`
5. `Follow-ups`

## What Makes A Strong Entry

- One logical unit of work per entry
- Real file paths in `Changes`
- Concrete verification commands or explicit skips
- Decisions written in plain language
- Follow-ups that are actionable, not vague

## When To Add A Worklog Entry

Add one when you changed:

- behavior
- architecture
- automation
- schema/contracts
- process/governance
- deployment or operator-facing workflows

## When To Also Use A Debug Journal

Use `DEBUG-JOURNAL.md` when:

- the main work was investigation rather than a landed change
- you chased multiple false leads
- the issue involved external outages or flaky systems
- you want to preserve root-cause details without polluting the main change log

## Anti-Patterns

- entries with no file paths
- entries that say only "fixed bug"
- hiding skipped checks
- editing old entries to rewrite history

## Rule Of Thumb

If a future-you would ask "wait, why did we do it that way?" then it belongs in the worklog.
