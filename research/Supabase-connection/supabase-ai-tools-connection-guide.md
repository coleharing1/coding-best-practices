# Connecting Cursor, Claude Code & OpenAI Codex to Supabase
## Complete Guide: Connection Methods, Pros/Cons, Dev/Prod Workflows & Key Storage

---

## The Big Picture: MCP Is the Standard

All three tools — **Cursor**, **Claude Code**, and **OpenAI Codex** — connect to Supabase through the **Model Context Protocol (MCP)**. Supabase now hosts an official remote MCP server at `https://mcp.supabase.com/mcp` that replaced the older local-only approach. This is the primary (and recommended) way to give your AI coding tools direct access to your Supabase projects.

Once connected via MCP, these tools can: create/manage tables, run SQL queries, apply migrations, generate TypeScript types, manage branches, fetch logs, deploy Edge Functions, and more — all through natural language prompts.

---

## 1. CURSOR → Supabase

### Method A: Official Supabase Remote MCP (Recommended)

**How it works:** Supabase's hosted MCP server uses OAuth-based dynamic client registration. You add the server URL to Cursor's MCP config, and it opens a browser window for you to authenticate with your Supabase account.

**Setup:**

1. Go to your Supabase Dashboard → Project → MCP connection tab (or use the docs page at supabase.com/docs/guides/getting-started/mcp)
2. Select "Cursor" as your client — it generates the config for you
3. Add to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project-level):

```json
{
  "mcpServers": {
    "supabase": {
      "url": "https://mcp.supabase.com/mcp?project_ref=YOUR_PROJECT_REF"
    }
  }
}
```

4. Restart Cursor → It will prompt you to authenticate in the browser
5. Verify: Settings → Cursor Settings → Tools & MCP → look for green dot

**Pros:**
- First-class official support — Supabase docs have Cursor as a primary client
- OAuth-based auth (no manual token management)
- Project-scoped by default when you include `project_ref`
- Supports read-only mode (`&read_only=true` URL param)
- Mature and stable — largest community of users

**Cons:**
- 40-tool limit in Cursor — if you have multiple MCP servers, you may hit the ceiling
- Can only scope to ONE project per MCP server entry (matters for your dev/prod setup)
- Some users report intermittent "client closed" or "failed to create server" errors on initial setup
- Token context can get eaten fast if MCP returns large table schemas

### Method B: STDIO-based Local MCP Server (Legacy/Alternative)

**How it works:** Runs the Supabase MCP package as a local Node process that Cursor communicates with over stdio.

**Setup:**
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--access-token",
        "YOUR_SUPABASE_PAT"
      ]
    }
  }
}
```

**Pros:**
- Works offline/air-gapped
- Full control over the process
- Can pass Personal Access Token (PAT) directly

**Cons:**
- Requires generating and managing a PAT manually
- PAT has broad org-level access (less secure)
- npx startup can be slow or timeout
- Being phased out in favor of the remote MCP approach

### Method C: Composio MCP (Third-Party Wrapper)

**How it works:** Composio acts as an integration layer that lets you pick specific Supabase tools and combine with other services (Jira, GitHub, etc.) on one MCP endpoint.

**Pros:**
- Cherry-pick only the tools you need (reduces context window bloat)
- Combine multiple services on one MCP endpoint
- OAuth managed by Composio

**Cons:**
- Third-party dependency and potential point of failure
- Additional latency
- Another account/service to manage

---

## 2. CLAUDE CODE → Supabase

### Method A: Official Supabase Remote MCP (Recommended)

**How it works:** Same hosted MCP server, but configured through Claude Code's CLI or `.claude.json` config file.

**Setup (CLI method — easiest):**

```bash
claude mcp add supabase --url "https://mcp.supabase.com/mcp?project_ref=YOUR_PROJECT_REF"
```

Then authenticate:
```bash
# In Claude Code, type /mcp to check status
# If it says "unauthenticated," it will give you an auth URL
# Complete the browser OAuth flow
```

**Setup (Config file method):**

Add to `.claude.json` in your project root or `~/.claude.json` globally:
```json
{
  "mcpServers": {
    "supabase": {
      "url": "https://mcp.supabase.com/mcp?project_ref=YOUR_PROJECT_REF"
    }
  }
}
```

**Pros:**
- Native MCP support — Claude Code was built with MCP as a core feature
- `/mcp` command lets you check status and trigger auth inline
- Works identically in Claude Code CLI and the Claude Code extension in VS Code/Cursor
- Supports custom headers for CI environments (PAT-based auth)
- Can install pre-built Claude Code Templates for Supabase (agents, commands, MCP):
  ```bash
  npx claude-code-templates@latest --mcp database/supabase
  ```
  This gives you 2 agents, 8 slash commands, and the MCP connection in one install

**Cons:**
- Auth flow can be finicky — some users report needing to run `/mcp` manually after adding the server to trigger authentication
- Like Cursor, scoped to one project per MCP entry
- Claude Code is terminal-based, so less visual feedback than Cursor's green-dot indicator

### Method B: STDIO Local MCP + PAT

Same as Cursor's Method B:
```bash
claude mcp add-json "supabase" '{"command":"npx","args":["-y","@supabase/mcp-server-supabase@latest","--access-token","YOUR_PAT"]}'
```

**Pros/Cons:** Same as Cursor's local method, plus Claude Code's CLI makes adding/removing MCP servers very clean.

### Method C: Claude Code Templates (Supabase-Specific Agents & Commands)

**How it works:** Community-built templates that install Supabase-specific slash commands and agent definitions into your `.claude/` directory.

```bash
# Install everything at once
npx claude-code-templates@latest \
  --command "database/supabase-schema-sync, database/supabase-migration-assistant, database/supabase-backup-manager, database/supabase-data-explorer" \
  --agent "database/supabase-schema-architect" \
  --mcp database/supabase
