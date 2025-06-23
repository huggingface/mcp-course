# imports
import asyncio, os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
# load environment variables
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="qwen-quq-32b")

async def main():
    clinet = MultiServerMCPClient(
        {
            "Math_Operations": {
                "command": "python",
                "args": ["math_operations.py"], # abs path [BEWARE]
                "transport": "stdio"
            },
            "flappy_bird": {
                "command": "python",
                "args": ["flappy_bird.py"],
                "transport": "streamable-http"
            }
        }
    )
    tools = await clinet.get_tools()
    agent=create_react_agent(llm, tools, verbose=True)

    math_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12 / 4?"}]})
    print("Math response:", math_response['messages'][-1].content)

    flappy_bird_response = await agent.ainvoke({"messages": [{"role": "user", "content": "play flappy bird"}]})
    print("Flappy bird response:", flappy_bird_response['messages'][-1].content)

asyncio.run(main())