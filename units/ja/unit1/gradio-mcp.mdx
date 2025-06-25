# Gradio MCP Integration

We've now explored the core concepts of the MCP protocol and how to implement MCP Servers and Clients. In this section, we're going to make things slightly easier by using Gradio to create an MCP Server!

<Tip>

Gradio is a popular Python library for quickly creating customizable web interfaces for machine learning models. 

</Tip>

## Introduction to Gradio

Gradio allows developers to create UIs for their models with just a few lines of Python code. It's particularly useful for:

- Creating demos and prototypes
- Sharing models with non-technical users
- Testing and debugging model behavior

With the addition of MCP support, Gradio now offers a straightforward way to expose AI model capabilities through the standardized MCP protocol.

Combining Gradio with MCP allows you to create both human-friendly interfaces and AI-accessible tools with minimal code. But best of all, Gradio is already well-used by the AI community, so you can use it to share your MCP Servers with others.

## Prerequisites

To use Gradio with MCP support, you'll need to install Gradio with the MCP extra:

```bash
pip install "gradio[mcp]"
```

You'll also need an LLM application that supports tool calling using the MCP protocol, such as Cursor ( known as "MCP Hosts").

## Creating an MCP Server with Gradio

Let's walk through a basic example of creating an MCP Server using Gradio:

```python
import gradio as gr

def letter_counter(word: str, letter: str) -> int:
    """
    Count the number of occurrences of a letter in a word or text.

    Args:
        word (str): The input text to search through
        letter (str): The letter to search for

    Returns:
        int: The number of times the letter appears in the text
    """
    word = word.lower()
    letter = letter.lower()
    count = word.count(letter)
    return count

# Create a standard Gradio interface
demo = gr.Interface(
    fn=letter_counter,
    inputs=["textbox", "textbox"],
    outputs="number",
    title="Letter Counter",
    description="Enter text and a letter to count how many times the letter appears in the text."
)

# Launch both the Gradio web interface and the MCP server
if __name__ == "__main__":
    demo.launch(mcp_server=True)
```

With this setup, your letter counter function is now accessible through:

1. A traditional Gradio web interface for direct human interaction
2. An MCP Server that can be connected to compatible clients

The MCP server will be accessible at:
```
http://your-server:port/gradio_api/mcp/sse
```

The application itself will still be accessible and it looks like this:

![Gradio MCP Server](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit1/7.png)

## How It Works Behind the Scenes

When you set `mcp_server=True` in `launch()`, several things happen:

1. Gradio functions are automatically converted to MCP Tools
2. Input components map to tool argument schemas
3. Output components determine the response format
4. The Gradio server now also listens for MCP protocol messages
5. JSON-RPC over HTTP+SSE is set up for client-server communication

## Key Features of the Gradio <> MCP Integration

1. **Tool Conversion**: Each API endpoint in your Gradio app is automatically converted into an MCP tool with a corresponding name, description, and input schema. To view the tools and schemas, visit `http://your-server:port/gradio_api/mcp/schema` or go to the "View API" link in the footer of your Gradio app, and then click on "MCP".

2. **Environment Variable Support**: There are two ways to enable the MCP server functionality:
- Using the `mcp_server` parameter in `launch()`:
  ```python
  demo.launch(mcp_server=True)
  ```
- Using environment variables:
  ```bash
  export GRADIO_MCP_SERVER=True
  ```

3. **File Handling**: The server automatically handles file data conversions, including:
   - Converting base64-encoded strings to file data
   - Processing image files and returning them in the correct format
   - Managing temporary file storage

   It is **strongly** recommended that input images and files be passed as full URLs ("http://..." or "https://...") as MCP Clients do not always handle local files correctly.

4. **Hosted MCP Servers on 🤗 Spaces**: You can publish your Gradio application for free on Hugging Face Spaces, which will allow you to have a free hosted MCP server. Here's an example of such a Space: https://huggingface.co/spaces/abidlabs/mcp-tools

## Troubleshooting Tips

1. **Type Hints and Docstrings**: Ensure you provide type hints and valid docstrings for your functions. The docstring should include an "Args:" block with indented parameter names.

2. **String Inputs**: When in doubt, accept input arguments as `str` and convert them to the desired type inside the function.

3. **SSE Support**: Some MCP Hosts don't support SSE-based MCP Servers. In those cases, you can use `mcp-remote`:
   ```json
   {
     "mcpServers": {
       "gradio": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "http://your-server:port/gradio_api/mcp/sse"
         ]
       }
     }
   }
   ```

4. **Restart**: If you encounter connection issues, try restarting both your MCP Client and MCP Server.

## Share your MCP Server

You can share your MCP Server by publishing your Gradio app to Hugging Face Spaces. The video below shows how to create a Hugging Face Space.

<Youtube id="3bSVKNKb_PY" />

Now, you can share your MCP Server with others by sharing your Hugging Face Space.

## Conclusion

Gradio's integration with MCP provides an accessible entry point to the MCP ecosystem. By leveraging Gradio's simplicity and adding MCP's standardization, developers can quickly create both human-friendly interfaces and AI-accessible tools with minimal code.

As we progress through this course, we'll explore more sophisticated MCP implementations, but Gradio offers an excellent starting point for understanding and experimenting with the protocol.

In the next unit, we'll dive deeper into building MCP applications, focusing on setting up development environments, exploring SDKs, and implementing more advanced MCP Servers and Clients. 
