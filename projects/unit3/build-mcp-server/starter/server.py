#!/usr/bin/env python3
"""
Module 1: Basic MCP Server - Starter Code
TODO: Implement tools for analyzing git changes and suggesting PR templates
"""
from dotenv import load_dotenv


import json
import subprocess
from pathlib import Path
import os
import sys

from mcp.server.fastmcp import FastMCP
load_dotenv()

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared across all modules)
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    # In one-file mode, sys._MEIPASS is the path to the temp directory where data is extracted
    # In one-folder mode, Path(__file__).parent is the app directory
    TEMPLATES_DIR = Path(sys._MEIPASS if hasattr(sys, '_MEIPASS') else Path(__file__).parent) / "templates"
else:
    # Running in a regular Python environment
    TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"
# Default PR templates
DEFAULT_TEMPLATES = {
    "bug.md": "Bug Fix",
    "feature.md": "Feature",
    "docs.md": "Documentation",
    "refactor.md": "Refactor",
    "test.md": "Test",
    "performance.md": "Performance",
    "security.md": "Security"
}

# Type mapping for PR templates
TYPE_MAPPING = {
    "bug": "bug.md",
    "fix": "bug.md",
    "feature": "feature.md",
    "enhancement": "feature.md",
    "docs": "docs.md",
    "documentation": "docs.md",
    "refactor": "refactor.md",
    "cleanup": "refactor.md",
    "test": "test.md",
    "testing": "test.md",
    "performance": "performance.md",
    "optimization": "performance.md",
    "security": "security.md"
}


