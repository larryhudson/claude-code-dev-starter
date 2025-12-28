# Implementation Plan: Full-Stack Chat Application

This plan adds a React frontend with shadcn/ui, an MCP server with FastMCP, and a chat interface using Pydantic AI with the Vercel AI SDK.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Vite + React)                  │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │   shadcn/ui     │    │  Chat Interface (useChat hook)      │ │
│  │   components    │    │  - Streams messages from /api/chat  │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                           │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │  MCP Server     │    │  Chat Endpoint (/api/chat)          │ │
│  │  (FastMCP)      │    │  - Pydantic AI Agent                │ │
│  │  mounted at     │    │  - VercelAIAdapter for streaming    │ │
│  │  /mcp           │    │  - SSE response to frontend         │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Frontend Setup (Vite + React + shadcn/ui + oxlint)

### 1.1 Create Vite Project

```bash
cd /root/github.com/larryhudson/claude-code-dev-starter
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

### 1.2 Install Tailwind CSS v4

```bash
npm install tailwindcss @tailwindcss/vite
```

Update `frontend/src/index.css`:
```css
@import "tailwindcss";
```

### 1.3 Configure Vite with Path Aliases

Install Node types:
```bash
npm install -D @types/node
```

Update `frontend/vite.config.ts`:
```typescript
import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
      '/mcp': 'http://localhost:8000',
    },
  },
})
```

Update `frontend/tsconfig.json` and `frontend/tsconfig.app.json`:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### 1.4 Initialize shadcn/ui

```bash
npx shadcn@latest init
```

Select:
- Style: Default
- Base color: Neutral
- CSS variables: Yes

### 1.5 Add Required shadcn Components

```bash
npx shadcn@latest add button input card scroll-area avatar
```

### 1.6 Install oxlint

```bash
npm install -D oxlint
```

Create `frontend/.oxlintrc.json`:
```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["import", "typescript", "react"],
  "env": {
    "browser": true,
    "es2024": true
  },
  "rules": {
    "eqeqeq": "warn",
    "no-console": "warn",
    "react/no-unknown-property": "error"
  }
}
```

Add scripts to `frontend/package.json`:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "oxlint",
    "preview": "vite preview"
  }
}
```

### 1.7 Install Vercel AI SDK

```bash
npm install @ai-sdk/react
```

