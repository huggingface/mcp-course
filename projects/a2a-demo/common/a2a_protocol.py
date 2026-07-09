"""
Minimal A2A (Agent-to-Agent) protocol layer.

This is a small, self-contained implementation of the *shape* of the A2A
spec (https://a2a-protocol.org) -- enough to demonstrate agent discovery and
agent-to-agent messaging in a toy project. It is NOT the official a2a-sdk;
it deliberately mirrors the real spec's core pieces so the concepts (and
code) transfer directly:

- Agent Card: a JSON document served at `/.well-known/agent.json` that lets
  one agent discover another agent's name, description, and skills.
- JSON-RPC 2.0 envelope with a `message/send` method, carrying a `Message`
  made of `Part`s (here we only need `text` parts).
- A `Task` object with a lifecycle state ("submitted" -> "completed" or
  "failed") that wraps the agent's reply.

Each agent in this demo runs one of these as a small FastAPI app, with its
"brain" being a plain async function: `Callable[[str], Awaitable[str]]` that
takes the incoming message text and returns the reply text.
"""

from __future__ import annotations

import uuid
from typing import Any, Awaitable, Callable

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langsmith import traceable
from langsmith.middleware import TracingMiddleware
from langsmith.run_helpers import get_current_run_tree
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------
# Agent Card (discovery document)
# --------------------------------------------------------------------------


class AgentSkill(BaseModel):
    id: str
    name: str
    description: str
    tags: list[str] = Field(default_factory=list)


class AgentCard(BaseModel):
    name: str
    description: str
    url: str
    version: str = "1.0.0"
    protocol: str = "a2a-toy/1.0"
    skills: list[AgentSkill] = Field(default_factory=list)


# --------------------------------------------------------------------------
# Messages & Tasks
# --------------------------------------------------------------------------


class TextPart(BaseModel):
    kind: str = "text"
    text: str


class Message(BaseModel):
    role: str  # "user" | "agent"
    parts: list[TextPart]
    message_id: str = Field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def user_text(cls, text: str) -> "Message":
        return cls(role="user", parts=[TextPart(text=text)])

    @classmethod
    def agent_text(cls, text: str) -> "Message":
        return cls(role="agent", parts=[TextPart(text=text)])

    def text(self) -> str:
        return "\n".join(p.text for p in self.parts)


class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    state: str  # "completed" | "failed"
    history: list[Message]


# --------------------------------------------------------------------------
# JSON-RPC 2.0 envelope
# --------------------------------------------------------------------------


class RpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int
    method: str
    params: dict[str, Any]


def _rpc_result(request_id: str | int, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _rpc_error(request_id: str | int, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


# --------------------------------------------------------------------------
# Server side: turn an agent card + handler into a FastAPI app
# --------------------------------------------------------------------------

AgentHandler = Callable[[str], Awaitable[str]]


class HandlerBox:
    """Mutable holder for an agent's handler.

    The FastAPI app and its routes are created once, up front. The actual
    handler (which needs an open MCP session) is only known once the app's
    `lifespan` has started. Routes read `handler_box.handler` on every
    request, so wiring it up during startup is enough.
    """

    def __init__(self) -> None:
        self.handler: AgentHandler | None = None


def build_a2a_app(card: AgentCard, handler_box: HandlerBox) -> FastAPI:
    """Build a FastAPI app exposing the agent-card + `message/send` JSON-RPC method."""

    app = FastAPI(title=card.name)
    # Continues a trace propagated via the `langsmith-trace` header (set by
    # A2AClient below) so a call chain spanning multiple agent processes
    # shows up as one nested trace in LangSmith, instead of two disconnected
    # ones. Does nothing if the header is absent or tracing is disabled.
    app.add_middleware(TracingMiddleware)

    @app.get("/.well-known/agent.json")
    async def agent_card() -> AgentCard:
        return card

    @app.post("/")
    async def rpc_endpoint(request: Request) -> JSONResponse:
        payload = await request.json()
        rpc_req = RpcRequest.model_validate(payload)

        if rpc_req.method != "message/send":
            return JSONResponse(_rpc_error(rpc_req.id, -32601, f"Unknown method '{rpc_req.method}'"))

        if handler_box.handler is None:
            return JSONResponse(_rpc_error(rpc_req.id, -32000, "Agent is still starting up"))

        try:
            incoming = Message.model_validate(rpc_req.params["message"])
            reply_text = await handler_box.handler(incoming.text())
            task = Task(
                state="completed",
                history=[incoming, Message.agent_text(reply_text)],
            )
            return JSONResponse(_rpc_result(rpc_req.id, task.model_dump()))
        except Exception as exc:  # noqa: BLE001 - surface any handler error as a task failure
            task = Task(
                state="failed",
                history=[Message.agent_text(f"Agent error: {exc}")],
            )
            return JSONResponse(_rpc_result(rpc_req.id, task.model_dump()))

    return app


# --------------------------------------------------------------------------
# Client side: discover a card, send a message, get the reply text back
# --------------------------------------------------------------------------


class A2AClient:
    """Tiny A2A client: fetch an Agent Card, then send messages via JSON-RPC."""

    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=timeout)

    @traceable(run_type="chain", name="a2a::discover_agent")
    async def get_agent_card(self) -> AgentCard:
        """Fetch the Agent Card (traced as an A2A discovery call)."""
        run_tree = get_current_run_tree()
        headers = {}
        if run_tree:
            run_tree.name = f"a2a::discover_agent -> {self.base_url}"
            headers = run_tree.to_headers()

        resp = await self._client.get(f"{self.base_url}/.well-known/agent.json", headers=headers)
        resp.raise_for_status()
        return AgentCard.model_validate(resp.json())

    @traceable(run_type="chain", name="a2a::message_send")
    async def send_message(self, text: str) -> str:
        """Send a text message to the agent and return its reply text (traced,
        propagating this call's trace context to the receiving agent so its
        own handler - and any MCP tool calls or further A2A calls it makes -
        shows up nested under this run in LangSmith)."""
        run_tree = get_current_run_tree()
        headers = {}
        if run_tree:
            run_tree.name = f"a2a::message_send -> {self.base_url}"
            headers = run_tree.to_headers()

        rpc_req = RpcRequest(
            id=uuid.uuid4().hex,
            method="message/send",
            params={"message": Message.user_text(text).model_dump()},
        )
        resp = await self._client.post(self.base_url + "/", json=rpc_req.model_dump(), headers=headers)
        resp.raise_for_status()
        body = resp.json()

        if "error" in body:
            raise RuntimeError(f"A2A error: {body['error']}")

        task = Task.model_validate(body["result"])
        if task.state != "completed":
            raise RuntimeError(f"A2A task did not complete: {task.model_dump()}")

        agent_messages = [m for m in task.history if m.role == "agent"]
        return agent_messages[-1].text() if agent_messages else ""

    async def aclose(self) -> None:
        await self._client.aclose()
