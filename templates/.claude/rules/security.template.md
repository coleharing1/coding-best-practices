---
description: Security rules for sensitive code paths
paths:
  - "src/auth/**"
  - "src/middleware/**"
  - "src/api/**"
  - "app/api/**"
  - "src/lib/auth*"
  - "src/lib/crypto*"
---

# Security Rules

## Authentication
- Always verify auth tokens server-side; never trust client-only auth state
- Use httpOnly, secure, sameSite cookies for session tokens
- Implement proper token expiry and refresh flows

## Input Handling
- Sanitize all user input before database queries or HTML rendering
- Use parameterized queries — never concatenate user input into SQL
- Validate file uploads: check MIME types, enforce size limits, scan for malicious content

## Secrets
- Never hardcode secrets, API keys, or credentials in source code
- Use environment variables for all secrets; document them in `.env.local.example`
- Never log secrets or include them in error messages

## Data Exposure
- Never return sensitive fields (passwords, tokens, internal IDs) in API responses
- Apply field-level access control — different roles see different data
- Audit what data you serialize before sending to the client

## Headers and Transport
- Set security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`
- Enforce HTTPS in production
- Configure CORS to allow only trusted origins
