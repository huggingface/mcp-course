# Unit 3 Implementation Plan: Advanced MCP Development

## Overview
This document outlines the implementation plan for Unit 3: Building Custom Workflow Servers for Claude Code. This unit bridges the gap between basic MCP concepts (Units 1-2) and production deployment (Unit 4).

## Core Philosophy: Local "Toy" to Production Pipeline

**Unit 3**: Build it locally, see it work (focus on workflow logic)
**Unit 4**: Ship it to production (add auth, deploy globally, handle real traffic)

## Module Structure: Jump-in Anywhere Design

Each module provides complete working solutions that serve as starting points for subsequent modules, allowing learners to begin at any point in the unit.

### Module 1: Basic Workflow Server (30 min)
**Learning Goal**: "I want Claude Code to help me create better PRs"

**What Learners Build**:
- Minimal MCP server with PR template suggestion
- Simple rule-based template selection (file extension → template type)
- Working Claude Code integration

**Starter Code**: Empty MCP template
**End State**: Working PR template suggester
**For Unit 4**: Perfect base for Cloudflare Workers deployment

**Key Files**:
```
/examples/unit3-module1-solution/
├── server.py (or server.js)
├── mcp_config.json
└── templates/
    ├── bug.md
    ├── feature.md
    └── docs.md
```

### Module 2: Smart File Analysis (45 min)
**Learning Goal**: "Make template selection actually intelligent"

**What Learners Build**:
- Context-aware file analysis (not just extensions)
- Pattern matching logic (tests → test template, config → ops template)
- Multi-file change analysis

**Starter Code**: Module 1 solution
**End State**: Intelligent template selection
**For Unit 4**: Core logic ready for remote deployment

**New Concepts**:
- File content analysis
- Pattern recognition
- Business logic separation

### Module 3: GitHub Actions Integration (45 min)
**Learning Goal**: "Tell me when my tests pass/fail"

**What Learners Build**:
- Local webhook receiver using Cloudflare Tunnel
- GitHub Actions event parsing
- Real-time CI/CD status in Claude Code

**Starter Code**: Module 2 solution
**End State**: Live CI/CD monitoring
**For Unit 4**: Key feature that benefits from remote hosting

**Technology Choice**: Cloudflare Tunnel (not ngrok)
- **Why**: Seamless Unit 4 transition, better security, preview-optimized
- **Bonus**: Uses Cloudflare preview feature for instant public URLs
- **Educational**: Builds familiarity with Cloudflare ecosystem

### Module 4: Team Communication (30 min)
**Learning Goal**: "Update my team automatically"

**What Learners Build**:
- Slack webhook integration for notifications
- Smart message formatting based on CI results
- Fallback options for free-tier users (console/file output)

**Starter Code**: Module 3 solution
**End State**: Complete workflow automation
**For Unit 4**: Ready for OAuth-protected remote deployment

### Module 5: Polish & Claude Code Integration (30 min)
**Learning Goal**: "Make it production-ready (locally)"

**What Learners Build**:
- Error handling and logging
- Configuration management
- Complete Claude Code workflow demonstration

**Starter Code**: Module 4 solution
**End State**: Unit 4-ready codebase
**For Unit 4**: Seamless transition to remote deployment

## Unit 3 → Unit 4 Transition Strategy

### Shared Codebase Approach
- Unit 3 final solution becomes Unit 4 starter template
- Same workflow logic, different deployment model
- Learners see immediate value of productionizing their work

### Knowledge Bridge
| Unit 3 (Local) | Unit 4 (Production) |
|----------------|-------------------|
| Local MCP server | Cloudflare Workers deployment |
| Cloudflare Tunnel | Native Cloudflare hosting |
| File-based config | Environment variables |
| Development webhooks | Production webhook security |
| Direct Claude Code connection | `mcp-remote` client adapter |

### Natural Progression Points
1. **Security**: "My webhook is public, how do I protect it?" → OAuth
2. **Reliability**: "What if my laptop is off?" → Remote hosting
3. **Scale**: "What about multiple team members?" → Shared deployment
4. **Maintenance**: "How do I update this?" → CI/CD deployment

## Repository Structure

```
/examples/
├── unit3-module1-solution/    # Basic workflow server
├── unit3-module2-solution/    # Smart file analysis
├── unit3-module3-solution/    # GitHub Actions integration
├── unit3-module4-solution/    # Team communication
├── unit3-final-solution/      # Complete local server
└── unit4-starter/             # Unit 3 final → Unit 4 starting point
```

## Free-Tier Compatibility

