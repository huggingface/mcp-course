import typer
from smolagents.mcp_client import MCPClient

import gradio as gr
import os

from mcp import StdioServerParameters
from smolagents import InferenceClientModel, CodeAgent, ToolCollection, MCPClient

app = typer.Typer()


@app.command()
def print_server_tools():
    """Print available tools from the MCP server."""
    with MCPClient(
            {"url": "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse"}
    ) as tools:
        # Tools from the remote server are available
        print("\n".join(f"\033[94m{t.name}\033[0m: \033[92m{t.description}\033[0m" for t in tools))


@app.command()
def client():
    """Get available tools from the MCP server."""

    mcp_client = MCPClient(
        {"url": "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse"}
    )

    try:
        tools = mcp_client.get_tools()
        model = InferenceClientModel(token=os.getenv("HUGGINGFACE_API_TOKEN"))
        agent = CodeAgent(tools=[*tools], model=model,
                          additional_authorized_imports=["json", "ast", "urllib", "base64"])

        demo = gr.ChatInterface(
            fn=lambda message, history: str(agent.run(message)),
            type="messages",
            examples=["Analyze the sentiment of the following text 'This is awesome'"],
            title="Agent with MCP Tools",
            description="This is a simple agent that uses MCP tools to answer questions.",
        )

        demo.launch()

    finally:
        mcp_client.disconnect()

if __name__ == "__main__":
    app()

