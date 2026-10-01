"""
Planning API Router.
Endpoints for STRIPS-style classical AI action planning.
"""

from fastapi import APIRouter, Body
from typing import Dict, List, Any, Optional, Set
from pydantic import BaseModel
from ..planning.planner import strips_planner

router = APIRouter(prefix="/api/planning", tags=["AI Planning"])


class PlanGenerateRequest(BaseModel):
    initial_state: List[str] = ["knows_python_basics"]
    goal_state: List[str] = ["ai_engineer_certified", "mock_interview_passed"]


@router.post("/generate")
def generate_strips_plan(req: PlanGenerateRequest):
    return strips_planner.generate_plan(
        initial_state=set(req.initial_state),
        goal_state=set(req.goal_state)
    )
