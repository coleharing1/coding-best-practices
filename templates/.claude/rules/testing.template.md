---
description: Testing requirements and conventions
---

# Testing

## Requirements
- Write tests alongside implementation, not as an afterthought
- New features require at least one happy-path test and one error-path test
- Bug fixes require a regression test that reproduces the original bug

## Structure
- Test files live next to source files: `Component.tsx` + `Component.test.tsx`
- Use descriptive test names: `it("returns 404 when user does not exist")`
- Group related tests with `describe` blocks

## Conventions
- Prefer real implementations over mocks when practical
- Mock only external boundaries (APIs, databases, third-party services)
- Use factories or fixtures for test data — avoid hardcoded objects in every test
- Clean up side effects (created files, DB records) in `afterEach`

## Commands
- `npm run test -- --run` — run full suite
- `npm run test -- --run path/to/file` — run single file
- `npm run test -- --coverage` — check coverage

## Quality Gate
- Tests must pass before any commit (enforced by quality gate)
- If tests fail after your changes, fix them before reporting completion
