"""
Dashboard API Router.
Compiles aggregate telemetry, student performance metrics, memory counts, and agent activity history.
"""

from fastapi import APIRouter, Header
from typing import Dict, Any, Optional
from ..services.student_service import student_service

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("", response_model=Dict[str, Any])
def get_student_dashboard(x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    user_id = x_user_id or "chitra_demo_user"
    return student_service.get_dashboard_data(user_id)
