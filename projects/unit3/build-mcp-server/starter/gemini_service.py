#!/usr/bin/env python3
"""
Gemini AI service for enhanced PR analysis and template suggestions.
"""

import json
import logging
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiService:
    """Service class for interacting with Google's Gemini AI."""
    
    def __init__(self):
        """Initialize the Gemini service."""
        self.model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini AI with API key and configuration."""
        if not config.is_gemini_configured():
            logger.warning("Gemini AI is not configured. Some features will be disabled.")
            return
        
        try:
            # Configure the API key
            genai.configure(api_key=config.gemini_api_key)
            
            # Initialize the model with safety settings
            self.model = genai.GenerativeModel(
                model_name=config.gemini_model,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
            )
            
            logger.info(f"Gemini AI initialized successfully with model: {config.gemini_model}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if Gemini service is available."""
        return self.model is not None
    
    async def analyze_code_changes(self, diff_content: str, changed_files: List[Dict], templates: List[Dict]) -> Dict[str, Any]:
        """
        Analyze code changes using Gemini AI to provide intelligent insights.
        
        Args:
            diff_content: The git diff content
            changed_files: List of changed files with their status
            templates: Available PR templates
            
        Returns:
            Dictionary with analysis results
        """
        if not self.is_available():
            return {
                "error": "Gemini AI service is not available",
                "fallback": True
            }
        
        try:
            # Prepare the prompt for analysis
            prompt = self._create_analysis_prompt(diff_content, changed_files, templates)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis = self._parse_analysis_response(response.text)
            
            return {
                "success": True,
                "analysis": analysis,
                "model_used": config.gemini_model
            }
            
        except Exception as e:
            logger.error(f"Error during Gemini analysis: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "fallback": True
            }
    
    def _create_analysis_prompt(self, diff_content: str, changed_files: List[Dict], templates: List[Dict]) -> str:
        """Create a comprehensive prompt for code change analysis."""

        # Get template names for reference
        template_names = [t.get("name", "unknown") for t in templates]

        # Analyze file types and patterns
        file_analysis = self._analyze_file_patterns(changed_files)

        prompt = f"""
You are an expert code reviewer and technical writer. Analyze the following code changes and provide insights for creating a pull request.

## Changed Files Analysis:
{json.dumps(changed_files, indent=2)}

## File Pattern Analysis:
{json.dumps(file_analysis, indent=2)}

## Available PR Templates:
{', '.join(template_names)}

## Code Diff:
```diff
{diff_content[:3000]}  # Limit diff to avoid token limits
```

Please provide a JSON response with the following structure:
{{
    "change_type": "bug|feature|docs|refactor|test|performance|security",
    "summary": "Brief description of what changed",
    "impact": "Description of the impact/importance",
    "recommended_template": "Name of the most appropriate template",
    "confidence": "high|medium|low",
    "key_changes": ["list", "of", "key", "changes"],
    "testing_suggestions": ["suggested", "testing", "approaches"],
    "review_focus": ["areas", "reviewers", "should", "focus", "on"],
    "breaking_changes": true/false,
    "security_implications": true/false,
    "complexity_score": "1-10 (1=simple, 10=very complex)",
    "estimated_review_time": "estimated time in minutes",
    "dependencies_affected": ["list", "of", "affected", "dependencies"],
    "rollback_risk": "low|medium|high"
}}

Focus on:
1. Identifying the primary type of change
2. Understanding the business/technical impact
3. Suggesting the most appropriate PR template
4. Highlighting important aspects for reviewers
5. Identifying potential risks or breaking changes
6. Assessing complexity and review requirements
7. Evaluating rollback risks and dependencies

Respond only with valid JSON.
"""
        return prompt.strip()

    def _analyze_file_patterns(self, changed_files: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in changed files to provide context."""
        patterns = {
            "total_files": len(changed_files),
            "file_types": {},
            "change_types": {},
            "directories": set(),
            "has_tests": False,
            "has_docs": False,
            "has_config": False
        }

        for file_info in changed_files:
            filename = file_info.get("filename", "")
            status = file_info.get("status", "")

            # Analyze file extension
            if "." in filename:
                ext = filename.split(".")[-1].lower()
                patterns["file_types"][ext] = patterns["file_types"].get(ext, 0) + 1

            # Analyze change type
            patterns["change_types"][status] = patterns["change_types"].get(status, 0) + 1

            # Analyze directory
            if "/" in filename:
                directory = filename.split("/")[0]
                patterns["directories"].add(directory)

            # Check for special file types
            filename_lower = filename.lower()
            if any(test_indicator in filename_lower for test_indicator in ["test", "spec", "__test__"]):
                patterns["has_tests"] = True
            if any(doc_indicator in filename_lower for doc_indicator in ["readme", "doc", ".md", "changelog"]):
                patterns["has_docs"] = True
            if any(config_indicator in filename_lower for config_indicator in ["config", "settings", ".json", ".yaml", ".toml", ".env"]):
                patterns["has_config"] = True

        # Convert set to list for JSON serialization
        patterns["directories"] = list(patterns["directories"])

        return patterns
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate the Gemini response."""
        try:
            # Try to extract JSON from the response
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            # Parse JSON
            analysis = json.loads(response_text.strip())
            
            # Validate required fields
            required_fields = ["change_type", "summary", "recommended_template"]
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = "unknown"
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
            logger.error(f"Response text: {response_text}")
            
            # Return a fallback analysis
            return {
                "change_type": "unknown",
                "summary": "Unable to analyze changes automatically",
                "recommended_template": "feature",
                "confidence": "low",
                "error": "Failed to parse AI response",
                "raw_response": response_text
            }

    async def generate_pr_description(self, analysis_result: Dict[str, Any], template_content: str = "") -> Dict[str, Any]:
        """
        Generate a comprehensive PR description based on analysis results.

        Args:
            analysis_result: Results from analyze_code_changes
            template_content: Optional template content to use as base

        Returns:
            Dictionary with generated PR description and metadata
        """
        if not self.is_available():
            return {
                "error": "Gemini AI service is not available",
                "fallback": True
            }

        try:
            # Create prompt for PR description generation
            prompt = self._create_pr_description_prompt(analysis_result, template_content)

            # Generate response
            response = self.model.generate_content(prompt)

            # Parse the response
            pr_description = self._parse_pr_description_response(response.text)

            return {
                "success": True,
                "pr_description": pr_description,
                "model_used": config.gemini_model,
                "based_on_analysis": analysis_result.get("analysis", {})
            }

        except Exception as e:
            logger.error(f"Error generating PR description: {str(e)}")
            return {
                "error": f"PR description generation failed: {str(e)}",
                "fallback": True
            }

    def _create_pr_description_prompt(self, analysis_result: Dict[str, Any], template_content: str) -> str:
        """Create a prompt for generating PR descriptions."""

        analysis = analysis_result.get("analysis", {})

        prompt = f"""
You are an expert technical writer creating a comprehensive pull request description.

## Analysis Results:
{json.dumps(analysis, indent=2)}

## Template Content (if available):
{template_content[:1000] if template_content else "No template provided"}

Generate a well-structured PR description that includes:

1. **Title**: A clear, concise title (50-72 characters)
2. **Summary**: Brief overview of changes
3. **Changes Made**: Detailed list of modifications
4. **Testing**: How the changes were tested
5. **Impact**: Business/technical impact
6. **Review Notes**: What reviewers should focus on
7. **Checklist**: Items to verify before merge

Please provide a JSON response with this structure:
{{
    "title": "Concise PR title",
    "summary": "Brief overview paragraph",
    "changes_made": ["detailed", "list", "of", "changes"],
    "testing_performed": ["testing", "approaches", "used"],
    "impact_assessment": "Description of impact",
    "review_focus": ["areas", "for", "reviewers"],
    "pre_merge_checklist": ["items", "to", "verify"],
    "labels_suggested": ["suggested", "github", "labels"],
    "estimated_review_time": "time in minutes"
}}

Make the description professional, clear, and actionable. Focus on helping reviewers understand the changes quickly.

Respond only with valid JSON.
"""
        return prompt.strip()

    def _parse_pr_description_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate the PR description response."""
        try:
            # Clean up response text
            response_text = response_text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            # Parse JSON
            pr_description = json.loads(response_text.strip())

            # Validate and provide defaults for required fields
            defaults = {
                "title": "Pull Request",
                "summary": "Changes made to the codebase",
                "changes_made": ["Changes not specified"],
                "testing_performed": ["Testing not specified"],
                "impact_assessment": "Impact not assessed",
                "review_focus": ["General review"],
                "pre_merge_checklist": ["Verify changes work as expected"],
                "labels_suggested": [],
                "estimated_review_time": "15-30 minutes"
            }

            for key, default_value in defaults.items():
                if key not in pr_description:
                    pr_description[key] = default_value

            return pr_description

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse PR description response: {str(e)}")

            # Return a fallback description
            return {
                "title": "Pull Request - Auto Generated",
                "summary": "Unable to generate description automatically",
                "changes_made": ["Changes not analyzed"],
                "testing_performed": ["Testing not specified"],
                "impact_assessment": "Impact not assessed",
                "review_focus": ["Manual review required"],
                "pre_merge_checklist": ["Verify all changes"],
                "labels_suggested": [],
                "estimated_review_time": "30+ minutes",
                "error": "Failed to parse AI response",
                "raw_response": response_text
            }


# Global service instance
gemini_service = GeminiService()
