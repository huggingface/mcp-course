# Module 2: GitHub Actions Integration - Starter Code

This is your starting point for Module 2. You'll extend the PR Agent from Module 1 with webhook handling and MCP Prompts.

## Your Task

1. **Import Required Types**: Add the necessary imports for MCP Prompts
2. **Connect to Events File**: Define the path to read webhook events
3. **Implement GitHub Actions Tools**: Complete the tools to query events
4. **Create MCP Prompts**: Build prompts for standardized CI/CD workflows

Note: The webhook server (`webhook_server.py`) is provided for you!

## Getting Started

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Start the webhook server (in a separate terminal):
   ```bash
   python webhook_server.py
   ```

3. Follow the TODOs in `server.py` to implement Module 2 features

## Testing Your Implementation

1. Start your server:
   ```bash
   uv run server.py
   ```

2. In another terminal, start Cloudflare Tunnel:
   ```bash
   cloudflared tunnel --url http://localhost:8080
   ```

3. Configure GitHub webhooks with your tunnel URL

4. Test with Claude Code using the new prompts

## Implementation Hints

- The webhook server stores events in `github_events.json`
- Read the JSON file in your tools to get event data
- Prompts are simple functions that return strings with instructions
- Decorate prompt functions with `@mcp.prompt()`

## Need Help?

- Review the Module 2 documentation
- Check the solution in the `solution/` directory
- Look at the MCP documentation for Prompts: https://modelcontextprotocol.io/docs/concepts/prompts