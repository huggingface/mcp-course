"""
Launches the Weather Agent and Activity Planner Agent as subprocesses and
waits for both to come up. Shared by run_demo.py and gradio_app.py so there's
one place that knows how these two agents are started and stopped.
"""

from __future__ import annotations

import asyncio
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import httpx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEATHER_AGENT_URL = "http://localhost:8001"
ACTIVITY_AGENT_URL = "http://localhost:8002"


@dataclass
class RunningAgents:
    weather_proc: subprocess.Popen
    activity_proc: subprocess.Popen


def _start(script: str, args: list[str]) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, str(PROJECT_ROOT / script), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


async def _wait_until_up(url: str, timeout: float = 20.0) -> None:
    deadline = time.monotonic() + timeout
    async with httpx.AsyncClient() as client:
        while time.monotonic() < deadline:
            try:
                resp = await client.get(f"{url}/.well-known/agent.json", timeout=2.0)
                if resp.status_code == 200:
                    return
            except httpx.HTTPError:
                pass
            await asyncio.sleep(0.5)
    raise TimeoutError(f"{url} did not come up within {timeout}s")


async def start_agents() -> RunningAgents:
    """Start both agents and block until they're both accepting requests."""
    weather_proc = _start("weather_agent/agent.py", ["--port", "8001"])
    activity_proc = _start(
        "activity_agent/agent.py",
        ["--port", "8002", "--weather-agent-url", WEATHER_AGENT_URL],
    )
    await _wait_until_up(WEATHER_AGENT_URL)
    await _wait_until_up(ACTIVITY_AGENT_URL)
    return RunningAgents(weather_proc=weather_proc, activity_proc=activity_proc)


def stop_agents(agents: RunningAgents) -> None:
    """Terminate both agent processes, surfacing their logs if either crashed."""
    procs = (agents.weather_proc, agents.activity_proc)
    for proc in procs:
        proc.terminate()
    for proc in procs:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    for name, proc in (("weather_agent", agents.weather_proc), ("activity_agent", agents.activity_proc)):
        if proc.returncode not in (0, None, -15):
            print(f"--- {name} output ---")
            if proc.stdout:
                print(proc.stdout.read())
