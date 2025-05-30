# Module 2: GitHub Actions Integration

This module extends the PR Agent with GitHub Actions webhook integration and MCP Prompts for standardized CI/CD workflows.

## Features Added in Module 2

1. **GitHub Actions Tools**:
   - `get_recent_actions_events()` - View recent webhook events
   - `get_workflow_status()` - Check workflow statuses

2. **MCP Prompts for CI/CD**:
   - `analyze_ci_results` - Comprehensive CI/CD analysis
   - `create_deployment_summary` - Team-friendly deployment updates
   - `generate_pr_status_report` - Combined code and CI/CD report
   - `troubleshoot_workflow_failure` - Systematic debugging guide

3. **Webhook Server**:
   - Separate script that runs on port 8080
   - Receives GitHub Actions events
   - Stores events in `github_events.json` for the MCP server to read

## Installation

```bash
# From the solution directory
uv sync
```

## Setting Up Cloudflare Tunnel

To receive GitHub webhooks locally, you'll need to set up Cloudflare Tunnel (cloudflared):

### Step 1: Install cloudflared

**macOS:**
```bash
brew install cloudflared
```

**Windows:**
Download the Windows installer from:
https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.msi

**Linux:**
```bash
# For Debian/Ubuntu (amd64)
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# For other Linux distros, download the appropriate binary:
# https://github.com/cloudflare/cloudflared/releases/latest
```

### Step 2: Start the Tunnel

```bash
# This creates a public URL that forwards to your local webhook server
cloudflared tunnel --url http://localhost:8080
```

You'll see output like:
```
Your quick tunnel has been created! Visit it at:
https://random-name-here.trycloudflare.com
```

### Step 3: Configure GitHub Webhook

1. Go to your GitHub repository → Settings → Webhooks
2. Click "Add webhook"
3. Set **Payload URL** to: `https://your-tunnel-url.trycloudflare.com/webhook/github`
4. Set **Content type** to: `application/json`
5. Select events:
   - Workflow runs
   - Check runs
   - Or choose "Send me everything"
6. Click "Add webhook"

## Running the Server

### For Development

```bash
# Terminal 1: Start the webhook server
python webhook_server.py

# Terminal 2: Start Cloudflare Tunnel (if testing with real GitHub)
cloudflared tunnel --url http://localhost:8080

# Terminal 3: Start the MCP server
uv run server.py
```

### With Claude Code

1. Add to Claude Code settings:
```json
{
  "pr-agent-actions": {
    "command": "uv",
    "args": ["run", "server.py"],
    "cwd": "/path/to/github-actions-integration/solution"
  }
}
```

2. Restart Claude Code
3. In a separate terminal, start the webhook server: `python webhook_server.py`
4. (Optional) Start Cloudflare Tunnel if testing with real GitHub webhooks

## Testing Webhooks

### Manual Test
```bash
# Send a test webhook
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d '{
    "action": "completed",
    "workflow_run": {
      "id": 123456789,
      "name": "CI Tests",
      "head_branch": "main",
      "run_number": 42,
      "status": "completed",
      "conclusion": "success",
      "html_url": "https://github.com/user/repo/actions/runs/123456789",
      "updated_at": "2024-01-01T10:00:00Z"
    },
    "repository": {
      "full_name": "user/repo"
    },
    "sender": {
      "login": "test-user"
    }
  }'
```

### With Claude Code

After setting up webhooks and pushing a commit:

1. **Check recent events**: 
   - Ask: "What GitHub Actions events have we received?"
   - Claude will use `get_recent_actions_events()`

2. **Analyze CI status**:
   - Use the prompt: "Analyze CI Results"
   - Claude will check workflows and provide insights

3. **Create deployment summary**:
   - Use the prompt: "Create Deployment Summary"
   - Claude will format a team-friendly update

## Module Structure

- `server.py` - Main MCP server with Tools and Prompts
- `webhook_server.py` - Separate webhook server that stores events
- `github_events.json` - File where webhook events are stored (created automatically)
- `pyproject.toml` - Dependencies for both servers
- `README.md` - This file

## Next Steps

- Complete the exercises in the module
- Experiment with different prompt workflows
- Move on to Module 3 for Hugging Face Hub integration