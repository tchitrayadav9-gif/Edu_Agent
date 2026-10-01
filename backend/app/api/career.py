"""
Career Guidance API Router.
Endpoints for career suitability analysis, skill gap assessment, and Bayesian ranking.
"""

from fastapi import APIRouter, Header, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..agents.career_agent import career_agent
from ..services.student_service import student_service

router = APIRouter(prefix="/api/career", tags=["Career Guidance"])


class CareerAnalyzeRequest(BaseModel):
    target_role: Optional[str] = "AI Engineer"


@router.post("/analyze")
def analyze_career(
    req: CareerAnalyzeRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    profile = student_service.get_or_create_profile(user_id)
    target_role = req.target_role or profile.get("career_goal", "AI Engineer")
    
    return career_agent.analyze_career_path(
        user_id=user_id,
        target_role=target_role,
        current_skills=profile.get("skills", {}),
        weak_topics=profile.get("weak_topics", [])
    )


@router.post("/skill-gap")
def get_skill_gap(
    req: CareerAnalyzeRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    profile = student_service.get_or_create_profile(user_id)
    target_role = req.target_role or profile.get("career_goal", "AI Engineer")
    
    analysis = career_agent.analyze_career_path(
        user_id=user_id,
        target_role=target_role,
        current_skills=profile.get("skills", {}),
        weak_topics=profile.get("weak_topics", [])
    )
    return {
        "target_role": target_role,
        "skill_gaps": analysis["skill_gaps"],
        "recommended_focus": analysis["recommended_focus"]
    }
