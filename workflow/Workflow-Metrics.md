# Workflow Metrics

> Last updated: April 1, 2026
> Role in workflow: Weekly measurement loop for quality, speed, cost, and workflow portability
> Companion template: `templates/weekly-retro.md`

---

## Goal

Measure workflow quality without over-instrumentation. Use a small set of metrics to answer:
1. Are we shipping faster?
2. Are we shipping safer?
3. Are we spending AI budget efficiently?
4. Are we reducing repeat work and manual dashboard round-trips?

---

## Cadence

Run this loop once per week:
1. Append one row to `metrics/weekly-metrics.csv` (or your own tracker).
2. Fill out `templates/weekly-retro.md` for that week.
3. Pick 1 process change to keep and 1 to adjust.

Keep cadence stable before changing metrics.

---

## Core Metrics (Start Here)

Track only these seven metrics for 4 weeks before adding more:

| Metric | Why It Matters | Definition |
|---|---|---|
| `merged_prs` | Throughput | Number of PRs merged in the week |
| `lead_time_hours_p50` | Speed | Median hours from first code commit to merge |
| `quality_gate_fail_rate` | Stability | Failed gate runs / total gate runs |
| `post_merge_regressions` | Escaped defects | Issues found after merge linked to that week's changes |
| `rework_prs` | Plan quality | PRs requiring major rework after review |
| `ai_cost_usd` | Budget control | Estimated weekly spend across tools |
| `high_risk_changes` | Exposure | Count of `T3` changes merged |

---

## Optional Metrics (Only If Needed)

- `review_turns_avg` — average review cycles before merge
- `flaky_test_events` — times tests failed without code changes
- `worklog_compliance_pct` — meaningful changes with worklog entry
- `automation_adoption_pct` — changes using script/CI gate vs manual only
- `repeatable_actions_promoted` — number of prompts upgraded into commands, skills, hooks, or automations
- `manual_dashboard_roundtrips` — times the human had to re-enter a service dashboard because the AI did not have a durable access path or handoff runbook

---

## Data Collection Sources

| Metric Family | Source |
|---|---|
| Throughput & lead time | GitHub PR metadata |
| Gate failures | CI logs + local gate logs |
| Regressions | Issue tracker labels + incident notes |
| AI spend | Plan dashboards + API usage pages |
| Risk-tier counts | PR template/commit body/worklog entries |
| Action promotion | worklog entries, commands/skills/hook diffs |
| Dashboard round-trips | weekly retro notes, service handoff runbooks |

---

## Guardrails

1. Do not optimize one metric at the expense of product outcomes.
2. Do not compare week-over-week if scope changed drastically.
3. Treat anomalies as investigation triggers, not immediate process rewrites.

---

## Weekly Interpretation Heuristics

- If `quality_gate_fail_rate` rises and `post_merge_regressions` also rise:
  - Tighten review prompts and risk-tier enforcement.

- If `lead_time_hours_p50` rises but defect metrics improve:
  - Likely intentional hardening; verify if sustainable.

- If `ai_cost_usd` rises with no throughput/quality gain:
  - Re-route more execution work to lower-cost models.

- If `rework_prs` is high:
  - Strengthen Phase 1 planning and acceptance criteria.

- If `manual_dashboard_roundtrips` is high:
  - Front-load service setup earlier and improve browser-login handoff docs.

- If `repeatable_actions_promoted` stays at zero while the same prompts keep recurring:
  - Promote those workflows into commands, skills, hooks, or automations instead of relying on memory.

---

## Monthly Reset

At month end:
1. Keep only metrics that informed at least one decision.
2. Remove vanity metrics.
3. Refresh target bands.

Example target bands (customize per project):
- `quality_gate_fail_rate <= 0.20`
- `post_merge_regressions <= 1 / week`
- `worklog_compliance_pct >= 0.90`

---

## Minimal Starter Tracker

Use `metrics/weekly-metrics.csv.template` as your starter and copy it to `metrics/weekly-metrics.csv`.
