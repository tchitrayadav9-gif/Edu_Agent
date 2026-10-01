"""
Memory API Router.
CRUD endpoints for inspecting, adding, updating, and deleting persistent long-term memories.
"""

from fastapi import APIRouter, HTTPException, Header, Path, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from ..memory.long_term_memory import long_term_memory
from ..database.models import MemoryItem

router = APIRouter(prefix="/api/memory", tags=["Memory System"])


class MemoryCreateRequest(BaseModel):
    memory_type: str = "important_fact"
    content: str
    importance: float = 0.8
    source: str = "user_manual"
    metadata: Dict[str, Any] = Field(default_factory=dict)


@router.get("", response_model=List[Dict[str, Any]])
def get_memories(
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    user_id_param: Optional[str] = Query(None, alias="user_id"),
    min_importance: float = 0.0
):
    user_id = user_id_param or x_user_id or "chitra_demo_user"
    return long_term_memory.get_all_memories(user_id=user_id, min_importance=min_importance)


@router.post("", response_model=Dict[str, Any])
def create_memory(
    req: MemoryCreateRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    mem = long_term_memory.save_memory(
        user_id=user_id,
        memory_type=req.memory_type,
        content=req.content,
        importance=req.importance,
        source=req.source,
        metadata=req.metadata
    )
    return mem


@router.delete("/{memory_id}")
def delete_memory(
    memory_id: str = Path(..., description="ID of memory to delete"),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    success = long_term_memory.delete_memory(user_id=user_id, memory_id=memory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memory item not found or unauthorized.")
    return {"message": "Memory successfully deleted", "memory_id": memory_id}


@router.get("/stats")
def get_memory_stats(x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    user_id = x_user_id or "chitra_demo_user"
    return long_term_memory.get_memory_stats(user_id)
