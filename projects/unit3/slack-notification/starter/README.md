# Module 3: Slack Notification - Starter

This starter code extends Modules 1 and 2 with Slack integration, demonstrating how to combine MCP Tools and Prompts for complete team communication workflows.

## What You'll Implement

In this module, you'll complete:

1. **`send_slack_notification` tool** - Send messages to Slack via webhook
2. **`format_ci_failure_alert` prompt** - Format CI failures for Slack
3. **`format_ci_success_summary` prompt** - Format successful deployments for Slack

## Prerequisites

- Completed Modules 1 and 2
- A Slack workspace with webhook permissions
- Environment variable: `SLACK_WEBHOOK_URL`

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up Slack webhook:
   - Create Slack app at https://api.slack.com/apps
   - App name: "MCP Course Notifications"
   - Enable incoming webhooks
   - Add webhook to workspace
   - Export URL: `export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."`

3. Test webhook:
   ```bash
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Hello from MCP Course!"}' \
     $SLACK_WEBHOOK_URL
   ```

## Implementation Tasks

### 1. Complete `send_slack_notification` Tool

In `server.py`, implement the TODO sections:

```python
@mcp.tool()
async def send_slack_notification(message: str) -> str:
    # TODO: Import requests library at top of file
    # TODO: Send POST request to webhook_url
    # TODO: Include message in JSON payload: {"text": message}
    # TODO: Handle response and return status
```

### 2. Test the Prompts

The formatting prompts are complete - test them with Claude Code:
- Use `format_ci_failure_alert` to create failure messages
- Use `format_ci_success_summary` to create success messages
- Send formatted messages using your `send_slack_notification` tool

### 3. End-to-End Workflow

Test the complete integration:

1. Start webhook server: `python webhook_server.py`
2. Start MCP server: `uv run server.py`
3. Start Cloudflare tunnel: `cloudflared tunnel --url http://localhost:8080`
4. Trigger GitHub Actions
5. Use prompts to format messages
6. Send to Slack and verify formatting

## Expected Slack Output

**Failure Alert:**
```
❌ *CI Failed* - mcp-course

> Tests failed in Module 3 implementation

*Details:*
• Workflow: `CI`
• Branch: `feature/slack-integration`
• Commit: `abc123f`

*Next Steps:*
• <https://github.com/user/mcp-course/pull/42|View Pull Request>
• <https://github.com/user/mcp-course/actions/runs/123|Check Action Logs>
```

## Security Note

⚠️ **Important**: The `SLACK_WEBHOOK_URL` is a sensitive secret that grants permission to post messages to your Slack channel. Always:
- Store it as an environment variable, never in code
- Never commit webhook URLs to version control
- Treat it like a password

## Available Tools & Prompts

This module includes all tools and prompts from Modules 1 & 2, plus:

**New Tools:**
- `send_slack_notification` - Send messages to Slack

**New Prompts:**  
- `format_ci_failure_alert` - Create failure alerts
- `format_ci_success_summary` - Create success summaries

**From Previous Modules:**
- All file analysis tools (Module 1)
- All GitHub Actions tools (Module 2)  
- All CI/CD analysis prompts (Module 2)

## Testing Your Implementation

1. **Tool Test**: Call `send_slack_notification` directly with a test message
2. **Prompt Test**: Use formatting prompts to generate messages, then send them
3. **Integration Test**: Full workflow from GitHub webhook to Slack notification
4. **Format Test**: Verify Slack markdown renders correctly in your channel

## Next Steps

Once complete, you'll have built a production-ready MCP server that demonstrates all core MCP primitives working together for real-world team automation!