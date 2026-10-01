"""
RAG Agent Module.
Specialized agent for retrieving document context, citing source files, and synthesizing grounded answers.
"""

from typing import Dict, List, Any, Optional
from ..rag.rag_pipeline import rag_pipeline, RAGPipeline
from ..llm.llm_factory import llm_factory
from ..llm.prompt_templates import RAG_AGENT_PROMPT


class RAGAgent:
    """Specialized agent grounded strictly in uploaded student notes & textbooks."""
    
    def __init__(self):
        self.pipeline: RAGPipeline = rag_pipeline
        self.llm = llm_factory

    async def answer_from_documents(
        self,
        query: str,
        user_id: Optional[str] = None,
        provider: str = "auto"
    ) -> Dict[str, Any]:
        """Retrieve relevant context chunks and generate grounded answer with citations."""
        rag_data = self.pipeline.retrieve_context(query, user_id=user_id, top_k=3)
        
        system_prompt = RAG_AGENT_PROMPT
        user_prompt = f"Query: {query}\n\nDocument Context:\n{rag_data['context_string']}"

        answer = await self.llm.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            provider=provider
        )

        return {
            "agent_name": "RAG Agent",
            "answer": answer,
            "citations": rag_data.get("citations", []),
            "has_context": rag_data.get("has_context", False),
            "chunks_used": len(rag_data.get("chunks", []))
        }


# Global RAG agent instance
rag_agent = RAGAgent()
