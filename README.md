# Claude Code Dev Starter

A production-ready full-stack template for building AI-powered applications optimized for [Claude Code](https://docs.claude.com/en/docs/claude-code/). This template combines a FastAPI backend with a React frontend, featuring an AI chat interface, MCP tool integration, automated code quality checks, and an agent evaluation framework.

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

The project includes hooks that integrate with Claude Code:

- **PostToolUse Hook** (LSP diagnostics): Queries the LSP bridge daemon after every Write/Edit
  - Returns real-time errors and warnings from language servers as context
  - Supports TypeScript, Python, and Go files

- **PostToolUse Hook** (config-driven checks): Runs additional checks based on `.post-claude-edit-config.yaml`
  - Type-checks Python files with ty
  - Lints frontend files with oxlint

- **SessionStart Hook**: Runs when a Claude Code session starts
  - Installs dependencies (npm, uv sync)
  - Starts the LSP bridge daemon
  - Provides context about available commands

- **SessionEnd Hook**: Runs when a Claude Code session ends
  - Stops the LSP bridge daemon

### LSP Bridge

The LSP bridge daemon (`.claude/hooks/lsp-bridge.mjs`) provides real-time diagnostics by running language servers in the background. It is started automatically by the SessionStart hook and queried after every file edit.

Configured language servers (in `.claude/hooks/lsp-servers.yaml`):
- **TypeScript** (`typescript-language-server`) - for `.ts`, `.tsx`, `.js`, `.jsx` files
- **Python** (`ruff server`) - for `.py` files
- **Go** (`gopls`) - for `.go` files

To add a new language server, add an entry to `lsp-servers.yaml`. See `CLAUDE.md` for the full configuration schema.

### MCP Tools

The FastMCP server exposes tools that the AI agent can use:

- `get_project_info()` - Returns project metadata
- `list_available_commands()` - Returns available make commands

Extend `app/mcp_server.py` to add custom tools.

## Agent Evaluations

The `evals/` directory contains a framework for testing agent behavior:

```bash
# Run all evaluations
make evals

# Run with detailed report
make evals-report

# Run specific tests
uv run pytest evals/ -k "tool_usage"
```

See [evals/README.md](evals/README.md) for detailed documentation.

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

## Learn More

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/)
- [Pydantic AI](https://ai.pydantic.dev/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Vercel AI SDK](https://sdk.vercel.ai/)
- [Hivemind](https://github.com/DarthSim/hivemind)

## License

This template is provided as-is for use with Claude Code projects.

hello world
