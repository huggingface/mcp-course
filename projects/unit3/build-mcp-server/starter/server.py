#!/usr/bin/env python3
"""
Module 1: Basic MCP Server - Starter Code
TODO: Implement tools for analyzing git changes and suggesting PR templates
"""

import json
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared across all modules)
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


# TODO: Implement tool functions here
# Example structure for a tool:
# @mcp.tool()
# async def analyze_file_changes(base_branch: str = "main", include_diff: bool = True) -> str:
#     """Get the full diff and list of changed files in the current git repository.
#     
#     Args:
#         base_branch: Base branch to compare against (default: main)
#         include_diff: Include the full diff content (default: true)
#     """
#     # Your implementation here
#     pass

# Minimal stub implementations so the server runs
# TODO: Replace these with your actual implementations

@mcp.tool()
async def analyze_file_changes(base_branch: str = "main", include_diff: bool = True) -> str:
    """Get the full diff and list of changed files in the current git repository.
    
    Args:
        base_branch: Base branch to compare against (default: main)
        include_diff: Include the full diff content (default: true)
    """
    # TODO: Implement this tool
    # IMPORTANT: MCP tools have a 25,000 token response limit!
    # Large diffs can easily exceed this. Consider:
    # - Adding a max_diff_lines parameter (e.g., 500 lines)
    # - Truncating large outputs with a message
    # - Returning summary statistics alongside limited diffs
    
    # NOTE: Git commands run in the server's directory by default!
    # To run in Claude's working directory, use MCP roots:
    # context = mcp.get_context()
    # roots_result = await context.session.list_roots()
    # working_dir = roots_result.roots[0].uri.path
    # subprocess.run(["git", "diff"], cwd=working_dir)

    try:
        context = mcp.get_context()
        roots_result = await context.session.list_roots()
        working_dir = roots_result.roots[0].uri.path
    except Exception as e:
        working_dir = Path.cwd()

    try:
        diff = subprocess.run(["git", "diff", f"{base_branch}..HEAD"], cwd=working_dir, capture_output=True, text=True) if include_diff else None
        changed_files = subprocess.run(["git", "diff", "--name-only", f"{base_branch}..HEAD"], cwd=working_dir, capture_output=True, text=True)

        return json.dumps({"diff": diff.stdout, "changed_files": changed_files.stdout})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""

    try:
        templates = [f.stem for f in TEMPLATES_DIR.glob("*.md")]
        return json.dumps({"templates": templates})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """

    template = TEMPLATES_DIR / f"{change_type}.md"
    if not template.exists():
        return json.dumps({"error": "Template not found for change type: " + change_type})
    
    template_content = template.read_text()

    return json.dumps({
        "recommended_template": change_type,
        "template_content": template_content
    })



if __name__ == "__main__":
    mcp.run()