```

This creates:
```
your-project/
├── .claude/
│   ├── commands/
│   │   ├── supabase-schema-sync.md
│   │   ├── supabase-migration-assistant.md
│   │   ├── supabase-backup-manager.md
│   │   └── supabase-data-explorer.md
│   └── agents/
│       └── supabase-schema-architect.md
└── .mcp.json
```

**Pros:**
- Pre-built workflows for schema sync, migrations, backups, data exploration
- Combines MCP connection with higher-level agent logic
- Plays perfectly with your existing `.claude/commands/` setup

**Cons:**
- Community-maintained (not official Supabase)
- Templates may lag behind MCP server updates

---

## 3. OPENAI CODEX → Supabase

### Method A: Remote MCP via config.toml (Recommended)

**How it works:** Codex stores MCP config in `~/.codex/config.toml` (or project-scoped `.codex/config.toml`). It supports both STDIO and Streamable HTTP MCP servers.

**Setup:**

```toml
# ~/.codex/config.toml

[mcp_servers.supabase]
url = "https://mcp.supabase.com/mcp?project_ref=YOUR_PROJECT_REF"
startup_timeout_sec = 120
tool_timeout_sec = 600
```

Then authenticate:
```bash
codex mcp login supabase
# Opens browser for OAuth flow
# Restart Codex CLI after completing
```

Verify with `/mcp` in the Codex TUI.

**Pros:**
- Config is shared between Codex CLI and the Codex VS Code extension (one setup, two clients)
- Supports OAuth login flow natively (`codex mcp login`)
- `codex mcp add` CLI makes server management easy
- Supports `bearer_token_env_var` for CI/automated environments

**Cons:**
- **Youngest/least mature of the three** — there are known issues with OAuth token refresh failing, requiring `codex mcp login` re-runs
- VS Code extension has had issues detecting MCP servers that work fine in the CLI (session isolation bug)
- TOML config format is different from Cursor/Claude Code's JSON — can't share configs
- Some users report MCP startup timeouts, especially with npx-based STDIO servers
- Community and documentation are thinner compared to Cursor and Claude Code for Supabase specifically

### Method B: STDIO Local MCP + PAT

```toml
[mcp_servers.supabase]
command = "npx"
args = ["-y", "@supabase/mcp-server-supabase@latest", "--read-only", "--project-ref=YOUR_PROJECT_REF"]

[mcp_servers.supabase.env]
SUPABASE_ACCESS_TOKEN = "your_pat_here"
```

**Pros/Cons:** Same general tradeoffs as the other tools' local STDIO approach. Codex-specific issue: startup timeouts are more common, and some users need to run `npx @supabase/mcp-server-supabase` once manually before Codex can pick it up.

---

## 4. YOUR DEV/PROD DUAL-PROJECT SETUP

Since you run two Supabase projects (dev database and prod database), here's the recommended approach:

### Option A: Two Named MCP Server Entries (Recommended)

Register each project as a separate MCP server with a clear name:

**Cursor** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "supabase-dev": {
      "url": "https://mcp.supabase.com/mcp?project_ref=DEV_PROJECT_REF"
    },
    "supabase-prod": {
      "url": "https://mcp.supabase.com/mcp?project_ref=PROD_PROJECT_REF&read_only=true"
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add supabase-dev --url "https://mcp.supabase.com/mcp?project_ref=DEV_PROJECT_REF"
claude mcp add supabase-prod --url "https://mcp.supabase.com/mcp?project_ref=PROD_PROJECT_REF&read_only=true"
```

