"""
Long-Term Memory module for EduAgent.
Provides persistent storage, querying, indexing, and updating of student profile,
career goals, skills, weaknesses, study preferences, interview scores, and episodic memories.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import logging
from ..database.mongodb import db_manager
from ..database.models import MemoryItem

logger = logging.getLogger("edumind.memory.long_term")


class LongTermMemory:
    """Manages persistent long-term storage in the 'memory' collection."""
    
    def __init__(self):
        self.db = db_manager

    def save_memory(
        self,
        user_id: str,
        memory_type: str,
        content: str,
        importance: float = 0.8,
        source: str = "chat_interaction",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store a new memory item or update existing memory item of same category.
        Handles deduplication and contradiction resolution.
        """
        # Check if updating an existing unique memory_type like career_goal or preference
        unique_types = ["career_goal", "study_preference_time", "academic_year", "branch"]
        if memory_type in unique_types:
            existing = self.db.memory.find_one({"user_id": user_id, "memory_type": memory_type})
            if existing:
                self.db.memory.update_one(
                    {"user_id": user_id, "memory_type": memory_type},
                    {
                        "$set": {
                            "content": content,
                            "importance": importance,
                            "updated_at": datetime.utcnow().isoformat(),
                            "source": source,
                            "metadata": metadata or {}
                        }
                    }
                )
                logger.info(f"Updated long-term memory for user {user_id}: [{memory_type}] -> {content}")
                existing["content"] = content
                existing["importance"] = importance
                return existing

        # Create new memory record
        memory_id = str(uuid.uuid4())
        record = {
            "memory_id": memory_id,
            "id": memory_id,
            "user_id": user_id,
            "memory_type": memory_type,
            "content": content,
            "importance": float(importance),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "source": source,
            "metadata": metadata or {}
        }
        self.db.memory.insert_one(record)
        logger.info(f"Saved new long-term memory for user {user_id}: [{memory_type}] -> {content}")
        return record

    def get_all_memories(self, user_id: str, min_importance: float = 0.0) -> List[Dict[str, Any]]:
        """Retrieve all long-term memories for a student, filtered by minimum importance."""
        memories = self.db.memory.find({"user_id": user_id})
        return [m for m in memories if m.get("importance", 0.0) >= min_importance]

    def get_memories_by_type(self, user_id: str, memory_type: str) -> List[Dict[str, Any]]:
        """Retrieve memories of a specific category."""
        return self.db.memory.find({"user_id": user_id, "memory_type": memory_type})

    def delete_memory(self, user_id: str, memory_id: str) -> bool:
        """Remove a specific memory item."""
        res = self.db.memory.delete_one({"user_id": user_id, "memory_id": memory_id})
        return res.get("deleted_count", 0) > 0

    def clear_user_memories(self, user_id: str):
        """Clear all memories for a user."""
        self.db.memory.delete_many({"user_id": user_id})

    def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Return memory breakdown statistics."""
        memories = self.get_all_memories(user_id)
        type_counts = {}
        for m in memories:
            t = m.get("memory_type", "general")
            type_counts[t] = type_counts.get(t, 0) + 1
        return {
            "total_memories": len(memories),
            "breakdown": type_counts,
            "last_updated": memories[-1].get("updated_at") if memories else None
        }


# Global long-term memory instance
long_term_memory = LongTermMemory()
