# Unit 3 Solution Walkthrough: Building a Pull Request Agent with MCP

## Overview

This walkthrough guides you through the complete solution for Unit 3's Pull Request Agent - an MCP server that helps developers create better pull requests by analyzing code changes, monitoring CI/CD pipelines, and automating team communications. The solution demonstrates all three MCP primitives (Tools, Resources, and Prompts) working together in a real-world workflow.

## Architecture Overview

The PR Agent consists of interconnected modules that progressively build a complete automation system:

1. **Build MCP Server** - Basic server with Tools for PR template suggestions
2. **Smart File Analysis** - Enhanced analysis using Resources for project context
3. **GitHub Actions Integration** - CI/CD monitoring with standardized Prompts
4. **Hugging Face Hub Integration** - Model deployment and dataset PR workflows
5. **Slack Notification** - Team communication integrating all MCP primitives

## Module 1: Build MCP Server

### What We're Building
A minimal MCP server that analyzes file changes and suggests appropriate PR templates using MCP Tools.

### Key Components

#### 1. Server Initialization (`server.py`)
```python
# The server registers three essential tools:
# - analyze_file_changes: Returns structured data about changed files
# - get_pr_templates: Lists available templates with metadata
# - suggest_template: Provides intelligent template recommendations
```

The server uses the MCP SDK to expose these tools to Claude Code, allowing it to gather information and make intelligent decisions about which PR template to use.

#### 2. File Analysis Tool
The `analyze_file_changes` tool examines the git diff to identify:
- File types and extensions
- Number of files changed
- Lines added/removed
- Common patterns (tests, configs, docs)

This structured data enables Claude to understand the nature of the changes without hard-coding decision logic.

#### 3. Template Management
Templates are stored as markdown files in the `templates/` directory:
- `bug.md` - For bug fixes
- `feature.md` - For new features
- `docs.md` - For documentation updates
- `refactor.md` - For code refactoring

Each template includes placeholders that Claude can fill based on the analysis.

### How Claude Uses These Tools

1. Claude calls `analyze_file_changes` to understand what changed
2. Uses `get_pr_templates` to see available options
3. Calls `suggest_template` with the analysis data
4. Receives a recommendation with reasoning
5. Can customize the template based on specific changes

### Learning Outcomes
- Understanding tool registration and schemas
- Letting Claude make decisions with structured data
- Separation of data gathering from decision logic

## Module 2: Smart File Analysis

### What We're Building
Enhanced file analysis using MCP Resources to provide project context and team guidelines.

### Key Components

#### 1. Resource Registration
The server exposes four types of resources:
```python
# Resources provide read-only access to:
# - file://templates/ - PR template files
# - file://project-context/ - Coding standards, conventions
# - git://recent-changes/ - Commit history and patterns
# - team://guidelines/ - Review processes and standards
```

#### 2. Project Context Resources
The `project-context/` directory contains:
- `coding-standards.md` - Language-specific conventions
- `review-guidelines.md` - What reviewers look for
- `architecture.md` - System design patterns
- `dependencies.md` - Third-party library policies

Claude can read these to understand project-specific requirements.

#### 3. Git History Analysis
The `git://recent-changes/` resource provides:
- Recent commit messages and patterns
- Common PR titles and descriptions
- Team member contribution patterns
- Historical template usage

This helps Claude suggest templates consistent with team practices.

### How Claude Uses Resources

1. Reads `team://guidelines/review-process.md` to understand PR requirements
2. Accesses `file://project-context/coding-standards.md` for style guides
3. Analyzes `git://recent-changes/` to match team patterns
4. Combines this context with file analysis for better suggestions

### Enhanced Decision Making
With resources, Claude can now:
- Suggest templates matching team conventions
- Include project-specific requirements in PRs
- Reference coding standards in descriptions
- Align with historical team practices

### Learning Outcomes
- Resource URI design and schemas
- Making project knowledge accessible to AI
- Context-aware decision making
- Balancing automation with team standards

## Module 3: GitHub Actions Integration

### What We're Building
Real-time CI/CD monitoring using webhooks and standardized prompts for consistent team communication.

### Key Components

#### 1. Webhook Server
Uses Cloudflare Tunnel to receive GitHub Actions events:
```python
# Webhook endpoint handles:
# - workflow_run events
# - check_run events  
# - pull_request status updates
# - deployment notifications
```

