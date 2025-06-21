from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Service")

@mcp.tool()
def get_waeather(location: str) -> str:
    """Get the current weather for a specified locaiton"""
    return f"Weather in {location} is sunny with a temperature of 22 degrees Celsius."

@mcp.resource("weather://{location}")
def weather_resource(location: str) -> str:
    """Provide weather data as a resource"""
    return f"Weather data for {location}: is Sunny."

@mcp.prompt()
def weather_report(location: str) -> str:
    """Create a weather report prompt"""
    return f"You are a weather reporter. Weather report for {location}"

if __name__ == "__main__":
    mcp.run(transport="sse", port=3001)