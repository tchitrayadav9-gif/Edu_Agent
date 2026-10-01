"""
Classical Search API Router.
Endpoints for executing and comparing BFS, DFS, UCS, A*, Hill Climbing, and Beam Search on curriculum graphs.
"""

from fastapi import APIRouter, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..search.path_optimizer import path_optimizer

router = APIRouter(prefix="/api/search", tags=["Classical AI Search"])


class SearchRunRequest(BaseModel):
    start_topic: Optional[str] = "Python Basics"
    goal_topic: Optional[str] = "AI Engineer Mastery"
    algorithm: Optional[str] = "a_star"


@router.post("/run")
def run_search(req: SearchRunRequest):
    return path_optimizer.find_optimal_path(
        start_topic=req.start_topic or "Python Basics",
        goal_topic=req.goal_topic or "AI Engineer Mastery",
        algorithm=req.algorithm or "a_star"
    )


@router.post("/compare")
def compare_all_search_algorithms(req: SearchRunRequest):
    return path_optimizer.run_all_algorithms(
        start_topic=req.start_topic or "Python Basics",
        goal_topic=req.goal_topic or "AI Engineer Mastery"
    )


@router.get("/nodes")
def get_curriculum_nodes():
    return {"nodes": path_optimizer.get_curriculum_nodes()}