@mcp.tool()
async def analyze_file_changes(
    base_branch: str = "main",
    include_diff: bool = True,
    max_diff_lines: int = 500,
    working_directory: str | None = None
) -> str:
    """Get the full diff and list of changed files in the current git repository.
    
    Args:
        base_branch: Base branch to compare against (default: main)
        include_diff: Include the full diff content (default: true)
        max_diff_lines: Maximum number of diff lines to return (default: 500)
        working_directory: Optional working directory to use instead of fetching from MCP context
    """
    try:
        # Try to get working directory from roots first
        if working_directory is None:
            try:
                context = mcp.get_context()
                roots_result = await context.session.list_roots()
                # Get the first root - Claude Code sets this to the CWD
                root = roots_result.roots[0]
                # FileUrl object has a .path property that gives us the path directly
                working_directory = root.uri.path
            except Exception:
                # If we can't get roots, fall back to current directory
                pass
        
        # Use provided working directory or current directory
        cwd = working_directory if working_directory else os.getcwd()
        
        # Debug output
        debug_info = {
            "provided_working_directory": working_directory,
            "actual_cwd": cwd,
            "server_process_cwd": os.getcwd(),
            "server_file_location": str(Path(__file__).parent),
            "roots_check": None
        }
        
        # Add roots debug info
        try:
            context = mcp.get_context()
            roots_result = await context.session.list_roots()
            debug_info["roots_check"] = {
                "found": True,
                "count": len(roots_result.roots),
                "roots": [str(root.uri) for root in roots_result.roots]
            }
        except Exception as e:
            debug_info["roots_check"] = {
                "found": False,
                "error": str(e)
            }
        
        analysis = await _get_git_changes(cwd, base_branch, include_diff, max_diff_lines)
        analysis["_debug"] = debug_info
        
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    templates = [
        {
            "filename": filename,
            "type": template_type,
            "content": (TEMPLATES_DIR / filename).read_text()
        }
        for filename, template_type in DEFAULT_TEMPLATES.items()
    ]
    
    return json.dumps(templates, indent=2)


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """
    
    # Get available templates
    templates_response = await get_pr_templates()
    templates = json.loads(templates_response)
    
    # Find matching template
    template_file = TYPE_MAPPING.get(change_type.lower(), "feature.md")
    selected_template = next(
        (t for t in templates if t["filename"] == template_file),
        templates[0]  # Default to first template if no match
    )
    
    suggestion = {
        "recommended_template": selected_template,
        "reasoning": f"Based on your analysis: '{changes_summary}', this appears to be a {change_type} change.",
        "template_content": selected_template["content"],
        "usage_hint": "Claude can help you fill out this template based on the specific changes in your PR."
    }
    
    return json.dumps(suggestion, indent=2)


@mcp.tool()
async def get_local_file_changes(working_directory: str | None = None) -> str:
    """Get a summary of local file changes (staged, unstaged, untracked).
    
    Args:
        working_directory: Optional working directory to use instead of fetching from MCP context
    """
    try:
        if working_directory is None:
            context = mcp.get_context()
            roots_result = await context.session.list_roots()
            working_directory = roots_result.roots[0].uri.path
        
        cwd = working_directory if working_directory else os.getcwd()

        # Get status of files (staged, unstaged, untracked)
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        status_output = status_result.stdout.strip().splitlines()

        # Get unstaged changes (diff of working tree vs index)
        unstaged_diff_result = subprocess.run(
            ["git", "diff"],
            cwd=cwd,
            capture_output=True,
            text=True
        )
        unstaged_diff = unstaged_diff_result.stdout

        # Get staged changes (diff of index vs HEAD)
        staged_diff_result = subprocess.run(
            ["git", "diff", "--staged"],
            cwd=cwd,
            capture_output=True,
            text=True
        )
        staged_diff = staged_diff_result.stdout

        return json.dumps({
            "status": status_output,
            "unstaged_diff": unstaged_diff,
            "staged_diff": staged_diff,
            "working_directory": cwd
        }, indent=2)
    
    except subprocess.CalledProcessError as e:
        return json.dumps({"error": f"Git command failed: {e.stderr}"})
    except Exception as e:
        return json.dumps({"error": f"Failed to get local file changes: {e}"})


async def _get_git_changes(working_dir: str, base_branch: str, include_diff: bool, max_diff_lines: int) -> dict:
    """Helper function to get git changes and diff, callable outside of MCP context."""
    # Get changed files with status
    try:
        result = subprocess.run(
            ["git", "diff", "--name-status", f"{base_branch}...HEAD"],
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=True
        )
        changed_files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        stat_result = subprocess.run(
            ["git", "diff", "--stat", f"{base_branch}...HEAD"],
            cwd=working_dir,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        return {"error": f"Git error: {e.stderr}"}
    except Exception as e:
        return {"error": f"Failed to get changed files or stats: {e}"}

    diff = ""
    truncated = False
    diff_line_count = 0
    if include_diff:
        try:
            diff_result = subprocess.run(
                ["git", "diff", f"{base_branch}...HEAD"],
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=True
            )
            diff_lines = diff_result.stdout.splitlines()
            diff_line_count = len(diff_lines)
            if diff_line_count > max_diff_lines:
                diff = "\n".join(diff_lines[:max_diff_lines]) + "\n\n... Output truncated. Showing {max_diff_lines} of {len(diff_lines)} lines ...\n... Use max_diff_lines parameter to see more ..."
                truncated = True
            else:
                diff = diff_result.stdout
            
            commits_result = subprocess.run(
                ["git", "log", "--oneline", f"{base_branch}..HEAD"],
                capture_output=True,
                text=True,
                cwd=working_dir
            )
        except subprocess.CalledProcessError as e:
            return {"error": f"Git error: {e.stderr}"}
        except Exception as e:
            return {"error": f"Failed to get diff or commits: {e}"}

    return {
        "changed_files": changed_files,
        "statistics": stat_result.stdout,
        "diff": diff if include_diff else "Diff not included (set include_diff=true to see full diff)",
        "truncated": truncated,
        "diff_line_count": diff_line_count,
        "commits": commits_result.stdout if include_diff else None
    }


if __name__ == "__main__":
    mcp.run()