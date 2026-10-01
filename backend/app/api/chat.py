"""
Chat API Router for EduMind Main Agent.
Receives user messages, executes multi-agent LangGraph workflow, manages memory, and returns rich activity stream.
"""

from fastapi import APIRouter, HTTPException, Header, Query
from typing import Optional, Dict, Any
from ..database.models import ChatRequest, ChatResponse
from ..agents.main_agent import main_agent

router = APIRouter(prefix="/api/chat", tags=["Agent Chat"])


@router.post("", response_model=ChatResponse)
async def chat_with_edumind(
    request: ChatRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    try:
        response = await main_agent.process_message(user_id=user_id, request=request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing error: {str(e)}")
