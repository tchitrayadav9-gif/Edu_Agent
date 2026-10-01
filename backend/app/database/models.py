"""
Pydantic schemas and data models for EduAgent system.
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    name: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: str
    name: str
    academic_year: Optional[str] = "2nd Year"
    branch: Optional[str] = "Computer Science and Engineering"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class StudentProfile(BaseModel):
    user_id: str
    name: str
    academic_year: str = "2nd Year"
    branch: str = "Computer Science and Engineering"
    career_goal: str = "AI Engineer"
    target_role: Optional[str] = "Artificial Intelligence Engineer"
    skills: Dict[str, int] = Field(default_factory=lambda: {
        "Python": 85,
        "SQL": 70,
        "Machine Learning": 40,
        "Data Structures": 75,
        "Statistics": 45
    })
    weak_topics: List[str] = Field(default_factory=lambda: ["Statistics", "Deep Learning", "System Design"])
    completed_topics: List[str] = Field(default_factory=lambda: ["Python Basics", "Object Oriented Programming", "SQL Fundamentals"])
    learning_progress: Dict[str, int] = Field(default_factory=lambda: {
        "Python": 85,
        "Machine Learning": 40,
        "Data Science": 55,
        "Algorithms": 65
    })
    study_preferences: Dict[str, Any] = Field(default_factory=lambda: {
        "preferred_time": "Evening",
        "daily_hours": 2,
        "learning_style": "Hands-on projects & Code examples"
    })
    interview_scores: Dict[str, float] = Field(default_factory=lambda: {
        "Python": 8.0,
        "Machine Learning": 4.5,
        "AI Fundamentals": 6.0
    })
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MemoryItem(BaseModel):
    memory_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    memory_type: str = "important_fact"  # career_goal, skill, preference, learning_progress, weakness, achievement, conversation_summary, important_fact
    content: str
    importance: float = 0.8  # 0.0 to 1.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    source: str = "chat_interaction"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatMessage(BaseModel):
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tools_used: List[str] = Field(default_factory=list)
    agents_used: List[str] = Field(default_factory=list)
    memory_used: List[Dict[str, Any]] = Field(default_factory=list)
    documents_used: List[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    provider: Optional[str] = "auto"  # auto, openai, ollama
    model_name: Optional[str] = None
    enable_tools: bool = True
    enable_rag: bool = True
    enable_memory: bool = True


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent_name: str = "EduMind Agent"
    intent: str = "general_query"
    activities: List[str] = Field(default_factory=list)
    memories_retrieved: List[Dict[str, Any]] = Field(default_factory=list)
    documents_retrieved: List[Dict[str, Any]] = Field(default_factory=list)
    tools_executed: List[Dict[str, Any]] = Field(default_factory=list)
    agents_invoked: List[str] = Field(default_factory=list)
    memory_saved: Optional[Dict[str, Any]] = None
    execution_time_ms: float = 0.0


class DocumentItem(BaseModel):
    doc_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    filename: str
    file_type: str
    file_size: int
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    chunk_count: int = 0
    summary: Optional[str] = None


class StudyPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    career_goal: str
    duration_days: int = 30
    daily_commitment_hours: float = 2.0
    schedule: List[Dict[str, Any]] = Field(default_factory=list)
    topics_covered: List[str] = Field(default_factory=list)
    prerequisite_chain: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class InterviewQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    difficulty: str  # Easy, Medium, Hard
    question: str
    expected_keywords: List[str] = Field(default_factory=list)
    sample_answer: Optional[str] = None


class InterviewSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    target_role: str
    difficulty: str = "Adaptive"
    status: str = "in_progress"  # in_progress, completed
    questions_answered: List[Dict[str, Any]] = Field(default_factory=list)
    total_score: float = 0.0
    feedback: Optional[str] = None
    topic_scores: Dict[str, float] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class EvaluationResult(BaseModel):
    eval_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_questions: int
    accuracy_score: float
    relevance_score: float
    faithfulness_score: float
    context_relevance_score: float
    avg_latency_ms: float
    total_tokens: int
    estimated_cost_usd: float
    results_breakdown: List[Dict[str, Any]] = Field(default_factory=list)
