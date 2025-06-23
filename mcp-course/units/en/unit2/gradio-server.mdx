# Building the Gradio MCP Server

In this section, we'll create our sentiment analysis MCP server using Gradio. This server will expose a sentiment analysis tool that can be used by both human users through a web interface and AI models through the MCP protocol.

## Introduction to Gradio MCP Integration

Gradio provides a straightforward way to create MCP servers by automatically converting your Python functions into MCP tools. When you set `mcp_server=True` in `launch()`, Gradio:

1. Automatically converts your functions into MCP Tools
2. Maps input components to tool argument schemas
3. Determines response formats from output components
4. Sets up JSON-RPC over HTTP+SSE for client-server communication
5. Creates both a web interface and an MCP server endpoint

## Setting Up the Project

First, let's create a new directory for our project and set up the required dependencies:

```bash
mkdir mcp-sentiment
cd mcp-sentiment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install "gradio[mcp]" textblob
```

## Creating the Server

> Hugging face spaces needs an app.py file to build the space. So the name of the python file has to be app.py 

Create a new file called `app.py` with the following code:

```python
import json
import gradio as gr
from textblob import TextBlob

def sentiment_analysis(text: str) -> str:
    """
    Analyze the sentiment of the given text.

    Args:
        text (str): The text to analyze

    Returns:
        str: A JSON string containing polarity, subjectivity, and assessment
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment
    
    result = {
        "polarity": round(sentiment.polarity, 2),  # -1 (negative) to 1 (positive)
        "subjectivity": round(sentiment.subjectivity, 2),  # 0 (objective) to 1 (subjective)
        "assessment": "positive" if sentiment.polarity > 0 else "negative" if sentiment.polarity < 0 else "neutral"
    }

    return json.dumps(result)

# Create the Gradio interface
demo = gr.Interface(
    fn=sentiment_analysis,
    inputs=gr.Textbox(placeholder="Enter text to analyze..."),
    outputs=gr.Textbox(),  # Changed from gr.JSON() to gr.Textbox()
    title="Text Sentiment Analysis",
    description="Analyze the sentiment of text using TextBlob"
)

# Launch the interface and MCP server
if __name__ == "__main__":
    demo.launch(mcp_server=True)
```

## Understanding the Code

Let's break down the key components:

1. **Function Definition**:
   - The `sentiment_analysis` function takes a text input and returns a dictionary
   - It uses TextBlob to analyze the sentiment
   - The docstring is crucial as it helps Gradio generate the MCP tool schema
   - Type hints (`str` and `dict`) help define the input/output schema

2. **Gradio Interface**:
   - `gr.Interface` creates both the web UI and MCP server
   - The function is exposed as an MCP tool automatically
   - Input and output components define the tool's schema
   - The JSON output component ensures proper serialization

3. **MCP Server**:
   - Setting `mcp_server=True` enables the MCP server
   - The server will be available at `http://localhost:7860/gradio_api/mcp/sse`
   - You can also enable it using the environment variable:
     ```bash
     export GRADIO_MCP_SERVER=True
     ```

## Running the Server

Start the server by running:

```bash
python app.py
```

You should see output indicating that both the web interface and MCP server are running. The web interface will be available at `http://localhost:7860`, and the MCP server at `http://localhost:7860/gradio_api/mcp/sse`.

## Testing the Server

You can test the server in two ways:

1. **Web Interface**:
   - Open `http://localhost:7860` in your browser
   - Enter some text and click "Submit"
   - You should see the sentiment analysis results

2. **MCP Schema**:
   - Visit `http://localhost:7860/gradio_api/mcp/schema`
   - This shows the MCP tool schema that clients will use
   - You can also find this in the "View API" link in the footer of your Gradio app

## Troubleshooting Tips

1. **Type Hints and Docstrings**:
   - Always provide type hints for your function parameters and return values
   - Include a docstring with an "Args:" block for each parameter
   - This helps Gradio generate accurate MCP tool schemas

2. **String Inputs**:
   - When in doubt, accept input arguments as `str`
   - Convert them to the desired type inside the function
   - This provides better compatibility with MCP clients

3. **SSE Support**:
   - Some MCP clients don't support SSE-based MCP Servers
   - In those cases, use `mcp-remote`:
     ```json
     {
       "mcpServers": {
         "gradio": {
           "command": "npx",
           "args": [
             "mcp-remote",
             "http://localhost:7860/gradio_api/mcp/sse"
           ]
         }
       }
     }
     ```

4. **Connection Issues**:
   - If you encounter connection problems, try restarting both the client and server
   - Check that the server is running and accessible
   - Verify that the MCP schema is available at the expected URL

## Deploying to Hugging Face Spaces

To make your server available to others, you can deploy it to Hugging Face Spaces:

1. Create a new Space on Hugging Face:
   - Go to huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Gradio" as the SDK
   - Name your space (e.g., "mcp-sentiment")

2. Create a `requirements.txt` file:
```txt
gradio[mcp]
textblob
```

3. Push your code to the Space:
```bash
git init
git add app.py requirements.txt
git commit -m "Initial commit"
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/mcp-sentiment
git push -u origin main
```

Your MCP server will now be available at:
```
https://YOUR_USERNAME-mcp-sentiment.hf.space/gradio_api/mcp/sse
```

## Next Steps

Now that we have our MCP server running, we'll create clients to interact with it. In the next sections, we'll:

1. Create a HuggingFace.js-based client inspired by Tiny Agents
2. Implement a SmolAgents-based Python client
3. Test both clients with our deployed server

Let's move on to building our first client! 
