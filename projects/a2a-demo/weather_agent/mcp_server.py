#!/usr/bin/env python3
"""
Weather MCP Server

Exposes weather-lookup tools backed by the XWeather API
(https://www.xweather.com/docs/weather-api) when credentials are configured:

    export XWEATHER_CLIENT_ID=...
    export XWEATHER_CLIENT_SECRET=...

Without credentials, tools fall back to a deterministic mock generated from
(location, date) so the rest of the demo (agents, notebook, run_demo.py)
keeps working offline with no signup required. Every response is tagged
with `"source": "xweather"` or `"source": "mock"` so callers can tell which
one they got.
"""

import hashlib
import json
import os
from datetime import date, timedelta

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")

XWEATHER_BASE_URL = "https://data.api.xweather.com"
CONDITIONS = ["sunny", "cloudy", "rainy", "stormy", "snowy", "windy"]


def _xweather_credentials() -> tuple[str, str] | None:
    client_id = os.environ.get("XWEATHER_CLIENT_ID")
    client_secret = os.environ.get("XWEATHER_CLIENT_SECRET")
    if client_id and client_secret:
        return client_id, client_secret
    return None


def _mock_weather(location: str, on_date: str) -> dict:
    """Deterministic pseudo-random weather for (location, date), no network calls."""
    seed = f"{location.strip().lower()}|{on_date}"
    digest = hashlib.sha256(seed.encode()).hexdigest()
    seed_int = int(digest[:8], 16)

    condition = CONDITIONS[seed_int % len(CONDITIONS)]
    temperature_c = 5 + (seed_int // len(CONDITIONS)) % 30  # 5..34 C
    humidity_pct = 30 + (seed_int // 1000) % 60             # 30..89 %
    wind_kph = (seed_int // 100) % 45                       # 0..44 kph

    return {
        "location": location,
        "date": on_date,
        "condition": condition,
        "temperature_c": temperature_c,
        "humidity_pct": humidity_pct,
        "wind_kph": wind_kph,
        "source": "mock",
    }


async def _xweather_get(path: str, location: str, params: dict | None = None) -> dict:
    client_id, client_secret = _xweather_credentials()  # type: ignore[misc]
    query = {"client_id": client_id, "client_secret": client_secret, **(params or {})}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{XWEATHER_BASE_URL}/{path}/{location}", params=query)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        message = (data.get("error") or {}).get("description", "unknown XWeather error")
        raise RuntimeError(f"XWeather API error: {message}")
    return data["response"]


def _first_periods(response: dict | list) -> list[dict]:
    """XWeather wraps `periods` in a list of location matches, e.g.
    `[{"loc": ..., "place": ..., "periods": [...]}]` - unwrap the first match."""
    if isinstance(response, list):
        if not response:
            raise RuntimeError("XWeather returned no location matches")
        return response[0]["periods"]
    return response["periods"]


async def _fetch_current(location: str) -> dict:
    """Fetch current conditions from XWeather's /conditions endpoint.

    Uses /conditions (globally interpolated) rather than /observations (real
    station data only) - /observations has essentially no coverage outside
    US airports, e.g. Paris,FR resolves but returns no data.
    """
    response = await _xweather_get("conditions", location)
    period = _first_periods(response)[0]
    return {
        "location": location,
        "date": (period.get("dateTimeISO") or date.today().isoformat())[:10],
        "condition": period.get("weather", "unknown"),
        "temperature_c": period.get("tempC"),
        "humidity_pct": period.get("humidity"),
        "wind_kph": period.get("windSpeedKPH"),
        "source": "xweather",
    }


async def _fetch_forecast(location: str, days_ahead: int) -> dict:
    """Fetch a daily forecast period from XWeather's /forecasts endpoint."""
    response = await _xweather_get("forecasts", location, params={"filter": "day"})
    periods = _first_periods(response)
    index = max(0, min(days_ahead, len(periods) - 1))
    period = periods[index]
    return {
        "location": location,
        "date": (period.get("dateTimeISO") or "")[:10],
        "condition": period.get("weather", "unknown"),
        "temperature_c": period.get("maxTempC"),
        "humidity_pct": period.get("maxHumidity"),
        "wind_kph": period.get("windSpeedKPH"),
        "source": "xweather",
    }


@mcp.tool()
async def get_current_weather(location: str) -> str:
    """Get the current weather conditions for a location.

    Args:
        location: City name. For real (non-mock) results, qualify ambiguous
            city names with a state/country, e.g. "Paris,FR" or "New York,NY" -
            XWeather's geocoder can't otherwise tell which "Paris" you mean.
    """
    if _xweather_credentials():
        try:
            return json.dumps(await _fetch_current(location), indent=2)
        except (httpx.HTTPError, RuntimeError, KeyError) as exc:
            result = _mock_weather(location, date.today().isoformat())
            result["source"] = "mock"
            result["fallback_reason"] = f"XWeather request failed: {exc}"
            return json.dumps(result, indent=2)

    return json.dumps(_mock_weather(location, date.today().isoformat()), indent=2)


@mcp.tool()
async def get_forecast(location: str, days_ahead: int = 1) -> str:
    """Get a weather forecast for a location N days from today.

    Args:
        location: City name. For real (non-mock) results, qualify ambiguous
            city names with a state/country, e.g. "Paris,FR" or "New York,NY".
        days_ahead: How many days from today to forecast (0 = today, default 1)
    """
    if _xweather_credentials():
        try:
            return json.dumps(await _fetch_forecast(location, days_ahead), indent=2)
        except (httpx.HTTPError, RuntimeError, KeyError) as exc:
            target_date = (date.today() + timedelta(days=days_ahead)).isoformat()
            result = _mock_weather(location, target_date)
            result["source"] = "mock"
            result["fallback_reason"] = f"XWeather request failed: {exc}"
            return json.dumps(result, indent=2)

    target_date = (date.today() + timedelta(days=days_ahead)).isoformat()
    return json.dumps(_mock_weather(location, target_date), indent=2)


if __name__ == "__main__":
    mcp.run()
