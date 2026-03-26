# Workflow Scorecard

> Use this scorecard weekly to measure whether the multi-model workflow is improving speed and quality.

---

## How to Use

1. Fill one row per shipped feature or meaningful PR.
2. Review the weekly rollup every Friday.
3. Adjust process only when metrics trend in the wrong direction for 2+ weeks.

---

## Core Metrics (Per Feature / PR)

| Metric | Definition | Target | Why It Matters |
|---|---|---|---|
| Lead time | Start of implementation -> merge time | Downward trend | Primary speed signal |
| First-pass gate success | % changes passing lint/test/build on first gate run | >= 70% | Planning quality + implementation discipline |
| Review finding hit rate | % Gemini/Claude findings accepted and fixed | 30-70% | Filters noisy reviews while keeping useful ones |
| Escaped defects (7-day) | Bugs found after merge in first 7 days | 0 high severity | True quality outcome |
| Rework ratio | Rewritten lines / added lines for same feature | <= 0.30 | Detects plan drift and churn |
| Cost per merged feature | Estimated model spend per merged feature | Stable/downward | Keeps orchestration economically sane |

---

## Feature Log Template

| Date | Branch/PR | Feature | Lead Time (hrs) | First-Pass Gate (Y/N) | Findings Accepted | Findings Rejected | Escaped Defects | Est. AI Cost | Notes |
|---|---|---|---:|---|---:|---:|---:|---:|---|
| [YYYY-MM-DD] | [branch or PR #] | [name] | [n] | [Y/N] | [n] | [n] | [n] | [$] | [short context] |

---

## Weekly Rollup Template

### Week of [YYYY-MM-DD]

- **Merged features/PRs**: [n]
- **Median lead time**: [n hours]
- **First-pass gate success**: [n%]
- **Escaped defects**: [n]
- **Average cost per feature**: [$]

### Interpretation

- If lead time increases and first-pass gate drops, tighten planning quality in Phase 1.
- If findings accepted < 20%, improve reviewer prompts or reduce over-reviewing.
- If escaped defects rise, add missing tests and strengthen failure playbooks.

### Next Week Process Adjustments

1. [Action]
2. [Action]
3. [Action]

---

## Data Collection Notes

- Lead time: derive from worklog start time and merge time.
- Gate success: first execution of `scripts/quality-gate.sh` per feature.
- Findings: count only substantive code findings, not style-only nits.
- Cost: estimate from plan dashboards or session summaries.
