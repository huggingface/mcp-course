# Module 3: Slack Notification

## The Communication Gap Crisis

Week 3 at CodeCraft Studios. Your automation system is already transforming how the team works:
- **PR Agent** (Module 1): Developers are writing clear, helpful pull request descriptions
- **CI/CD Monitor** (Module 2): The team catches test failures immediately, preventing bugs from reaching production

The team is feeling much more confident... until Monday morning brings a new crisis.

The frontend team (Emma and Jake) spent the entire weekend debugging a nasty API integration issue. They tried everything: checked their network calls, validated request formats, even rewrote the error handling. Finally, at 2 AM Sunday, they discovered the backend team had fixed this exact issue on Friday and deployed the fix to staging - but forgot to announce it.

"We wasted 12 hours solving a problem that was already fixed!" Emma says, frustrated.

Meanwhile, the design team finished the new user onboarding flow illustrations last week, but the frontend team didn't know they were ready. Those beautiful assets are still sitting unused while the team ships a temporary design.

The team realizes they have an information silo problem. Everyone's working hard, but they're not communicating effectively about what's happening when.

**Your mission**: Complete the automation system with intelligent Slack notifications that keep the whole team informed about important developments automatically.

## What You'll Build

This final module completes the CodeCraft Studios transformation. You'll integrate Tools and Prompts to create a smart notification system that sends formatted Slack messages about CI/CD events, demonstrating how all MCP primitives work together in a real-world scenario.

Building on the foundation from Modules 1 and 2, you'll add the final piece of the puzzle:
- **Slack webhook tool** for sending messages to your team channel
- **Two notification prompts** that intelligently format CI events
- **Complete integration** showing all MCP primitives working together

### Screencast: The Complete Automation System! 🎉

<Youtube id="sX5qrbDG-oY" />

**The Final Piece**: Watch how your complete automation system prevents those Monday morning surprises that plagued Emma and Jake!

**What You'll See**: 
- **Claude's intelligent workflow** - Notice how Claude breaks down the task: ☐ Check events → ☐ Send notification
- **Real-time MCP tools in action** - `get_recent_actions_events` pulls fresh CI data, then `send_slack_notification` delivers the alert
- **Side-by-side demonstration** - The Slack channel is open in parallel to show the formatted message appearing as Claude sends it

**The Smart Notification**: Claude doesn't just spam the team—it crafts a professional alert with:
- 🚨 Clear urgency indicators and emoji
- **Detailed failure breakdown** (test-auth-service ❌, test-api ❌, test-frontend ⏳)
- **Actionable links** to the pipeline run and pull request
- **Context everyone needs** - repository, PR #1 "various improvements", commit hash

**Why This Matters**: Remember the communication gap crisis? No more! This system ensures that when CI fails on `demo-bad-pr` branch, the whole team knows immediately. No more weekend debugging sessions for issues that were already fixed!

**The Complete Journey**: From Module 1's PR chaos to Module 3's intelligent team notifications—you've built a system that transforms how CodeCraft Studios collaborates. The weekend warriors become informed teammates! 🚀

## Learning Objectives

By the end of this module, you'll understand:
1. How to integrate external APIs with MCP Tools
2. How to combine Tools and Prompts for complete workflows  
3. How to format rich messages using Slack markdown
4. How all MCP primitives work together in practice

## Prerequisites

You'll need everything from the previous modules plus:
- **Completed Modules 1 and 2** - This module directly extends your existing MCP server
- **A Slack workspace** where you can create incoming webhooks (personal workspaces work fine)
- **Basic understanding of REST APIs** - You'll be making HTTP requests to Slack's webhook endpoints

## Key Concepts

### MCP Integration Pattern

This module demonstrates the complete workflow:
1. **Events** → GitHub Actions webhook (from Module 2)
2. **Prompts** → Format events into readable messages
3. **Tools** → Send formatted messages to Slack
4. **Result** → Professional team notifications

### Slack Markdown Formatting

