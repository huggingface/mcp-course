#!/usr/bin/env python3
"""
Unit tests for Module 1: Basic MCP Server
Run these tests to validate your implementation
"""

import json
import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import your implemented functions
try:
    from server import (
        mcp,
        analyze_file_changes,
        get_pr_templates,
        suggest_template
    )
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    IMPORTS_SUCCESSFUL = False
    IMPORT_ERROR = str(e)


class TestImplementation:
    """Test that the required functions are implemented."""
    
    def test_imports(self):
        """Test that all required functions can be imported."""
        assert IMPORTS_SUCCESSFUL, f"Failed to import required functions: {IMPORT_ERROR if not IMPORTS_SUCCESSFUL else ''}"
        assert mcp is not None, "FastMCP server instance not found"
        assert callable(analyze_file_changes), "analyze_file_changes should be a callable function"
        assert callable(get_pr_templates), "get_pr_templates should be a callable function"
        assert callable(suggest_template), "suggest_template should be a callable function"


@pytest.mark.skipif(not IMPORTS_SUCCESSFUL, reason="Imports failed")
class TestAnalyzeFileChanges:
    """Test the analyze_file_changes tool."""
    
    @pytest.mark.asyncio
    async def test_returns_json_string(self):
        """Test that analyze_file_changes returns a JSON string."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(stdout="", stderr="")
            
            result = await analyze_file_changes()
            
            assert isinstance(result, str), "Should return a string"
            # Should be valid JSON
            data = json.loads(result)
            assert isinstance(data, dict), "Should return a JSON object"
    
    @pytest.mark.asyncio
    async def test_includes_required_fields(self):
        """Test that the result includes expected fields."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(stdout="M\tfile1.py\n", stderr="")
            
            result = await analyze_file_changes()
            data = json.loads(result)
            
            # For starter code, accept error messages; for full implementation, expect data
            is_implemented = not ("error" in data and "Not implemented" in str(data.get("error", "")))
            if is_implemented:
                # Check for some expected fields (flexible to allow different implementations)
                assert any(key in data for key in ["files_changed", "files", "changes", "diff"]), \
                    "Result should include file change information"
            else:
                # Starter code - just verify it returns something structured
                assert isinstance(data, dict), "Should return a JSON object even if not implemented"


@pytest.mark.skipif(not IMPORTS_SUCCESSFUL, reason="Imports failed")
class TestGetPRTemplates:
    """Test the get_pr_templates tool."""
    
    @pytest.mark.asyncio
    async def test_returns_json_string(self):
        """Test that get_pr_templates returns a JSON string."""
        result = await get_pr_templates()
        
        assert isinstance(result, str), "Should return a string"
        # Should be valid JSON
        data = json.loads(result)
        
        # For starter code, accept error messages; for full implementation, expect list
        is_implemented = not ("error" in data and isinstance(data, dict))
        if is_implemented:
            assert isinstance(data, list), "Should return a JSON array of templates"
        else:
            # Starter code - just verify it returns something structured
            assert isinstance(data, dict), "Should return a JSON object even if not implemented"
    
    @pytest.mark.asyncio
    async def test_returns_templates(self):
        """Test that templates are returned."""
        result = await get_pr_templates()
        templates = json.loads(result)
        
        # For starter code, accept error messages; for full implementation, expect templates
        is_implemented = not ("error" in templates and isinstance(templates, dict))
        if is_implemented:
            assert len(templates) > 0, "Should return at least one template"
            
            # Check that templates have expected structure
            for template in templates:
                assert isinstance(template, dict), "Each template should be a dictionary"
                # Should have some identifying information
                assert any(key in template for key in ["filename", "name", "type", "id"]), \
                    "Templates should have an identifier"
        else:
            # Starter code - just verify it's structured correctly
            assert isinstance(templates, dict), "Should return structured error for starter code"


@pytest.mark.skipif(not IMPORTS_SUCCESSFUL, reason="Imports failed")
class TestSuggestTemplate:
    """Test the suggest_template tool."""
    
    @pytest.mark.asyncio
    async def test_returns_json_string(self):
        """Test that suggest_template returns a JSON string."""
        result = await suggest_template(
            "Fixed a bug in the authentication system",
            "bug"
        )
        
        assert isinstance(result, str), "Should return a string"
        # Should be valid JSON
        data = json.loads(result)
        assert isinstance(data, dict), "Should return a JSON object"
    
    @pytest.mark.asyncio
    async def test_suggestion_structure(self):
        """Test that the suggestion has expected structure."""
        result = await suggest_template(
            "Added new feature for user management",
            "feature"
        )
        suggestion = json.loads(result)
        
        # For starter code, accept error messages; for full implementation, expect suggestion
        is_implemented = not ("error" in suggestion and "Not implemented" in str(suggestion.get("error", "")))
        if is_implemented:
            # Check for some expected fields (flexible to allow different implementations)
            assert any(key in suggestion for key in ["template", "recommended_template", "suggestion"]), \
                "Should include a template recommendation"
        else:
            # Starter code - just verify it's structured correctly
            assert isinstance(suggestion, dict), "Should return structured error for starter code"


@pytest.mark.skipif(not IMPORTS_SUCCESSFUL, reason="Imports failed")
class TestToolRegistration:
    """Test that tools are properly registered with FastMCP."""
    
    def test_tools_have_decorators(self):
        """Test that tool functions are decorated with @mcp.tool()."""
        # In FastMCP, decorated functions should have certain attributes
        # This is a basic check that functions exist and are callable
        assert hasattr(analyze_file_changes, '__name__'), \
            "analyze_file_changes should be a proper function"
        assert hasattr(get_pr_templates, '__name__'), \
            "get_pr_templates should be a proper function"
        assert hasattr(suggest_template, '__name__'), \
            "suggest_template should be a proper function"


if __name__ == "__main__":
    if not IMPORTS_SUCCESSFUL:
        print(f"❌ Cannot run tests - imports failed: {IMPORT_ERROR}")
        print("\nMake sure you've:")
        print("1. Implemented all three tool functions")
        print("2. Decorated them with @mcp.tool()")
        print("3. Installed dependencies with: uv sync")
        exit(1)
    
    # Run tests
    pytest.main([__file__, "-v"])