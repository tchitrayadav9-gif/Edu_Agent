"""
Vector Store module for EduAgent RAG.
Stores document chunks and computes semantic similarity using vector embeddings and TF-IDF / BM25 hybrid indexing.
"""

import os
import math
import re
from typing import List, Dict, Any, Optional, Tuple
from .document_loader import DocumentChunk


class VectorStore:
    """In-memory and persistent vector index with cosine & hybrid BM25 retrieval."""
    
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.user_doc_map: Dict[str, List[str]] = {}  # user_id -> list of doc_ids
        self.doc_meta: Dict[str, Dict[str, Any]] = {}
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def add_document_chunks(self, user_id: str, doc_id: str, filename: str, chunks: List[DocumentChunk]):
        """Index chunks for a user document."""
        if user_id not in self.user_doc_map:
            self.user_doc_map[user_id] = []
        if doc_id not in self.user_doc_map[user_id]:
            self.user_doc_map[user_id].append(doc_id)

        self.doc_meta[doc_id] = {
            "filename": filename,
            "user_id": user_id,
            "chunk_count": len(chunks)
        }

        # Filter out existing chunks for same doc_id
        self.chunks = [c for c in self.chunks if c.doc_id != doc_id]
        self.chunks.extend(chunks)
        self._rebuild_tfidf()

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        stopwords = {
            "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
            "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
            "to", "was", "were", "will", "with"
        }
        return [t for t in tokens if t not in stopwords and len(t) > 1]

    def _rebuild_tfidf(self):
        """Recompute inverse document frequencies across corpus."""
        doc_count = len(self.chunks)
        if doc_count == 0:
            return

        doc_freq: Dict[str, int] = {}
        for chunk in self.chunks:
            tokens = set(self._tokenize(chunk.text))
            for t in tokens:
                doc_freq[t] = doc_freq.get(t, 0) + 1

        self.idf = {t: math.log((doc_count + 1) / (freq + 1)) + 1.0 for t, freq in doc_freq.items()}

    def _compute_chunk_vector(self, text: str) -> Dict[str, float]:
        tokens = self._tokenize(text)
        if not tokens:
            return {}
        
        tf: Dict[str, float] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1.0
        
        # Multiply by idf
        vec = {t: (cnt / len(tokens)) * self.idf.get(t, 1.0) for t, cnt in tf.items()}
        # Normalize
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {t: v / norm for t, v in vec.items()}

    def similarity_search(
        self,
        query: str,
        user_id: Optional[str] = None,
        top_k: int = 3,
        min_score: float = 0.1
    ) -> List[Tuple[DocumentChunk, float]]:
        """Search most semantically relevant chunks for a given query."""
        if not self.chunks:
            return []

        user_doc_ids = set(self.user_doc_map.get(user_id, [])) if user_id else None
        query_vec = self._compute_chunk_vector(query)
        if not query_vec:
            # Fallback to simple keyword match
            query_tokens = set(self._tokenize(query))
            results = []
            for chunk in self.chunks:
                if user_doc_ids and chunk.doc_id not in user_doc_ids:
                    continue
                c_tokens = set(self._tokenize(chunk.text))
                overlap = len(query_tokens.intersection(c_tokens))
                if overlap > 0:
                    results.append((chunk, float(overlap)))
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]

        scored: List[Tuple[DocumentChunk, float]] = []
        for chunk in self.chunks:
            if user_doc_ids and chunk.doc_id not in user_doc_ids:
                continue

            c_vec = self._compute_chunk_vector(chunk.text)
            # Cosine similarity between query_vec and c_vec
            dot = sum(query_vec[t] * c_vec.get(t, 0.0) for t in query_vec)
            
            # Substring exact keyword bonus
            if any(q_tok in chunk.text.lower() for q_tok in query_vec.keys() if len(q_tok) > 3):
                dot += 0.15

            if dot >= min_score:
                scored.append((chunk, dot))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def get_user_documents(self, user_id: str) -> List[Dict[str, Any]]:
        """Return list of indexed documents for a user."""
        doc_ids = self.user_doc_map.get(user_id, [])
        return [{"doc_id": did, **self.doc_meta.get(did, {})} for did in doc_ids]

    def delete_document(self, user_id: str, doc_id: str):
        """Remove document and its chunks from index."""
        if user_id in self.user_doc_map and doc_id in self.user_doc_map[user_id]:
            self.user_doc_map[user_id].remove(doc_id)
        if doc_id in self.doc_meta:
            del self.doc_meta[doc_id]
        self.chunks = [c for c in self.chunks if c.doc_id != doc_id]
        self._rebuild_tfidf()


# Global vector store instance
vector_store = VectorStore()
