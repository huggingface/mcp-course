#!/usr/bin/env python3
"""
End-to-end demo: launches the Weather Agent and Activity Planner Agent as
separate processes (each with its own internal MCP server), waits for both
to come up, then sends a few sample A2A requests to the Activity Planner
and prints the full agent-to-agent exchange.

Run with:
    uv run python run_demo.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common.env  # noqa: E402,F401 - loads .env as an import side effect
from common.a2a_protocol import A2AClient  # noqa: E402
from common.agent_launcher import ACTIVITY_AGENT_URL, WEATHER_AGENT_URL, start_agents, stop_agents  # noqa: E402
from common.tracing import tracing_status  # noqa: E402

SAMPLE_QUERIES = [
    "What should we do in Paris, FR today?",
    "Plan something fun in New York, NY.",
    "What can we do in Tokyo, JP today?",
]


async def main() -> None:
    print(tracing_status())
    print("Starting Weather Agent on :8001 and Activity Planner Agent on :8002 ...")
    agents = await start_agents()

    try:
        print("Both agents are up.\n")

        weather_client = A2AClient(WEATHER_AGENT_URL)
        activity_client = A2AClient(ACTIVITY_AGENT_URL)

        weather_card = await weather_client.get_agent_card()
        activity_card = await activity_client.get_agent_card()
        print(f"Discovered agent: {weather_card.name} - {weather_card.description}")
        print(f"Discovered agent: {activity_card.name} - {activity_card.description}\n")

        for query in SAMPLE_QUERIES:
            print(f"USER -> Activity Planner Agent: {query}")
            reply = await activity_client.send_message(query)
            print(f"Activity Planner Agent -> USER: {reply}\n")

        await weather_client.aclose()
        await activity_client.aclose()

    finally:
        print("Shutting down agents...")
        stop_agents(agents)


if __name__ == "__main__":
    asyncio.run(main())
