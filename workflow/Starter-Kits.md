# Starter Kits

## Goal

Start new repos from the closest proven shape instead of a generic blank template.

## Available Kits

### Analytics Warehouse

Use when the app sits on top of modeled business data.

Good fit:

- multi-tenant dashboards
- raw -> staging -> mart -> semantic pipelines
- warehouse health endpoints

Start with:

- `templates/archetypes/analytics-warehouse/`
- `knowledgebase/`
- `runbooks/`
- parity + health-check workflow templates

### Dual-Stack Platform

Use when the backend and frontend are separate codebases in one repo.

Good fit:

- FastAPI + Next.js
- separate package managers/toolchains
- schema sync across layers

Start with:

- `templates/archetypes/dual-stack-platform/`
- `TESTING_AND_BROWSER_AUTOMATION.template.md`
- explicit schema-sync checklist

### Internal Ops Dashboard

Use when the product is an operator tool with queues, batch actions, smoke tests, and lots of workflow state.

Start with:

- `templates/archetypes/internal-ops-dashboard/`
- safe fallback guidance in the archetype README
- browser/testing guide
- debug journal

### AI Media SaaS

Use when the product has AI generation, background jobs, asset pipelines, or model/provider complexity.

Start with:

- `templates/archetypes/ai-media-saas/`
- parity docs
- debug journal
- runbooks

## Rule Of Thumb

Pick the nearest kit, then trim what you do not need. Do not start from zero unless the project is truly unusual.
