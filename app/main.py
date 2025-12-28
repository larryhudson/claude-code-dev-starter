from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.chat import router as chat_router
from app.mcp_server import mcp

# Create MCP ASGI app
mcp_app = mcp.http_app()


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

# Mount MCP server (will be accessible at /mcp/mcp due to internal path)
app.mount("/mcp", mcp_app)

# Include chat router
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Claude Code Dev Starter API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
