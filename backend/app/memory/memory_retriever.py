"""
Memory Retriever module for EduAgent.
Ranks and retrieves the most relevant long-term memories for any user query,
factoring in semantic relevance, entity match, recency, and importance weighting.
"""

import re
from typing import List, Dict, Any, Tuple
from datetime import datetime
from .long_term_memory import long_term_memory


class MemoryRetriever:
    """Intelligent memory retrieval and ranking engine."""
    
    def __init__(self):
        self.ltm = long_term_memory

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract search tokens from query string."""
        tokens = re.findall(r'\b\w+\b', text.lower())
        stopwords = {
            "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
            "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
            "to", "was", "were", "will", "with", "i", "my", "me", "what", "should",
            "how", "can", "tell", "show", "please", "about"
        }
        return [t for t in tokens if t not in stopwords and len(t) > 2]

    def _calculate_relevance(self, memory: Dict[str, Any], query_tokens: List[str], raw_query: str) -> float:
        """Calculate multi-factor relevance score between 0.0 and 1.0."""
        content = memory.get("content", "").lower()
        mem_type = memory.get("memory_type", "").lower()
        importance = float(memory.get("importance", 0.5))
        
        # 1. Exact query match or strong substring
        exact_score = 0.0
        if raw_query.lower() in content:
            exact_score = 0.5

        # 2. Token overlap score
        mem_tokens = set(re.findall(r'\b\w+\b', content))
        if query_tokens:
            matches = sum(1 for t in query_tokens if t in mem_tokens or t in mem_type)
            token_score = min(1.0, matches / max(1, len(query_tokens)))
        else:
            token_score = 0.2

        # 3. Intent relevance boosts:
        intent_boost = 0.0
        # If user asks "what next", "what should I focus on", "career", "study"
        q_lower = raw_query.lower()
        if any(w in q_lower for w in ["next", "focus", "learn", "study", "plan", "start", "career", "become"]):
            if mem_type in ["career_goal", "weakness", "skill", "learning_progress"]:
                intent_boost = 0.4
        if any(w in q_lower for w in ["interview", "mock", "test", "score", "evaluate", "weak"]):
            if mem_type in ["weakness", "interview_score", "skill"]:
                intent_boost = 0.4

        # 4. Total weighted score
        final_score = (token_score * 0.45) + (exact_score * 0.25) + (intent_boost * 0.2) + (importance * 0.1)
        return min(1.0, final_score)

    def retrieve_relevant_memories(
        self,
        user_id: str,
        query: str,
        top_k: int = 4,
        min_threshold: float = 0.25
    ) -> List[Dict[str, Any]]:
        """
        Retrieve and rank top-k relevant memories for a user given a query.
        """
        all_memories = self.ltm.get_all_memories(user_id)
        if not all_memories:
            return []

        query_tokens = self._extract_keywords(query)
        scored_memories: List[Tuple[float, Dict[str, Any]]] = []

        for mem in all_memories:
            score = self._calculate_relevance(mem, query_tokens, query)
            if score >= min_threshold:
                scored_memories.append((score, mem))

        # Sort descending by score
        scored_memories.sort(key=lambda x: x[0], reverse=True)

        # Return top_k
        results = []
        for score, mem in scored_memories[:top_k]:
            mem_copy = dict(mem)
            mem_copy["retrieval_score"] = round(score, 3)
            results.append(mem_copy)
        
        # If no memories met the strict threshold but memories exist, return high-importance profile memories
        if not results and all_memories:
            core_memories = [m for m in all_memories if m.get("memory_type") in ["career_goal", "weakness", "skill"]]
            for m in core_memories[:top_k]:
                mem_copy = dict(m)
                mem_copy["retrieval_score"] = 0.5
                results.append(mem_copy)

        return results

    def format_memories_for_context(self, memories: List[Dict[str, Any]]) -> str:
        """Format retrieved memories into a clean string for prompt injection."""
        if not memories:
            return "No specific long-term memories retrieved for this query."
        
        lines = []
        for i, m in enumerate(memories, 1):
            m_type = m.get("memory_type", "fact").replace("_", " ").title()
            content = m.get("content", "")
            lines.append(f"[{i}] ({m_type}): {content}")
        return "\n".join(lines)


# Global memory retriever instance
memory_retriever = MemoryRetriever()
