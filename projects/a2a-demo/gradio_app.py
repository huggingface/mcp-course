#!/usr/bin/env python3
"""
Gradio chat frontend for the Activity Planner Agent.

Starts both agents as subprocesses (same as run_demo.py), then serves a chat
UI where each message is sent to the Activity Planner Agent over A2A. Behind
the scenes that agent calls the Weather Agent over A2A and its own MCP
server - see README.md for the architecture diagram.

Run with:
    uv run python gradio_app.py

If LANGSMITH_TRACING=true and LANGSMITH_API_KEY are set in .env, every
request's full call tree (A2A discovery + message/send, MCP tool calls,
latency at each step) is visible in your LangSmith project - see
common/tracing.py for what is and isn't traced.
"""

import asyncio
import atexit
import signal
import sys
from pathlib import Path

import gradio as gr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common.env  # noqa: E402,F401 - loads .env as an import side effect
from common.a2a_protocol import A2AClient  # noqa: E402
from common.agent_launcher import ACTIVITY_AGENT_URL, start_agents, stop_agents  # noqa: E402
from common.tracing import tracing_status  # noqa: E402

_activity_client: A2AClient | None = None


async def respond(message: str, history: list) -> str:
    assert _activity_client is not None, "agents not started yet"
    try:
        return await _activity_client.send_message(message)
    except Exception as exc:  # noqa: BLE001 - surface any A2A/MCP failure in the chat itself
        return f"Something went wrong talking to the agents: {exc}"


def main() -> None:
    print(tracing_status())
    print("Starting Weather Agent and Activity Planner Agent...")
    agents = asyncio.run(start_agents())
    atexit.register(stop_agents, agents)
    # atexit alone only fires on normal interpreter shutdown (e.g. Ctrl+C,
    # which gr.ChatInterface.launch() turns into a clean exit) - SIGTERM
    # bypasses it by default, which would orphan the two agent subprocesses.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    print("Both agents are up.")

    global _activity_client
    _activity_client = A2AClient(ACTIVITY_AGENT_URL)

    demo = gr.ChatInterface(
        fn=respond,
        title="Activity Planner Agent",
        description=(
            "Ask what to do in a city today, e.g. *\"what should we do in Paris, FR today?\"*. "
            "This chat talks to the Activity Planner Agent over A2A, which itself calls the "
            "Weather Agent over A2A and its own MCP tools to build a weather-aware suggestion. "
            "Qualify ambiguous city names with a state/country (\"New York, NY\") for real "
            "weather data - see README.md for details."
        ),
        examples=[
            "What should we do in Paris, FR today?",
            "Plan something fun in New York, NY.",
            "What can we do in Tokyo, JP tomorrow?",
        ],
    )
    demo.launch()


if __name__ == "__main__":
    main()
