"""
Short-Term Memory module for EduAgent.
Maintains active conversation context, recent dialogue turns, entity references,
and working memory for ongoing sessions.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque


class ShortTermMemory:
    """Manages active short-term session conversation and immediate context buffer."""
    
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        # Store turns per conversation_id
        self._conversations: Dict[str, deque] = {}
        # Working memory variables per conversation
        self._working_memory: Dict[str, Dict[str, Any]] = {}

    def add_turn(self, conversation_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a dialogue turn to the short-term buffer."""
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = deque(maxlen=self.max_turns * 2)
            self._working_memory[conversation_id] = {}

        turn_data = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        self._conversations[conversation_id].append(turn_data)

    def get_recent_turns(self, conversation_id: str, n_turns: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve recent conversation turns up to n_turns (defaults to all buffer)."""
        if conversation_id not in self._conversations:
            return []
        
        history = list(self._conversations[conversation_id])
        if n_turns:
            return history[-(n_turns * 2):]
        return history

    def get_formatted_dialogue(self, conversation_id: str, n_turns: int = 5) -> str:
        """Get formatted conversation string for prompt injection."""
        turns = self.get_recent_turns(conversation_id, n_turns)
        if not turns:
            return "No previous turns in current session."
        
        formatted = []
        for turn in turns:
            role_label = "Student" if turn["role"] == "user" else "EduMind"
            formatted.append(f"{role_label}: {turn['content']}")
        return "\n".join(formatted)

    def set_working_variable(self, conversation_id: str, key: str, value: Any):
        """Set a variable in current session working memory."""
        if conversation_id not in self._working_memory:
            self._working_memory[conversation_id] = {}
        self._working_memory[conversation_id][key] = value

    def get_working_variable(self, conversation_id: str, key: str, default: Any = None) -> Any:
        """Get a working variable from session memory."""
        return self._working_memory.get(conversation_id, {}).get(key, default)

    def get_working_context(self, conversation_id: str) -> Dict[str, Any]:
        """Get all working memory context for session."""
        return self._working_memory.get(conversation_id, {}).copy()

    def clear(self, conversation_id: str):
        """Clear short-term memory for a conversation."""
        if conversation_id in self._conversations:
            self._conversations[conversation_id].clear()
        if conversation_id in self._working_memory:
            self._working_memory[conversation_id].clear()


# Global short-term memory instance
short_term_memory = ShortTermMemory()