**Codex** (`~/.codex/config.toml`):
```toml
[mcp_servers.supabase-dev]
url = "https://mcp.supabase.com/mcp?project_ref=DEV_PROJECT_REF"

[mcp_servers.supabase-prod]
url = "https://mcp.supabase.com/mcp?project_ref=PROD_PROJECT_REF&read_only=true"
```

**Critical security note:** Always add `&read_only=true` to your production MCP URL. This prevents the AI from accidentally running destructive queries against production data. Supabase themselves strongly recommend never connecting MCP to production in write mode.

### Option B: Un-scoped MCP (Access All Projects)

If you omit the `project_ref` parameter, the MCP server can see ALL projects in your org. Then you can ask the AI "list my projects" and it can switch between them.

**Pros:** Simpler config (one entry instead of two)
**Cons:** Broader access surface, easier to accidentally hit the wrong project, and tools like `list_projects` add noise to the context

### Comparing Dev vs Prod Schemas (The "Dump" Workflow)

To have the AI compare what's different between your two databases, you can:

1. **Via MCP directly:** Ask the AI to use `execute_sql` on both servers and compare schemas:
   ```
   "Using supabase-dev, run: SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' ORDER BY table_name, ordinal_position"
   
   "Now do the same on supabase-prod and tell me what's different"
   ```

2. **Via Supabase CLI (better for full dumps):**
   ```bash
   # Dump dev schema
   npx supabase db dump --db-url "$DEV_DB_URL" --schema public > dev_schema.sql
   
   # Dump prod schema  
   npx supabase db dump --db-url "$PROD_DB_URL" --schema public > prod_schema.sql
   
   # Diff them
   diff dev_schema.sql prod_schema.sql
   ```

3. **Via `supabase db diff`:** If you have your local Supabase CLI linked to production, you can generate a migration diff against your dev database:
   ```bash
   supabase db diff -f schema_changes --db-url "DEV_DB_CONNECTION_STRING"
   ```
   This outputs a `.sql` migration file showing exactly what needs to change.

4. **Database Branching (Paid plans):** If you're on a Supabase paid plan, you can use database branching through MCP — the AI can create branches, run migrations against them, and merge back. This is the cleanest workflow but costs per-branch.

---

## 5. WHERE TO STORE KEYS, URLS & CONNECTION INFO

### The File Hierarchy

Here's the complete picture of where different credentials and configs live:

```
your-project/
├── .env                          # Shared defaults (committed to git)
├── .env.local                    # LOCAL overrides (NEVER committed)
├── .env.development              # Dev-specific (optional, committed)
├── .env.production               # Prod-specific (optional, committed)
│
├── .cursor/
│   └── mcp.json                  # Cursor MCP config (project-scoped)
│
├── .claude.json                  # Claude Code MCP config (project-scoped)
├── .claude/
│   └── commands/                 # Your slash commands
│
├── .codex/
│   └── config.toml               # Codex MCP config (project-scoped)
│
├── .gitignore                    # MUST include .env.local and any PAT files
│
└── supabase/
    ├── config.toml               # Supabase CLI config
    └── functions/
        └── .env                  # Edge Function secrets (local dev)
```

### What Goes Where

**`.env` (committed to git — public/shared values only):**
```bash
# Safe to commit — these are public-facing keys
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...your_anon_key
# OR the new publishable key format:
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY=sb_publishable_xxx

# App-level defaults
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

**`.env.local` (NEVER committed — secrets and local overrides):**
```bash
# DANGER ZONE — never commit this file
SUPABASE_SERVICE_ROLE_KEY=eyJ...your_service_role_key
SUPABASE_DB_URL=postgresql://postgres:PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres

# For dev database (override the .env defaults)
NEXT_PUBLIC_SUPABASE_URL=https://dev-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...dev_anon_key

# Personal Access Token for MCP/CLI
SUPABASE_ACCESS_TOKEN=sbp_xxxxxxxxxxxxx
```

**`.env.development` and `.env.production` (optional, committed):**
```bash
# .env.development
NEXT_PUBLIC_SUPABASE_URL=https://dev-project-ref.supabase.co

