from pydantic_ai import Agent

agent = Agent(
    "anthropic:claude-sonnet-4-20250514",
    system_prompt="""You are a helpful assistant for a software development project.
    You can help with coding questions, explain concepts, and assist with development tasks.
    Be concise and helpful in your responses.""",
)
