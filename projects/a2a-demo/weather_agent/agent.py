#!/usr/bin/env python3
"""
Weather Agent -- an A2A server backed by an internal Weather MCP server.

Architecture:

    (A2A request) --> Weather Agent (this file) --> MCP client --stdio--> weather_agent/mcp_server.py

The agent's "brain" is intentionally simple (regex parsing, no LLM) so the
demo has zero external API dependencies and runs fully offline. Swap
`handle_message` for an LLM-driven tool-calling loop and the MCP + A2A
plumbing around it doesn't need to change.
"""

import argparse
import json
import re
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from langsmith import traceable

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import common.env  # noqa: E402,F401 - loads .env as an import side effect
from common.a2a_protocol import AgentCard, AgentSkill, HandlerBox, build_a2a_app  # noqa: E402
from common.mcp_client import call_tool, mcp_session  # noqa: E402
from common.tracing import tracing_status  # noqa: E402

MCP_SERVER_SCRIPT = str(Path(__file__).resolve().parent / "mcp_server.py")

DAYS_AHEAD_WORDS = {"today": 0, "tomorrow": 1, "day after tomorrow": 2}


def _parse_request(text: str) -> tuple[str, int]:
    """Extract (location, days_ahead) from a free-text weather request."""
    lowered = text.lower()

    days_ahead = 0
    for phrase, n in DAYS_AHEAD_WORDS.items():
        if phrase in lowered:
            days_ahead = n
            break
    else:
        match = re.search(r"in (\d+) days?", lowered)
        if match:
            days_ahead = int(match.group(1))

    # Location may be "City" or "City, ST"/"City, Country" - real weather APIs
    # need that qualifier to disambiguate (there are many towns named "Paris").
    location_match = re.search(
        r"(?:weather|forecast)?\s*\b(?:in|for|at)\b\s+"
        r"([a-zA-Z]+(?:\s+[a-zA-Z]+)*(?:,\s*[a-zA-Z]+)?)"
        r"(?=\s*(?:\?|$|,|\.|\btoday\b|\btomorrow\b|\bin\s+\d+\s+days?\b))",
        text,
        re.IGNORECASE,
    )
    location = location_match.group(1).strip() if location_match else text.strip()
    return location, days_ahead


def make_handler(session):
    @traceable(run_type="chain", name="weather_agent.handle_message")
    async def handle_message(text: str) -> str:
        location, days_ahead = _parse_request(text)
        if days_ahead == 0:
            raw = await call_tool(session, "get_current_weather", {"location": location})
        else:
            raw = await call_tool(
                session, "get_forecast", {"location": location, "days_ahead": days_ahead}
            )
        data = json.loads(raw)
        temperature_c = data.get("temperature_c")
        humidity_pct = data.get("humidity_pct")
        wind_kph = data.get("wind_kph")
        return (
            f"Weather for {data['location']} on {data['date']}: {data['condition']}, "
            f"{temperature_c if temperature_c is not None else 0:.1f}C, "
            f"humidity {humidity_pct if humidity_pct is not None else 0:.0f}%, "
            f"wind {wind_kph if wind_kph is not None else 0:.1f} kph. "
            f"(source: {data.get('source', 'mock')})"
        )

    return handle_message


def build_app() -> FastAPI:
    card = AgentCard(
        name="Weather Agent",
        description="Reports current weather and short-range forecasts for a city.",
        url="http://localhost:8001",
        skills=[
            AgentSkill(
                id="get_weather",
                name="Get weather",
                description="Get current or forecast weather for a location, e.g. "
                "'weather in Paris' or 'forecast for Tokyo tomorrow'.",
                tags=["weather", "forecast"],
            )
        ],
    )

    handler_box = HandlerBox()
    app = build_a2a_app(card, handler_box)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        async with mcp_session(MCP_SERVER_SCRIPT) as session:
            handler_box.handler = make_handler(session)
            yield

    app.router.lifespan_context = lifespan
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()
    print(tracing_status())
    uvicorn.run(build_app(), host="127.0.0.1", port=args.port)
