#!/usr/bin/env python3
"""
Module 1: Basic MCP Server with PR Template Tools
A minimal MCP server that provides tools for analyzing file changes and suggesting PR templates.

ENHANCEMENT: Added intelligent change pattern analysis for smarter PR categorization.
"""

import json
import os
import subprocess
from typing import Optional
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared between starter and solution)
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
    working_directory: Optional[str] = None
) -> str:
    """Get the full diff and list of changed files in the current git repository.

    Args:
        base_branch: Base branch to compare against (default: main)
        include_diff: Include the full diff content (default: true)
        max_diff_lines: Maximum number of diff lines to include (default: 500)
        working_directory: Directory to run git commands in (default: current directory)
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

        # Get list of changed files
        files_result = subprocess.run(
            ["git", "diff", "--name-status", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )

        # Get diff statistics
        stat_result = subprocess.run(
            ["git", "diff", "--stat", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd
        )

        # Get the actual diff if requested
        diff_content = ""
        truncated = False
        if include_diff:
            diff_result = subprocess.run(
                ["git", "diff", f"{base_branch}...HEAD"],
                capture_output=True,
                text=True,
                cwd=cwd
            )
            diff_lines = diff_result.stdout.split('\n')

            # Check if we need to truncate
            if len(diff_lines) > max_diff_lines:
                diff_content = '\n'.join(diff_lines[:max_diff_lines])
                diff_content += f"\n\n... Output truncated. Showing {max_diff_lines} of {len(diff_lines)} lines ..."
                diff_content += "\n... Use max_diff_lines parameter to see more ..."
                truncated = True
            else:
                diff_content = diff_result.stdout

        # Get commit messages for context
        commits_result = subprocess.run(
            ["git", "log", "--oneline", f"{base_branch}..HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd
        )

        analysis = {
            "base_branch": base_branch,
            "files_changed": files_result.stdout,
            "statistics": stat_result.stdout,
            "commits": commits_result.stdout,
            "diff": diff_content if include_diff else "Diff not included (set include_diff=true to see full diff)",
            "truncated": truncated,
            "total_diff_lines": len(diff_lines) if include_diff else 0
        }

        return json.dumps(analysis, indent=2)

    except subprocess.CalledProcessError as e:
        return json.dumps({"error": f"Git error: {e.stderr}"})
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
async def analyze_change_patterns(base_branch: str = "main") -> str:
    """Analyze file change patterns to intelligently detect the type of changes made.

    This new tool uses file extensions, paths, and change patterns to automatically
    determine what kind of changes were made, making PR categorization smarter.

    Args:
        base_branch: Base branch to compare against (default: main)
    """
    try:
        # Get working directory from MCP context
        working_dir = os.getcwd()
        try:
            context = mcp.get_context()
            roots_result = await context.session.list_roots()
            if roots_result.roots:
                working_dir = roots_result.roots[0].uri.path
        except Exception:
            pass

        # Get changed files with their status
        files_result = subprocess.run(
            ["git", "diff", "--name-status", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=working_dir
        )

        if files_result.returncode != 0:
            return json.dumps({"error": "Failed to get file changes"})

        # Analyze file patterns
        analysis = {
            "detected_patterns": [],
            "change_indicators": {},
            "recommended_type": "feature",
            "confidence": "medium"
        }

        changed_files = []
        for line in files_result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    status, filename = parts
                    changed_files.append({"status": status, "filename": filename})

        # Pattern analysis
        test_files = sum(1 for f in changed_files if 'test' in f['filename'].lower() or f['filename'].endswith('.test.py'))
        doc_files = sum(1 for f in changed_files if f['filename'].endswith(('.md', '.rst', '.txt')) or 'doc' in f['filename'].lower())
        config_files = sum(1 for f in changed_files if f['filename'].endswith(('.json', '.yaml', '.yml', '.toml', '.ini')))
        python_files = sum(1 for f in changed_files if f['filename'].endswith('.py'))

        # Smart detection logic
        if test_files > 0 and test_files == len(changed_files):
            analysis["recommended_type"] = "test"
            analysis["confidence"] = "high"
            analysis["detected_patterns"].append("Only test files modified")
        elif doc_files > 0 and doc_files >= len(changed_files) * 0.8:
            analysis["recommended_type"] = "docs"
            analysis["confidence"] = "high"
            analysis["detected_patterns"].append("Primarily documentation changes")
        elif config_files > python_files:
            analysis["recommended_type"] = "refactor"
            analysis["confidence"] = "medium"
            analysis["detected_patterns"].append("Configuration changes detected")
        elif any(f['status'] == 'A' for f in changed_files):
            analysis["recommended_type"] = "feature"
            analysis["confidence"] = "high"
            analysis["detected_patterns"].append("New files added")
        else:
            analysis["recommended_type"] = "refactor"
            analysis["confidence"] = "medium"
            analysis["detected_patterns"].append("Existing files modified")

        analysis["change_indicators"] = {
            "total_files": len(changed_files),
            "test_files": test_files,
            "doc_files": doc_files,
            "config_files": config_files,
            "python_files": python_files,
            "new_files": sum(1 for f in changed_files if f['status'] == 'A'),
            "modified_files": sum(1 for f in changed_files if f['status'] == 'M'),
            "deleted_files": sum(1 for f in changed_files if f['status'] == 'D')
        }

        return json.dumps(analysis, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Failed to analyze change patterns: {str(e)}"})


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Gemini analyze the changes and suggest the most appropriate PR template.

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
        "usage_hint": "Gemini can help you fill out this template based on the specific changes in your PR."
    }

    return json.dumps(suggestion, indent=2)


if __name__ == "__main__":
    mcp.run()