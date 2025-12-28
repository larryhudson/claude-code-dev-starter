from fastmcp import FastMCP

mcp = FastMCP("Claude Code Dev Tools")


@mcp.tool
def get_project_info() -> dict:
    """Get information about the current project."""
    return {
        "name": "Claude Code Dev Starter",
        "description": "A production-ready Python template for Claude Code",
        "tech_stack": ["FastAPI", "FastMCP", "Pydantic AI", "React", "shadcn/ui"],
    }


@mcp.tool
def list_available_commands() -> list[str]:
    """List available make commands for development."""
    return [
        "make dev - Start development server",
        "make dev-logs - View development logs",
        "make lint - Lint Python files",
        "make format - Format Python files",
        "make type-check - Type check Python files",
        "make stop-dev - Stop the development server",
    ]
