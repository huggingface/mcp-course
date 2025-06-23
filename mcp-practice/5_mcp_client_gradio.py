import gradio as gr, os
from mcp import StdioServerParameters
from smolagents import InferenceClientModel, CodeAgent, ToolCollection, MCPClient


mcp_client = MCPClient({
    'url': "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse"
})

tools = mcp_client.get_tools()
print(f"Tools: {tools}")

from dotenv import load_dotenv
load_dotenv()

model = InferenceClientModel(token=os.getenv("HUGGINGFACE_API_TOKEN"))
agent = CodeAgent(tools=[*tools], model=model)

demo = gr.ChatInterface(
    fn=lambda message, history: str(agent.run(message)),
    type="messages",
    examples=["Prime factorization of 68"],
    title="Agent with MCL tools",
    description="This is a simple agent that uses MCP tools to answer questions."
)

demo.launch()