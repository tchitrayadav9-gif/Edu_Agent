"""
Student Profile API Router.
Endpoints for student profile retrieval, updating, and knowledge graph visualization.
"""

from fastapi import APIRouter, HTTPException, Header, Body
from typing import Dict, Any, Optional
from ..services.student_service import student_service
from ..knowledge.knowledge_graph import knowledge_graph

router = APIRouter(prefix="/api/student", tags=["Student Management"])


@router.get("/profile", response_model=Dict[str, Any])
def get_profile(x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    user_id = x_user_id or "chitra_demo_user"
    return student_service.get_or_create_profile(user_id)


@router.put("/profile", response_model=Dict[str, Any])
def update_profile(
    updates: Dict[str, Any] = Body(...),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    return student_service.update_profile(user_id, updates)


@router.get("/graph")
def get_student_knowledge_graph(x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    user_id = x_user_id or "chitra_demo_user"
    student_service.get_or_create_profile(user_id)
    return knowledge_graph.get_subgraph_for_student(user_id)
