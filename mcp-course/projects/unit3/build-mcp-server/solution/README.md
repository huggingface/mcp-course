# Module 1: Basic MCP Server with PR Template Tools

This module implements a basic MCP server that provides tools for analyzing git changes and suggesting appropriate PR templates.

## Setup

### 1. Install uv

Follow the official installation instructions at: https://docs.astral.sh/uv/getting-started/installation/

### 2. Install dependencies

```bash
# Install all dependencies
uv sync

# Or install with dev dependencies for testing
uv sync --all-extras
```

### 3. Configure the MCP Server

Add the server to Claude Code:

```bash
# Add the MCP server
claude mcp add pr-agent -- uv --directory /absolute/path/to/module1/solution run server.py

# Verify it's configured
claude mcp list
```

## Tools Available

1. **analyze_file_changes** - Get the full diff and list of changed files
2. **get_pr_templates** - List available PR templates with their content
3. **suggest_template** - Let Claude analyze changes and suggest a template

## Usage Example

1. Make some changes in a git repository
2. Ask Claude: "Can you analyze my changes and suggest a PR template?"
3. Claude will:
   - Use `analyze_file_changes` to see what changed
   - Analyze the diff to understand the nature of changes
   - Use `suggest_template` to recommend the most appropriate template
   - Help you fill out the template based on the specific changes

## How It Works

Unlike traditional template systems that rely on file extensions or simple patterns, this MCP server provides Claude with raw git data and lets Claude's intelligence determine:
- What type of change is being made (bug fix, feature, refactor, etc.)
- Which template is most appropriate
- How to fill out the template based on the actual code changes

This approach leverages Claude's understanding of code and context rather than rigid rules.

## Running Tests

```bash
# Run the validation script
uv run python validate_solution.py

# Run unit tests
uv run pytest test_server.py -v
```

## Running the Server Directly

```bash
# Start the MCP server
uv run server.py
```