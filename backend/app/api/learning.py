"""
Learning Platform API Router.
Dedicated REST endpoints for subject selection, verified learning resources,
personalized roadmap generation, topic content, progress tracking, and EduMind AI tutoring.
"""

from fastapi import APIRouter, Header, Query, HTTPException, Body
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from ..services.learning_service import learning_service
from ..services.student_service import student_service

router = APIRouter(prefix="/api/learning", tags=["Learning Agent & Platform"])
edumind_router = APIRouter(prefix="/api/edumind", tags=["EduMind AI Tutor"])


# --- Request & Response Models ---
class LearningPlanRequest(BaseModel):
    subject: str
    level: Optional[str] = "Beginner"
    goal: Optional[str] = "Career"
    daily_minutes: Optional[int] = 60
    days_per_week: Optional[int] = 5
    deadline: Optional[str] = None


class ProgressRecordRequest(BaseModel):
    subject: str
    topic: str
    status: Optional[str] = "Completed"
    time_spent_minutes: Optional[int] = 45
    quiz_score: Optional[int] = None


class EduMindChatRequest(BaseModel):
    message: str
    subject: str
    topic: str
    level: Optional[str] = "Beginner"
    goal: Optional[str] = "Career"
    action_type: Optional[str] = None


# --- Endpoints ---

@router.get("/subjects")
def get_subjects(category: Optional[str] = Query(None)):
    """Retrieve all available subjects or filter by category."""
    return learning_service.get_subjects(category)


@router.get("/subjects/{subject_id}")
def get_subject_details(subject_id: str):
    """Retrieve detailed subject metadata and prerequisite tracks."""
    return learning_service.get_subject_details(subject_id)


@router.get("/resources/{subject_id}")
def get_subject_resources(subject_id: str):
    """Retrieve curated, verified external learning references for a subject."""
    return {
        "subject": subject_id,
        "resources": learning_service.get_resources_for_subject(subject_id)
    }


@router.post("/plan")
def create_learning_plan(
    req: LearningPlanRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """Generate or customize a structured learning plan with weekly roadmap and daily breakdown."""
    user_id = x_user_id or "chitra_demo_user"
    return learning_service.generate_personalized_plan(
        user_id=user_id,
        subject=req.subject,
        level=req.level or "Beginner",
        goal=req.goal or "Career",
        daily_minutes=req.daily_minutes or 60,
        days_per_week=req.days_per_week or 5,
        deadline=req.deadline
    )


@router.get("/plan")
def get_learning_plan(
    subject: Optional[str] = Query(None),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """Retrieve active learning plan for the current user and subject."""
    user_id = x_user_id or "chitra_demo_user"
    profile = student_service.get_or_create_profile(user_id)
    target_subj = subject or profile.get("current_learning_subject", "Python")
    
    return learning_service.generate_personalized_plan(
        user_id=user_id,
        subject=target_subj,
        level="Beginner",
        goal=profile.get("career_goal", "Career")
    )


@router.get("/topic-content")
def get_topic_content(
    subject: str = Query(...),
    topic: str = Query(...),
    level: Optional[str] = Query("Beginner")
):
    """Fetch structured topic explanation, key points, examples, practice, and 5-question diagnostic quiz."""
    return learning_service.get_topic_content(subject, topic, level)


@router.post("/progress")
def record_topic_progress(
    req: ProgressRecordRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """Save completed topic into MongoDB Atlas, update student profile, streak, and unlocked topics."""
    user_id = x_user_id or "chitra_demo_user"
    return learning_service.update_progress(
        user_id=user_id,
        subject=req.subject,
        topic_title=req.topic,
        status=req.status or "Completed",
        time_spent_minutes=req.time_spent_minutes or 45,
        quiz_score=req.quiz_score
    )


@router.get("/progress")
def get_progress_summary(
    subject: Optional[str] = Query(None),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """Get overall completion percentage, active streak, and completed topics list."""
    user_id = x_user_id or "chitra_demo_user"
    return learning_service.get_user_progress_summary(user_id, subject)


@edumind_router.post("/chat")
async def edumind_doubt_chat(
    req: EduMindChatRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """Ask EduMind AI Assistant contextual questions about the active topic and subject."""
    user_id = x_user_id or "chitra_demo_user"
    return await learning_service.answer_edumind_doubt(
        user_id=user_id,
        message=req.message,
        subject=req.subject,
        topic=req.topic,
        level=req.level or "Beginner",
        goal=req.goal or "Career",
        action_type=req.action_type
    )