# .env.production  
NEXT_PUBLIC_SUPABASE_URL=https://prod-project-ref.supabase.co
```

### Priority Order (Next.js)

`.env.local` > `.env.development` / `.env.production` > `.env`

This means `.env.local` always wins, which is exactly what you want — your local machine uses dev keys, and your CI/hosting platform (Vercel, etc.) sets production keys as environment variables at the platform level.

### Key Types Explained

| Key | Where It Lives | Exposed to Browser? | Purpose |
|-----|---------------|---------------------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | `.env` | Yes | Your project's API URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `.env` | Yes | Client-side operations (protected by RLS) |
| `SUPABASE_SERVICE_ROLE_KEY` | `.env.local` only | **NEVER** | Bypasses RLS — server-side only |
| `SUPABASE_DB_URL` | `.env.local` only | **NEVER** | Direct Postgres connection string |
| `SUPABASE_ACCESS_TOKEN` (PAT) | `.env.local` or system env | **NEVER** | MCP/CLI authentication |

### The `NEXT_PUBLIC_` Prefix Rule

In Next.js (and Vite with `VITE_`), any variable prefixed with `NEXT_PUBLIC_` gets bundled into the client-side JavaScript and is visible to anyone who inspects your site. This is fine for the `anon` key because it's designed to be public (RLS policies protect your data). But **never** prefix `SERVICE_ROLE_KEY` or `DB_URL` with `NEXT_PUBLIC_` — that would expose your admin credentials.

### For Vite/React (Non-Next.js) Projects

Use `VITE_` prefix instead:
```bash
VITE_SUPABASE_URL=https://your-project-ref.supabase.co
VITE_SUPABASE_PUBLISHABLE_DEFAULT_KEY=sb_publishable_xxx
```

### MCP Config vs .env — They're Separate Things

Your `.env` / `.env.local` files are for **your application code** (the website/app you're building). The MCP config files (`.cursor/mcp.json`, `.claude.json`, `~/.codex/config.toml`) are for **your AI tools** to access Supabase's management API. They serve different purposes:

- **`.env.local`** → Your app talks to Supabase at runtime via the JS client
- **MCP config** → Your AI tool talks to Supabase's management API to create tables, run queries, apply migrations, etc.

You need both. The MCP connection lets the AI manage your database schema and data. The `.env` keys let your actual application connect to and query the database.

### .gitignore Must-Haves

```gitignore
# Environment files with secrets
.env.local
.env.*.local

# Supabase local
supabase/functions/.env

# Never commit PATs or service role keys anywhere
*.pem
*.key
```

---

## 6. COMPARISON MATRIX

| Feature | Cursor | Claude Code | OpenAI Codex |
|---------|--------|-------------|--------------|
| **MCP Config Format** | JSON (`.cursor/mcp.json`) | JSON (`.claude.json`) | TOML (`~/.codex/config.toml`) |
| **Auth Method** | OAuth (auto browser popup) | OAuth (`/mcp` trigger) | OAuth (`codex mcp login`) |
| **PAT Fallback** | Yes | Yes (custom headers) | Yes (`bearer_token_env_var`) |
| **Project Scoping** | `?project_ref=` URL param | Same | Same |
| **Read-Only Mode** | `&read_only=true` | Same | Same |
| **Multi-Project** | Multiple server entries | Multiple entries | Multiple `[mcp_servers.X]` blocks |
| **Tool Limit** | 40 tools max | No hard limit | No documented limit |
| **CLI Management** | Manual JSON editing | `claude mcp add/remove` | `codex mcp add/remove` |
| **Shared Config** | Global `~/.cursor/mcp.json` or per-project | Global `~/.claude.json` or per-project | Global `~/.codex/config.toml` or per-project |
| **VS Code Extension** | N/A (Cursor IS the IDE) | Yes (Claude Code extension) | Yes (Codex extension) — but has session isolation bugs |
| **Stability** | Most mature for Supabase | Solid, occasional auth quirks | Least mature, known OAuth/startup issues |
| **Templates/Agents** | None built-in | Claude Code Templates ecosystem | Skills system |
| **Best For** | Visual IDE workflow, inline code + MCP | Terminal-first workflow, CLI power users | OpenAI ecosystem users |

---

## 7. RECOMMENDED SETUP FOR YOUR WORKFLOW

Given your dual-project (dev/prod) setup and use of all three tools, here's the play:

1. **Use the official remote MCP server** for all three tools — no STDIO/local servers needed
2. **Always scope to project** using `?project_ref=` — don't leave it open to all projects
3. **Always set prod to read-only** — append `&read_only=true` to any production MCP URL
4. **Store your MCP configs per-project** (`.cursor/mcp.json`, `.claude.json`, `.codex/config.toml`) so each project repo has its own dev/prod server pair
5. **Keep your app keys in `.env.local`** (never committed) with `.env` holding only the public-safe `anon` key and URL defaults
6. **Use Supabase CLI for full schema dumps** when you need to compare dev vs prod — MCP is great for individual queries but the CLI's `db dump` + `db diff` is purpose-built for migration workflows
7. **Set production secrets in your hosting platform** (Vercel, Netlify, etc.) rather than in any file — this keeps prod credentials completely out of your repo

---

*Last updated: March 2026. Based on Supabase MCP docs, OpenAI Codex docs, Claude Code docs, and community reports.*
