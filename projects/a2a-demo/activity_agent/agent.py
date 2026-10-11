#!/usr/bin/env python3
"""
Activity Planner Agent -- an A2A server that orchestrates a second agent.

This is the interesting one: to plan an activity it needs the weather, but
it doesn't know how to look that up itself. So it acts as an A2A *client* to
the Weather Agent (agent-to-agent communication over HTTP + JSON-RPC), and
as an MCP *client* to its own internal Activity MCP server (tool calls over
stdio) to turn "sunny, 22C" into a concrete suggestion.

    (A2A request)
        |
        v
    Activity Agent (this file)
        |-- A2A client --> Weather Agent  (http://localhost:8001)
        |-- MCP client --> activity_agent/mcp_server.py (stdio)
        v
    (A2A response: weather-aware activity plan)
"""

import argparse
import json
import re
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from langsmith import traceable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import common.env  # noqa: E402,F401 - loads .env as an import side effect
from common.a2a_protocol import A2AClient, AgentCard, AgentSkill, HandlerBox, build_a2a_app  # noqa: E402
from common.mcp_client import call_tool, mcp_session  # noqa: E402
from common.tracing import tracing_status  # noqa: E402

MCP_SERVER_SCRIPT = str(Path(__file__).resolve().parent / "mcp_server.py")

# Matches the Weather Agent's reply format, e.g.
# "Weather for Paris on 2026-07-08: Mostly Cloudy, 22.5C, humidity 54%, wind 12.0 kph."
# Condition may be multi-word (real APIs return phrases like "Mostly Cloudy"),
# and temperature/wind may be decimals (real APIs rarely round to whole degrees).
WEATHER_REPLY_RE = re.compile(
    r"([a-zA-Z][a-zA-Z\s\-]*?),\s*(-?\d+(?:\.\d+)?)C.*?wind\s+(-?\d+(?:\.\d+)?)\s*kph",
    re.IGNORECASE,
)


def _extract_location(text: str) -> str:
    # Location may be "City" or "City, ST"/"City, Country" - preserve that
    # qualifier so it survives the trip to the Weather Agent unmangled.
    match = re.search(
        r"\b(?:in|for|at)\b\s+"
        r"([a-zA-Z]+(?:\s+[a-zA-Z]+)*(?:,\s*[a-zA-Z]+)?)"
        r"(?=\s*(?:\?|$|,|\.|\btoday\b|\btomorrow\b))",
        text,
        re.IGNORECASE,
    )
    return match.group(1).strip() if match else text.strip()


def make_handler(mcp_session_obj, weather_client: A2AClient):
    @traceable(run_type="chain", name="activity_agent.handle_message")
    async def handle_message(text: str) -> str:
        location = _extract_location(text)

        weather_reply = await weather_client.send_message(f"What's the weather in {location}?")
        match = WEATHER_REPLY_RE.search(weather_reply)
        if not match:
            return f"Couldn't understand the weather report for {location}: '{weather_reply}'"

        condition, temperature_c, wind_kph = match.group(1), float(match.group(2)), float(match.group(3))

        raw = await call_tool(
            mcp_session_obj,
            "recommend_activity",
            {"condition": condition, "temperature_c": temperature_c, "wind_kph": wind_kph},
        )
        plan = json.loads(raw)
        # "about Xh" rather than "~Xh" - a bare tilde is Markdown strikethrough
        # syntax, and this text gets rendered as Markdown by the Gradio frontend.
        suggestions = "; ".join(
            f"{s['name']} (about {s['duration_hr']}h, tip: {s['tip']})" for s in plan["suggestions"]
        )

        source_match = re.search(r"\(source:\s*(\w+)\)", weather_reply)
        source = source_match.group(1) if source_match else "mock"
        weather_summary = re.split(r"\s*\(source:.*?\)\.?\s*$", weather_reply.split(":", 1)[1].strip())[0]

        return (
            f"For {location} ({weather_summary.rstrip('.')}): "
            f"{plan['reason']} Suggestions -> {suggestions} [weather data: {source}]"
        )

    return handle_message


def build_app(weather_agent_url: str) -> FastAPI:
    card = AgentCard(
        name="Activity Planner Agent",
        description="Plans indoor, picnic, or outdoor activities based on the weather "
        "in a given city. Delegates weather lookups to the Weather Agent over A2A.",
        url="http://localhost:8002",
        skills=[
            AgentSkill(
                id="plan_activity",
                name="Plan activity",
                description="Suggest an activity for a city, weather-aware, e.g. "
                "'what should we do in Paris today?'",
                tags=["activity", "planning", "outdoor", "picnic", "indoor"],
            )
        ],
    )

    handler_box = HandlerBox()
    app = build_a2a_app(card, handler_box)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        weather_client = A2AClient(weather_agent_url)
        async with mcp_session(MCP_SERVER_SCRIPT) as session:
            handler_box.handler = make_handler(session, weather_client)
            try:
                yield
            finally:
                await weather_client.aclose()

    app.router.lifespan_context = lifespan
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8002)
    parser.add_argument("--weather-agent-url", default="http://localhost:8001")
    args = parser.parse_args()
    print(tracing_status())
    uvicorn.run(build_app(args.weather_agent_url), host="127.0.0.1", port=args.port)
