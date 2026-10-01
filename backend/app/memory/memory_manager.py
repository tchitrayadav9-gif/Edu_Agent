"""
Memory Manager for EduAgent.
Orchestrates short-term conversation context, automatic memory extraction from dialogue,
importance assessment, deduplication, conflict resolution, and synchronization with student profiles.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from .short_term_memory import short_term_memory, ShortTermMemory
from .long_term_memory import long_term_memory, LongTermMemory
from .memory_retriever import memory_retriever, MemoryRetriever
from ..database.mongodb import db_manager

logger = logging.getLogger("edumind.memory.manager")


class MemoryManager:
    """Central Memory Manager handling working context, extraction, updates, and persistence."""
    
    def __init__(self):
        self.stm: ShortTermMemory = short_term_memory
        self.ltm: LongTermMemory = long_term_memory
        self.retriever: MemoryRetriever = memory_retriever
        self.db = db_manager

    def extract_facts_from_text(self, text: str, user_id: str) -> List[Dict[str, Any]]:
        """
        Extract key educational and personal facts from student utterance.
        Recognizes career goals, names, strong skills, weak topics, preferences, interview scores, and achievements.
        """
        extracted = []
        t_lower = text.lower()

        # 1. Name extraction
        name_match = re.search(r'\bmy name is ([a-zA-Z\s]+?)(?:\.|\,|$|\band\b)', text, re.IGNORECASE)
        if name_match:
            name_val = name_match.group(1).strip()
            if len(name_val) < 30:
                extracted.append({
                    "memory_type": "important_fact",
                    "content": f"Student's name is {name_val}.",
                    "importance": 0.95,
                    "metadata": {"name": name_val}
                })

        # 2. Career Goal extraction (e.g. "I want to become an AI Engineer", "My goal is Data Scientist", "Target role: ML Engineer")
        goal_patterns = [
            r'(?:want to become|aiming to be|goal is|dream of becoming|aspire to be|career goal is|target role is)\s+(?:an?|the)?\s*([a-zA-Z\s\+\#]+?)(?:\.|\,|$|\band\b|\bwith\b)',
            r'(?:become an?|work as an?)\s+([a-zA-Z\s\+\#]+?)(?:\.|\,|$|\band\b)'
        ]
        for pat in goal_patterns:
            g_match = re.search(pat, text, re.IGNORECASE)
            if g_match:
                goal_val = g_match.group(1).strip()
                if len(goal_val) < 40 and not any(w in goal_val.lower() for w in ["expert", "good", "better", "ready"]):
                    extracted.append({
                        "memory_type": "career_goal",
                        "content": f"Target Career Goal is {goal_val.title()}.",
                        "importance": 1.0,
                        "metadata": {"career_goal": goal_val.title()}
                    })
                    # Also update profile
                    self._sync_profile_field(user_id, "career_goal", goal_val.title())
                    break

        # 3. Weakness / Weak Skill extraction (e.g. "I am weak in statistics", "struggling with deep learning", "need help with SQL")
        weak_patterns = [
            r'(?:weak in|struggling with|bad at|difficulty with|need help with|poor in|not good at)\s+([a-zA-Z0-9\s\+\#]+?)(?:\.|\,|$|\band\b)',
            r'([a-zA-Z0-9\s\+\#]+?)\s+is my weak (?:point|area|subject|topic)'
        ]
        for pat in weak_patterns:
            w_match = re.search(pat, text, re.IGNORECASE)
            if w_match:
                weak_val = w_match.group(1).strip()
                if len(weak_val) < 35:
                    extracted.append({
                        "memory_type": "weakness",
                        "content": f"Student is weak in {weak_val.title()}.",
                        "importance": 0.85,
                        "metadata": {"weak_topic": weak_val.title()}
                    })
                    self._add_profile_weakness(user_id, weak_val.title())

        # 4. Strong Skill / Knowledge extraction (e.g. "I know Python", "strong in SQL", "proficient in Java", "I completed Python")
        strong_patterns = [
            r'(?:i know|strong in|good at|proficient in|skilled in|experienced in)\s+([a-zA-Z0-9\s\+\#]+?)(?:\.|\,|$|\band\b|\bbut\b)',
            r'(?:completed|finished|mastered)\s+([a-zA-Z0-9\s\+\#]+?)(?:\.|\,|$|\band\b)'
        ]
        for pat in strong_patterns:
            s_match = re.search(pat, text, re.IGNORECASE)
            if s_match:
                skill_val = s_match.group(1).strip()
                if len(skill_val) < 35 and not any(w in skill_val.lower() for w in ["that", "this", "nothing", "everything"]):
                    extracted.append({
                        "memory_type": "skill",
                        "content": f"Student has proficiency in {skill_val.title()}.",
                        "importance": 0.85,
                        "metadata": {"skill": skill_val.title(), "level": "Strong"}
                    })
                    self._sync_profile_skill(user_id, skill_val.title(), 80)

        # 5. Study Preferences (e.g. "prefer studying in the evening", "can study 2 hours daily")
        if "evening" in t_lower:
            extracted.append({
                "memory_type": "preference",
                "content": "Prefers studying during evening hours.",
                "importance": 0.75,
                "metadata": {"preferred_time": "Evening"}
            })
        elif "morning" in t_lower:
            extracted.append({
                "memory_type": "preference",
                "content": "Prefers studying during morning hours.",
                "importance": 0.75,
                "metadata": {"preferred_time": "Morning"}
            })

        # 6. Interview Score memory (e.g. "I scored 7/10 in my last interview", "scored 8 in python")
        score_match = re.search(r'(?:scored|got|received)\s+(\d+(?:\.\d+)?)\s*(?:\/|\s*out of\s*)(\d+)?\s*(?:in|on)?\s*([a-zA-Z\s]+)?', text, re.IGNORECASE)
        if score_match:
            val = score_match.group(1)
            topic = (score_match.group(3) or "Interview").strip()
            extracted.append({
                "memory_type": "achievement",
                "content": f"Scored {val}/10 in {topic.title()} interview session.",
                "importance": 0.8,
                "metadata": {"score": float(val), "topic": topic.title()}
            })

        return extracted

    def _sync_profile_field(self, user_id: str, field: str, value: Any):
        """Update a specific field in student profile."""
        self.db.student_profiles.update_one(
            {"user_id": user_id},
            {"$set": {field: value}},
            upsert=True
        )

    def _add_profile_weakness(self, user_id: str, topic: str):
        """Add a weakness to the student profile weak_topics list."""
        profile = self.db.student_profiles.find_one({"user_id": user_id})
        if profile:
            weak_topics = profile.get("weak_topics", [])
            if topic not in weak_topics:
                weak_topics.append(topic)
                self.db.student_profiles.update_one(
                    {"user_id": user_id},
                    {"$set": {"weak_topics": weak_topics}}
                )

    def _sync_profile_skill(self, user_id: str, skill_name: str, score: int = 80):
        """Sync a recognized skill into profile skills dictionary."""
        profile = self.db.student_profiles.find_one({"user_id": user_id})
        if profile:
            skills = profile.get("skills", {})
            skills[skill_name] = max(skills.get(skill_name, 0), score)
            self.db.student_profiles.update_one(
                {"user_id": user_id},
                {"$set": {"skills": skills}}
            )

    def process_turn(
        self,
        user_id: str,
        conversation_id: str,
        user_message: str,
        agent_response: str,
        tools_used: Optional[List[str]] = None,
        agents_used: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Record dialogue into short-term buffer, persist conversation turn in chat_history,
        and extract/save critical long-term facts.
        """
        # 1. Update Short Term Memory
        self.stm.add_turn(conversation_id, "user", user_message)
        self.stm.add_turn(conversation_id, "assistant", agent_response)

        # 2. Extract and save persistent long-term facts
        saved_memories = []
        facts = self.extract_facts_from_text(user_message, user_id)
        for fact in facts:
            saved = self.ltm.save_memory(
                user_id=user_id,
                memory_type=fact["memory_type"],
                content=fact["content"],
                importance=fact.get("importance", 0.8),
                source=f"conversation:{conversation_id}",
                metadata=fact.get("metadata", {})
            )
            saved_memories.append(saved)

        # 3. Store conversation turn in chat_history collection
        chat_record = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "user_message": user_message,
            "agent_response": agent_response,
            "tools_used": tools_used or [],
            "agents_used": agents_used or [],
            "memories_extracted": len(saved_memories),
            "timestamp": db_manager.student_profiles # datetime string formatted
        }
        # Save to chat_history
        import datetime
        chat_record["timestamp"] = datetime.datetime.utcnow().isoformat()
        self.db.chat_history.insert_one(chat_record)

        return saved_memories


# Global memory manager instance
memory_manager = MemoryManager()
