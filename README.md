# Claude Code Dev Starter

A production-ready full-stack template for building AI-powered applications optimized for [Claude Code](https://docs.claude.com/en/docs/claude-code/). This template combines a FastAPI backend with a React frontend, featuring an AI chat interface, MCP tool integration, automated code quality checks, and an agent evaluation framework.

## What This Template Provides

This template demonstrates best practices for building production-ready AI agents with proper tooling, testing, and Claude Code integration. It serves as both a working example and a foundation for your own AI-powered applications.

**Out of the box, you get:**

1. **Working AI Chat Application**: A fully functional chat interface where users can interact with a Claude-powered agent that can access project information and execute commands through MCP tools.

2. **Real-Time Development Feedback**: LSP (Language Server Protocol) integration provides instant feedback on TypeScript, Python, and Go code as Claude edits files - catching errors before they become problems.

3. **Automated Testing for AI Behavior**: An evaluation framework with 10 pre-configured test cases that verify your agent uses tools appropriately and responds correctly to different types of queries.

4. **Quality Assurance Automation**: Pre-commit hooks and post-edit checks ensure code quality is maintained automatically as you and Claude work together.

5. **Production Deployment Path**: CI/CD pipeline configuration for GitHub Actions, with linting, type-checking, and agent evaluations running automatically on every push.

6. **Extension Points**: Clear patterns for adding your own MCP tools, evaluation tests, and post-edit validation rules.

## Features

- **AI Chat Interface**: Real-time chat with a Claude-powered agent via Pydantic AI
- **MCP Tool Server**: FastMCP server exposing project information and commands as tools
- **Full-Stack Architecture**: FastAPI backend + React/TypeScript frontend
- **LSP Bridge Daemon**: Real-time diagnostics from TypeScript, Python, and Go language servers after every file edit
- **Post-Edit Automation**: Automatic type-checking and linting after Claude modifies files
- **Agent Evaluations**: Pydantic-evals framework for testing agent behavior
- **CI/CD Pipeline**: GitHub Actions for linting, type-checking, and evaluations

## Tech Stack

### Backend
- **FastAPI 0.120+** - Modern async Python web framework
- **Pydantic AI 0.2+** - AI agent framework with tool integration
- **FastMCP 2.0+** - Model Context Protocol server for exposing tools
- **Uvicorn** - ASGI application server
- **Python 3.12+**

### Frontend
- **React 19** - Latest React with hooks
- **TypeScript 5.9+** - Static typing
- **Vite** - Fast build tool and dev server
- **Tailwind CSS 4** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **AI SDK React** - Integration with AI chat protocols
- **Lucide React** - Icon library

### Quality & Testing
- **Ruff** - Fast Python linter and formatter
- **Ty** - Python type checker
- **Pytest** - Testing framework
- **Pydantic Evals** - Agent evaluation framework
- **Pre-commit** - Git hooks for code quality
- **ESLint/Oxlint** - Frontend linting

### DevOps
- **GitHub Actions** - CI/CD pipeline
- **Hivemind** - Process manager for running multiple services
- **uv** - Fast Python package manager
- **npm** - Node package manager

## Quick Start

Get the template running in under 5 minutes:

```bash
# 1. Clone and enter directory
git clone https://github.com/larryhudson/claude-code-dev-starter.git
cd claude-code-dev-starter

# 2. Install dependencies (requires uv and node)
uv sync
cd frontend && npm install && cd ..

# 3. Set up environment
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# 4. Start the application
make dev
```

Visit http://localhost:5173 and start chatting with the AI agent!

## Getting Started

### Prerequisites

```bash
# Install uv (Python package manager)
# On macOS
brew install uv

# On Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install hivemind (for process management)
# On macOS
brew install hivemind

# On Linux - see https://github.com/DarthSim/hivemind

# Install Node.js (for frontend)
# On macOS
brew install node

# On Linux - see https://nodejs.org/
```

### Installation

```bash
# Clone the repository
git clone https://github.com/larryhudson/claude-code-dev-starter.git
cd claude-code-dev-starter

# Install Python dependencies
uv sync

# Install frontend dependencies
cd frontend && npm install && cd ..

# Set up pre-commit hooks
uv run pre-commit install

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### Running the Application

```bash
# Start both backend and frontend (uses hivemind)
make dev

# In another terminal, view live logs
make dev-logs

# When done, stop the server
make stop-dev
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## How It Works

### Architecture Overview

This template uses a modern full-stack architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  - Chat interface with streaming responses                   │
│  - Tool call visualization and state tracking               │
│  - Uses Vercel AI SDK's useChat hook                        │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP (POST /api/chat)
                   │ Streaming via SSE
┌──────────────────▼──────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Chat Endpoint (/api/chat)                          │   │
│  │  - Uses VercelAIAdapter for streaming               │   │
│  │  - Routes messages to Pydantic AI Agent             │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │                                        │
│  ┌──────────────────▼──────────────────────────────────┐   │
│  │  Pydantic AI Agent                                   │   │
│  │  - Model: claude-sonnet-4-20250514                   │   │
│  │  - System prompt for development assistance          │   │
│  │  - Connected to MCP Server for tools                 │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │                                        │
│  ┌──────────────────▼──────────────────────────────────┐   │
│  │  FastMCP Server (/mcp/mcp)                           │   │
│  │  - get_project_info() - Returns tech stack & metadata│   │
│  │  - list_available_commands() - Returns make commands │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

1. **User Input**: User types a message in the React chat interface
2. **Streaming Request**: Frontend sends POST to `/api/chat` with conversation history
3. **Agent Processing**: Pydantic AI agent receives message and decides whether to:
   - Respond directly with text
   - Call one or more MCP tools to gather information
   - Return a combination of tool calls and text
4. **Tool Execution**: If tools are needed, agent calls MCP server endpoints
5. **Streaming Response**: Response streams back to frontend via Server-Sent Events (SSE)
6. **UI Rendering**: React components render text and visualize tool calls with expandable JSON views

### MCP (Model Context Protocol) Integration

The agent connects to tools via the MCP protocol:

- **Connection**: HTTP-based MCP server at `http://localhost:8000/mcp/mcp`
- **Tool Discovery**: Agent automatically discovers available tools from the MCP server
- **Type Safety**: Tools are defined with Pydantic models for input/output validation
- **Extensibility**: Add new tools by decorating functions with `@mcp.tool()` in `app/mcp_server.py`

### Development Workflow with Claude Code

When working with Claude Code, the integrated hooks provide real-time feedback:

1. **File Edit**: Claude uses the Edit or Write tool to modify code
2. **LSP Check**: Post-edit hook queries LSP bridge for diagnostics
3. **Custom Checks**: Config-driven validation (type-checking, linting) runs automatically
4. **Feedback Loop**: Errors/warnings are provided back to Claude as context
5. **Automatic Fixes**: Claude can immediately fix issues based on the diagnostic feedback

This creates a tight feedback loop that catches issues early and maintains code quality.

## Project Structure

```
.
├── .claude/                          # Claude Code integration
│   ├── settings.json                 # Permissions and hook configuration
│   └── hooks/
│       ├── lsp-bridge.mjs            # LSP bridge daemon (spawns language servers)
│       ├── lsp-servers.yaml          # Language server configuration
│       ├── lsp-diagnostics-check.sh  # PostToolUse hook: queries LSP diagnostics
│       ├── lsp-bridge-stop.sh        # SessionEnd hook: stops LSP bridge
│       ├── post-tool-use.py          # PostToolUse hook: config-driven checks
│       └── session-start.sh          # SessionStart hook: env setup + LSP start
│
├── app/                              # FastAPI backend
│   ├── main.py                       # FastAPI app with MCP mounting
│   ├── chat.py                       # Chat endpoint with Vercel AI adapter
│   ├── agent.py                      # Pydantic AI agent definition
│   └── mcp_server.py                 # FastMCP tool definitions
│
├── frontend/                         # React application
│   ├── src/
│   │   ├── App.tsx                   # Main chat interface
│   │   ├── components/
│   │   │   ├── ai-elements/          # Chat UI components
│   │   │   └── ui/                   # Reusable UI components
│   │   └── main.tsx                  # React entry point
│   ├── package.json                  # Frontend dependencies
│   └── vite.config.ts                # Build configuration
│
├── evals/                            # Agent evaluation framework
│   ├── test_evals.py                 # Pytest test entry point
│   ├── tasks/
│   │   └── agent_task.py             # Agent execution wrapper
│   ├── graders/
│   │   ├── code_based.py             # Deterministic evaluators
│   │   └── llm_based.py              # LLM-based judges
│   ├── datasets/
│   │   └── tool_usage.yaml           # Test case definitions
│   └── README.md                     # Evaluation guide
│
├── .github/workflows/                # CI/CD automation
│   └── ci.yaml                       # GitHub Actions pipeline
│
├── .post-claude-edit-config.yaml     # Post-edit check configuration
├── .pre-commit-config.yaml           # Pre-commit hook configuration
├── Makefile                          # Development commands
├── Procfile                          # Hivemind process definitions
├── pyproject.toml                    # Python project config
├── CLAUDE.md                         # Claude Code guidelines
└── AGENTS.md                         # Agent workflow instructions
```

## Development Commands

### General

```bash
make dev          # Start backend and frontend
make dev-logs     # View live development logs
make stop-dev     # Stop the development server
```

### Python

```bash
make lint         # Lint Python files with ruff
make format       # Format Python files with ruff
make type-check   # Type check with ty
uv run pytest     # Run tests
```

### Frontend

```bash
cd frontend
npm run dev       # Start frontend dev server
npm run build     # Build for production
npm run lint      # Lint TypeScript files
```

### Evaluations

```bash
make evals        # Run agent evaluations
make evals-report # Run evals with detailed report
```

## Claude Code Integration

### Hooks

The project includes hooks that integrate with Claude Code to provide automated feedback and quality checks:

#### PostToolUse Hooks

Executed after Claude uses the Write or Edit tools:

**1. LSP Diagnostics Check** (`.claude/hooks/lsp-diagnostics-check.sh`):
- **Purpose**: Get real-time errors/warnings from language servers
- **Process**:
  - Queries the LSP bridge daemon via Unix socket
  - Requests diagnostics for the modified file
  - Parses LSP response and formats errors/warnings
- **Timeout**: 20 seconds
- **Output**: Returns diagnostics as context to Claude
- **File types**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`

**2. Config-Driven Checks** (`.claude/hooks/post-tool-use.py`):
- **Purpose**: Run additional validation based on file patterns
- **Configuration**: `.post-claude-edit-config.yaml`
- **Timeout**: 30 seconds
- **Configured checks**:
  - **Python type-check**: Runs `ty check` on `.py` files (enabled)
  - **Frontend lint**: Runs `oxlint` on `.ts`, `.tsx`, `.js`, `.jsx` files (enabled)
  - **Python format/lint**: Runs `ruff check` on `.py` files (disabled by default)

**Adding custom checks:**

Edit `.post-claude-edit-config.yaml`:

```yaml
checks:
  - name: "my-custom-check"
    patterns: ['*.py']  # Glob patterns
    command: 'uv run mycheck {file}'  # {file} is replaced with file path
    enabled: true
    timeout: 10  # Optional, seconds
```

#### SessionStart Hook

Executed when a Claude Code session begins (`.claude/hooks/session-start.sh`):

1. **Install jq**: Required for JSON parsing (if not present)
2. **Check hivemind**: Warns if not installed (needed for `make dev`)
3. **Install dependencies**:
   - `npm install` in frontend directory
   - Note about pre-commit (requires uv)
4. **Start LSP bridge**: Spawns the daemon in the background
5. **Provide context**: Shows available commands and configuration

#### SessionEnd Hook

Executed when a Claude Code session ends (`.claude/hooks/lsp-bridge-stop.sh`):

- Gracefully shuts down the LSP bridge daemon
- Cleans up Unix socket files
- Ensures language servers are properly terminated

#### Hook Best Practices

- **Keep hooks fast**: Use timeouts to avoid blocking Claude
- **Provide actionable feedback**: Return clear error messages Claude can understand
- **Test hooks independently**: Run them manually to debug issues
- **Log for debugging**: Hooks can write to `.claude/hooks/*.log` files

### LSP Bridge

The LSP bridge daemon (`.claude/hooks/lsp-bridge.mjs`) provides real-time diagnostics by running language servers in the background. It is started automatically by the SessionStart hook and queried after every file edit.

**How it works:**

1. **Startup**: The SessionStart hook spawns the bridge as a Node.js daemon
2. **Server Management**: Bridge starts configured language servers and communicates via LSP JSON-RPC
3. **HTTP API**: Exposes diagnostics via HTTP over a Unix socket
4. **Post-Edit**: After Claude modifies files, the PostToolUse hook queries the bridge
5. **Feedback**: Diagnostics (errors/warnings) are provided back to Claude as context
6. **Auto-Fix**: Claude can immediately address issues based on diagnostic feedback

**Configured language servers** (in `.claude/hooks/lsp-servers.yaml`):
- **TypeScript** (`typescript-language-server`) - for `.ts`, `.tsx`, `.js`, `.jsx` files
  - Provides type checking, IntelliSense, and error detection
  - Searches `frontend/node_modules/.bin` for the binary
- **Python** (`ruff server`) - for `.py`, `.pyi` files
  - Fast linting and error detection using Ruff
  - Searches project root and `$HOME/.local/bin`
- **Go** (`gopls`) - for `.go` files (if `go.mod` exists)
  - Official Go language server
  - Provides type checking and diagnostics

**Debugging the LSP Bridge:**

```bash
# Check bridge health
curl --unix-socket "$(cat .claude/hooks/lsp-bridge.socket)" http://localhost/health

# Request diagnostics for a file
curl --unix-socket "$(cat .claude/hooks/lsp-bridge.socket)" \
  -X POST -H "Content-Type: application/json" \
  -d '{"file":"/absolute/path/to/file.ts"}' \
  http://localhost/diagnostics

# View bridge logs
tail -f .claude/hooks/lsp-bridge.log
```

To add a new language server, add an entry to `lsp-servers.yaml`. See `CLAUDE.md` for the full configuration schema.

### MCP Tools

The FastMCP server (`app/mcp_server.py`) exposes tools that the AI agent can use during conversations:

#### Available Tools

**`get_project_info()`**
- **Purpose**: Returns project metadata and technical information
- **Returns**:
  - Project name: "Claude Code Dev Starter"
  - Description: "A production-ready Python template for Claude Code"
  - Tech stack: FastAPI, FastMCP, Pydantic AI, React, shadcn/ui
- **When to use**: When users ask about project technologies, architecture, or what the project is
- **Example prompts**: "What technologies does this project use?", "What's in the tech stack?"

**`list_available_commands()`**
- **Purpose**: Lists development commands available via Makefile
- **Returns**: Dictionary of command names and descriptions:
  - `make dev` - Start development server
  - `make dev-logs` - View development logs
  - `make lint` - Lint Python files
  - `make format` - Format Python files
  - `make type-check` - Type check Python files
  - `make stop-dev` - Stop the development server
- **When to use**: When users ask how to run, test, or work with the project
- **Example prompts**: "How do I start the server?", "What commands are available?"

#### Adding Your Own Tools

Extend the MCP server by adding tool functions to `app/mcp_server.py`:

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
def my_custom_tool(param: str) -> dict:
    """
    Description of what this tool does. This docstring becomes
    the tool description that the agent sees.

    Args:
        param: Description of the parameter

    Returns:
        A dictionary with the tool result
    """
    # Your tool logic here
    return {"result": f"Processed: {param}"}
```

**Tool Best Practices**:
- Use clear, descriptive function names
- Write detailed docstrings (the agent sees these)
- Use Pydantic models for complex input/output
- Keep tools focused on a single responsibility
- Return structured data (dict/list) rather than plain strings
- Handle errors gracefully with informative messages

## Agent Evaluations

The `evals/` directory contains a comprehensive framework for systematically testing agent behavior. This ensures your AI agent behaves correctly and maintains quality as you make changes.

### Evaluation Framework Structure

```
evals/
├── test_evals.py              # Pytest test entry point
├── tasks/
│   └── agent_task.py          # Agent execution wrapper
├── graders/
│   ├── code_based.py          # Deterministic evaluators
│   └── llm_based.py           # LLM-as-judge evaluators
└── datasets/
    └── tool_usage.yaml        # Test case definitions
```

### Running Evaluations

```bash
# Run all evaluations
make evals

# Run with detailed report
make evals-report

# Run specific test suite
uv run pytest evals/test_evals.py::test_tool_usage_eval

# Run with verbose output
uv run pytest evals/ -v

# Run tests matching a pattern
uv run pytest evals/ -k "should_use_tools"
```

### What Gets Tested

The template includes 10 pre-configured test cases in `datasets/tool_usage.yaml`:

**Tool Usage Tests (6 cases)** - Verify agent correctly uses tools when appropriate:
- Project information queries ("What technologies does this project use?")
- Project name queries ("What is the name of this project?")
- Tech stack queries ("What's in the tech stack?")
- Command queries ("How do I start the development server?")
- Specific command lookup ("What command do I run to lint?")
- General command listing ("What make commands are available?")

**Tool Restraint Tests (4 cases)** - Verify agent doesn't use tools unnecessarily:
- General Python questions ("What is a Python decorator?")
- General coding questions ("How do I write a for loop in JavaScript?")
- Conceptual questions ("What is the difference between REST and GraphQL?")
- Best practices ("What are some best practices for clean code?")

### Evaluation Types

**Code-Based Graders** (`graders/code_based.py`):
- **`UsedExpectedTool(tool_name)`**: Verifies a specific tool was called
- **`ResponseContains(substring)`**: Checks response includes expected content
- **`NoToolsCalled()`**: Validates no tools were used (for general knowledge questions)

Example:
```python
graders=[
    UsedExpectedTool("get_project_info"),
    ResponseContains("FastAPI")
]
```

**LLM-Based Judges** (`graders/llm_based.py`):
- **`accuracy_judge`**: Evaluates factual correctness of responses
- **`helpfulness_judge`**: Checks if responses are actionable and clear
- **`safety_judge`**: Verifies appropriate refusals of harmful requests
- **`tool_appropriateness_judge`**: Validates tool usage decisions

These use Claude itself as a judge to evaluate subjective qualities.

### Test Configuration

Each test case in `tool_usage.yaml` has:
- **`input`**: The user message to test
- **`expected_tools`**: List of tools that should be called (optional)
- **`graders`**: List of evaluation criteria
- **`metadata`**: Tags for organizing tests (e.g., `should_use_tool`)

Example:
```yaml
- input: "What technologies does this project use?"
  expected_tools: ["get_project_info"]
  graders:
    - UsedExpectedTool(expected_tool="get_project_info")
    - ResponseContains(expected_substring="FastAPI")
  metadata:
    should_use_tool: true
```

### Success Criteria

- **Overall pass rate**: 80% minimum (configurable in `test_tool_usage_eval`)
- **Tool usage tests**: Agent should call the expected tools
- **Tool restraint tests**: Agent should respond directly without tools
- **Response quality**: Responses should be accurate, helpful, and safe

### Extending the Evaluation Suite

Add new test cases to `datasets/tool_usage.yaml`:

```yaml
- input: "Your test prompt here"
  expected_tools: ["tool_name"]  # Optional
  graders:
    - UsedExpectedTool(expected_tool="tool_name")
    - ResponseContains(expected_substring="expected text")
  metadata:
    category: "your_category"
    should_use_tool: true
```

Create custom graders in `graders/code_based.py` or `graders/llm_based.py` for specialized validation logic.

See [evals/README.md](evals/README.md) for detailed documentation on building evaluations.

## Customization

### Adding MCP Tools

Edit `app/mcp_server.py` to add new tools:

```python
@mcp.tool()
def my_custom_tool(param: str) -> str:
    """Description of what this tool does."""
    return f"Result: {param}"
```

### Adding Post-Edit Checks

Edit `.post-claude-edit-config.yaml`:

```yaml
checks:
  - name: my-check
    patterns: ['*.py']
    command: 'uv run my-check {file}'
    enabled: true
```

### Adding Dependencies

Python (edit `pyproject.toml`):
```bash
uv add package-name
uv add --dev dev-package-name
```

Frontend (in `frontend/` directory):
```bash
npm install package-name
npm install --save-dev dev-package-name
```

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yaml`) runs:

1. **Lint**: Python code style with ruff
2. **Type-check**: Python types with ty
3. **Evaluations**: Agent behavior tests with pydantic-evals

Triggered on pushes to main/develop and pull requests.

## Troubleshooting

### Common Issues

#### Port Already in Use

If you see `Address already in use` errors:

```bash
# Check what's using port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Check what's using port 5173 (frontend)
lsof -ti:5173 | xargs kill -9

# Or use the stop command
make stop-dev
```

#### Pre-commit Hook Failures

If pre-commit hooks fail during git commit:

```bash
# Ensure pre-commit is installed
uv run pre-commit install

# Run hooks manually to see detailed errors
uv run pre-commit run --all-files

# Update hooks to latest versions
uv run pre-commit autoupdate
```

#### LSP Bridge Not Starting

If the LSP bridge daemon fails to start:

```bash
# Check the bridge log
cat .claude/hooks/lsp-bridge.log

# Verify Node.js is installed
node --version  # Should be v18+

# Manually test the bridge
node .claude/hooks/lsp-bridge.mjs
```

#### Type Server Not Found

If you see "typescript-language-server not found":

```bash
# Install frontend dependencies
cd frontend && npm install

# The language server is in node_modules/.bin/
ls frontend/node_modules/.bin/typescript-language-server
```

#### Python Type Check Fails

If `ty` type checking reports errors:

```bash
# Run type check manually to see full output
uv run ty check .

# Type errors are often due to missing type stubs
uv add --dev types-<package-name>
```

#### Agent Not Using Tools

If the agent isn't calling MCP tools:

1. **Check MCP server is running**: Visit http://localhost:8000/docs
2. **Verify tool connection**: Check `app/agent.py` - should connect to `http://localhost:8000/mcp/mcp`
3. **Test tools directly**: Use the FastAPI docs interface to test MCP endpoints
4. **Check agent logs**: Backend logs will show tool calls and errors

#### Evaluation Tests Failing

If agent evaluations fail:

```bash
# Run with verbose output to see details
uv run pytest evals/ -v -s

# Run a single test to debug
uv run pytest evals/test_evals.py::test_tool_usage_eval -v

# Check if ANTHROPIC_API_KEY is set
echo $ANTHROPIC_API_KEY
```

#### Frontend Build Errors

If the frontend fails to build:

```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors
npm run type-check
```

### Getting Help

- **Claude Code Documentation**: https://docs.claude.com/en/docs/claude-code/
- **Issues**: Report bugs at https://github.com/larryhudson/claude-code-dev-starter/issues
- **Pydantic AI Docs**: https://ai.pydantic.dev/
- **FastMCP Guide**: https://github.com/jlowin/fastmcp

## Learn More

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/)
- [Pydantic AI](https://ai.pydantic.dev/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Vercel AI SDK](https://sdk.vercel.ai/)
- [Hivemind](https://github.com/DarthSim/hivemind)

## License

This template is provided as-is for use with Claude Code projects.
