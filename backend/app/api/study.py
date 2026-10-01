"""
Study Planning API Router.
Endpoints for generating 30-day curriculum plans, viewing active schedules, and updating topic progress.
"""

from fastapi import APIRouter, Header, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..agents.study_agent import study_agent
from ..services.student_service import student_service
from ..database.mongodb import db_manager

router = APIRouter(prefix="/api/study", tags=["Study Planning"])


class StudyGenerateRequest(BaseModel):
    career_goal: Optional[str] = None
    daily_hours: Optional[float] = 2.0
    preferred_time: Optional[str] = "Evening"


class ProgressUpdateRequest(BaseModel):
    topic: str
    progress: int


@router.post("/generate")
def generate_study_plan(
    req: StudyGenerateRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    profile = student_service.get_or_create_profile(user_id)
    goal = req.career_goal or profile.get("career_goal", "AI Engineer")

    return study_agent.generate_plan_for_student(
        user_id=user_id,
        career_goal=goal,
        skills=profile.get("skills", {}),
        weak_topics=profile.get("weak_topics", []),
        daily_hours=req.daily_hours or 2.0,
        preferred_time=req.preferred_time or "Evening"
    )


@router.get("/progress")
def get_study_progress(x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    user_id = x_user_id or "chitra_demo_user"
    profile = student_service.get_or_create_profile(user_id)
    plans = db_manager.study_plans.find({"user_id": user_id})
    return {
        "learning_progress": profile.get("learning_progress", {}),
        "completed_topics": profile.get("completed_topics", []),
        "active_plan": plans[-1] if plans else None
    }


@router.put("/progress")
def update_study_progress(
    req: ProgressUpdateRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    profile = student_service.get_or_create_profile(user_id)
    lp = profile.get("learning_progress", {})
    lp[req.topic] = max(0, min(100, req.progress))

    completed = profile.get("completed_topics", [])
    if req.progress >= 100 and req.topic not in completed:
        completed.append(req.topic)

    student_service.update_profile(user_id, {
        "learning_progress": lp,
        "completed_topics": completed
    })

    return {"topic": req.topic, "progress": lp[req.topic], "completed_topics": completed}
