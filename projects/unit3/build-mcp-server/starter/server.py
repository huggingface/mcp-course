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
    # Implementation
    try:
        # Get the working directory (from MCP roots or current directory)
        working_dir = Path.cwd()
        if mcp:
            try:
                context = mcp.get_context()
                if context and context.session:
                    roots_result = await context.session.list_roots()
                    if roots_result and roots_result.roots:
                        working_dir = Path(roots_result.roots[0].uri.path)
            except Exception:
                # Fallback to current directory if context/roots aren't available
                pass
        
        # 1. Get list of changed files
        status_cmd = ["git", "diff", "--name-status", base_branch]
        status_result = subprocess.run(
            status_cmd, 
            cwd=working_dir, 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if status_result.returncode != 0:
            # Try to fetch if the branch isn't found? Or just return error
            return json.dumps({
                "error": f"Git command failed: {status_result.stderr}",
                "hint": f"Make sure {base_branch} exists and is a valid branch."
            })
            
        changed_files_list = status_result.stdout.strip().split('\n')
        changed_files = [line.split('\t')[-1] for line in changed_files_list if line]
        
        response = {
            "files_changed": changed_files,
            "comparison_branch": base_branch
        }
        
        # 2. Get the diff content if requested
        if include_diff:
            diff_cmd = ["git", "diff", base_branch]
            diff_result = subprocess.run(
                diff_cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False
            )
            
            diff_content = diff_result.stdout
            
            # Truncate if too large (MCP limit is around 25k tokens, so ~100k chars is safe-ish, but let's be conservative)
            MAX_CHARS = 50000 
            if len(diff_content) > MAX_CHARS:
                diff_content = diff_content[:MAX_CHARS] + "\n... (Diff truncated due to size limits) ..."
                response["truncated"] = True
                
            response["diff"] = diff_content
            
        return json.dumps(response, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    # Implementation
    try:
        templates = []
        if TEMPLATES_DIR.exists():
            for template_file in TEMPLATES_DIR.glob("*.md"):
                try:
                    content = template_file.read_text()
                    templates.append({
                        "name": template_file.name,
                        "content": content
                    })
                except Exception as e:
                    # Skip files that can't be read
                    continue
        
        return json.dumps(templates, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to list templates: {str(e)}"})


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """
    # Implementation
    try:
        # Map common change types to template files
        type_mapping = {
            "bug": "bug.md",
            "fix": "bug.md",
            "feature": "feature.md",
            "feat": "feature.md",
            "docs": "docs.md",
            "documentation": "docs.md",
            "refactor": "refactor.md",
            "test": "test.md",
            "tests": "test.md",
            "perf": "performance.md",
            "performance": "performance.md",
            "security": "security.md"
        }
        
        # Normalize input
        normalized_type = change_type.lower().strip()
        
        # Determine best template
        template_name = type_mapping.get(normalized_type, "feature.md") # Default to feature if unknown
        
        response = {
            "recommended_template": template_name,
            "reasoning": f"Based on the change type '{change_type}', we recommend the {template_name} template.",
            "change_type_detected": normalized_type
        }
        
        # Try to include content if available
        template_path = TEMPLATES_DIR / template_name
        if template_path.exists():
            response["template_content"] = template_path.read_text()
            
        return json.dumps(response, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to suggest template: {str(e)}"})


if __name__ == "__main__":
    mcp.run()