#### 2. Prompt Templates
Four standardized prompts ensure consistency:
- **"Analyze CI Results"** - Process test failures and build errors
- **"Generate Status Summary"** - Create human-readable status updates
- **"Create Follow-up Tasks"** - Suggest next steps based on results
- **"Draft Team Notification"** - Format updates for different audiences

#### 3. Event Processing Pipeline
1. Receive webhook from GitHub
2. Parse event data and extract relevant information
3. Use appropriate prompt based on event type
4. Generate standardized response
5. Store for team notification

### How Claude Uses Prompts

Example prompt usage:
```python
# When tests fail, Claude uses the "Analyze CI Results" prompt:
prompt_data = {
    "event_type": "workflow_run",
    "status": "failure",
    "failed_jobs": ["unit-tests", "lint"],
    "error_logs": "...",
    "pr_context": {...}
}

# Claude generates:
# - Root cause analysis
# - Suggested fixes
# - Impact assessment
# - Next steps
```

### Standardized Workflows
Prompts ensure that regardless of who's working:
- CI failures are analyzed consistently
- Status updates follow team formats
- Follow-up actions align with processes
- Notifications contain required information

### Learning Outcomes
- Webhook integration patterns
- Prompt engineering for consistency
- Event-driven architectures
- Standardizing team workflows

## Module 4: Hugging Face Hub Integration

### What We're Building
Integration with Hugging Face Hub for LLM and dataset PRs, adding specialized workflows for teams working with language models.

### Key Components

#### 1. Hub-Specific Tools
```python
# Tools for Hugging Face workflows:
# - analyze_model_changes: Detect LLM file modifications
# - validate_dataset_format: Check training data compliance
# - generate_model_card: Create/update model documentation
# - suggest_hub_template: PR templates for LLMs/datasets
```

#### 2. Hub Resources
```python
# Resources for Hub context:
# - hub://model-cards/ - LLM card templates and examples
# - hub://dataset-formats/ - Training data specifications
# - hub://community-standards/ - Hub community guidelines
# - hub://license-info/ - License compatibility checks
```

#### 3. LLM-Specific Prompts
```python
# Prompts for LLM workflows:
# - "Analyze Model Changes" - Understand LLM updates
# - "Generate Benchmark Summary" - Create evaluation metrics
# - "Check Dataset Quality" - Validate training data
# - "Draft Model Card Update" - Update documentation
```

### Hub-Specific Workflows

When a PR modifies LLM files:
1. **Tool**: `analyze_model_changes` detects model architecture changes
2. **Resource**: Reads `hub://model-cards/llm-template.md`
3. **Prompt**: "Generate Benchmark Summary" creates evaluation section
4. **Tool**: `generate_model_card` updates documentation
5. **Resource**: Checks `hub://license-info/` for compatibility

### Dataset PR Handling
For training data updates:
- Validates format consistency
- Checks data quality metrics
- Updates dataset cards
- Suggests appropriate reviewers

### Learning Outcomes
- Hugging Face Hub API integration
- LLM-specific PR workflows
- Model and dataset documentation
- Community standards compliance

## Module 5: Slack Notification

### What We're Building
Automated team notifications combining Tools, Resources, and Prompts for complete workflow automation.

### Key Components

#### 1. Communication Tools
```python
# Three tools for team updates:
# - send_slack_message: Post to team channels
# - get_team_members: Identify who to notify
# - track_notification_status: Monitor delivery
```

#### 2. Team Resources
```python
# Resources for team data:
# - team://members/ - Developer profiles and preferences
# - slack://channels/ - Channel configurations
# - notification://templates/ - Message formats
```

#### 3. Notification Prompts
```python
# Prompts for communication:
# - "Format Team Update" - Style messages appropriately
# - "Choose Communication Channel" - Select right audience
# - "Escalate if Critical" - Handle urgent issues
```

### Integration Example

When CI fails on a critical PR:
1. **Tool**: `get_team_members` identifies the PR author and reviewers
2. **Resource**: `team://members/{user}/preferences` checks notification settings
3. **Prompt**: "Format Team Update" creates appropriate message
4. **Tool**: `send_slack_message` delivers to right channel
5. **Resource**: `notification://templates/ci-failure` ensures consistent format
6. **Prompt**: "Escalate if Critical" determines if additional alerts needed

