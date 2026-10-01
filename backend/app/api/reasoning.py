"""
Logical Reasoning API Router.
Endpoints for Forward Chaining and Backward Chaining inference over student facts.
"""

from fastapi import APIRouter, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..reasoning.forward_chaining import forward_chaining_engine
from ..reasoning.backward_chaining import backward_chaining_engine
from ..reasoning.rule_engine import get_default_career_rules

router = APIRouter(prefix="/api/reasoning", tags=["Logical Reasoning"])


class ForwardInferRequest(BaseModel):
    facts: Dict[str, Any]


class BackwardInferRequest(BaseModel):
    goal_key: str = "Career_Recommendation"
    goal_value: str = "AI Engineer"
    facts: Dict[str, Any]


@router.post("/forward")
def run_forward_chaining(req: ForwardInferRequest):
    return forward_chaining_engine.infer(initial_facts=req.facts)


@router.post("/backward")
def run_backward_chaining(req: BackwardInferRequest):
    return backward_chaining_engine.evaluate_goal(
        goal_key=req.goal_key,
        goal_value=req.goal_value,
        known_facts=req.facts
    )


@router.get("/rules")
def get_rule_base():
    rules = get_default_career_rules()
    return {"rules": [r.to_dict() for r in rules]}