### Core Features (Always Free)
- Local MCP server development
- Cloudflare Tunnel for webhooks
- Basic GitHub Actions integration
- File-based team notifications

### Upgrade Paths
- Slack integration (free Slack workspaces)
- Enhanced GitHub Actions (public repos)
- Advanced notifications (email fallbacks)

### Unit 4 Preparation
- All Unit 3 code runs on Cloudflare free tier
- No premium services required for core functionality
- Optional features clearly marked

## Interactive Learning Elements

### Quiz Contribution Areas for @burtenshaw

#### Module 1 Quizzes: MCP Server Fundamentals
**Focus Areas**:
- MCP protocol understanding
- Client-server communication patterns
- Tool registration and discovery
- Configuration management

**Sample Question Types**:
- "Which MCP method is used for tool discovery?"
- "How does Claude Code connect to MCP servers?"
- "What's the difference between tools and resources in MCP?"

#### Module 2 Quizzes: Logic & Pattern Recognition
**Focus Areas**:
- File analysis strategies
- Business logic separation
- Pattern matching concepts
- Error handling in analysis

**Sample Question Types**:
- "How would you detect if a change is test-related?"
- "What file patterns indicate a configuration change?"
- "When should template selection fallback to defaults?"

#### Module 3 Quizzes: Integration & Webhooks
**Focus Areas**:
- Webhook security concepts
- GitHub Actions event types
- Network tunneling basics
- Event-driven architecture

**Sample Question Types**:
- "What GitHub Actions events trigger on PR completion?"
- "How does Cloudflare Tunnel maintain security?"
- "What's the difference between push and workflow_run events?"

#### Module 4 Quizzes: Team Workflows
**Focus Areas**:
- Team communication patterns
- Notification strategies
- Fallback mechanisms
- Workflow integration

**Sample Question Types**:
- "When should automated notifications be sent?"
- "How do you handle notification failures?"
- "What information is most valuable in CI/CD alerts?"

#### Module 5 Quizzes: Production Readiness
**Focus Areas**:
- Error handling strategies
- Configuration management
- Monitoring and debugging
- Performance considerations

**Sample Question Types**:
- "What configuration should never be hardcoded?"
- "How do you debug MCP server connectivity issues?"
- "What logs are essential for troubleshooting?"

#### Unit 3 → Unit 4 Bridge Quiz
**Focus Areas**:
- Local vs remote deployment trade-offs
- Security model differences
- Scalability considerations
- DevOps pipeline concepts

**Sample Question Types**:
- "Why might you choose remote deployment over local?"
- "What security concerns arise with public webhook endpoints?"
- "How does team collaboration change with remote servers?"

### Hands-On Exercises
- **Module Checkpoints**: "Quick Check" after each module
- **Integration Tests**: End-to-end workflow verification
- **Customization Challenges**: "Adapt this for your team's workflow"
- **Troubleshooting Labs**: Common problems and solutions

## Implementation Timeline

### Week 1: Foundation
- Module 1: Basic workflow server
- Module 2: Smart file analysis
- Create starter code templates

### Week 2: Integration
- Module 3: GitHub Actions + Cloudflare Tunnel
- Module 4: Team communication
- End-to-end testing

### Week 3: Polish
- Module 5: Production readiness
- Unit 4 transition preparation
- Interactive elements and quizzes

### Week 4: Review & Refinement
- Team feedback integration
- Documentation polish
- Community preview

## Success Metrics

### Learning Outcomes
- Learners can build production-ready MCP servers locally
- Understanding of workflow automation concepts
- Confidence to tackle Unit 4 remote deployment
- Practical skills applicable to real development teams

### Technical Deliverables
- 5 complete working code examples
- Seamless Unit 4 transition codebase
- Comprehensive troubleshooting documentation
- Interactive assessment materials

## Next Steps

1. **Team Review**: Gather feedback on this plan
2. **Quiz Development**: Collaborate with @burtenshaw on assessment design
3. **Module 1 Implementation**: Start with basic workflow server
4. **Iterative Development**: Build and test each module sequentially

## Questions for Team Discussion

1. **Scope**: Is the 3-hour total time commitment appropriate?
2. **Technology**: Any concerns about Cloudflare Tunnel?
3. **Modularity**: Does the jump-in-anywhere approach work for our audience?
4. **Unit 4 Bridge**: Is the transition strategy clear and compelling?
5. **Free Tier**: Any features that might require paid services?

---

*This plan emphasizes practical, hands-on learning that prepares students for real-world MCP server development while maintaining a clear path to production deployment in Unit 4.*