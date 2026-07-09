"""
LangSmith tracing.

Set these in .env to enable (see .env.example):
    LANGSMITH_TRACING=true
    LANGSMITH_API_KEY=...
    LANGSMITH_PROJECT=a2a-demo          # optional, defaults to "default"

When unset, every @traceable call in this project is a no-op - LangSmith's
SDK checks LANGSMITH_TRACING itself, so nothing here needs to branch on it.
The demo runs identically either way, just without traces being uploaded.

What gets traced:
    - MCP tool calls (common/mcp_client.py::call_tool) - tool name, args,
      result, latency.
    - A2A protocol calls (common/a2a_protocol.py::A2AClient) - agent
      discovery (get_agent_card) and message/send, both client- and
      server-side, stitched into one trace across the two agent processes
      via LangSmith's distributed-tracing headers (see build_a2a_app's
      TracingMiddleware and A2AClient's get_current_run_tree().to_headers()).
    - Each agent's top-level request handler, as the root/parent span.

What does NOT get traced: token usage. LangSmith only reports token counts
for `run_type="llm"` spans, and neither agent calls an LLM - both use
regex-based parsing for their "brain" by design, so this demo needs no LLM
API key on top of XWeather + LangSmith. Expect an empty token count in
every trace; that's correct, not a bug.
"""

import os


def tracing_status() -> str:
    """Human-readable one-liner for agent startup logs."""
    enabled = (
        bool(os.environ.get("LANGSMITH_API_KEY"))
        and os.environ.get("LANGSMITH_TRACING", "").lower() == "true"
    )
    if enabled:
        project = os.environ.get("LANGSMITH_PROJECT", "default")
        return f"LangSmith tracing: ON (project='{project}')"
    return "LangSmith tracing: OFF (set LANGSMITH_TRACING=true and LANGSMITH_API_KEY in .env to enable)"
