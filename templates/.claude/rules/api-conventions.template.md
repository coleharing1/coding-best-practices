---
description: API design and handler conventions
paths:
  - "src/api/**"
  - "src/handlers/**"
  - "src/routes/**"
  - "app/api/**"
---

# API Conventions

## Response Shape
All API responses use a consistent envelope:
```json
{ "data": <payload>, "error": null }
{ "data": null, "error": { "message": "...", "code": "..." } }
```

## Validation
- Validate all request bodies at the handler boundary using zod (or your schema library)
- Never trust client input — validate types, ranges, and required fields
- Return 400 with a descriptive error for invalid input

## Error Handling
- Never expose stack traces or internal error details to the client
- Use structured error codes for programmatic handling (e.g., `AUTH_REQUIRED`, `NOT_FOUND`)
- Log full error details server-side; return sanitized messages client-side

## Auth
- Check authentication and authorization at the top of every protected handler
- Never rely on client-side-only auth checks

## Naming
- Use RESTful resource naming: `/users`, `/users/:id`, `/users/:id/orders`
- Use plural nouns for collections
- Use HTTP methods correctly: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