You'll use [Slack's markdown](https://api.slack.com/reference/surfaces/formatting) for rich messages:
- [`*bold text*`](https://api.slack.com/reference/surfaces/formatting#visual-styles) for emphasis
- [`_italic text_`](https://api.slack.com/reference/surfaces/formatting#visual-styles) for details
- [`` `code blocks` ``](https://api.slack.com/reference/surfaces/formatting#inline-code) for technical info
- [`> quoted text`](https://api.slack.com/reference/surfaces/formatting#quotes) for summaries
- [Emoji](https://api.slack.com/reference/surfaces/formatting#emoji): ✅ ❌ 🚀 ⚠️
- [Links](https://api.slack.com/reference/surfaces/formatting#linking-urls): `<https://github.com/user/repo|Repository>`

## Project Structure

```
slack-notification/
├── starter/          # Your starting point
│   ├── server.py     # Modules 1+2 code + TODOs
│   ├── webhook_server.py  # From Module 2
│   ├── pyproject.toml
│   └── README.md
└── solution/         # Complete implementation
    ├── server.py     # Full Slack integration
    ├── webhook_server.py
    └── README.md
```

## Implementation Steps

### Step 1: Set Up Slack Integration (10 min)

1. Create a Slack webhook:
   - Go to [Slack API Apps](https://api.slack.com/apps)
   - Create new app → "From scratch" ([Creating an app guide](https://api.slack.com/authentication/basics#creating))
   - App Name: "MCP Course Notifications"
   - Choose your workspace
   - Go to "Features" → "[Incoming Webhooks](https://api.slack.com/messaging/webhooks)"
   - [Activate incoming webhooks](https://api.slack.com/messaging/webhooks#enable_webhooks)
   - Click "Add New Webhook to Workspace"
   - Choose channel and authorize ([Webhook setup guide](https://api.slack.com/messaging/webhooks#getting_started))
   - Copy the webhook URL

2. Test webhook works (following [webhook posting examples](https://api.slack.com/messaging/webhooks#posting_with_webhooks)):
   ```bash
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Hello from MCP Course!"}' \
     YOUR_WEBHOOK_URL
   ```

3. Set environment variable:
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   ```

   **⚠️ Security Note**: The webhook URL is a sensitive secret that grants permission to post messages to your Slack channel. Always:
   - Store it as an environment variable, never hardcode it in your code
   - Never commit webhook URLs to version control (add to .gitignore)
   - Treat it like a password - anyone with this URL can send messages to your channel

<Tip warning={true}>

**Security Alert**: Webhook URLs are sensitive credentials! Anyone with your webhook URL can send messages to your Slack channel. Always store them as environment variables and never commit them to version control.

</Tip>

### Step 2: Add Slack Tool (15 min)

Now that you have a working webhook, you'll add a new MCP tool to your existing server.py from Module 2. This tool will handle sending notifications to Slack by making HTTP requests to the webhook URL.

<Tip>

**Note**: The starter code includes all improvements from Modules 1 & 2 (output limiting, webhook handling). Focus on the new Slack integration!

</Tip>

Add this tool to your server.py:

**`send_slack_notification`**:
- Takes a message string parameter
- Reads webhook URL from environment variable
- Sends POST request to Slack webhook
- Returns success/failure message
- Handles basic error cases

```python
import os
import requests
from mcp.types import TextContent

@mcp.tool()
def send_slack_notification(message: str) -> str:
    """Send a formatted notification to the team Slack channel."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return "Error: SLACK_WEBHOOK_URL environment variable not set"
    
    try:
        # TODO: Send POST request to webhook_url
        # TODO: Include message in JSON payload with "mrkdwn": true
        # TODO: Handle response and return status
        pass
    except Exception as e:
        return f"Error sending message: {str(e)}"
```

### Step 3: Create Formatting Prompts (15 min)

Next, you'll add MCP Prompts to your server - this is where the magic happens! These prompts will work with Claude to automatically format your GitHub webhook data into well-structured Slack messages. Remember from Module 1 that Prompts provide reusable instructions that Claude can use consistently.

Implement two prompts that generate Slack-formatted messages:

1. **`format_ci_failure_alert`**:
   ```python
   @mcp.prompt()
   def format_ci_failure_alert() -> str:
       """Create a Slack alert for CI/CD failures."""
       return """Format this GitHub Actions failure as a Slack message:

   Use this template:
   :rotating_light: *CI Failure Alert* :rotating_light:
   
   A CI workflow has failed:
   *Workflow*: workflow_name
   *Branch*: branch_name
   *Status*: Failed
   *View Details*: <LOGS_LINK|View Logs>
   
   Please check the logs and address any issues.
   
   Use Slack markdown formatting and keep it concise for quick team scanning."""
   ```

2. **`format_ci_success_summary`**:
   ```python
   @mcp.prompt()
   def format_ci_success_summary() -> str:
       """Create a Slack message celebrating successful deployments."""
       return """Format this successful GitHub Actions run as a Slack message:

   Use this template:
   :white_check_mark: *Deployment Successful* :white_check_mark:
   
   Deployment completed successfully for [Repository Name]
   
   *Changes:*
   - Key feature or fix 1
   - Key feature or fix 2
   
   *Links:*
   <PR_LINK|View Changes>
   
   Keep it celebratory but informative. Use Slack markdown formatting."""
   ```

### Step 4: Test Complete Workflow (10 min)

Now comes the exciting part - testing your complete MCP workflow! You'll have all three components working together: webhook capture from Module 2, prompt formatting from this module, and Slack notifications.

1. Start all services (just like in Module 2, but now with Slack integration):
   ```bash
   # Terminal 1: Start webhook server
   python webhook_server.py
   
   # Terminal 2: Start MCP server
   uv run server.py
   
   # Terminal 3: Start Cloudflare Tunnel  
   cloudflared tunnel --url http://localhost:8080
   ```

2. Test the complete integration with Claude Code:
   - **Configure GitHub webhook** with tunnel URL (same as Module 2)
   - **Push changes** to trigger GitHub Actions 
   - **Ask Claude** to check recent events and format them using your prompts
   - **Let Claude send** the formatted message using your Slack tool
   - **Verify** notifications appear in your Slack channel

### Step 5: Verify Integration (5 min)

You can test your implementation without setting up a real GitHub repository! See `manual_test.md` for curl commands that simulate GitHub webhook events.

**Understanding the webhook event flow:**
- Your webhook server (from Module 2) captures GitHub events and stores them in `github_events.json`
- Your MCP tools read from this file to get recent CI/CD activity  
- Claude uses your formatting prompts to create readable messages
- Your Slack tool sends the formatted messages to your team channel
- This creates a complete pipeline: GitHub → Local Storage → Claude Analysis → Slack Notification

**Quick Test Workflow:**
1. Use curl to send fake GitHub events to your webhook server
2. Ask Claude to check recent events and format them
3. Send formatted messages to Slack
4. Verify everything works end-to-end

**Manual Testing Alternative:** For a complete testing experience without GitHub setup, follow the step-by-step curl commands in `manual_test.md`.

## Example Workflow in Claude Code

```
User: "Check recent CI events and notify the team about any failures"

Claude: 
1. Uses get_recent_actions_events (from Module 2)
2. Finds a workflow failure
3. Uses format_ci_failure_alert prompt to create message
4. Uses send_slack_notification tool to deliver it
5. Reports back: "Sent failure alert to #dev-team channel"
```

## Expected Slack Message Output

**Failure Alert:**
```
🚨 *CI Failure Alert* 🚨

A CI workflow has failed:
*Workflow*: CI (Run #42)
*Branch*: feature/slack-integration
*Status*: Failed
*View Details*: <https://github.com/user/mcp-course/actions/runs/123|View Logs>

Please check the logs and address any issues.
```

**Success Summary:**
```
✅ *Deployment Successful* ✅

Deployment completed successfully for mcp-course

*Changes:*
- Added team notification system
- Integrated MCP Tools and Prompts

*Links:*
<https://github.com/user/mcp-course/pull/42|View Changes>
```

## Common Issues

### Webhook URL Issues
- Verify the environment variable is set correctly
- Test webhook directly with curl before integrating
- Ensure Slack app has proper permissions

### Message Formatting
- [Slack markdown](https://api.slack.com/reference/surfaces/formatting) differs from GitHub markdown
- **Important**: Use `*text*` for bold (not `**text**`)
- Include `"mrkdwn": true` in webhook payload for proper formatting
- Test message formatting manually before automating
- Handle special characters in commit messages properly ([formatting reference](https://api.slack.com/reference/surfaces/formatting#escaping))

### Network Errors
- Add basic timeout handling to webhook requests ([webhook error handling](https://api.slack.com/messaging/webhooks#handling_errors))
- Return meaningful error messages from the tool
- Check internet connectivity if requests fail

## Key Takeaways

You've now built a complete MCP workflow that demonstrates:
- **Tools** for external API integration (Slack webhooks)
- **Prompts** for intelligent message formatting
- **Integration** of all MCP primitives working together
- **Real-world application** that teams can actually use

This shows the power of MCP for building practical development automation tools!

<Tip>

**Key Learning**: You've now built a complete MCP workflow that combines Tools (for external API calls) with Prompts (for consistent formatting). This pattern of Tools + Prompts is fundamental to advanced MCP development and can be applied to many other automation scenarios.

</Tip>

## Next Steps

Congratulations! You've completed the final module of Unit 3 and built a complete end-to-end automation system. Your journey through all three modules has given you hands-on experience with:

- **Module 1**: MCP Tools and intelligent data analysis
- **Module 2**: Real-time webhooks and MCP Prompts
- **Module 3**: External API integration and workflow completion

### What to do next:
1. **Test your complete system** - Try triggering real GitHub events and watch the full pipeline work
2. **Experiment with customization** - Modify the Slack message formats or add new notification types
3. **Review the Unit 3 Conclusion** - Reflect on everything you've learned and explore next steps
4. **Share your success** - Show teammates how MCP can automate your development workflows

You now have a solid foundation for building intelligent automation systems with MCP!

### The transformation is complete!
CodeCraft Studios has gone from chaotic development to a well-oiled machine. The automation system you built handles:
- **Smart PR descriptions** that help reviewers understand changes
- **Real-time CI/CD monitoring** that catches failures before they reach production  
- **Intelligent team notifications** that keep everyone informed automatically

The team can now focus on building great products instead of fighting process problems. And you've learned advanced MCP patterns that you can apply to any automation challenge!

## Additional Resources

- [Slack Incoming Webhooks Documentation](https://api.slack.com/messaging/webhooks)
- [Slack Message Formatting Guide](https://api.slack.com/reference/surfaces/formatting)
- [MCP Tools Documentation](https://modelcontextprotocol.io/docs/concepts/tools)
- [MCP Prompts Guide](https://modelcontextprotocol.io/docs/concepts/prompts)