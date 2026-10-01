"""
Interview API Router.
Endpoints for starting adaptive mock interviews, grading answers, and viewing interview history.
"""

from fastapi import APIRouter, Header, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..agents.interview_agent import interview_agent
from ..database.mongodb import db_manager

router = APIRouter(prefix="/api/interview", tags=["Mock Interview"])


class InterviewStartRequest(BaseModel):
    target_role: Optional[str] = "AI Engineer"
    topic: Optional[str] = "Machine Learning"


class InterviewAnswerRequest(BaseModel):
    session_id: str
    answer: str


@router.post("/start")
def start_interview(
    req: InterviewStartRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    return interview_agent.start_session(
        user_id=user_id,
        target_role=req.target_role or "AI Engineer",
        topic=req.topic or "Machine Learning"
    )


@router.post("/answer")
def submit_answer(
    req: InterviewAnswerRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    return interview_agent.evaluate_answer(
        session_id=req.session_id,
        user_id=user_id,
        student_answer=req.answer
    )


@router.get("/history")
def get_interview_history(x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    user_id = x_user_id or "chitra_demo_user"
    return db_manager.interview_sessions.find({"user_id": user_id})
