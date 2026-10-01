"""
RAG Pipeline Module for EduAgent.
Coordinates document retrieval, relevant chunk extraction, citation generation,
and context synthesis for document-grounded question answering.
"""

from typing import Dict, List, Any, Optional
import logging
from .vector_store import vector_store, VectorStore
from .document_loader import document_processor, DocumentProcessor

logger = logging.getLogger("edumind.rag")


class RAGPipeline:
    """End-to-end Retrieval-Augmented Generation engine."""
    
    def __init__(self):
        self.vector_store: VectorStore = vector_store
        self.doc_processor: DocumentProcessor = document_processor

    def process_and_index_file(self, user_id: str, doc_id: str, filename: str, filepath: str, file_type: str) -> Dict[str, Any]:
        """Load document, extract text, chunk it, and index into vector store."""
        try:
            raw_text = self.doc_processor.extract_text_from_file(filepath, file_type)
            chunks = self.doc_processor.chunk_text(raw_text, doc_id, filename)
            
            self.vector_store.add_document_chunks(user_id, doc_id, filename, chunks)
            logger.info(f"Indexed document '{filename}' ({doc_id}) with {len(chunks)} chunks for user {user_id}")
            
            return {
                "success": True,
                "doc_id": doc_id,
                "filename": filename,
                "chunk_count": len(chunks),
                "total_words": len(raw_text.split()),
                "preview": raw_text[:200] + "..." if len(raw_text) > 200 else raw_text
            }
        except Exception as e:
            logger.error(f"Error indexing file {filename}: {e}")
            return {
                "success": False,
                "error": str(e),
                "doc_id": doc_id,
                "filename": filename
            }

    def retrieve_context(
        self,
        query: str,
        user_id: Optional[str] = None,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Search for top-k document chunks relevant to query.
        Returns:
            - context_string: Formatted text snippet for LLM prompt injection
            - citations: Source filename and chunk references
            - chunks: Raw chunk list
        """
        results = self.vector_store.similarity_search(query, user_id=user_id, top_k=top_k)
        
        if not results:
            return {
                "has_context": False,
                "context_string": "No relevant uploaded document context found for this query.",
                "citations": [],
                "chunks": []
            }

        citations = []
        context_parts = []
        chunk_items = []

        for idx, (chunk, score) in enumerate(results, 1):
            cite_tag = f"[{chunk.filename} (Chunk #{chunk.chunk_index + 1}, Relevance: {round(score, 2)})]"
            citations.append({
                "filename": chunk.filename,
                "chunk_index": chunk.chunk_index,
                "relevance_score": round(score, 3)
            })
            context_parts.append(f"--- SOURCE {idx}: {cite_tag} ---\n{chunk.text.strip()}\n")
            chunk_items.append(chunk.to_dict())

        return {
            "has_context": True,
            "context_string": "\n".join(context_parts),
            "citations": citations,
            "chunks": chunk_items
        }


# Global RAG pipeline instance
rag_pipeline = RAGPipeline()
