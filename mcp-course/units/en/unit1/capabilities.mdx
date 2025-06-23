# Understanding MCP Capabilities

MCP Servers expose a variety of capabilities to Clients through the communication protocol. These capabilities fall into four main categories, each with distinct characteristics and use cases. Let's explore these core primitives that form the foundation of MCP's functionality.

<Tip>

In this section, we'll show examples as framework agnostic functions in each language. This is to focus on the concepts and how they work together, rather than the complexities of any framework.

In the coming units, we'll show how these concepts are implemented in MCP specific code.

</Tip>

## Tools

Tools are executable functions or actions that the AI model can invoke through the MCP protocol.

- **Control**: Tools are typically **model-controlled**, meaning that the AI model (LLM) decides when to call them based on the user's request and context.
- **Safety**: Due to their ability to perform actions with side effects, tool execution can be dangerous. Therefore, they typically require explicit user approval.
- **Use Cases**: Sending messages, creating tickets, querying APIs, performing calculations.

**Example**: A weather tool that fetches current weather data for a given location:

<hfoptions id="tool-example">
<hfoption id="python">

```python
def get_weather(location: str) -> dict:
    """Get the current weather for a specified location."""
    # Connect to weather API and fetch data
    return {
        "temperature": 72,
        "conditions": "Sunny",
        "humidity": 45
    }
```

</hfoption>
<hfoption id="javascript">

```javascript
function getWeather(location) {
    // Connect to weather API and fetch data
    return {
        temperature: 72,
        conditions: 'Sunny',
        humidity: 45
    };
}
```

</hfoption>
</hfoptions>

## Resources

Resources provide read-only access to data sources, allowing the AI model to retrieve context without executing complex logic.

- **Control**: Resources are **application-controlled**, meaning the Host application typically decides when to access them.
- **Nature**: They are designed for data retrieval with minimal computation, similar to GET endpoints in REST APIs.
- **Safety**: Since they are read-only, they typically present lower security risks than Tools.
- **Use Cases**: Accessing file contents, retrieving database records, reading configuration information.

**Example**: A resource that provides access to file contents:

<hfoptions id="resource-example">
<hfoption id="python">

```python
def read_file(file_path: str) -> str:
    """Read the contents of a file at the specified path."""
    with open(file_path, 'r') as f:
        return f.read()
```

</hfoption>
<hfoption id="javascript">

```javascript
function readFile(filePath) {
    // Using fs.readFile to read file contents
    const fs = require('fs');
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                reject(err);
                return;
            }
            resolve(data);
        });
    });
}
```

</hfoption>
</hfoptions>

## Prompts

Prompts are predefined templates or workflows that guide the interaction between the user, the AI model, and the Server's capabilities.

- **Control**: Prompts are **user-controlled**, often presented as options in the Host application's UI.
- **Purpose**: They structure interactions for optimal use of available Tools and Resources.
- **Selection**: Users typically select a prompt before the AI model begins processing, setting context for the interaction.
- **Use Cases**: Common workflows, specialized task templates, guided interactions.

**Example**: A prompt template for generating a code review:

<hfoptions id="prompt-example">
<hfoption id="python">

```python
def code_review(code: str, language: str) -> list:
    """Generate a code review for the provided code snippet."""
    return [
        {
            "role": "system",
            "content": f"You are a code reviewer examining {language} code. Provide a detailed review highlighting best practices, potential issues, and suggestions for improvement."
        },
        {
            "role": "user",
            "content": f"Please review this {language} code:\n\n```{language}\n{code}\n```"
        }
    ]
```

</hfoption>
<hfoption id="javascript">

