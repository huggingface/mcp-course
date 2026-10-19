#!/usr/bin/env python3
"""
Module 1: Basic MCP Server - Starter Code
TODO: Implement tools for analyzing git changes and suggesting PR templates
"""

import json
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname

from mcp.server.mcpserver import MCPServer

# Initialize the MCPServer server
mcp = MCPServer("pr-agent")

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
async def analyze_file_changes(base_branch: str = "main", include_diff: bool = True, max_diff_lines: int = 500) -> str:
    """Analyze file changes with smart output limiting.
    
    Args:
        base_branch: Branch to compare against
        include_diff: Whether to include the actual diff
        max_diff_lines: Maximum diff lines to include (default 500)
    """
    try:
        # Get Claude's working directory from roots
        try:
            context = mcp.get_context()
            roots_result = await context.session.list_roots()
            # Convert the file:// URI to a native path (handles /C:/... on Windows and %20 escapes)
            working_dir = url2pathname(urlparse(str(roots_result.roots[0].uri)).path)
        except Exception:
            # No roots available (e.g. outside a client session), use current directory
            working_dir = os.getcwd()

        # Get the list of changed files
        files_result = subprocess.run(
            ["git", "diff", "--name-status", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=working_dir
        )

        # Get the diff
        result = subprocess.run(
            ["git", "diff", f"{base_branch}...HEAD"],
            capture_output=True, 
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=working_dir
        )
        
        diff_output = result.stdout
        diff_lines = diff_output.split('\n')
        
        # Smart truncation if needed
        if len(diff_lines) > max_diff_lines:
            truncated_diff = '\n'.join(diff_lines[:max_diff_lines])
            truncated_diff += f"\n\n... Output truncated. Showing {max_diff_lines} of {len(diff_lines)} lines ..."
            diff_output = truncated_diff
        
        # Get summary statistics
        stats_result = subprocess.run(
            ["git", "diff", "--stat", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=working_dir
        )
        
        return json.dumps({
            "stats": stats_result.stdout,
            "total_lines": len(diff_lines),
            "diff": diff_output if include_diff else "Use include_diff=true to see diff",
            "files_changed": files_result.stdout
        })
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    # TODO: Implement this tool
    return json.dumps({"error": "Not implemented yet", "hint": "Read templates from TEMPLATES_DIR"})


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """
    # TODO: Implement this tool
    return json.dumps({"error": "Not implemented yet", "hint": "Map change_type to templates"})


if __name__ == "__main__":
    mcp.run()