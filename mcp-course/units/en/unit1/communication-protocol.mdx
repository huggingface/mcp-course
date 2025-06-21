# The Communication Protocol

MCP defines a standardized communication protocol that enables Clients and Servers to exchange messages in a consistent, predictable way. This standardization is critical for interoperability across the community. In this section, we'll explore the protocol structure and transport mechanisms used in MCP.

<Tip warning={true}>

We're getting down to the nitty-gritty details of the MCP protocol. You won't need to know all of this to build with MCP, but it's good to know that it exists and how it works.

</Tip>

## JSON-RPC: The Foundation

At its core, MCP uses **JSON-RPC 2.0** as the message format for all communication between Clients and Servers. JSON-RPC is a lightweight remote procedure call protocol encoded in JSON, which makes it:

- Human-readable and easy to debug
- Language-agnostic, supporting implementation in any programming environment
- Well-established, with clear specifications and widespread adoption

![message types](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit1/5.png)

The protocol defines three types of messages:

### 1. Requests

Sent from Client to Server to initiate an operation. A Request message includes:
- A unique identifier (`id`)
- The method name to invoke (e.g., `tools/call`)
- Parameters for the method (if any)

Example Request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "weather",
    "arguments": {
      "location": "San Francisco"
    }
  }
}
```

### 2. Responses

Sent from Server to Client in reply to a Request. A Response message includes:
- The same `id` as the corresponding Request
- Either a `result` (for success) or an `error` (for failure)

Example Success Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "temperature": 62,
    "conditions": "Partly cloudy"
  }
}
```

Example Error Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid location parameter"
  }
}
```

### 3. Notifications

One-way messages that don't require a response. Typically sent from Server to Client to provide updates or notifications about events.

Example Notification:
```json
{
  "jsonrpc": "2.0",
  "method": "progress",
  "params": {
    "message": "Processing data...",
    "percent": 50
  }
}
```

## Transport Mechanisms

JSON-RPC defines the message format, but MCP also specifies how these messages are transported between Clients and Servers. Two primary transport mechanisms are supported:

### stdio (Standard Input/Output)

The stdio transport is used for local communication, where the Client and Server run on the same machine:

The Host application launches the Server as a subprocess and communicates with it by writing to its standard input (stdin) and reading from its standard output (stdout).

<Tip>

**Use cases** for this transport are local tools like file system access or running local scripts.

</Tip>

The main **Advantages** of this transport are that it's simple, no network configuration required, and securely sandboxed by the operating system.

### HTTP + SSE (Server-Sent Events) / Streamable HTTP

The HTTP+SSE transport is used for remote communication, where the Client and Server might be on different machines:

Communication happens over HTTP, with the Server using Server-Sent Events (SSE) to push updates to the Client over a persistent connection.

<Tip>

**Use cases** for this transport are connecting to remote APIs, cloud services, or shared resources.

</Tip>

The main **Advantages** of this transport are that it works across networks, enables integration with web services, and is compatible with serverless environments.

Recent updates to the MCP standard have introduced or refined "Streamable HTTP," which offers more flexibility by allowing servers to dynamically upgrade to SSE for streaming when needed, while maintaining compatibility with serverless environments.

## The Interaction Lifecycle

In the previous section, we discussed the lifecycle of a single interaction between a Client (💻) and a Server (🌐). Let's now look at the lifecycle of a complete interaction between a Client and a Server in the context of the MCP protocol.

The MCP protocol defines a structured interaction lifecycle between Clients and Servers:

### Initialization

The Client connects to the Server and they exchange protocol versions and capabilities, and the Server responds with its supported protocol version and capabilities.

<table style="width: 100%;">
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">→<br>initialize</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">←<br>response</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">→<br>initialized</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
</table>

The Client confirms the initialization is complete via a notification message.

### Discovery

The Client requests information about available capabilities and the Server responds with a list of available tools.

<table style="width: 100%;">
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">→<br>tools/list</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">←<br>response</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
</table>

This process could be repeated for each tool, resource, or prompt type.

### Execution

The Client invokes capabilities based on the Host's needs.

<table style="width: 100%;">
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">→<br>tools/call</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">←<br>notification (optional progress)</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">←<br>response</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
</table>

### Termination

The connection is gracefully closed when no longer needed and the Server acknowledges the shutdown request.

<table style="width: 100%;">
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">→<br>shutdown</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">←<br>response</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
  <tr>
    <td style="background-color: lightgreen; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">💻</td>
    <td style="text-align: center;">→<br>exit</td>
    <td style="background-color: lightblue; text-align: center; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">🌐</td>
  </tr>
</table>

The Client sends the final exit message to complete the termination.

## Protocol Evolution

The MCP protocol is designed to be extensible and adaptable. The initialization phase includes version negotiation, allowing for backward compatibility as the protocol evolves. Additionally, capability discovery enables Clients to adapt to the specific features each Server offers, enabling a mix of basic and advanced Servers in the same ecosystem.
