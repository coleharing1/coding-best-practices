# Schema Sync Recipes

> Different stacks drift in different ways. The fix is to define the layers that must move together.

## Goal

Make schema changes explicit, reviewable, and synchronized across code, types, and runtime behavior.

## Recipe 1: SQLAlchemy + Pydantic + Alembic + TypeScript Frontend

When the data model changes, update all layers:

1. ORM model
2. validation/schema layer
3. migration
4. frontend/shared types
5. API client or contract surface

This is the BanBox pattern.

## Recipe 2: Supabase / SQL Migrations + Generated Types + App Validators

When migrations change:

1. migration SQL
2. generated database types
3. runtime validators / Zod schemas
4. API/loader code
5. parity checks

This is the LifeCurrent and Admatrix pattern.

## Recipe 3: Warehouse Modeling Stack

When a modeled warehouse changes:

1. raw landing assumptions
2. staging views
3. mart/semantic views
4. app query builders/loaders
5. refresh helpers and warehouse health checks

This is the Coupler / Texas Fowlers OS pattern.

## Required Behaviors

- treat schema changes as their own phase when practical
- document the sync checklist in `AGENTS.md` or `CLAUDE.md`
- add or update contract-focused tests
- run parity or verification queries, not just unit tests

## Anti-Patterns

- updating only the migration
- updating only generated types
- trusting the dashboard UI as the first proof the schema works

## Recommendation

Every repo with data-model changes should name its schema-sync layers explicitly.
