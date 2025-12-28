from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

# Connect to the MCP server running on the same host
# Path is /mcp/mcp because FastMCP's http_app() creates a /mcp route, and we mount at /mcp
mcp_server = MCPServerStreamableHTTP("http://localhost:8000/mcp/mcp")

agent = Agent(
    "anthropic:claude-sonnet-4-20250514",
    system_prompt="""You are a helpful assistant for a software development project.
    You can help with coding questions, explain concepts, and assist with development tasks.
    Be concise and helpful in your responses.

    You have access to tools that can provide information about the project.""",
    toolsets=[mcp_server],
)
