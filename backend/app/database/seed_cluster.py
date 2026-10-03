"""
MongoDB Atlas Cluster Data Seeder.
Initializes and populates all required collections in 'edumind_db' with comprehensive,
production-style student data, memory records, skills, career benchmarks, study plans,
interview sessions, and evaluation results.
"""

import os
import sys
import hashlib
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Database URI
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://CHITRA:CHITRA@cluster0.jtoswvx.mongodb.net/edumind_db?appName=Cluster0"
)
DB_NAME = os.getenv("MONGODB_DB_NAME", "edumind_db")


def hash_password(password: str) -> str:
    salt = "edumind_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def seed_mongodb():
    print(f"Connecting to MongoDB Atlas: {MONGODB_URI[:35]}...")
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test ping
    try:
        client.admin.command('ping')
        print(" Connected successfully to MongoDB Atlas Cluster0!")
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")
        return False

    db = client[DB_NAME]
    print(f"Target Database: '{DB_NAME}'\n")

    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. USERS COLLECTION
    users = [
        {
            "id": "user_chitra",
            "user_id": "user_chitra",
            "username": "chitra",
            "email": "chitra@eduagent.ai",
            "name": "Chitra Yadav",
            "academic_year": "2nd Year",
            "branch": "Computer Science and Engineering",
            "password_hash": hash_password("chitra123"),
            "created_at": now_iso,
            "is_active": True
        },
        {
            "id": "user_alex",
            "user_id": "user_alex",
            "username": "alex",
            "email": "alex@eduagent.ai",
            "name": "Alex Smith",
            "academic_year": "3rd Year",
            "branch": "Artificial Intelligence & Data Science",
            "password_hash": hash_password("alex123"),
            "created_at": now_iso,
            "is_active": True
        }
    ]
    for u in users:
        db.users.update_one({"username": u["username"]}, {"$set": u}, upsert=True)
    print(f"[OK] Seeded 'users' collection ({db.users.count_documents({})} documents)")

    # 2. STUDENT PROFILES COLLECTION
    profiles = [
        {
            "user_id": "user_chitra",
            "name": "Chitra Yadav",
            "academic_year": "2nd Year",
            "branch": "Computer Science and Engineering",
            "career_goal": "AI Engineer",
            "target_role": "Artificial Intelligence Engineer",
            "skills": {
                "Python": 85,
                "SQL": 70,
                "Machine Learning": 40,
                "Data Structures": 75,
                "Statistics": 45
            },
            "weak_topics": ["Statistics", "Deep Learning", "System Design"],
            "completed_topics": ["Python Basics", "Object Oriented Programming", "SQL Fundamentals"],
            "learning_progress": {
                "Python": 85,
                "Machine Learning": 40,
                "Data Science": 55,
                "Algorithms": 65
            },
            "study_preferences": {
                "preferred_time": "Evening",
                "daily_hours": 2.0,
                "learning_style": "Hands-on projects & Code examples"
            },
            "interview_scores": {
                "Python": 8.0,
                "Machine Learning": 4.5,
                "AI Fundamentals": 6.0
            },
            "updated_at": now_iso
        },
        {
            "user_id": "chitra_demo_user",
            "name": "Chitra",
            "academic_year": "2nd Year",
            "branch": "Computer Science and Engineering",
            "career_goal": "AI Engineer",
            "target_role": "Artificial Intelligence Engineer",
            "skills": {
                "Python": 85,
                "SQL": 70,
                "Machine Learning": 40,
                "Data Structures": 75,
                "Statistics": 45
            },
            "weak_topics": ["Statistics", "Deep Learning"],
            "completed_topics": ["Python Basics", "Object Oriented Programming"],
            "learning_progress": {
                "Python": 85,
                "Machine Learning": 40
            },
            "study_preferences": {
                "preferred_time": "Evening",
                "daily_hours": 2.0
            },
            "interview_scores": {
                "Python": 8.0,
                "Machine Learning": 4.5
            },
            "updated_at": now_iso
        }
    ]
    for p in profiles:
        db.student_profiles.update_one({"user_id": p["user_id"]}, {"$set": p}, upsert=True)
    print(f"[OK] Seeded 'student_profiles' collection ({db.student_profiles.count_documents({})} documents)")

    # 3. LONG-TERM MEMORY COLLECTION
    memories = [
        {
            "memory_id": "mem_001",
            "user_id": "user_chitra",
            "memory_type": "career_goal",
            "content": "Target Career Goal is AI Engineer.",
            "importance": 1.0,
            "created_at": now_iso,
            "updated_at": now_iso,
            "source": "onboarding",
            "metadata": {"career_goal": "AI Engineer"}
        },
        {
            "memory_id": "mem_002",
            "user_id": "user_chitra",
            "memory_type": "skill",
            "content": "Student has strong proficiency in Python (85%).",
            "importance": 0.85,
            "created_at": now_iso,
            "updated_at": now_iso,
            "source": "skill_assessment",
            "metadata": {"skill": "Python", "score": 85}
        },
        {
            "memory_id": "mem_003",
            "user_id": "user_chitra",
            "memory_type": "weakness",
            "content": "Student is weak in Statistics and needs probability foundation review.",
            "importance": 0.90,
            "created_at": now_iso,
            "updated_at": now_iso,
            "source": "diagnostic",
            "metadata": {"weak_topic": "Statistics"}
        },
        {
            "memory_id": "mem_004",
            "user_id": "user_chitra",
            "memory_type": "preference",
            "content": "Prefers studying during evening hours (2.0 hours daily commitment).",
            "importance": 0.75,
            "created_at": now_iso,
            "updated_at": now_iso,
            "source": "preference_survey",
            "metadata": {"preferred_time": "Evening", "daily_hours": 2.0}
        },
        {
            "memory_id": "mem_005",
            "user_id": "user_chitra",
            "memory_type": "achievement",
            "content": "Scored 8.0/10 in Python Technical Mock Interview.",
            "importance": 0.80,
            "created_at": now_iso,
            "updated_at": now_iso,
            "source": "mock_interview_session",
            "metadata": {"score": 8.0, "topic": "Python"}
        }
    ]
    for m in memories:
        db.memory.update_one({"memory_id": m["memory_id"]}, {"$set": m}, upsert=True)
    for m in memories:
        m_copy = dict(m)
        m_copy["memory_id"] = "demo_" + m["memory_id"]
        m_copy["user_id"] = "chitra_demo_user"
        db.memory.update_one({"memory_id": m_copy["memory_id"]}, {"$set": m_copy}, upsert=True)
    print(f"[OK] Seeded 'memory' collection ({db.memory.count_documents({})} documents)")

    # 4. SKILLS COLLECTION
    skills_data = [
        {"skill_name": "Python", "category": "Programming", "difficulty": "Intermediate", "market_demand": 98},
        {"skill_name": "Machine Learning", "category": "AI/Data Science", "difficulty": "Advanced", "market_demand": 95},
        {"skill_name": "Deep Learning", "category": "AI/Data Science", "difficulty": "Advanced", "market_demand": 92},
        {"skill_name": "Statistics", "category": "Mathematics", "difficulty": "Intermediate", "market_demand": 88},
        {"skill_name": "Data Structures", "category": "Core CS", "difficulty": "Intermediate", "market_demand": 96},
        {"skill_name": "SQL", "category": "Databases", "difficulty": "Fundamental", "market_demand": 90},
        {"skill_name": "System Design", "category": "Software Architecture", "difficulty": "Advanced", "market_demand": 89}
    ]
    for s in skills_data:
        db.skills.update_one({"skill_name": s["skill_name"]}, {"$set": s}, upsert=True)
    print(f"[OK] Seeded 'skills' collection ({db.skills.count_documents({})} documents)")

    # 5. CAREER PROFILES COLLECTION
    career_profiles = [
        {
            "role": "AI Engineer",
            "required_skills": {"Python": 85, "Machine Learning": 80, "Deep Learning": 75, "Statistics": 70, "Data Structures": 70},
            "description": "Develops production GenAI models, autonomous agent frameworks, and neural network architectures.",
            "average_salary_range": "$120,000 - $185,000"
        },
        {
            "role": "Data Scientist",
            "required_skills": {"Python": 80, "SQL": 85, "Statistics": 85, "Machine Learning": 75, "Data Visualization": 75},
            "description": "Performs predictive modeling, hypothesis testing, and business insight extraction from big data.",
            "average_salary_range": "$115,000 - $170,000"
        },
        {
            "role": "Machine Learning Engineer",
            "required_skills": {"Python": 85, "Machine Learning": 85, "Deep Learning": 80, "System Design": 75, "MLOps": 75},
            "description": "Scales model training pipelines, optimizes inference latency, and deploys ML systems into production.",
            "average_salary_range": "$130,000 - $190,000"
        }
    ]
    for c in career_profiles:
        db.career_profiles.update_one({"role": c["role"]}, {"$set": c}, upsert=True)
    print(f"[OK] Seeded 'career_profiles' collection ({db.career_profiles.count_documents({})} documents)")

    # 6. STUDY PLANS COLLECTION
    study_plans = [
        {
            "plan_id": "plan_ai_eng_30days",
            "user_id": "user_chitra",
            "career_goal": "AI Engineer",
            "duration_days": 30,
            "daily_commitment_hours": 2.0,
            "preferred_time": "Evening",
            "total_estimated_study_hours": 60.0,
            "weak_topics_addressed": ["Statistics Foundation", "Machine Learning Core", "Deep Learning"],
            "created_at": now_iso
        }
    ]
    for sp in study_plans:
        db.study_plans.update_one({"plan_id": sp["plan_id"]}, {"$set": sp}, upsert=True)
    print(f"[OK] Seeded 'study_plans' collection ({db.study_plans.count_documents({})} documents)")

    # 7. DOCUMENTS COLLECTION (RAG)
    docs_data = [
        {
            "doc_id": "doc_ai_notes_01",
            "user_id": "user_chitra",
            "filename": "AI_Notes.txt",
            "file_type": "txt",
            "file_size": 1420,
            "chunk_count": 3,
            "summary": "AI Lecture Notes covering Informed State Space Search, Heuristics, Admissibility, and A* Search.",
            "upload_date": now_iso
        }
    ]
    for d in docs_data:
        db.documents.update_one({"doc_id": d["doc_id"]}, {"$set": d}, upsert=True)
    print(f"[OK] Seeded 'documents' collection ({db.documents.count_documents({})} documents)")

    # 8. CHAT HISTORY COLLECTION
    chat_logs = [
        {
            "user_id": "user_chitra",
            "conversation_id": "conv_init_sample",
            "user_message": "My name is Chitra. I want to become an AI Engineer. I know Python but weak in Machine Learning.",
            "agent_response": "Great to meet you Chitra! I have saved your target career as AI Engineer, noted your strong Python foundation, and flagged Machine Learning as a priority topic.",
            "tools_used": ["save_memory", "get_student_profile"],
            "agents_used": ["EduMind Coordinator", "Career Agent"],
            "timestamp": now_iso
        }
    ]
    for cl in chat_logs:
        db.chat_history.update_one({"conversation_id": cl["conversation_id"]}, {"$set": cl}, upsert=True)
    print(f"[OK] Seeded 'chat_history' collection ({db.chat_history.count_documents({})} documents)")

    # 9. INTERVIEW QUESTIONS COLLECTION
    interview_qs = [
        {
            "question_id": "q101",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "question": "Explain the difference between L1 (Lasso) and L2 (Ridge) Regularization and why L1 drives coefficients to zero.",
            "expected_keywords": ["Lasso", "Ridge", "sparsity", "diamond constraint", "L1 norm", "feature selection"]
        },
        {
            "question_id": "q102",
            "topic": "Python",
            "difficulty": "Medium",
            "question": "How do Python generators differ from regular functions, and what is the internal role of the yield keyword?",
            "expected_keywords": ["yield", "iterator", "lazy evaluation", "memory efficiency", "__next__"]
        },
        {
            "question_id": "q103",
            "topic": "AI Fundamentals",
            "difficulty": "Hard",
            "question": "What is the mathematical condition for a heuristic to be admissible and consistent in A* search?",
            "expected_keywords": ["admissible", "consistent", "triangle inequality", "h(n) <= h*(n)", "monotonic"]
        }
    ]
    for q in interview_qs:
        db.interview_questions.update_one({"question_id": q["question_id"]}, {"$set": q}, upsert=True)
    print(f"[OK] Seeded 'interview_questions' collection ({db.interview_questions.count_documents({})} documents)")

    # 10. INTERVIEW SESSIONS COLLECTION
    interview_sessions = [
        {
            "session_id": "sess_sample_01",
            "user_id": "user_chitra",
            "target_role": "AI Engineer",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "status": "completed",
            "total_score": 8.0,
            "feedback": "Strong conceptual clarity on regularization and cost functions.",
            "created_at": now_iso
        }
    ]
    for isess in interview_sessions:
        db.interview_sessions.update_one({"session_id": isess["session_id"]}, {"$set": isess}, upsert=True)
    print(f"[OK] Seeded 'interview_sessions' collection ({db.interview_sessions.count_documents({})} documents)")

    # 11. EVALUATION RESULTS COLLECTION
    eval_benchmark = {
        "eval_id": "eval_benchmark_initial",
        "timestamp": now_iso,
        "provider": "auto",
        "total_questions": 50,
        "accuracy_score": 0.942,
        "relevance_score": 0.965,
        "faithfulness_score": 0.950,
        "context_relevance_score": 0.910,
        "avg_latency_ms": 142.5,
        "total_tokens": 12450,
        "estimated_cost_usd": 0.0075
    }
    db.evaluation_results.update_one({"eval_id": eval_benchmark["eval_id"]}, {"$set": eval_benchmark}, upsert=True)
    print(f"[OK] Seeded 'evaluation_results' collection ({db.evaluation_results.count_documents({})} documents)")

    print("\n" + "=" * 65)
    print("ALL COLLECTIONS SUCCESSFULLY POPULATED IN MONGODB ATLAS!")
    print("=" * 65)
    return True


if __name__ == "__main__":
    seed_mongodb()
