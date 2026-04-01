# Service Setup Handoff

## Purpose

Use this when a hosted service needs a browser-login handoff before the AI agent can finish setup.

## Ownership Pattern

1. `[AI]` Open the exact service page or auth command.
2. `[User]` Complete login, 2FA, org selection, consent, or account linking.
3. `[AI]` Resume setup immediately after the authenticated session exists.
4. `[AI]` Document what changed and how to verify it later.

## Record

- service name
- environment (`dev`, `preview`, `prod`)
- project ref, team ID, org ID, or account selected
- auth method now available to the AI
- local artifacts created
  - `.vercel/project.json`
  - `supabase/config.toml`
  - MCP config entries
  - `.env.local.example` updates
- remaining human-only steps
- next commands or verification steps
