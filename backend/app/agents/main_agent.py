"""
Main EduMind Agent Module.
The central AI Agent orchestrating Intent Analysis, Long/Short-Term Memory,
Dynamic Context Building, Tool Dispatching, Multi-Agent Collaboration, and Memory Persistence.
"""

import time
import uuid
import logging
from typing import Dict, List, Any, Optional
from ..database.models import ChatRequest, ChatResponse
from .langgraph_workflow import workflow_engine, EduMindWorkflow
from ..services.student_service import student_service

logger = logging.getLogger("edumind.main_agent")


class EduMindAgent:
    """Central AI Agent for EduAgent system."""
    
    def __init__(self):
        self.workflow: EduMindWorkflow = workflow_engine

    async def process_message(
        self,
        user_id: str,
        request: ChatRequest
    ) -> ChatResponse:
        """
        Execute full agent pipeline:
        Receive Query -> Load Memory -> Intent -> Tool/RAG -> Sub-Agent -> Synthesize -> Persist Memory.
        """
        start_time = time.perf_counter()
        conv_id = request.conversation_id or str(uuid.uuid4())

        # Execute the LangGraph State Workflow
        state = await self.workflow.execute_graph(
            user_id=user_id,
            conversation_id=conv_id,
            query=request.message,
            provider=request.provider or "auto",
            model_name=request.model_name
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Construct ChatResponse
        response = ChatResponse(
            response=state["final_response"],
            conversation_id=conv_id,
            agent_name="EduMind Agent",
            intent=state["intent"],
            activities=state["activities"],
            memories_retrieved=state["retrieved_memories"],
            documents_retrieved=state["rag_context"].get("citations", []),
            tools_executed=state["tools_executed"],
            agents_invoked=state["agents_invoked"],
            memory_saved=state["memory_saved"],
            execution_time_ms=round(elapsed_ms, 2)
        )

        return response


# Global EduMind Agent instance
main_agent = EduMindAgent()
