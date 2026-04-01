---
description: Browser QA and Playwright workflow guidance
---

# Browser QA

- Follow the documented browser/test path for this repo.
- Prefer isolated Playwright or an auth-bypass copy when the real app blocks agent QA.
- Capture artifacts when a browser check fails.
- When browser login is required, use the handoff pattern: agent opens page, user logs in, agent resumes.
