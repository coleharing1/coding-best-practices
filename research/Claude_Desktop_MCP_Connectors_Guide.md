# Claude Desktop MCP Connectors: The Complete Guide

**Last Updated: March 2026**
**Author: Compiled for Oceans 6 Media**

---

## Table of Contents

1. [What Is MCP?](#what-is-mcp)
2. [The Two Connection Surfaces](#the-two-connection-surfaces)
3. [Remote (Web) MCP Connectors](#remote-web-mcp-connectors)
4. [Local MCP Servers & Desktop Extensions](#local-mcp-servers--desktop-extensions)
5. [Global vs. Project-Scoped MCPs](#global-vs-project-scoped-mcps)
6. [MCP Scoping in Claude Code](#mcp-scoping-in-claude-code)
7. [Best Practices](#best-practices)
8. [Practical Setup Walkthroughs](#practical-setup-walkthroughs)
9. [Troubleshooting](#troubleshooting)
10. [Decision Framework: Which MCP Type to Use When](#decision-framework-which-mcp-type-to-use-when)

---

## What Is MCP?

The **Model Context Protocol (MCP)** is an open standard created by Anthropic (released November 2024) that provides a universal communication layer between AI applications and external tools, data sources, and services. Think of it as the USB-C of AI integrations — one protocol that lets Claude plug into anything.

MCP servers expose **tools** (actions Claude can take), **resources** (data Claude can read), and **prompts** (predefined interaction templates) to the AI model. Claude can then invoke these capabilities during your conversation to read data, create content, take actions, and more — all with your explicit permission.

---

## The Two Connection Surfaces

Claude Desktop (and the broader Claude ecosystem) provides two fundamentally different ways to connect MCP servers:

| Feature | Remote (Web) Connectors | Local Desktop Extensions / MCP Servers |
|---|---|---|
| **Where it runs** | External servers on the internet | Your local machine |
| **Available on** | Claude.ai (web), Claude Desktop, Claude Mobile, Claude Code | Claude Desktop only |
| **Setup method** | Settings > Connectors (paste URL or browse directory) | Desktop Extensions (one-click .mcpb install) or manual JSON config |
| **Authentication** | Typically OAuth | API keys, env variables, or no auth |
| **Data flow** | Data travels between Claude and external cloud services | Data stays on your machine |
| **Plan requirements** | Free (limited to 1 custom), Pro, Max, Team, Enterprise | All users on Claude Desktop |
| **Use case** | Cloud SaaS tools (Notion, Slack, Asana, Gmail, etc.) | Local files, dev tools, databases, private data |

---

## Remote (Web) MCP Connectors

### What They Are

Remote connectors are MCP servers hosted on the internet by third-party developers (or by you). They communicate with Claude over HTTPS using either **Streamable HTTP** or **SSE (Server-Sent Events)** transport. Anthropic's Connectors Directory (as of early 2026) features 50+ curated integrations spanning productivity, communication, design, engineering, finance, and more.

### When to Use Remote Connectors

- **Cloud-based work tools**: Accessing real-time data from Asana, Linear, Notion, Jira, etc.
- **Team collaboration**: Working with shared workspaces and team projects.
- **Cross-device consistency**: Same connectors available whether you're on desktop, web, or mobile.
- **Actions in external services**: Creating tasks, sending messages, updating records.
- **No local setup needed**: No runtime installations, no JSON editing.

### How to Set Up Remote Connectors

**Via the Connectors Directory (easiest):**

1. In Claude (web or Desktop), click the **"+"** button in the lower-left of the chat box.
2. Select **"Connectors"** to open the connectors panel.
3. Browse the directory or search for a specific integration (e.g., Notion, Slack, Asana).
4. Click **"Connect"** or **"Install"** on the connector you want.
5. Complete the **OAuth authentication** flow — this grants Claude permission-scoped access to your account in that service.
6. The connector is now available. Toggle it on/off per conversation as needed.

**Adding a Custom Remote Connector:**

1. Navigate to **Settings > Connectors**.
2. Click **"Add custom connector"** at the bottom.
3. Enter the connector's **name** and the remote MCP server **URL**.
4. Optionally, click **"Advanced settings"** to provide an OAuth Client ID and Client Secret.
5. Click **"Add"** and follow the authentication flow.

**For Team/Enterprise plans**, an Owner or Primary Owner must first add the custom connector at the organization level (Organization Settings > Connectors) before individual members can connect to it.

### Key Details About Remote Connectors

- Connectors are **enabled/disabled per conversation** via the "+" > "Connectors" menu. This means you can have Notion active in one chat and turned off in another.
- As of early 2026, Claude **does not support per-project scoping** of web connectors in the claude.ai interface. All your connected services are available across all conversations and projects — you toggle them on/off manually per chat.
- **Interactive connectors** can render live UI elements (dashboards, task boards, design tools) directly inside your conversation. Look for the "Interactive" badge in the directory.
- **Advanced Research** (deep research mode) can invoke remote connector tools automatically during research, but **cannot** use local MCP servers.
- Claude supports both **SSE** and **Streamable HTTP** transports for remote servers, though SSE may be deprecated in coming months.

---

## Local MCP Servers & Desktop Extensions

### What They Are

Local MCP servers run directly on your Mac (or PC) and communicate with Claude Desktop via **stdio** (standard input/output). They give Claude access to your local file system, applications, databases, dev tools, and any private data — all without that data ever leaving your machine.

**Desktop Extensions** are the modern, user-friendly packaging format for local MCP servers. They use the **.mcpb** file format (formerly .dxt) and bundle the entire MCP server — including all code, dependencies, and a manifest — into a single-click installable package. No Node.js, Python, or manual JSON config required.

### When to Use Local MCP Servers

- **Privacy and security**: Working with confidential documents, client files, or proprietary data without sending anything to external servers.
- **Local file operations**: Organizing files, summarizing documents in your folders, creating content from local data.
- **Development tools**: Accessing your local dev environment, running linters, interacting with local databases, browser automation (Playwright, Puppeteer).
- **System integration**: Clipboard access, screenshots, local calendar/contacts.
- **Offline-capable workflows**: Some local servers work without internet access.

### How to Set Up Desktop Extensions (Recommended for Non-Developers)

1. Open **Claude Desktop**.
2. Navigate to **Settings > Extensions**.
3. Click **"Browse extensions"** to view Anthropic's curated directory of reviewed extensions.
4. Click on any extension you want to install.
5. If the extension requires configuration (e.g., an API key), Claude will prompt you for it. Secrets are stored in your OS keychain.
6. The extension appears under Settings > Extensions with a status indicator.

**Installing a custom .mcpb file:**

1. Download the .mcpb file from the extension developer.
2. In Claude Desktop, go to Settings > Extensions.
3. Click **"Install Extension…"** and select the .mcpb file.
4. Follow the prompts. Done.

### How to Set Up Local MCP Servers Manually (Developer Method)

This is the classic approach — editing the JSON config file directly. Necessary for custom or community MCP servers that aren't packaged as Desktop Extensions.

1. Open Claude Desktop.
2. Click the **Claude menu** in the system menu bar (top of screen on Mac), then **"Settings…"**.
3. Navigate to the **"Developer"** tab in the left sidebar.
4. Click **"Edit Config"** to open the configuration file.

The config file lives at:
```
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
```

5. Add your MCP server configuration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/cole/Documents/safe-folder"],
      "env": {}
    },
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_pat_here"
      }
    }
  }
}
```

6. Save the file and **restart Claude Desktop** (Quit fully, then relaunch).
7. Verify: Click the **"+"** button in the chat box, then "Connectors" — your local servers should appear with toggle switches.

### Key Details About Local MCP Servers

- Claude Desktop includes a **built-in Node.js environment**, so Desktop Extensions using Node don't require you to install Node separately.
- Desktop Extensions support **Node.js, Python, and binary** MCP servers.
- Manual JSON-configured servers require the appropriate runtime (Node.js, Python, Docker, etc.) to be installed on your machine.
- Before executing any local file operation, Claude will **request your approval** — you control what it can and can't do.
- **Important**: Claude Desktop will NOT connect to remote MCP servers configured in the `claude_desktop_config.json` file. Remote servers must be added via Settings > Connectors.
- Logs for local MCP servers are found at: `~/Library/Logs/Claude/mcp-server-*.log`

---

## Global vs. Project-Scoped MCPs

This is one of the most important distinctions to understand, especially if you're working across multiple clients or projects.

### In Claude.ai (Web Interface) and Claude Desktop

**As of March 2026, the claude.ai web interface and Claude Desktop UI do not have native per-project MCP scoping for connectors.** Here's what that means in practice:

- **Remote connectors** you add in Settings > Connectors are available across ALL your conversations and projects. You toggle them on/off manually per conversation.
- **Local Desktop Extensions** configured in Claude Desktop are similarly available globally across all conversations in the Desktop app.
- **Claude Projects** (the feature where you can set custom instructions and upload reference files) have their own **memory space** and can auto-synthesize project context — but they do not have a built-in mechanism to restrict which MCP connectors are available to that specific project vs. others.

**The workaround**: Manually toggle connectors on/off in the "+" > "Connectors" menu at the start of each conversation. If you're in a Fish Monkey project, turn on the connectors you need for that client and turn off the rest.

### In Claude Code (CLI / Terminal)

Claude Code provides **true project-level MCP scoping** with three distinct scope levels. This is where it gets powerful:

#### 1. Local Scope (Default)

- **Stored in**: `~/.claude.json` under your project's specific path
- **Visibility**: Only you, only in the current project directory
- **Best for**: Personal dev servers, experimental configs, sensitive credentials that shouldn't be shared
- **How to add**:
```bash
claude mcp add my-server npx some-package
# or explicitly:
claude mcp add --scope local my-server npx some-package
```

#### 2. Project Scope

- **Stored in**: `.mcp.json` at the project root (committed to version control)
- **Visibility**: Everyone on the team who clones the repo
- **Best for**: Team-shared servers, project-specific tools, services required for collaboration
- **How to add**:
```bash
claude mcp add --scope project playwright npx @playwright/mcp@latest
```
- The `.mcp.json` file supports **environment variable expansion** (`${VAR}` and `${VAR:-default}`), so team members can share configs while keeping API keys in their own env.

#### 3. User Scope (Global)

- **Stored in**: `~/.claude.json` (available across ALL projects)
- **Visibility**: Only you, but available everywhere
- **Best for**: Personal utility servers you use across many projects (e.g., a personal task manager, general-purpose search)
- **How to add**:
```bash
claude mcp add --scope user hubspot --transport http https://mcp.hubspot.com/anthropic
```

#### Precedence Hierarchy

When servers with the same name exist at multiple scopes, Claude Code resolves conflicts in this order:

1. **Local** (highest priority — your personal project config overrides everything)
2. **Project** (team-shared config)
3. **User** (global config — lowest priority)

This means you can have a project-wide default for a server but override it locally with your own credentials or configuration.

#### Claude.ai Connectors Auto-Sync to Claude Code

If you've logged into Claude Code with your claude.ai account, any remote MCP servers you've connected via claude.ai Settings > Connectors are **automatically available** in Claude Code too. You can disable this with:
```bash
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

---

## MCP Scoping in Claude Code

Here's a practical reference for how configs are stored and where to find them:

| Scope | Config File Location | Shared? | Use Case |
|---|---|---|---|
| Local | `~/.claude.json` (under project path key) | No (just you, just this project) | Personal credentials, experimental servers |
| Project | `.mcp.json` in project root | Yes (version controlled) | Team tools, project-specific services |
| User | `~/.claude.json` (global mcpServers key) | No (just you, all projects) | Personal utilities, general-purpose tools |
| Claude.ai sync | Synced from claude.ai/settings/connectors | No (your account) | Web connectors you've already set up |

### Useful Claude Code MCP Commands

```bash
# Add a server (defaults to local scope)
claude mcp add my-server npx some-package

# Add with explicit scope
claude mcp add --scope project my-server npx some-package
claude mcp add --scope user my-server npx some-package

# Add a remote HTTP server
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Add with environment variables
claude mcp add my-server --env API_KEY=abc123 -- npx some-package

# Add from JSON
claude mcp add-json github '{"type":"http","url":"https://api.example.com/mcp"}'

# List all configured servers
claude mcp list

# Remove a server
claude mcp remove my-server

# Import from Claude Desktop config
claude mcp import-from-claude-desktop

# Reset project-level approval choices
claude mcp reset-project-choices

# Interactive MCP management
/mcp  (inside Claude Code session)
```

---

## Best Practices

### General MCP Hygiene

1. **Principle of least privilege**: Only connect the tools and grant the permissions you actually need. Don't leave 15 connectors active when you only need 2 for the current task.
2. **Toggle per conversation**: Get in the habit of enabling only relevant connectors for each chat. This reduces token overhead (each active connector's tool schemas consume context window) and prevents Claude from invoking irrelevant tools.
3. **Secrets management**: Never hardcode API keys in config files that get committed to version control. Use environment variables, OS keychain (Desktop Extensions handle this automatically), or `.env` files with `${VAR}` expansion in `.mcp.json`.
4. **Review tool approvals carefully**: When Claude asks to use a tool for the first time, read what it wants to do. Only click "Allow always" for servers and tools you fully trust to run unsupervised.

### Remote Connector Best Practices

1. **Start with the Connectors Directory**: Use Anthropic-reviewed connectors when available — they've been vetted for quality and security.
2. **Review OAuth scopes**: When authenticating, check what permissions the connector requests. Some ask for read+write when you only need read.
3. **Audit connected services regularly**: Visit Settings > Connectors periodically and disconnect services you no longer use.
4. **For teams**: Have your Owner/Admin curate which connectors are enabled for the organization rather than letting everyone connect freely.
5. **Custom connectors**: Only add custom remote MCP server URLs from sources you trust. These connect to unverified services.

### Local MCP Best Practices

1. **Sandbox your file access**: When setting up filesystem servers, restrict the paths to specific folders. Don't give Claude access to your entire home directory.
2. **Use Desktop Extensions when available**: They're easier to install, manage, and update than manual JSON configs. Plus, they handle dependency management automatically.
3. **Keep Claude Desktop updated**: Extensions and MCP support improve with each release. Check for updates regularly.
4. **Create a dedicated workspace folder**: Set up a specific directory (e.g., `~/claude-workspace/`) for Claude to operate in, keeping it isolated from your system files.
5. **Check logs when things break**: `~/Library/Logs/Claude/mcp-server-*.log` on Mac. This is your first stop for debugging.

### Claude Code Project Scoping Best Practices

1. **Default to project scope** (`--scope project`) for any MCP server the team needs. This goes into `.mcp.json` and travels with the repo.
2. **Use local scope** for personal credentials or experimental servers you don't want to share.
3. **Use user scope sparingly** — only for truly personal productivity tools (like a personal task manager) that aren't related to any specific project.
4. **Leverage env var expansion** in `.mcp.json` so team members share structure but use their own keys:
```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```
5. **Restart Claude Code** after any MCP config changes.

---

## Practical Setup Walkthroughs

### Walkthrough 1: Connect Notion (Remote Connector)

**Goal**: Let Claude read and write to your Notion workspace across web, desktop, and mobile.

1. Go to **claude.ai** > **Settings** > **Connectors** (or in Claude Desktop: "+" > "Connectors" > "Manage Connectors").
2. Find **Notion** in the directory.
3. Click **"Connect"** and authenticate with your Notion account.
4. Authorize the requested permissions.
5. In any new conversation, click "+" > "Connectors" and toggle Notion **on**.
6. Ask Claude: *"Search my Notion workspace for the latest client brief"* — Claude will use the Notion connector.

### Walkthrough 2: Set Up a Local Filesystem Server (Manual JSON)

**Goal**: Let Claude Desktop manage files in a specific folder on your Mac.

1. Create a safe working directory:
```bash
mkdir -p ~/claude-workspace
```

2. Ensure Node.js is installed (check with `node --version`). If not, install via [nodejs.org](https://nodejs.org) or `brew install node`.

3. Open Claude Desktop > Claude menu (top bar) > Settings > Developer > Edit Config.

4. Add this to the config:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/YOUR_USERNAME/claude-workspace"
      ]
    }
  }
}
```

5. Save and **fully restart** Claude Desktop.

6. Verify: Click "+" in chat > you should see the Filesystem server with available tools.

### Walkthrough 3: Add a Project-Scoped MCP in Claude Code

**Goal**: Add Playwright browser automation to a specific project, shared with your team.

```bash
cd /path/to/your/project

# Add Playwright MCP at project scope
claude mcp add --scope project playwright npx @playwright/mcp@latest

# Verify it was added
claude mcp list

# The .mcp.json file is now in your project root — commit it
git add .mcp.json
git commit -m "Add Playwright MCP server for browser testing"
```

Now anyone who clones the repo and runs Claude Code will have Playwright available.

### Walkthrough 4: Import Claude Desktop Servers into Claude Code

**Goal**: You've already configured MCP servers in Claude Desktop and want them available in Claude Code.

```bash
claude mcp import-from-claude-desktop
```

An interactive dialog will let you select which servers to import. They'll be added to your local scope by default.

---

## Troubleshooting

### Common Issues

**Server shows as disconnected or doesn't appear:**
- Fully **quit and relaunch** Claude Desktop (not just close the window).
- Check the Developer settings to see connection status.
- Review logs: `ls ~/Library/Logs/Claude/` and `cat ~/Library/Logs/Claude/mcp-server-SERVERNAME.log`

**"Command not found" errors for npx-based servers:**
- Ensure Node.js and npm are installed and in your PATH.
- Try running the server command manually in Terminal to see specific errors.
- Desktop Extensions bundle their own Node.js runtime — if available as an extension, use that instead.

**Remote connector won't authenticate:**
- Ensure you're on a paid plan (Pro, Max, Team, or Enterprise) for full connector access. Free plans are limited to 1 custom connector.
- Try removing the connector and re-adding it.
- Check if the service requires admin approval on your team's plan.

**MCP servers in Claude Code not showing up:**
- Check which scope they're in with `claude mcp list`.
- If you added at one scope but are checking from another context, they may not be visible.
- Project-scoped servers in `.mcp.json` persist independently from global servers in `~/.claude.json`.

**macOS security warnings:**
- Check System Preferences > Security & Privacy if you receive warnings when installing extensions.
- Grant necessary permissions for Claude Desktop to access required directories.

---

## Decision Framework: Which MCP Type to Use When

```
┌─────────────────────────────────────────────────┐
│           WHAT DO YOU NEED CLAUDE TO ACCESS?      │
└───────────────────────┬─────────────────────────┘
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
    Cloud/SaaS Tool            Local Resources
    (Notion, Slack,            (Files, DBs,
     Asana, Gmail)              Dev Tools)
           │                         │
           ▼                         ▼
    REMOTE CONNECTOR           LOCAL MCP SERVER
    (Settings > Connectors)    (Desktop Extension
                                or manual JSON)
           │                         │
           │                    ┌────┴────┐
           │                    ▼         ▼
           │              Extension    Manual
           │              Available?   JSON Config
           │                    │         │
           │                    ▼         ▼
           │              One-click   Edit config
           │              install     + restart
           │
    ┌──────┴──────────────────────────┐
    │  SCOPING DECISION (Claude Code)  │
    ├──────────────────────────────────┤
    │ Team needs it? → Project scope   │
    │ Just you, this project? → Local  │
    │ You, everywhere? → User scope    │
    └──────────────────────────────────┘
```

### Quick Reference Matrix

| Scenario | MCP Type | Scope | Setup Location |
|---|---|---|---|
| Search Notion from claude.ai | Remote | Global (all convos) | Settings > Connectors |
| Manage local project files | Local | N/A (Desktop only) | Extension or JSON config |
| Team browser testing (Playwright) | Local | Project | `.mcp.json` in repo |
| Personal GitHub across all work | Local or Remote | User | `~/.claude.json` or Settings > Connectors |
| Client-specific Shopify integration | Remote (custom) | Per-conversation toggle | Settings > Connectors > Add Custom |
| Experimental AI model testing | Local | Local | `~/.claude.json` under project path |

---

## Additional Resources

- **Connectors Directory**: [claude.com/connectors](https://claude.com/connectors)
- **MCP Protocol Docs**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Claude Code MCP Docs**: [code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)
- **Desktop Extensions Engineering Blog**: [anthropic.com/engineering/desktop-extensions](https://www.anthropic.com/engineering/desktop-extensions)
- **Custom Connectors Guide**: [support.claude.com/en/articles/11175166](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- **When to Use Desktop vs. Web Connectors**: [support.claude.com/en/articles/11725091](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors)
- **Building Desktop Extensions (MCPB)**: [support.claude.com/en/articles/12922929](https://support.claude.com/en/articles/12922929-building-desktop-extensions-with-mcpb)

---

*This guide was researched and compiled from Anthropic's official documentation, Claude Help Center articles, MCP Protocol documentation, and community resources as of March 2026.*
