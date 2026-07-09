#!/usr/bin/env python3
"""
Outdoor Activity Planning MCP Server (toy)

A minimal MCP server exposing activity-suggestion tools: indoor play,
picnics, and outdoor adventures. Each tool returns a small curated list plus
packing/prep tips. `recommend_activity` is the "smart" tool: given a weather
condition and temperature it picks the right category automatically, which
is what the Activity Planner Agent calls after it learns the weather.
"""

import json
import random

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("activity-server")

INDOOR_ACTIVITIES = [
    {"name": "Board game cafe", "duration_hr": 2, "tip": "Book a table ahead on weekends."},
    {"name": "Museum or art gallery", "duration_hr": 3, "tip": "Check for free-entry days."},
    {"name": "Indoor climbing gym", "duration_hr": 2, "tip": "Rent shoes and a harness on site."},
    {"name": "Movie marathon at home", "duration_hr": 4, "tip": "Stock up on snacks first."},
    {"name": "Cooking or baking class", "duration_hr": 2, "tip": "Great for groups of 2-6."},
]

PICNIC_SPOTS = [
    {"name": "Riverside park", "duration_hr": 2, "tip": "Bring a blanket, arrive before noon for shade."},
    {"name": "Botanical garden lawn", "duration_hr": 2, "tip": "Check garden opening hours."},
    {"name": "Hilltop viewpoint", "duration_hr": 2, "tip": "Pack a windbreaker, it's breezy up there."},
    {"name": "Lakeside deck", "duration_hr": 3, "tip": "Mosquito repellent recommended at dusk."},
]

OUTDOOR_ACTIVITIES = [
    {"name": "Hiking trail", "duration_hr": 3, "tip": "Carry at least 1L of water per person."},
    {"name": "Cycling loop", "duration_hr": 2, "tip": "Check tire pressure before you set off."},
    {"name": "Kayaking", "duration_hr": 2, "tip": "Life jackets are usually available for rent."},
    {"name": "City walking tour", "duration_hr": 2, "tip": "Wear comfortable shoes."},
    {"name": "Open-air sports (football/frisbee)", "duration_hr": 1, "tip": "Grab a group of 4+ for the best time."},
]

# Keyword-based (not exact-match) so this works whether `condition` came from
# the mock's fixed vocabulary ("rainy", "cloudy"...) or a real weather API's
# free-text phrases ("Thunderstorms", "Mostly Cloudy", "Rain Likely"...).
BAD_OUTDOOR_KEYWORDS = ("rain", "storm", "thunder", "snow", "sleet", "hail", "fog")
MILD_KEYWORDS = ("clear", "sun", "fair", "cloud", "overcast")


def _pick(options: list[dict], n: int = 2) -> list[dict]:
    return random.sample(options, k=min(n, len(options)))


@mcp.tool()
async def suggest_indoor_activity() -> str:
    """Suggest indoor activities, useful for bad weather or very hot/cold days."""
    return json.dumps({"category": "indoor", "suggestions": _pick(INDOOR_ACTIVITIES)}, indent=2)


@mcp.tool()
async def suggest_picnic() -> str:
    """Suggest picnic spots, best for mild, dry, low-wind weather."""
    return json.dumps({"category": "picnic", "suggestions": _pick(PICNIC_SPOTS)}, indent=2)


@mcp.tool()
async def suggest_outdoor_activity() -> str:
    """Suggest more active outdoor activities (hiking, cycling, kayaking...), best for clear weather."""
    return json.dumps({"category": "outdoor", "suggestions": _pick(OUTDOOR_ACTIVITIES)}, indent=2)


@mcp.tool()
async def recommend_activity(condition: str, temperature_c: float, wind_kph: float = 0) -> str:
    """Recommend an activity category and specific suggestions based on weather.

    Args:
        condition: Weather condition, e.g. "sunny", "rainy", "cloudy", "stormy", "snowy", "windy"
        temperature_c: Current or forecast temperature in Celsius
        wind_kph: Wind speed in kph (default 0)
    """
    condition_lower = condition.lower().strip()
    is_bad = any(keyword in condition_lower for keyword in BAD_OUTDOOR_KEYWORDS)
    is_mild = any(keyword in condition_lower for keyword in MILD_KEYWORDS)

    if is_bad or temperature_c < 5 or temperature_c > 38:
        category, options = "indoor", INDOOR_ACTIVITIES
        reason = f"Conditions are {condition} at {temperature_c}C, best to stay indoors."
    elif is_mild and 15 <= temperature_c <= 30 and wind_kph < 25:
        category, options = "picnic", PICNIC_SPOTS
        reason = f"Mild {condition} weather at {temperature_c}C with low wind, perfect for a picnic."
    else:
        category, options = "outdoor", OUTDOOR_ACTIVITIES
        reason = f"{condition} weather at {temperature_c}C is good for an active outing."

    return json.dumps(
        {
            "category": category,
            "reason": reason,
            "suggestions": _pick(options),
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
