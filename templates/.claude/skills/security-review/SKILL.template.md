---
name: security-review
description: >
  Comprehensive security audit. Use when reviewing code for vulnerabilities,
  before deployments, when the user mentions security, or when changes touch
  auth, payments, middleware, or sensitive data handlers.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Security Review

Analyze the codebase for security vulnerabilities. Focus on code that has changed recently or is flagged as high-risk.

## Audit Checklist

1. **Authentication & Authorization**
   - Are auth checks present on all protected routes?
   - Are tokens validated server-side?
   - Are role/permission checks in place?

2. **Input Validation**
   - Is all user input validated at the boundary?
   - Are parameterized queries used (no string concatenation in SQL)?
   - Are file uploads validated (type, size, content)?

3. **Secrets & Credentials**
   - Are any secrets hardcoded in source files?
   - Are `.env` files properly gitignored?
   - Are secrets exposed in logs, error messages, or API responses?

4. **Data Exposure**
   - Are sensitive fields (passwords, tokens) excluded from API responses?
   - Is PII properly handled and encrypted at rest?
   - Are error messages sanitized (no stack traces to clients)?

5. **Transport & Headers**
   - Are security headers set (CSP, HSTS, X-Frame-Options)?
   - Is CORS configured restrictively?
   - Is HTTPS enforced in production?

## Output Format

Report findings with:
- **Severity**: critical / high / medium / low
- **Location**: file path + line range
- **Description**: what the vulnerability is
- **Remediation**: specific fix with code suggestion
- **Impact**: what an attacker could achieve

End with a final verdict: `secure` or `needs remediation`.
