"""
Tiny helper for talking to a local MCP server over stdio.

Each agent in this demo owns exactly one MCP server (started as a subprocess)
and uses this helper to call its tools. This keeps the "agent" layer (A2A,
orchestration, deciding which tool to call) separate from the "tool" layer
(MCP server, actually doing the work).
"""

from __future__ import annotations

import os
import sys
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@asynccontextmanager
async def mcp_session(server_script: str) -> AsyncIterator[ClientSession]:
    """Start `server_script` as a subprocess and yield an initialized MCP session.

    The MCP SDK does not forward the parent process's environment to the
    subprocess by default (only a small safe allowlist like PATH/HOME) - a
    sane default when the server is untrusted third-party code. Here the
    "server" is our own mcp_server.py in the same repo, so we pass the full
    environment through explicitly; otherwise things like XWEATHER_CLIENT_ID
    loaded from .env would never reach it.
    """
    params = StdioServerParameters(command=sys.executable, args=[server_script], env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


def _drop_session(inputs: dict[str, Any]) -> dict[str, Any]:
    """`session` isn't JSON-serializable and isn't useful in a trace anyway."""
    return {k: v for k, v in inputs.items() if k != "session"}


@traceable(run_type="tool", process_inputs=_drop_session)
async def call_tool(session: ClientSession, tool_name: str, arguments: dict[str, Any]) -> str:
    """Call an MCP tool (traced) and return its text content."""
    if run_tree := get_current_run_tree():
        run_tree.name = f"mcp::{tool_name}"

    result = await session.call_tool(tool_name, arguments=arguments)
    if result.isError:
        raise RuntimeError(f"MCP tool '{tool_name}' failed: {result.content}")
    return "\n".join(
        block.text for block in result.content if getattr(block, "type", None) == "text"
    )
