from smolagents.mcp_client import MCPClient

with MCPClient({
    'url': "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse"
}) as tools:
    print("\n".join(f"{tool.name}: {tool.description}" for tool in tools))