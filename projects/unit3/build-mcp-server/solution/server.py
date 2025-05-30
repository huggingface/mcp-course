#!/usr/bin/env python3
"""
Module 1: Basic MCP Server with PR Template Tools
A minimal MCP server that provides tools for analyzing file changes and suggesting PR templates.
"""

import json
import os
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared between starter and solution)
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


@mcp.tool()
async def analyze_file_changes(
    base_branch: str = "main",
    include_diff: bool = True
) -> str:
    """Get the full diff and list of changed files in the current git repository.
    
    Args:
        base_branch: Base branch to compare against (default: main)
        include_diff: Include the full diff content (default: true)
    """
    try:
        # Get list of changed files
        files_result = subprocess.run(
            ["git", "diff", "--name-status", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get diff statistics
        stat_result = subprocess.run(
            ["git", "diff", "--stat", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True
        )
        
        # Get the actual diff if requested
        diff_content = ""
        if include_diff:
            diff_result = subprocess.run(
                ["git", "diff", f"{base_branch}...HEAD"],
                capture_output=True,
                text=True
            )
            diff_content = diff_result.stdout
        
        # Get commit messages for context
        commits_result = subprocess.run(
            ["git", "log", "--oneline", f"{base_branch}..HEAD"],
            capture_output=True,
            text=True
        )
        
        analysis = {
            "base_branch": base_branch,
            "files_changed": files_result.stdout,
            "statistics": stat_result.stdout,
            "commits": commits_result.stdout,
            "diff": diff_content if include_diff else "Diff not included (set include_diff=true to see full diff)"
        }
        
        return json.dumps(analysis, indent=2)
        
    except subprocess.CalledProcessError as e:
        return f"Error analyzing changes: {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    templates = []
    
    # Define default templates
    default_templates = {
        "bug.md": "Bug Fix",
        "feature.md": "Feature",
        "docs.md": "Documentation",
        "refactor.md": "Refactor",
        "test.md": "Test",
        "performance.md": "Performance",
        "security.md": "Security"
    }
    
    for filename, template_type in default_templates.items():
        template_path = TEMPLATES_DIR / filename
        
        # Read template content
        content = template_path.read_text()
        
        templates.append({
            "filename": filename,
            "type": template_type,
            "content": content
        })
    
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
    
    # Map change types to template files
    type_mapping = {
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
    
    # Find matching template
    template_file = type_mapping.get(change_type.lower(), "feature.md")
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


if __name__ == "__main__":
    mcp.run()