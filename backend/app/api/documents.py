"""
Documents & RAG API Router.
Endpoints for uploading course notes/textbooks (PDF, DOCX, TXT), indexing into vector store, and running RAG queries.
"""

import os
import shutil
import uuid
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException, Body
from pydantic import BaseModel
from ..rag.rag_pipeline import rag_pipeline
from ..rag.vector_store import vector_store
from ..database.mongodb import db_manager
from ..agents.rag_agent import rag_agent

router = APIRouter(prefix="/api/documents", tags=["RAG Documents"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    doc_id = str(uuid.uuid4())
    filename = file.filename or "uploaded_file.txt"
    file_ext = filename.split(".")[-1].lower() if "." in filename else "txt"

    if file_ext not in ["pdf", "docx", "doc", "txt", "md", "csv", "py"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_ext}")

    dest_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{filename}")
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(dest_path)

    # Process and index into vector store
    index_res = rag_pipeline.process_and_index_file(
        user_id=user_id,
        doc_id=doc_id,
        filename=filename,
        filepath=dest_path,
        file_type=file_ext
    )

    if not index_res.get("success"):
        raise HTTPException(status_code=500, detail=f"Failed to process document: {index_res.get('error')}")

    # Record document in database
    doc_record = {
        "doc_id": doc_id,
        "user_id": user_id,
        "filename": filename,
        "file_type": file_ext,
        "file_size": file_size,
        "chunk_count": index_res.get("chunk_count", 0),
        "upload_date": db_manager.student_profiles # datetime string formatted
    }
    import datetime
    doc_record["upload_date"] = datetime.datetime.utcnow().isoformat()
    db_manager.documents.insert_one(doc_record)

    return {
        "message": "Document successfully uploaded and indexed for RAG",
        "doc_id": doc_id,
        "filename": filename,
        "chunks_indexed": index_res.get("chunk_count", 0),
        "file_size_bytes": file_size
    }


@router.get("")
def list_documents(x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    user_id = x_user_id or "chitra_demo_user"
    return db_manager.documents.find({"user_id": user_id})


@router.post("/query")
async def query_documents(
    req: DocumentQueryRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    return await rag_agent.answer_from_documents(query=req.query, user_id=user_id)


@router.delete("/{doc_id}")
def delete_document(
    doc_id: str,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    user_id = x_user_id or "chitra_demo_user"
    vector_store.delete_document(user_id=user_id, doc_id=doc_id)
    db_manager.documents.delete_one({"user_id": user_id, "doc_id": doc_id})
    return {"message": "Document deleted", "doc_id": doc_id}
