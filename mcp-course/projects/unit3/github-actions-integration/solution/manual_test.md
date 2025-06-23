# Manual Testing Guide - Module 2: GitHub Actions Integration

This guide walks through comprehensive testing of the GitHub Actions integration module.

## Prerequisites

- Python environment with `uv` installed
- Claude Code configured
- Port 8080 available
- (Optional) Cloudflare Tunnel installed for real GitHub testing

## Test Sequence

### 1. Environment Setup

```bash
cd projects/unit3/github-actions-integration/solution
uv sync
```

### 2. Start Services

**Terminal 1 - Webhook Server:**
```bash
python webhook_server.py
```

Expected output:
```
🚀 Starting webhook server on http://localhost:8080
📝 Events will be saved to: /path/to/github_events.json
🔗 Webhook URL: http://localhost:8080/webhook/github
```

**Terminal 2 - MCP Server:**
```bash
uv run server.py
```

Expected output:
```
Starting PR Agent MCP server...
To receive GitHub webhooks, run the webhook server separately:
  python webhook_server.py
```

### 3. Claude Code Configuration

Add to Claude Code settings and restart:
```json
{
  "mcpServers": {
    "pr-agent-actions": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/path/to/github-actions-integration/solution"
    }
  }
}
```

### 4. Test Module 1 Functionality

Verify existing tools still work:

```
User: "Analyze my file changes"
Expected: Claude uses analyze_file_changes() tool

User: "Show me available PR templates"
Expected: Claude lists all templates

User: "Suggest a template for a bug fix"
Expected: Claude recommends bug.md template
```

### 5. Send Test Webhook Events

**Success Event:**
```bash
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d '{
    "action": "completed",
    "workflow_run": {
      "id": 123456789,
      "name": "CI Tests",
      "head_branch": "main",
      "head_sha": "abc123",
      "path": ".github/workflows/ci.yml",
      "display_title": "CI Tests for PR #42",
      "run_number": 42,
      "event": "push",
      "status": "completed",
      "conclusion": "success",
      "workflow_id": 12345,
      "url": "https://api.github.com/repos/user/repo/actions/runs/123456789",
      "html_url": "https://github.com/user/repo/actions/runs/123456789",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:05:00Z",
      "run_started_at": "2024-01-01T10:00:00Z"
    },
    "repository": {
      "id": 987654321,
      "name": "repo",
      "full_name": "user/repo",
      "owner": {
        "login": "user",
        "type": "User"
      }
    },
    "sender": {
      "login": "test-user",
      "type": "User"
    }
  }'
```

**Failure Event:**
```bash
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d '{
    "action": "completed",
    "workflow_run": {
      "id": 123456790,
      "name": "Deploy to Production",
      "head_branch": "release/v1.0",
      "status": "completed",
      "conclusion": "failure",
      "run_number": 15,
      "html_url": "https://github.com/user/repo/actions/runs/123456790",
      "updated_at": "2024-01-01T10:10:00Z"
    },
    "repository": {"full_name": "user/repo"},
    "sender": {"login": "test-user"}
  }'
```

**In-Progress Event:**
```bash
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d '{
    "action": "in_progress",
    "workflow_run": {
      "id": 123456791,
      "name": "Build and Test",
      "status": "in_progress",
      "conclusion": null,
      "run_number": 100,
      "html_url": "https://github.com/user/repo/actions/runs/123456791",
      "updated_at": "2024-01-01T10:15:00Z"
    },
    "repository": {"full_name": "user/repo"},
    "sender": {"login": "test-user"}
  }'
```

### 6. Test New Tools

```
User: "What GitHub Actions events have we received?"
Expected: Claude shows all 3 events with details

User: "Show me the workflow status"
Expected: Claude shows:
- CI Tests: success
- Deploy to Production: failure  
- Build and Test: in_progress
```

### 7. Test MCP Prompts

Test each prompt by name:

**Prompt 1:**
```
User: "analyze ci results"
Expected: Claude provides formatted analysis showing:
- Overall health: Warning (due to failure)
- Failed workflows: Deploy to Production
- Successful workflows: CI Tests
- In-progress: Build and Test
- Recommendations based on failures
```

**Prompt 2:**
```
User: "create deployment summary"
Expected: Claude creates Slack-style message about the deployment failure
```

**Prompt 3:**
```
User: "generate pr status report"
Expected: Claude combines file changes analysis with CI/CD status
```

**Prompt 4:**
```
User: "troubleshoot workflow failure"
Expected: Claude provides structured troubleshooting for Deploy to Production failure
```

### 8. Verify File Storage

Check that events are persisted:
```bash
cat github_events.json
```

Should contain all 3 events in JSON array format.

### 9. Test Event Limit

Send 5 more events to verify only last 100 are kept (manual verification).

### 10. Test with Real GitHub (Optional)

**Terminal 3 - Cloudflare Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8080
```

1. Note the tunnel URL (e.g., https://random-name.trycloudflare.com)
2. Configure GitHub webhook:
   - Go to repo Settings → Webhooks
   - Add webhook with URL: `https://your-tunnel.trycloudflare.com/webhook/github`
   - Select "Workflow runs" events
3. Push a commit or manually trigger a workflow
4. Verify real events appear in Claude

## Troubleshooting

### No events showing up
- Check webhook server is running
- Verify `github_events.json` exists
- Ensure correct curl commands

### Port 8080 already in use
```bash
lsof -i :8080  # Find process
kill -9 <PID>  # Kill it
```

### Prompts not working
- Use exact lowercase names with spaces
- Don't use quotes around prompt names

### Claude not finding server
- Restart Claude Code after config changes
- Check the cwd path is absolute

## Success Criteria

- [ ] All Module 1 tools work
- [ ] Webhook server receives and stores events
- [ ] Both new tools return correct data
- [ ] All 4 prompts execute successfully
- [ ] Events persist in JSON file
- [ ] Multiple event types handled correctly
- [ ] Real GitHub integration works (if tested)