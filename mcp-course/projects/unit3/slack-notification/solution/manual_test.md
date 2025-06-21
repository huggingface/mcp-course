# Manual Testing Guide - Slack Notification Module

This guide provides curl-based tests so you can verify your implementation without setting up a full GitHub repository and Actions workflow.

## Prerequisites

1. MCP server running: `uv run server.py`
2. Webhook server running: `python webhook_server.py` 
3. Slack webhook URL set: `export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."`

## Test 1: Direct Slack Tool Test

Test your `send_slack_notification` tool directly via Claude Code:

```bash
# Start your MCP server and connect with Claude Code, then ask:
# "Send a test message to Slack: 'Hello from MCP Course Module 3!'"
```

Expected result: Message appears in your Slack channel.

## Test 2: Simulate GitHub Webhook Events

### 2a. Simulate CI Failure Event

Send a fake GitHub Actions failure event to your webhook server:

```bash
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d '{
    "action": "completed",
    "workflow_run": {
      "id": 123456789,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "run_number": 42,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z",
      "html_url": "https://github.com/user/repo/actions/runs/123456789",
      "head_branch": "feature/slack-integration",
      "head_sha": "abc123f456789",
      "repository": {
        "name": "mcp-course",
        "full_name": "user/mcp-course",
        "html_url": "https://github.com/user/mcp-course"
      },
      "pull_requests": [{
        "number": 42,
        "url": "https://api.github.com/repos/user/mcp-course/pulls/42",
        "html_url": "https://github.com/user/mcp-course/pull/42"
      }]
    }
  }'
```

### 2b. Simulate CI Success Event

```bash
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d '{
    "action": "completed",
    "workflow_run": {
      "id": 123456790,
      "name": "Deploy",
      "status": "completed",
      "conclusion": "success",
      "run_number": 43,
      "created_at": "2024-01-15T11:30:00Z",
      "updated_at": "2024-01-15T11:35:00Z",
      "html_url": "https://github.com/user/repo/actions/runs/123456790",
      "head_branch": "main",
      "head_sha": "def456g789012",
      "repository": {
        "name": "mcp-course",
        "full_name": "user/mcp-course",
        "html_url": "https://github.com/user/mcp-course"
      },
      "pull_requests": [{
        "number": 43,
        "url": "https://api.github.com/repos/user/mcp-course/pulls/43",
        "html_url": "https://github.com/user/mcp-course/pull/43"
      }]
    }
  }'
```

## Test 3: End-to-End Workflow Tests

After sending the webhook events above, test the complete workflow via Claude Code:

### 3a. Test Failure Alert Workflow

Ask Claude Code:
```
"Check recent CI events, find any failures, format them as a Slack alert, and send to the team"
```

Expected workflow:
1. Claude calls `get_recent_actions_events()` → finds failure event
2. Claude calls `format_ci_failure_alert()` → generates formatted message
3. Claude calls `send_slack_notification()` → sends to Slack

Expected Slack message:
```
❌ *CI Failed* - mcp-course

> CI workflow failed on feature/slack-integration

*Details:*
• Workflow: `CI`
• Branch: `feature/slack-integration`
• Commit: `abc123f`

*Next Steps:*
• <https://github.com/user/mcp-course/pull/42|View Pull Request>
• <https://github.com/user/repo/actions/runs/123456789|Check Action Logs>
```

### 3b. Test Success Summary Workflow

Ask Claude Code:
```
"Check recent CI events, find any successful deployments, format them as a celebration message, and send to the team"
```

Expected workflow:
1. Claude calls `get_recent_actions_events()` → finds success event
2. Claude calls `format_ci_success_summary()` → generates formatted message  
3. Claude calls `send_slack_notification()` → sends to Slack

Expected Slack message:
```
✅ *Deployment Successful* - mcp-course

> Deploy workflow completed successfully on main

*Changes:*
• Module 3 Slack integration added
• Team notification system implemented

*Links:*
• <https://github.com/user/mcp-course/pull/43|View Changes>
• <https://github.com/user/mcp-course|Visit Repository>
```

## Test 4: Error Handling Tests

### 4a. Test Missing Webhook URL

```bash
# Temporarily unset the environment variable
unset SLACK_WEBHOOK_URL

# Ask Claude Code to send a message
# Expected: Error message about missing environment variable
```

### 4b. Test Invalid Webhook URL

```bash
# Set invalid webhook URL
export SLACK_WEBHOOK_URL="https://invalid-webhook-url.com/test"

# Ask Claude Code to send a message  
# Expected: Error message about connection failure
```

### 4c. Restore Valid Webhook URL

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/ACTUAL/URL"
```

## Test 5: Prompt-Only Tests

Test the formatting prompts without sending to Slack:

### 5a. Test Failure Alert Prompt

Ask Claude Code:
```
"Use the format_ci_failure_alert prompt to create a failure message for the recent CI failure, but don't send it to Slack yet"
```

### 5b. Test Success Summary Prompt

Ask Claude Code:
```
"Use the format_ci_success_summary prompt to create a success message for the recent deployment, but don't send it to Slack yet"
```

## Test 6: Integration with Previous Modules

Test that all previous module functionality still works:

### 6a. Module 1 Integration

Ask Claude Code:
```
"Analyze current file changes, suggest a PR template, then create a Slack message about the PR status"
```

### 6b. Module 2 Integration

Ask Claude Code:
```
"Check workflow status, analyze the CI results, and create a comprehensive team update for Slack"
```

## Verification Checklist

After running these tests, verify:

- [ ] Direct Slack tool works (Test 1)
- [ ] Webhook server receives and stores events (Test 2)
- [ ] Failure alert workflow works end-to-end (Test 3a)
- [ ] Success summary workflow works end-to-end (Test 3b)
- [ ] Error handling works properly (Test 4)
- [ ] Prompts work independently (Test 5)
- [ ] Integration with previous modules works (Test 6)
- [ ] Slack messages display with proper formatting
- [ ] All tools and prompts are accessible to Claude Code

## Troubleshooting

### Webhook Server Issues
```bash
# Check if webhook server is running
curl http://localhost:8080/health

# Check stored events
cat github_events.json
```

### MCP Server Issues
```bash
# Check if MCP server is responding
# Should see server startup messages when running uv run server.py
```

### Slack Issues
```bash
# Test webhook URL directly
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Direct webhook test"}' \
  $SLACK_WEBHOOK_URL
```

This testing approach lets you validate your implementation without needing to set up a real GitHub repository with Actions workflows!