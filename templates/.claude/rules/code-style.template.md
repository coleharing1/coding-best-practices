---
description: Code style and naming conventions
---

# Code Style

## Naming
- Components: PascalCase (`UserProfile.tsx`)
- Utilities/hooks: camelCase (`useAuth.ts`, `formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRIES`, `API_BASE_URL`)
- Types/interfaces: PascalCase with descriptive names (`UserProfile`, `ApiResponse<T>`)

## File Organization
- One component per file; filename matches export name
- Keep files under 500 lines; split into modules when approaching the limit
- Group imports: external libs > internal modules > relative imports > types

## Patterns
- Prefer functional/declarative patterns; avoid classes unless integrating external SDKs
- Prefer named exports over default exports
- Prefer explicit error handling over silent fallbacks
- Prefer composition over inheritance
- Avoid `any` — use `unknown` with type guards when the type is truly dynamic

## What Not To Do
- No unused imports or variables (TypeScript strict mode enforces this)
- No magic numbers — extract to named constants
- No deeply nested ternaries — use early returns or switch statements