**Sources:**
- [shadcn/ui Vite Installation](https://ui.shadcn.com/docs/installation/vite)
- [Oxlint Configuration](https://oxc.rs/docs/guide/usage/linter/config.html)
- [Oxlint Getting Started](https://betterstack.com/community/guides/scaling-nodejs/oxlint-explained/)

---

## Phase 2: Backend Setup (FastMCP + Pydantic AI)

### 2.1 Add Python Dependencies

Update `pyproject.toml`:
```toml
[project]
dependencies = [
    "fastapi[standard]>=0.120.0",
    "uvicorn[standard]>=0.38.0",
    "fastmcp>=2.0.0",
    "pydantic-ai[openai]>=0.2.0",
]
```

Run:
```bash
uv sync
```

### 2.2 Create MCP Server

Create `app/mcp_server.py`:
```python
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
```

### 2.3 Create Pydantic AI Agent

Create `app/agent.py`:
```python
from pydantic_ai import Agent

agent = Agent(
    "openai:gpt-4o",
    system_prompt="""You are a helpful assistant for a software development project.
    You can help with coding questions, explain concepts, and assist with development tasks.
    Be concise and helpful in your responses.""",
)
```

### 2.4 Create Chat Endpoint

Create `app/chat.py`:
```python
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from pydantic_ai.ui.vercel_ai import VercelAIAdapter

from app.agent import agent

router = APIRouter()


@router.post("/api/chat")
async def chat(request: Request) -> Response:
    """Chat endpoint that streams responses using Vercel AI protocol."""
    return await VercelAIAdapter.dispatch_request(request, agent=agent)
```

### 2.5 Update Main Application

Update `app/main.py`:
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.chat import router as chat_router
from app.mcp_server import mcp


# Create MCP ASGI app
mcp_app = mcp.http_app(path="/mcp")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Combined lifespan for FastAPI and MCP."""
    async with mcp_app.lifespan(app):
        yield


app = FastAPI(
    title="Claude Code Dev Starter API",
    lifespan=lifespan,
)

# CORS for frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount MCP server
app.mount("/mcp", mcp_app)

# Include chat router
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Claude Code Dev Starter API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Sources:**
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [FastMCP FastAPI Integration](https://gofastmcp.com/integrations/fastapi)
- [Pydantic AI Vercel AI Adapter](https://ai.pydantic.dev/ui/vercel-ai/)
- [Pydantic AI Vercel AI API Reference](https://ai.pydantic.dev/api/ui/vercel_ai/)

---

## Phase 3: Chat Interface

### 3.1 Install AI Elements

Use Vercel's AI Elements library for pre-built chat components:

```bash
npx ai-elements@latest add conversation
npx ai-elements@latest add message
npx ai-elements@latest add prompt-input
```

This installs production-ready components to `src/components/ai-elements/`.

### 3.2 Update App.tsx

Update `frontend/src/App.tsx` to use AI Elements with useChat:
```tsx
import { useChat } from "@ai-sdk/react"
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation"
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message"
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputFooter,
  PromptInputSubmit,
} from "@/components/ai-elements/prompt-input"
import { Card } from "@/components/ui/card"
import { MessageCircle } from "lucide-react"

function App() {
  const { messages, handleSubmit, status, input, setInput } = useChat({
    api: "/api/chat",
  })

  const isLoading = status === "streaming" || status === "submitted"

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="flex flex-col h-[600px] w-full max-w-2xl">
        <div className="p-4 border-b">
          <h2 className="text-lg font-semibold">Chat</h2>
        </div>

        <Conversation className="flex-1">
          <ConversationContent>
            {messages.length === 0 ? (
              <ConversationEmptyState
                title="Start a conversation"
                description="Send a message to begin chatting with the AI assistant"
                icon={<MessageCircle className="size-8" />}
              />
            ) : (
              messages.map((message) => (
                <Message key={message.id} from={message.role}>
                  <MessageContent>
                    {message.role === "assistant" ? (
                      <MessageResponse>{message.content}</MessageResponse>
                    ) : (
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    )}
                  </MessageContent>
                </Message>
              ))
            )}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>

        <div className="p-4 border-t">
          <PromptInput
            onSubmit={({ text }, event) => {
              handleSubmit(event, { data: { message: text } })
            }}
          >
            <PromptInputTextarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              disabled={isLoading}
            />
            <PromptInputFooter>
              <div />
              <PromptInputSubmit status={status} disabled={isLoading} />
            </PromptInputFooter>
          </PromptInput>
        </div>
      </Card>
    </div>
  )
}

export default App
```

**Sources:**
- [Vercel AI SDK useChat Reference](https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat)
- [Vercel AI SDK Introduction](https://ai-sdk.dev/docs/introduction)
- [AI SDK 5 Blog Post](https://vercel.com/blog/ai-sdk-5)

---

## Phase 4: Development Workflow Updates

### 4.1 Update Procfile

```procfile
backend: uv run fastapi dev app/main.py
frontend: cd frontend && npm run dev
```

### 4.2 Update Makefile

Add new targets:
```makefile
# Frontend commands
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

frontend-lint:
	cd frontend && npm run lint

# Combined dev (requires hivemind)
dev:
	hivemind Procfile
```

### 4.3 Update Post-Claude-Edit Config

Add frontend linting to `.post-claude-edit-config.yaml`:
```yaml
checks:
  - name: lint-python
    patterns: ['*.py', 'app/**/*.py']
    command: 'uv run ruff check --fix {file}'
    enabled: true

  - name: format-python
    patterns: ['*.py', 'app/**/*.py']
    command: 'uv run ruff format {file}'
    enabled: true

  - name: type-check-python
    patterns: ['*.py', 'app/**/*.py']
    command: 'uv run ty check {file}'
    enabled: true

  - name: lint-frontend
    patterns: ['frontend/**/*.ts', 'frontend/**/*.tsx']
    command: 'cd frontend && npx oxlint {file}'
    enabled: true
```

### 4.4 Update CI Workflow

Update `.github/workflows/ci.yaml` to include frontend checks:
```yaml
jobs:
  lint-python:
    # ... existing Python lint job

  lint-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      - run: cd frontend && npm install
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run build
```

---

## Phase 5: Environment Configuration

### 5.1 Create Environment Files

Create `.env.example`:
```env
# OpenAI API Key (required for Pydantic AI)
OPENAI_API_KEY=sk-...

# Optional: Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-...
```

Create `frontend/.env.example`:
```env
# API URL (for production builds)
VITE_API_URL=http://localhost:8000
```

### 5.2 Update .gitignore

Add:
```gitignore
# Environment files
.env
.env.local

# Frontend
frontend/node_modules/
frontend/dist/
```

---

## File Structure After Implementation

```
.
├── .claude/                          # Claude Code hooks
├── .github/workflows/
│   └── ci.yaml                       # Updated with frontend jobs
├── app/
│   ├── __init__.py
│   ├── main.py                       # Updated with MCP + chat
│   ├── agent.py                      # Pydantic AI agent
│   ├── chat.py                       # Chat endpoint
│   └── mcp_server.py                 # FastMCP server
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                   # shadcn components
│   │   │   └── chat/
│   │   │       ├── Chat.tsx
│   │   │       ├── ChatMessage.tsx
│   │   │       └── ChatInput.tsx
│   │   ├── lib/
│   │   │   └── utils.ts              # shadcn utils
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── .oxlintrc.json
│   ├── components.json               # shadcn config
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   └── vite.config.ts
├── .env.example
├── .post-claude-edit-config.yaml     # Updated with frontend checks
├── Makefile                          # Updated with frontend targets
├── Procfile                          # Updated with frontend process
├── pyproject.toml                    # Updated with new deps
└── README.md
```

---

## Implementation Order

1. **Phase 1**: Set up frontend with Vite, Tailwind, shadcn/ui, and oxlint
2. **Phase 2**: Add FastMCP and Pydantic AI to backend
3. **Phase 3**: Build chat interface components
4. **Phase 4**: Update development workflow (Makefile, Procfile, CI)
5. **Phase 5**: Add environment configuration

---

## Testing the Implementation

### Start Development Servers

```bash
# Terminal 1: Backend
uv run fastapi dev app/main.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

Or with hivemind:
```bash
make dev
```

### Test Endpoints

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- MCP Server: http://localhost:8000/mcp
- Chat API: POST http://localhost:8000/api/chat
- Health Check: http://localhost:8000/health

### Test Chat Flow

1. Open http://localhost:5173
2. Type a message in the chat input
3. See streaming response from the AI agent

---

## Additional Considerations

### API Key Setup
You'll need an `OPENAI_API_KEY` environment variable for Pydantic AI to work. Create a `.env` file:
```bash
export OPENAI_API_KEY=sk-...
```

### Switching AI Providers
Pydantic AI supports multiple providers. To use Anthropic instead:
```python
agent = Agent("anthropic:claude-sonnet-4-20250514", ...)
```

### MCP Tool Integration
The MCP server can be extended with more tools that the AI agent can use. Consider connecting the agent to the MCP tools for a more integrated experience.

---

## Sources

### Frontend
- [shadcn/ui Vite Installation](https://ui.shadcn.com/docs/installation/vite)
- [Oxlint Documentation](https://oxc.rs/docs/guide/usage/linter)
- [Oxlint Configuration](https://oxc.rs/docs/guide/usage/linter/config.html)
- [Vercel AI SDK useChat](https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat)
- [AI SDK Introduction](https://ai-sdk.dev/docs/introduction)

### Backend
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [FastMCP FastAPI Integration](https://gofastmcp.com/integrations/fastapi)
- [Pydantic AI Vercel AI Adapter](https://ai.pydantic.dev/ui/vercel-ai/)
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
