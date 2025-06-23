# Building Tiny Agents with MCP and the Hugging Face Hub

Now that we've built MCP servers in Gradio and learned about creating MCP clients, let's complete our end-to-end application by building an agent that can seamlessly interact with our sentiment analysis tool. This section builds on the project [Tiny Agents](https://huggingface.co/blog/tiny-agents), which demonstrates a super simple way of deploying MCP clients that can connect to services like our Gradio sentiment analysis server.

In this final exercise of Unit 2, we will walk you through how to implement both TypeScript (JS) and Python MCP clients that can communicate with any MCP server, including the Gradio-based sentiment analysis server we built in the previous sections. This completes our end-to-end MCP application flow: from building a Gradio MCP server exposing a sentiment analysis tool, to creating a flexible agent that can use this tool alongside other capabilities.

![meme](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/tiny-agents/thumbnail.jpg)
<figcaption>Image credit https://x.com/adamdotdev</figcaption>

## Installation

Let's install the necessary packages to build our Tiny Agents.

<Tip>

Some MCP Clients, notably Claude Desktop, do not yet support SSE-based MCP Servers. In those cases, you can use a tool such as [mcp-remote](https://github.com/geelen/mcp-remote). First install Node.js. Then, add the following to your own MCP Client config:

</Tip>

Tiny Agent can run MCP servers with a command line environment. To do this, we will need to install `npm` and run the server with `npx`. **We'll need these for both Python and JavaScript.**

Let's install `npx` with `npm`. If you don't have `npm` installed, check out the [npm documentation](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

```bash
# install npx
npm install -g npx
```

Then, we need to install the `mcp-remote` package.

```bash
npm i mcp-remote
```

<hfoptions id="tiny-agents">
<hfoption id="typescript">

For JavaScript, we need to install the `tiny-agents` package.

```bash
npm install @huggingface/tiny-agents
```

</hfoption>
<hfoption id="python">

For Python, you need to install the latest version of `huggingface_hub` with the `mcp` extra to get all the necessary components.

```bash
pip install "huggingface_hub[mcp]>=0.32.0"
```

</hfoption>
</hfoptions>

## Tiny Agents MCP Client in the Command Line

Let's repeat the example from [Unit 1](../unit1/mcp-clients.mdx) to create a basic Tiny Agent. Tiny Agents can create MCP clients from the command line based on JSON configuration files.

<hfoptions id="tiny-agents">
<hfoption id="typescript">

Let's setup a project with a basic Tiny Agent.

```bash
mkdir my-agent
touch my-agent/agent.json
```

The JSON file will look like this:

```json
{
	"model": "Qwen/Qwen2.5-72B-Instruct",
	"provider": "nebius",
	"servers": [
		{
			"type": "stdio",
			"config": {
				"command": "npx",
				"args": [
					"mcp-remote",
					"http://localhost:7860/gradio_api/mcp/sse" // This is the MCP Server we created in the previous section
				]
			}
		}
	]
}
```

We can then run the agent with the following command:

```bash
npx @huggingface/tiny-agents run ./my-agent
```

</hfoption>
<hfoption id="python">

Let's setup a project with a basic Tiny Agent.

```bash
mkdir my-agent
touch my-agent/agent.json
cd my-agent
```

The JSON file will look like this:

```json
{
	"model": "Qwen/Qwen2.5-72B-Instruct",
	"provider": "nebius",
	"servers": [
		{
			"type": "stdio",
			"config": {
				"command": "npx",
				"args": [
					"mcp-remote", 
					"http://localhost:7860/gradio_api/mcp/sse"
				]
			}
		}
	]
}
```

We can then run the agent with the following command:

```bash
tiny-agents run agent.json
```

</hfoption>
</hfoptions>

Here we have a basic Tiny Agent that can connect to our Gradio MCP server. It includes a model, provider, and a server configuration.

| Field | Description |
|-------|-------------|
| `model` | The open source model to use for the agent |
| `provider` | The inference provider to use for the agent |
| `servers` | The servers to use for the agent. We'll use the `mcp-remote` server for our Gradio MCP server. |

<Tip>

We could also use an open source model running locally with Tiny Agents. If we start a local inference server with 

```json
{
	"model": "Qwen/Qwen3-32B",
	"endpointUrl": "http://localhost:1234/v1",
	"servers": [
		{
			"type": "stdio",
			"config": {
				"command": "npx",
				"args": [
					"mcp-remote",
					"http://localhost:1234/v1/mcp/sse"
				]
			}
		}
	]
}
```


Here we have a Tiny Agent that can connect to a local model. It includes a model, endpoint URL (`http://localhost:1234/v1`), and a server configuration. The endpoint should be an OpenAI-compatible endpoint.

</Tip>

## Custom Tiny Agents MCP Client

Now that we understand both Tiny Agents and Gradio MCP servers, let's see how they work together! The beauty of MCP is that it provides a standardized way for agents to interact with any MCP-compatible server, including our Gradio-based sentiment analysis server from earlier sections.

### Using the Gradio Server with Tiny Agents

To connect our Tiny Agent to the Gradio sentiment analysis server we built earlier in this unit, we just need to add it to our list of servers. Here's how we can modify our agent configuration:

<hfoptions id="tiny-agents">
<hfoption id="typescript">

```ts
const agent = new Agent({
    provider: process.env.PROVIDER ?? "nebius",
    model: process.env.MODEL_ID ?? "Qwen/Qwen2.5-72B-Instruct",
    apiKey: process.env.HF_TOKEN,
    servers: [
        // ... existing servers ...
        {
            command: "npx",
            args: [
                "mcp-remote",
                "http://localhost:7860/gradio_api/mcp/sse"  // Your Gradio MCP server
            ]
        }
    ],
});
```

</hfoption>
<hfoption id="python">

```python
import os

from huggingface_hub import Agent

agent = Agent(
    model="Qwen/Qwen2.5-72B-Instruct",
    provider="nebius",
    servers=[
        {
            "command": "npx",
            "args": [
                "mcp-remote",
                "http://localhost:7860/gradio_api/mcp/sse"  # Your Gradio MCP server
            ]
        }
    ],
)
```

</hfoption>
</hfoptions>

Now our agent can use the sentiment analysis tool alongside other tools! For example, it could:
1. Read text from a file using the filesystem server
2. Analyze its sentiment using our Gradio server
3. Write the results back to a file

### Deployment Considerations

When deploying your Gradio MCP server to Hugging Face Spaces, you'll need to update the server URL in your agent configuration to point to your deployed space:


```json
{
    command: "npx",
    args: [
        "mcp-remote",
        "https://YOUR_USERNAME-mcp-sentiment.hf.space/gradio_api/mcp/sse"
    ]
}
```


This allows your agent to use the sentiment analysis tool from anywhere, not just locally!

## Conclusion: Our Complete End-to-End MCP Application

In this unit, we've gone from understanding MCP basics to building a complete end-to-end application:

1. We created a Gradio MCP server that exposes a sentiment analysis tool
2. We learned how to connect to this server using MCP clients
3. We built a tiny agent in TypeScript and Python that can interact with our tool

This demonstrates the power of the Model Context Protocol - we can create specialized tools using frameworks we're familiar with (like Gradio), expose them through a standardized interface (MCP), and then have agents seamlessly use these tools alongside other capabilities.

The complete flow we've built allows an agent to:
- Connect to multiple tool providers
- Dynamically discover available tools
- Use our custom sentiment analysis tool
- Combine it with other capabilities like file system access and web browsing

This modular approach is what makes MCP so powerful for building flexible AI applications.

## Next Steps

- Check out the Tiny Agents blog posts in [Python](https://huggingface.co/blog/python-tiny-agents) and [TypeScript](https://huggingface.co/blog/tiny-agents)
- Review the [Tiny Agents documentation](https://huggingface.co/docs/huggingface.js/main/en/tiny-agents/README)
- Build something with Tiny Agents!