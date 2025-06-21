# Module 3: Slack Notification - Complete Solution

This is the complete implementation of Module 3, demonstrating how to integrate MCP Tools and Prompts for team communication via Slack.

## What This Implements

This solution extends Modules 1 and 2 with:

1. **`send_slack_notification` tool** - Sends formatted messages to Slack via webhook with proper error handling
2. **`format_ci_failure_alert` prompt** - Creates rich failure alerts with Slack markdown
3. **`format_ci_success_summary` prompt** - Creates celebration messages for successful deployments

## Setup and Usage

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up Slack webhook:
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   ```

3. Start services:
   ```bash
   # Terminal 1: Webhook server
   python webhook_server.py
   
   # Terminal 2: MCP server
   uv run server.py
   
   # Terminal 3: Cloudflare tunnel (optional)
   cloudflared tunnel --url http://localhost:8080
   ```

## Testing

See `manual_test.md` for comprehensive testing instructions using curl commands to simulate GitHub webhook events.

## Key Learning Outcomes

This solution demonstrates all MCP primitives working together for real-world team automation.