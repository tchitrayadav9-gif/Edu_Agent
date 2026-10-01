"""
Context Engineering Module for EduAgent.
Dynamically constructs compact, high-relevance prompt contexts by synthesizing:
Current Query + Short-Term Dialogue + Retrieved Long-Term Memories +
Student Profile + Learning Progress + Retrieved RAG Documents + Tool Outputs.
"""

from typing import Dict, List, Any, Optional
from ..memory.short_term_memory import short_term_memory
from ..memory.memory_retriever import memory_retriever
from ..database.mongodb import db_manager


class ContextBuilder:
    """Orchestrates dynamic prompt context engineering."""
    
    def __init__(self):
        self.stm = short_term_memory
        self.retriever = memory_retriever
        self.db = db_manager

    def build_agent_context(
        self,
        user_id: str,
        conversation_id: str,
        current_query: str,
        profile: Optional[Dict[str, Any]] = None,
        retrieved_memories: Optional[List[Dict[str, Any]]] = None,
        rag_context: Optional[Dict[str, Any]] = None,
        tool_results: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Assemble comprehensive structured context block for LLM inference.
        """
        profile = profile or self.db.student_profiles.find_one({"user_id": user_id}) or {}
        student_name = profile.get("name", "Student")
        year = profile.get("academic_year", "2nd Year")
        branch = profile.get("branch", "CSE")
        career_goal = profile.get("career_goal", "AI Engineer")
        skills = profile.get("skills", {})
        weak_topics = profile.get("weak_topics", [])
        preferences = profile.get("study_preferences", {})

        # 1. Format Student Profile Section
        profile_section = (
            f"### 👤 STUDENT PROFILE\n"
            f"- **Name**: {student_name}\n"
            f"- **Academic Year & Branch**: {year}, {branch}\n"
            f"- **Declared Career Goal**: {career_goal}\n"
            f"- **Evaluated Skills**: {', '.join([f'{k} ({v}%)' for k, v in skills.items()])}\n"
            f"- **Weak Topics**: {', '.join(weak_topics) if weak_topics else 'None flagged'}\n"
            f"- **Study Preference**: {preferences.get('preferred_time', 'Evening')} ({preferences.get('daily_hours', 2)} hrs/day)\n"
        )

        # 2. Format Retrieved Long-Term Memories
        if retrieved_memories is None:
            retrieved_memories = self.retriever.retrieve_relevant_memories(user_id, current_query, top_k=4)
        
        memory_lines = []
        if retrieved_memories:
            for m in retrieved_memories:
                m_type = m.get("memory_type", "fact").replace("_", " ").title()
                content = m.get("content", "")
                score = m.get("retrieval_score", 0.5)
                memory_lines.append(f"- [{m_type}] {content} (Relevance: {score})")
            memory_section = "### 🧠 RELEVANT LONG-TERM MEMORIES\n" + "\n".join(memory_lines) + "\n"
        else:
            memory_section = "### 🧠 RELEVANT LONG-TERM MEMORIES\n- No prior memories matched this specific query.\n"

        # 3. Format Short-Term Conversation Context
        short_term_dialogue = self.stm.get_formatted_dialogue(conversation_id, n_turns=3)
        dialogue_section = f"### 💬 RECENT CONVERSATION TURNS\n{short_term_dialogue}\n"

        # 4. Format Retrieved Document Context (RAG)
        rag_section = ""
        if rag_context and rag_context.get("has_context"):
            rag_section = f"### 📄 RETRIEVED DOCUMENT CONTEXT (RAG)\n{rag_context.get('context_string')}\n"

        # 5. Format Tool Execution Results
        tool_section = ""
        if tool_results:
            tool_lines = [f"- **{t['tool_name']}**: {t['output']}" for t in tool_results]
            tool_section = f"### 🛠️ TOOL EXECUTION OUTPUTS\n" + "\n".join(tool_lines) + "\n"

        # Synthesize combined prompt
        full_system_context = (
            f"{profile_section}\n"
            f"{memory_section}\n"
            f"{dialogue_section}\n"
            f"{rag_section}"
            f"{tool_section}"
        )

        return {
            "full_context_prompt": full_system_context,
            "retrieved_memories": retrieved_memories,
            "student_profile": profile,
            "has_rag_context": bool(rag_context and rag_context.get("has_context")),
            "short_term_turns_count": len(self.stm.get_recent_turns(conversation_id))
        }


# Global context builder instance
context_builder = ContextBuilder()
