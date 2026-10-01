"""
Test suite for Document Chunking, Vector Storage, and RAG Pipeline.
"""

import pytest
from backend.app.rag.document_loader import document_processor
from backend.app.rag.vector_store import vector_store
from backend.app.rag.rag_pipeline import rag_pipeline


def test_document_chunking():
    sample_text = "Word " * 600
    chunks = document_processor.chunk_text(sample_text, "doc_test_1", "notes.txt")
    assert len(chunks) > 1
    assert chunks[0].doc_id == "doc_test_1"
    assert chunks[0].chunk_index == 0


def test_vector_store_indexing_and_similarity():
    user_id = "test_user_rag"
    doc_id = "doc_test_search"
    text = (
        "Informed search algorithms like A* use evaluation function f(n) = g(n) + h(n). "
        "A heuristic is admissible if it never overestimates the true cost to reach the goal state."
    )
    chunks = document_processor.chunk_text(text, doc_id, "ai_search.txt")
    vector_store.add_document_chunks(user_id, doc_id, "ai_search.txt", chunks)

    results = vector_store.similarity_search("A* admissible heuristic", user_id=user_id, top_k=1)
    assert len(results) > 0
    best_chunk, score = results[0]
    assert "admissible" in best_chunk.text
    assert score > 0


def test_rag_pipeline_retrieve_context():
    user_id = "test_user_rag"
    doc_id = "doc_test_db"
    text = "Relational databases enforce ACID properties: Atomicity, Consistency, Isolation, Durability."
    chunks = document_processor.chunk_text(text, doc_id, "dbms.txt")
    vector_store.add_document_chunks(user_id, doc_id, "dbms.txt", chunks)

    ctx = rag_pipeline.retrieve_context("What are ACID properties?", user_id=user_id)
    assert ctx["has_context"] is True
    assert len(ctx["citations"]) > 0
    assert "Atomicity" in ctx["context_string"]
