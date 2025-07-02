#!/usr/bin/env python3
"""
Configuration module for the MCP PR Agent server.
Handles API keys and other configuration settings.
"""

import os
from typing import Optional


class Config:
    """Configuration class for the MCP server."""
    
    def __init__(self):
        """Initialize configuration with environment variables and defaults."""
        # Gemini API configuration
        self.gemini_api_key = self._get_gemini_api_key()
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        
        # Server configuration
        self.max_diff_lines = int(os.getenv("MAX_DIFF_LINES", "500"))
        self.enable_gemini_analysis = os.getenv("ENABLE_GEMINI_ANALYSIS", "true").lower() == "true"
        
    def _get_gemini_api_key(self) -> Optional[str]:
        """Get Gemini API key from environment or fallback to hardcoded value."""
        # First try environment variable (recommended for production)
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key:
            return api_key
            
        # Fallback to hardcoded key (for development/testing)
        # Note: In production, always use environment variables!
        fallback_key = "AIzaSyCtdIPcCFtcnlXbzpPi6J64TREtWp39vHs"
        
        print("⚠️  Using hardcoded Gemini API key. For production, set GEMINI_API_KEY environment variable.")
        return fallback_key
    
    def is_gemini_configured(self) -> bool:
        """Check if Gemini API is properly configured."""
        return self.gemini_api_key is not None and self.enable_gemini_analysis
    
    def get_gemini_config(self) -> dict:
        """Get Gemini configuration as a dictionary."""
        return {
            "api_key": self.gemini_api_key,
            "model": self.gemini_model,
            "enabled": self.enable_gemini_analysis
        }

    def validate_configuration(self) -> dict:
        """Validate the current configuration and return status."""
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }

        # Check Gemini API key
        if not self.gemini_api_key:
            validation_result["errors"].append("Gemini API key is not configured")
            validation_result["valid"] = False
        elif len(self.gemini_api_key) < 20:  # Basic length check
            validation_result["warnings"].append("Gemini API key seems too short")

        # Check model configuration
        valid_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        if self.gemini_model not in valid_models:
            validation_result["warnings"].append(f"Gemini model '{self.gemini_model}' is not in the list of known models: {valid_models}")

        # Check numeric configurations
        if self.max_diff_lines <= 0:
            validation_result["errors"].append("max_diff_lines must be positive")
            validation_result["valid"] = False
        elif self.max_diff_lines > 2000:
            validation_result["warnings"].append("max_diff_lines is very high, may cause token limit issues")

        return validation_result

    def get_debug_info(self) -> dict:
        """Get configuration information for debugging (without sensitive data)."""
        return {
            "gemini_model": self.gemini_model,
            "max_diff_lines": self.max_diff_lines,
            "enable_gemini_analysis": self.enable_gemini_analysis,
            "api_key_configured": bool(self.gemini_api_key),
            "api_key_length": len(self.gemini_api_key) if self.gemini_api_key else 0,
            "validation": self.validate_configuration()
        }


# Global configuration instance
config = Config()
