## Code Refactoring

### Description
<!-- What code is being refactored? -->
Updated dependencies in pyproject.toml and modified server.py to include working_directory parameter in analyze_file_changes tool.

### Motivation
<!-- Why is this refactoring needed? -->
To improve the functionality of the analyze_file_changes tool by allowing it to run in a specified working directory.

### Changes
<!-- List of specific refactoring changes -->
1. Updated dependencies in pyproject.toml
2. Added working_directory parameter to analyze_file_changes tool in server.py
3. Removed mcp-server-hf-course-in-action.png

### Testing
- [ ] All existing tests pass
- [ ] No functional changes
- [ ] Performance impact assessed

### Risk Assessment
<!-- Any risks with this refactoring? -->
Low risk, as the changes are primarily related to dependency updates and adding a new parameter to an existing tool.
