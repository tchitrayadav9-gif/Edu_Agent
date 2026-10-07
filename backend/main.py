"""
EduAgent FastAPI Application.
Main backend server entry point coordinating all API routes, database connections, and background workers.
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .app.database.mongodb import db_manager
from .app.rag.rag_pipeline import rag_pipeline
from .app.services.student_service import student_service

# Import API Routers
from .app.api.auth import router as auth_router
from .app.api.chat import router as chat_router
from .app.api.memory import router as memory_router
from .app.api.student import router as student_router
from .app.api.career import router as career_router
from .app.api.study import router as study_router
from .app.api.documents import router as documents_router
from .app.api.interview import router as interview_router
from .app.api.search import router as search_router
from .app.api.reasoning import router as reasoning_router
from .app.api.planning import router as planning_router
from .app.api.evaluation import router as evaluation_router
from .app.api.mcp_api import router as mcp_router
from .app.api.dashboard import router as dashboard_router
from .app.api.learning import router as learning_router, edumind_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("edumind.server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup initialization and seed default demo resources."""
    logger.info("Starting EduAgent AI Server...")
    
    # Initialize default student profile for instant seamless demo
    demo_user = "chitra_demo_user"
    student_service.get_or_create_profile(demo_user, default_name="Chitra")
    
    # Pre-seed foundational AI course notes into RAG index
    sample_notes_text = (
        "AI Lecture Notes - Module 3: Informed State Space Search & Heuristics.\n"
        "1. A* Search Algorithm: A* evaluates nodes by combining g(n) (cost to reach node n from start) "
        "and h(n) (estimated heuristic cost from n to goal): f(n) = g(n) + h(n).\n"
        "2. Heuristic Admissibility: A heuristic h(n) is admissible if for every node n, h(n) <= h*(n), "
        "where h*(n) is the true optimal cost from n to goal. An admissible heuristic never overestimates the cost to reach the goal.\n"
        "3. Optimality & Completeness: A* is complete and optimal if h(n) is admissible (for tree search) or consistent (for graph search).\n"
        "4. Consistency: Satisfies the triangle inequality: h(n) <= c(n, a, n') + h(n').\n"
        "5. Comparison with BFS/Dijkstra: Unlike uninformed Dijkstra/BFS which expand equally in all directions, "
        "A* uses heuristic guidance to prune irrelevant search branches, reducing explored nodes significantly."
    )
    
    data_dir = os.path.join(os.path.dirname(__file__), "data", "sample_docs")
    os.makedirs(data_dir, exist_ok=True)
    sample_file = os.path.join(data_dir, "AI_Notes.txt")
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write(sample_notes_text)

    rag_pipeline.process_and_index_file(
        user_id=demo_user,
        doc_id="doc_ai_notes_01",
        filename="AI_Notes.txt",
        filepath=sample_file,
        file_type="txt"
    )
    logger.info("Default AI_Notes seeded into RAG vector store.")
    
    yield
    logger.info("Shutting down EduAgent AI Server...")


app = FastAPI(
    title="EduAgent API",
    description="Python-Powered Memory-Enabled Multi-Agent RAG System for Personalized Learning & Career Guidance",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All API Routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(memory_router)
app.include_router(student_router)
app.include_router(career_router)
app.include_router(study_router)
app.include_router(documents_router)
app.include_router(interview_router)
app.include_router(search_router)
app.include_router(reasoning_router)
app.include_router(planning_router)
app.include_router(evaluation_router)
app.include_router(mcp_router)
app.include_router(dashboard_router)
app.include_router(learning_router)
app.include_router(edumind_router)

# Mount Frontend static files if built
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/app", StaticFiles(directory=frontend_dist, html=True), name="frontend_app")


@app.get("/")
def root():
    return {
        "system": "EduAgent - AI Learning & Career Agent",
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs",
        "web_ui_url": "/app",
        "technologies": ["FastAPI", "LangChain", "LangGraph", "CrewAI", "RAG", "MCP", "Classical AI", "Bayesian Networks"]
    }



@app.get("/health")
def health_check():
    return {"status": "healthy", "database_connected": db_manager.is_connected}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
