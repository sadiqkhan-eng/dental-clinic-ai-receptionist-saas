# OpenCode MCP Server Setup Guide

Complete instructions for connecting MCP servers to OpenCode CLI.

---

## What is MCP?

Model Context Protocol (MCP) lets you add external tools to OpenCode. Once added, MCP tools are automatically available to the LLM alongside built-in tools.

---

## 1. GitHub MCP Server Setup

### Option A: Remote GitHub MCP (OAuth)

#### Step 1: Create GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill in:
   - **Application name:** `OpenCode MCP`
   - **Homepage URL:** `https://opencode.ai`
   - **Authorization callback URL:** `https://mcp.github.com/callback`
4. Click **"Register application"**
5. Copy the **Client ID**
6. Click **"Generate a new client secret"** and copy it

#### Step 2: Add to OpenCode Config

Create or edit `opencode.jsonc` in your project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "github": {
      "type": "remote",
      "url": "https://mcp.github.com/mcp",
      "oauth": {
        "clientId": "YOUR_CLIENT_ID",
        "clientSecret": "YOUR_CLIENT_SECRET"
      },
      "enabled": true
    }
  }
}
```

#### Step 3: Authenticate

```bash
opencode mcp auth github
```

This opens your browser. Authorize the app, then tokens are stored in `~/.local/share/opencode/mcp-auth.json`.

#### Step 4: Verify

```bash
opencode mcp list
```

#### Step 5: Use It

```
use the github tool to list my repositories
use the github tool to create an issue
use the github tool to list pull requests
```

---

### Option B: Local GitHub MCP (Personal Access Token)

#### Step 1: Generate GitHub Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Select scopes:
   - `repo` - Full control of private repositories
   - `read:org` - Read organization membership
   - `read:user` - Read user profile
4. Click **"Generate token"**
5. Copy the token (`ghp_xxxxx`)

#### Step 2: Set Environment Variable

```bash
# Windows PowerShell
$env:GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"

# Windows CMD
set GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here

# Linux/Mac
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"
```

Or add to `.env` file:

```
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
```

#### Step 3: Add to OpenCode Config

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "environment": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "{env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      },
      "enabled": true
    }
  }
}
```

#### Step 4: Use It

```
use the github tool to search my repositories
```

---

## 2. Other Popular MCP Servers

### Sentry

```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

Authenticate:
```bash
opencode mcp auth sentry
```

### Context7 (Documentation Search)

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

With API key:
```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}"
      }
    }
  }
}
```

### Grep by Vercel (Code Search)

```json
{
  "mcp": {
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app"
    }
  }
}
```

---

## 3. Management Commands

```bash
# List all MCP servers and auth status
opencode mcp list

# Authenticate with a server
opencode mcp auth <server-name>

# Remove stored credentials
opencode mcp logout <server-name>

# Debug connection and OAuth flow
opencode mcp debug <server-name>

# View auth status for all servers
opencode mcp auth list
```

---

## 4. Enable/Disable MCP Servers

### Globally Disable

```json
{
  "tools": {
    "github*": false
  }
}
```

### Per Agent

```json
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "enabled": true
    }
  },
  "tools": {
    "github*": false
  },
  "agent": {
    "my-agent": {
      "tools": {
        "github*": true
      }
    }
  }
}
```

---

## 5. Complete Example: DentalOS Project

For this project, you might want:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "environment": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "{env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      },
      "enabled": true
    },
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true
    }
  }
}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP not showing | Check `SKILL.md` spelling, frontmatter has `name` and `description` |
| Auth fails | Run `opencode mcp debug <server-name>` |
| Token expired | Run `opencode mcp logout <server-name>` then re-auth |
| Too many tokens | Disable unused MCP servers with `"enabled": false` |
| Connection timeout | Check network, firewall, or proxy settings |
