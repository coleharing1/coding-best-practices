# Testing And Browser Automation

Use this file as the repo's quick reference for what testing and browser automation exists, what each path is good for, and how an AI agent should use it.

## What We Have

### 1. Unit / Integration Tests

Command:

```bash
[test command]
```

What it covers:

- [service logic]
- [contract checks]
- [other]

### 2. Browser / E2E

Commands:

```bash
[playwright install command]
[e2e command]
[headed debug command]
```

What it checks:

- [route or flow]
- [route or flow]

Artifacts on failure:

- screenshots
- traces
- videos

### 3. Quality Gate

Command:

```bash
scripts/quality-gate.sh
```

Useful variants:

```bash
scripts/quality-gate.sh --skip-review
scripts/quality-gate.sh --risk-tier T2
```

## Browser Paths

### Isolated Playwright Server

- Base URL: `[url]`
- Best for: [why]

### Existing Local App

- Base URL override: `[url]`
- Best for: [why]

### Real Browser / User Lane

- Browser: `[Google Chrome / other]`
- Best for: [logged-in state, extensions, real profile, auth debugging]

### Auth / Bypass Notes

- [document auth bypass or credential requirements]

### Browser Login Handoff

- How the agent opens the page: `[command or browser action]`
- What the user must do manually: `[login / 2FA / org selection / consent]`
- What the agent resumes after login: `[env setup / QA / route verification / docs update]`

## Current Limits

- [known test or browser limitations]

## Good Prompts To Give An Agent

- "Run the quality gate and fix what fails."
- "Use Playwright to reproduce this UI bug."
- "Use the isolated browser harness instead of my current dev server."