```javascript
function codeReview(code, language) {
    return [
        {
            role: 'system',
            content: `You are a code reviewer examining ${language} code. Provide a detailed review highlighting best practices, potential issues, and suggestions for improvement.`
        },
        {
            role: 'user',
            content: `Please review this ${language} code:\n\n\`\`\`${language}\n${code}\n\`\`\``
        }
    ];
}
```

</hfoption>
</hfoptions>

## Sampling

Sampling allows Servers to request the Client (specifically, the Host application) to perform LLM interactions.

- **Control**: Sampling is **server-initiated** but requires Client/Host facilitation.
- **Purpose**: It enables server-driven agentic behaviors and potentially recursive or multi-step interactions.
- **Safety**: Like Tools, sampling operations typically require user approval.
- **Use Cases**: Complex multi-step tasks, autonomous agent workflows, interactive processes.

**Example**: A Server might request the Client to analyze data it has processed:

<hfoptions id="sampling-example">
<hfoption id="python">

```python
def request_sampling(messages, system_prompt=None, include_context="none"):
    """Request LLM sampling from the client."""
    # In a real implementation, this would send a request to the client
    return {
        "role": "assistant",
        "content": "Analysis of the provided data..."
    }
```

</hfoption>
<hfoption id="javascript">

```javascript
function requestSampling(messages, systemPrompt = null, includeContext = 'none') {
    // In a real implementation, this would send a request to the client
    return {
        role: 'assistant',
        content: 'Analysis of the provided data...'
    };
}

function handleSamplingRequest(request) {
    const { messages, systemPrompt, includeContext } = request;
    // In a real implementation, this would process the request and return a response
    return {
        role: 'assistant',
        content: 'Response to the sampling request...'
    };
}
```

</hfoption>
</hfoptions>

The sampling flow follows these steps:
1. Server sends a `sampling/createMessage` request to the client
2. Client reviews the request and can modify it
3. Client samples from an LLM
4. Client reviews the completion
5. Client returns the result to the server

<Tip>

This human-in-the-loop design ensures users maintain control over what the LLM sees and generates. When implementing sampling, it's important to provide clear, well-structured prompts and include relevant context.

</Tip>

## How Capabilities Work Together

Let's look at how these capabilities work together to enable complex interactions. In the table below, we've outlined the capabilities, who controls them, the direction of control, and some other details.

| Capability | Controlled By | Direction | Side Effects | Approval Needed | Typical Use Cases |
|------------|---------------|-----------|--------------|-----------------|-------------------|
| Tools      | Model (LLM)   | Client → Server | Yes (potentially) | Yes | Actions, API calls, data manipulation |
| Resources  | Application   | Client → Server | No (read-only) | Typically no | Data retrieval, context gathering |
| Prompts    | User          | Server → Client | No | No (selected by user) | Guided workflows, specialized templates |
| Sampling   | Server        | Server → Client → Server | Indirectly | Yes | Multi-step tasks, agentic behaviors |

These capabilities are designed to work together in complementary ways:

1. A user might select a **Prompt** to start a specialized workflow
2. The Prompt might include context from **Resources**
3. During processing, the AI model might call **Tools** to perform specific actions
4. For complex operations, the Server might use **Sampling** to request additional LLM processing

The distinction between these primitives provides a clear structure for MCP interactions, enabling AI models to access information, perform actions, and engage in complex workflows while maintaining appropriate control boundaries.

## Discovery Process

One of MCP's key features is dynamic capability discovery. When a Client connects to a Server, it can query the available Tools, Resources, and Prompts through specific list methods:

- `tools/list`: Discover available Tools
- `resources/list`: Discover available Resources
- `prompts/list`: Discover available Prompts

This dynamic discovery mechanism allows Clients to adapt to the specific capabilities each Server offers without requiring hardcoded knowledge of the Server's functionality.

## Conclusion

Understanding these core primitives is essential for working with MCP effectively. By providing distinct types of capabilities with clear control boundaries, MCP enables powerful interactions between AI models and external systems while maintaining appropriate safety and control mechanisms.

In the next section, we'll explore how Gradio integrates with MCP to provide easy-to-use interfaces for these capabilities. 