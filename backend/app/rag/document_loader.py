"""
Document Loader module for EduAgent RAG.
Extracts clean text and metadata from PDF, DOCX, and TXT files, and chunks them with overlap.
"""

import os
import re
from typing import List, Dict, Any, Optional
import pypdf
import docx


class DocumentChunk:
    def __init__(self, doc_id: str, filename: str, chunk_index: int, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.doc_id = doc_id
        self.filename = filename
        self.chunk_index = chunk_index
        self.text = text
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "filename": self.filename,
            "chunk_index": self.chunk_index,
            "text": self.text,
            "metadata": self.metadata
        }


class DocumentProcessor:
    """Extracts text and generates chunks from academic documents."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_file(self, filepath: str, file_type: str) -> str:
        """Extract plain text from PDF, DOCX, or TXT."""
        file_ext = file_type.lower().replace(".", "")
        
        if file_ext == "pdf":
            text_parts = []
            with open(filepath, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page_idx, page in enumerate(reader.pages):
                    extracted = page.extract_text() or ""
                    if extracted.strip():
                        text_parts.append(f"[Page {page_idx + 1}]\n{extracted}")
            return "\n\n".join(text_parts)

        elif file_ext in ["docx", "doc"]:
            doc = docx.Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

        elif file_ext in ["txt", "md", "csv", "py"]:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        else:
            raise ValueError(f"Unsupported document format: {file_type}")

    def chunk_text(self, text: str, doc_id: str, filename: str) -> List[DocumentChunk]:
        """Split document text into overlapping sliding chunks."""
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        words = text.split(' ')
        
        if not words:
            return []

        chunks = []
        chunk_idx = 0
        step = max(1, self.chunk_size - self.chunk_overlap)

        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.chunk_size]
            chunk_str = " ".join(chunk_words)
            if len(chunk_str.strip()) > 20:
                chunks.append(DocumentChunk(
                    doc_id=doc_id,
                    filename=filename,
                    chunk_index=chunk_idx,
                    text=chunk_str,
                    metadata={"word_count": len(chunk_words), "start_word": i}
                ))
                chunk_idx += 1

        return chunks


# Global document processor instance
document_processor = DocumentProcessor()
