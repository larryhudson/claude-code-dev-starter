from fastapi import APIRouter
from pydantic_ai.ui.vercel_ai import VercelAIAdapter
from starlette.requests import Request
from starlette.responses import Response

from app.agent import agent

router = APIRouter()


@router.post("/api/chat")
async def chat(request: Request) -> Response:
    """Chat endpoint that streams responses using Vercel AI protocol."""
    return await VercelAIAdapter.dispatch_request(request, agent=agent)
