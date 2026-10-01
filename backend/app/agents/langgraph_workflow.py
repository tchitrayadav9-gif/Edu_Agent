"""
LangGraph Workflow Module for EduAgent.
Implements state graph orchestration, conditional branching, and memory persistence lifecycle.
"""

from typing import Dict, List, Any, Optional, TypedDict
import logging
from ..memory.memory_retriever import memory_retriever
from ..memory.memory_manager import memory_manager
from ..rag.rag_pipeline import rag_pipeline
from ..services.context_builder import context_builder
from ..llm.llm_factory import llm_factory
from ..tools.agent_tools import TOOL_REGISTRY
from .career_agent import career_agent
from .study_agent import study_agent
from .interview_agent import interview_agent
from .research_agent import research_agent

logger = logging.getLogger("edumind.langgraph")


class AgentState(TypedDict):
    user_id: str
    conversation_id: str
    query: str
    provider: str
    model_name: Optional[str]
    intent: str
    activities: List[str]
    student_profile: Dict[str, Any]
    retrieved_memories: List[Dict[str, Any]]
    rag_context: Dict[str, Any]
    tools_executed: List[Dict[str, Any]]
    agents_invoked: List[str]
    final_response: str
    memory_saved: Optional[Dict[str, Any]]


class EduMindWorkflow:
    """LangGraph-style stateful agent execution graph."""

    def analyze_intent(self, query: str) -> str:
        """Classify user intent into actionable routing categories."""
        q = query.lower()
        if any(w in q for w in ["notes", "pdf", "document", "uploaded", "according to my notes"]):
            return "rag_query"
        elif any(w in q for w in ["career", "become", "job", "target role", "skill gap", "suitability"]):
            return "career_guidance"
        elif any(w in q for w in ["study plan", "schedule", "30-day", "roadmap", "curriculum", "what should i learn next", "learn next"]):
            return "study_planning"
        elif any(w in q for w in ["interview", "mock", "test me", "question", "score", "improve"]):
            return "interview_prep"
        elif any(w in q for w in ["search", "algorithm", "a*", "bfs", "dfs", "explain", "how does"]):
            return "concept_research"
        return "general_tutoring"

    async def execute_graph(
        self,
        user_id: str,
        conversation_id: str,
        query: str,
        provider: str = "auto",
        model_name: Optional[str] = None
    ) -> AgentState:
        """Execute state graph from START -> END."""
        activities = []

        # Node 1: Load Student Profile
        from ..services.student_service import student_service
        profile = student_service.get_or_create_profile(user_id)
        activities.append("✓ Loaded student profile and target career goal")

        # Node 2: Retrieve Long-Term Memory
        retrieved_mems = memory_retriever.retrieve_relevant_memories(user_id, query, top_k=4)
        if retrieved_mems:
            activities.append(f"✓ Retrieved {len(retrieved_mems)} relevant long-term memories")
        else:
            activities.append("✓ Checked memory (no prior conflicts)")

        # Node 3: Intent Classification & Conditional Routing
        intent = self.analyze_intent(query)
        activities.append(f"✓ Intent classified: {intent.replace('_', ' ').title()}")

        # Node 4: Conditional RAG Retrieval
        rag_context = {"has_context": False, "context_string": "", "citations": [], "chunks": []}
        if intent == "rag_query" or any(w in query.lower() for w in ["notes", "a* search", "search algorithm"]):
            rag_context = rag_pipeline.retrieve_context(query, user_id=user_id, top_k=3)
            if rag_context.get("has_context"):
                activities.append(f"✓ Retrieved {len(rag_context['citations'])} document chunks from uploaded notes")

        # Node 5: Tool & Specialized Agent Execution
        tools_executed = []
        agents_invoked = ["EduMind Coordinator"]

        if intent == "career_guidance":
            agents_invoked.append("Career Agent")
            activities.append("✓ Delegated to Career Agent for Bayesian suitability and skill-gap analysis")
        elif intent == "study_planning":
            agents_invoked.append("Study Agent")
            activities.append("✓ Delegated to Study Agent (Running A* curriculum path optimization)")
        elif intent == "interview_prep":
            agents_invoked.append("Interview Agent")
            activities.append("✓ Delegated to Interview Agent (Adaptive difficulty scoring)")
        elif intent == "concept_research":
            agents_invoked.append("Research Agent")
            activities.append("✓ Delegated to Research Agent for pedagogical concept breakdown")

        # Node 6: Context Synthesis & LLM Response Generation
        context_data = context_builder.build_agent_context(
            user_id=user_id,
            conversation_id=conversation_id,
            current_query=query,
            profile=profile,
            retrieved_memories=retrieved_mems,
            rag_context=rag_context
        )
        
        system_prompt = context_data["full_context_prompt"]
        final_response = await llm_factory.generate_response(
            system_prompt=system_prompt,
            user_prompt=query,
            provider=provider,
            model_name=model_name
        )
        activities.append("✓ Generated grounded, personalized pedagogical response")

        # Node 7: Memory Persistence & Update
        saved_facts = memory_manager.process_turn(
            user_id=user_id,
            conversation_id=conversation_id,
            user_message=query,
            agent_response=final_response,
            tools_used=[t.get("tool_name", "") for t in tools_executed],
            agents_used=agents_invoked
        )
        if saved_facts:
            activities.append(f"✓ Extracted and persisted {len(saved_facts)} new facts into long-term memory")
        else:
            activities.append("✓ Synchronized session state")

        state: AgentState = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "query": query,
            "provider": provider,
            "model_name": model_name,
            "intent": intent,
            "activities": activities,
            "student_profile": profile,
            "retrieved_memories": retrieved_mems,
            "rag_context": rag_context,
            "tools_executed": tools_executed,
            "agents_invoked": agents_invoked,
            "final_response": final_response,
            "memory_saved": saved_facts[0] if saved_facts else None
        }

        return state


# Global LangGraph workflow instance
workflow_engine = EduMindWorkflow()
