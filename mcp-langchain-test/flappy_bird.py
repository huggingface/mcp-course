"""
This is a simple flappy bird server.
"""

# imports
from mcp.server.fastmcp import FastMCP

mcp=FastMCP("flappy_bird")

@mcp.tool()
async def get_weather(location:str)->str:
    """Talks more abt the game: Flappy Bird"""
    return "The creator ditched the game after 2 days of development, too addictive, itseems."

if __name__=="__main__":
    mcp.run(transport="streamable-http")