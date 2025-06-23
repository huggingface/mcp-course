"""
This is a simple math operations server.
"""

# imports
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
# load environment variables
load_dotenv()

mcp = FastMCP("math_operations")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divide two numbers."""
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")