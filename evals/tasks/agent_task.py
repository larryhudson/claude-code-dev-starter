"""Agent task wrapper for running the Pydantic AI agent in evaluation mode."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic_ai import Agent


@dataclass
class AgentInput:
    """Input for the agent evaluation task."""

    user_message: str
    conversation_history: list[dict] | None = None


@dataclass
class AgentOutput:
    """Output from the agent evaluation task."""

    response: str
    tool_calls: list[str] = field(default_factory=list)


def _create_agent() -> "Agent[None, str]":
    """Create a fresh agent instance to avoid shared state issues in concurrent tests."""
    from pydantic_ai import Agent
    from pydantic_ai.mcp import MCPServerStreamableHTTP

    mcp_server = MCPServerStreamableHTTP("http://localhost:8000/mcp/mcp")

    return Agent(
        "anthropic:claude-sonnet-4-20250514",
        system_prompt="""You are a helpful assistant for a software development project.
        You can help with coding questions, explain concepts, and assist with development tasks.
        Be concise and helpful in your responses.

        You have access to tools that can provide information about the project.""",
        toolsets=[mcp_server],
    )


async def run_agent_task(input: AgentInput) -> AgentOutput:
    """Run the agent and capture output + tool usage.

    Args:
        input: The input containing the user message and optional conversation history.

    Returns:
        AgentOutput containing the response text and list of tool names called.
    """
    from pydantic_ai.messages import ToolCallPart

    agent = _create_agent()

    # Use async context manager to properly manage MCP connection lifecycle
    async with agent:
        result = await agent.run(input.user_message)

    # Extract tool call names from the result
    tool_calls: list[str] = []
    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolCallPart):
                tool_calls.append(part.tool_name)

    return AgentOutput(
        response=result.output,
        tool_calls=tool_calls,
    )