### Intelligent Routing
The system considers:
- Team member availability (from calendar resources)
- Notification preferences (email vs Slack)
- Message urgency (based on PR labels)
- Time zones and working hours

### Learning Outcomes
- Primitive integration patterns
- Complex workflow orchestration
- Balancing automation with human needs
- Production-ready error handling

## Complete Workflow Example

Here's how all components work together for a typical PR:

1. **Developer creates PR**
   - GitHub webhook triggers the server
   - Tool: `analyze_file_changes` examines the diff
   - Resource: Reads team guidelines and project context
   - Prompt: Suggests optimal PR template

2. **CI/CD Pipeline Runs**
   - Webhook receives workflow events
   - Prompt: "Analyze CI Results" processes outcomes
   - Resource: Checks team escalation policies
   - Tool: Updates PR status in GitHub

3. **Hugging Face Hub Integration**
   - Tool: Detects LLM/dataset changes
   - Resource: Reads Hub guidelines
   - Prompt: Generates model card updates
   - Tool: Validates against Hub standards

4. **Team Notification**
   - Tool: Identifies relevant team members
   - Resource: Reads notification preferences
   - Prompt: Formats appropriate message
   - Tool: Sends via Slack channels

5. **Follow-up Actions**
   - Prompt: "Create Follow-up Tasks" generates next steps
   - Tool: Creates GitHub issues if needed
   - Resource: Links to documentation
   - All primitives work together seamlessly

## Testing Strategy

### Unit Tests
Each module includes comprehensive unit tests:
- Tool schema validation
- Resource URI parsing
- Prompt template rendering
- Integration scenarios

### Integration Tests
End-to-end tests cover:
- Complete PR workflow
- Error recovery scenarios
- Performance under load
- Security validation

### Test Structure
```
tests/
├── unit/
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_prompts.py
│   └── test_integration.py
├── integration/
│   ├── test_workflow.py
│   ├── test_webhooks.py
│   └── test_notifications.py
└── fixtures/
    ├── sample_events.json
    └── mock_responses.json
```

## Running the Solution

### Local Development Setup
1. **Start the MCP server**: `python server.py`
2. **Configure Claude Code**: Add server to MCP settings
3. **Set up Cloudflare Tunnel**: `cloudflared tunnel --url http://localhost:3000`
4. **Configure webhooks**: Add tunnel URL to GitHub repository
5. **Test the workflow**: Create a PR and watch the automation

### Configuration
Simple file-based configuration for easy setup:
- GitHub tokens in `.env` file
- Slack webhooks in config
- Template customization in `templates/`
- All settings in one place

## Common Patterns and Best Practices

### Tool Design
- Keep tools focused and single-purpose
- Return structured data for AI interpretation
- Include comprehensive error messages
- Version your tool schemas

### Resource Organization
- Use clear URI hierarchies
- Implement resource discovery
- Cache frequently accessed resources
- Version control all resources

### Prompt Engineering
- Make prompts specific but flexible
- Include context and examples
- Test with various inputs
- Maintain prompt libraries

### Integration Patterns
- Use events for loose coupling
- Implement circuit breakers
- Add retries with backoff
- Monitor all external calls

## Troubleshooting Guide

### Common Issues

1. **Webhook not receiving events**
   - Check Cloudflare Tunnel is running
   - Verify GitHub webhook configuration
   - Confirm secret matches

2. **Tools not appearing in Claude**
   - Validate tool schemas
   - Check server registration
   - Review MCP connection

3. **Resources not accessible**
   - Verify file permissions
   - Check URI formatting
   - Confirm resource registration

4. **Prompts producing inconsistent results**
   - Review prompt templates
   - Check context provided
   - Validate input formatting

## Next Steps and Extensions

### Potential Enhancements
1. Add more code analysis tools (complexity, security)
2. Integrate with more communication platforms
3. Add custom workflow definitions
4. Implement PR auto-merge capabilities

### Learning Path
- **Next**: Unit 4 - Deploy this server remotely
- **Advanced**: Custom MCP protocol extensions
- **Expert**: Multi-server orchestration

## Conclusion

This PR Agent demonstrates the power of MCP's three primitives working together. Tools provide capabilities, Resources offer context, and Prompts ensure consistency. Combined, they create an intelligent automation system that enhances developer productivity while maintaining team standards.

The modular architecture ensures each component can be understood, tested, and extended independently, while the integration showcases real-world patterns you'll use in production MCP servers.