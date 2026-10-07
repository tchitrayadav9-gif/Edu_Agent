"""
Interview Agent Module.
Conducts adaptive mock technical interviews, evaluates student answers with scoring & feedback,
adapts difficulty dynamically, and logs topic scores into long-term student memory.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from ..database.mongodb import db_manager
from ..memory.long_term_memory import long_term_memory


class InterviewAgent:
    """Adaptive Mock Interview Agent with multi-factor scoring and shared memory persistence."""
    
    def __init__(self):
        self.db = db_manager
        self.ltm = long_term_memory

        # Comprehensive question bank
        self.question_bank = {
            "Machine Learning": [
                {
                    "q": "Explain the difference between L1 (Lasso) and L2 (Ridge) Regularization. Why does L1 regularization drive coefficients to absolute zero while L2 shrinks them smoothly?",
                    "keywords": ["lasso", "ridge", "sparsity", "penalty", "norm", "zero", "feature", "loss", "weights", "regularization", "shrinkage"]
                },
                {
                    "q": "What is the Bias-Variance Tradeoff in machine learning? How do model complexity, underfitting, and overfitting relate to this tradeoff?",
                    "keywords": ["bias", "variance", "tradeoff", "overfitting", "underfitting", "complexity", "generalization", "error", "noise"]
                },
                {
                    "q": "How does gradient descent work mathematically, and what are the key differences between Batch, Stochastic (SGD), and Mini-Batch Gradient Descent?",
                    "keywords": ["gradient", "derivative", "learning rate", "batch", "sgd", "mini-batch", "convergence", "epoch", "loss", "step"]
                },
                {
                    "q": "Explain the mechanics of Decision Trees and how Random Forests use Bagging and feature sub-sampling to reduce variance.",
                    "keywords": ["decision tree", "random forest", "bagging", "bootstrap", "variance", "ensemble", "gini", "entropy", "split"]
                }
            ],
            "Python": [
                {
                    "q": "How do Python generators differ from regular functions, and what is the role of the yield keyword in memory efficiency?",
                    "keywords": ["generator", "yield", "iterator", "memory", "lazy", "stream", "next", "state", "collection"]
                },
                {
                    "q": "Explain the Global Interpreter Lock (GIL) in CPython. How does it impact multi-threaded CPU-bound programs vs I/O-bound programs?",
                    "keywords": ["gil", "thread", "cpu", "io", "cpython", "concurrency", "multiprocessing", "asyncio", "lock"]
                },
                {
                    "q": "What is the difference between shallow copy and deep copy in Python? Give an example involving nested data structures.",
                    "keywords": ["shallow", "deep", "copy", "nested", "reference", "mutable", "object", "memory", "id"]
                }
            ],
            "AI Fundamentals": [
                {
                    "q": "What is the mathematical definition of heuristic admissibility and consistency in A* Search? Why is an admissible heuristic guaranteed to find the optimal path?",
                    "keywords": ["admissible", "consistent", "heuristic", "a*", "optimal", "triangle inequality", "underestimate", "cost", "h(n)"]
                },
                {
                    "q": "Explain Alpha-Beta Pruning in adversarial search. Under what move-ordering conditions is pruning most effective?",
                    "keywords": ["alpha", "beta", "pruning", "minimax", "game", "branch", "cutoff", "optimal", "ordering", "tree"]
                },
                {
                    "q": "How does a Bayesian Belief Network represent conditional independence, and how is Bayes' Theorem used to update posterior probabilities?",
                    "keywords": ["bayes", "prior", "posterior", "conditional", "independence", "dag", "network", "evidence", "probability"]
                }
            ],
            "Data Structures": [
                {
                    "q": "Explain the time and space complexity trade-offs of QuickSort vs MergeSort. In what scenarios would you prefer HeapSort?",
                    "keywords": ["quicksort", "mergesort", "heapsort", "time", "space", "o(n log n)", "worst case", "pivot", "in-place", "stable"]
                },
                {
                    "q": "How does a Hash Table handle collisions using Open Addressing vs Chaining, and what factors degrade search performance to O(n)?",
                    "keywords": ["hash", "collision", "chaining", "open addressing", "probing", "load factor", "o(1)", "o(n)", "bucket"]
                }
            ],
            "HR & Behavioral": [
                {
                    "q": "Describe a challenging technical project you worked on where you encountered an unexpected roadblock. How did you overcome it?",
                    "keywords": ["project", "challenge", "solution", "debug", "team", "learned", "outcome", "result", "improved", "deadline"]
                },
                {
                    "q": "Where do you see yourself in 3 years in your AI and Software Engineering career, and what technical milestones are you pursuing?",
                    "keywords": ["career", "growth", "lead", "ai", "engineer", "learning", "contribution", "skills", "projects", "impact"]
                }
            ]
        }

    def start_session(
        self,
        user_id: str,
        target_role: str = "AI Engineer",
        topic: str = "Machine Learning",
        interview_type: str = "Technical",
        num_questions: int = 3
    ) -> Dict[str, Any]:
        """Initialize new mock interview session and return initial question."""
        session_id = str(uuid.uuid4())
        
        # Check previous student performance on this topic for adaptive difficulty
        profile = self.db.student_profiles.find_one({"user_id": user_id}) or {}
        prev_scores = profile.get("interview_scores", {})
        topic_score = prev_scores.get(topic, 6.0)

        if topic_score >= 8.0:
            difficulty = "Advanced"
        elif topic_score <= 5.0:
            difficulty = "Beginner"
        else:
            difficulty = "Intermediate"

        # Select questions from bank
        questions_pool = self.question_bank.get(topic, self.question_bank["Machine Learning"])
        total_q = min(len(questions_pool), max(1, num_questions))
        
        first_q = questions_pool[0]

        session_doc = {
            "session_id": session_id,
            "user_id": user_id,
            "target_role": target_role,
            "topic": topic,
            "interview_type": interview_type,
            "difficulty": difficulty,
            "total_questions": total_q,
            "current_index": 0,
            "status": "in_progress",
            "questions_pool": questions_pool[:total_q],
            "answers_history": [],
            "total_score": 0.0,
            "created_at": datetime.utcnow().isoformat()
        }
        self.db.interview_sessions.insert_one(session_doc)

        return {
            "agent_name": "Interview Agent",
            "session_id": session_id,
            "target_role": target_role,
            "topic": topic,
            "interview_type": interview_type,
            "difficulty": difficulty,
            "question_index": 1,
            "total_questions": total_q,
            "question": first_q["q"]
        }

    def evaluate_answer(
        self,
        session_id: str,
        user_id: str,
        student_answer: str
    ) -> Dict[str, Any]:
        """
        Evaluate student response across multi-factor rubric, update session,
        provide constructive feedback, and return next question or final evaluation report.
        """
        session = self.db.interview_sessions.find_one({"session_id": session_id})
        if not session:
            topic = "Machine Learning"
            curr_idx = 0
            questions_pool = self.question_bank[topic]
        else:
            topic = session.get("topic", "Machine Learning")
            curr_idx = session.get("current_index", 0)
            questions_pool = session.get("questions_pool", self.question_bank.get(topic, self.question_bank["Machine Learning"]))

        current_q = questions_pool[curr_idx] if curr_idx < len(questions_pool) else questions_pool[-1]
        keywords = current_q.get("keywords", ["concept", "logic", "explanation", "analysis"])
        
        # Scoring metrics (0-100 scale)
        ans_lower = student_answer.lower()
        matched_kw = [k for k in keywords if k in ans_lower]
        kw_ratio = min(1.0, len(matched_kw) / max(1, min(4, len(keywords))))
        word_count = len(student_answer.split())

        # Multi-factor Rubric
        technical_score = min(100, max(30, int(kw_ratio * 70 + (20 if word_count >= 10 else 10) + (10 if word_count >= 25 else 0))))
        communication_score = min(100, max(40, int(min(1.0, word_count / 25.0) * 50 + 35 + (15 if "." in student_answer else 0))))
        problem_solving_score = min(100, max(30, int(technical_score * 0.6 + communication_score * 0.4)))
        confidence_score = min(100, max(50, int(85 if word_count >= 15 else 70)))
        
        overall_score = round((technical_score * 0.4 + problem_solving_score * 0.3 + communication_score * 0.2 + confidence_score * 0.1), 1)
        scale_10 = round(overall_score / 10.0, 1)

        # Construct actionable feedback
        if scale_10 >= 8.0:
            feedback = "Outstanding response! You demonstrated solid depth, articulated technical principles clearly, and covered core trade-offs."
        elif scale_10 >= 5.5:
            feedback = "Good response! You captured the main concept, but adding more mathematical formulation and edge-case handling will elevate your answer."
        else:
            feedback = "Developing! Focus on reviewing foundational definitions, penalty formulations, and specific algorithmic mechanics."

        answer_record = {
            "question_index": curr_idx + 1,
            "question": current_q.get("q", ""),
            "answer": student_answer,
            "score_10": scale_10,
            "overall_score": overall_score,
            "technical_score": technical_score,
            "communication_score": communication_score,
            "problem_solving_score": problem_solving_score,
            "confidence_score": confidence_score,
            "feedback": feedback,
            "keywords_detected": matched_kw
        }

        answers_hist = session.get("answers_history", []) if session else []
        answers_hist.append(answer_record)
        next_idx = curr_idx + 1
        is_completed = next_idx >= len(questions_pool)

        # Update Session Record
        if session:
            self.db.interview_sessions.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "current_index": next_idx,
                        "status": "completed" if is_completed else "in_progress",
                        "answers_history": answers_hist,
                        "total_score": scale_10
                    }
                }
            )

        # 1. Update Student Profile Scores in Shared Memory
        profile = self.db.student_profiles.find_one({"user_id": user_id})
        if profile:
            interview_scores = profile.get("interview_scores", {})
            interview_scores[topic] = scale_10
            
            # If student scored low, automatically tag as weak topic for Learning Agent
            weak_topics = list(profile.get("weak_topics", []))
            if scale_10 < 6.0 and topic not in weak_topics:
                weak_topics.append(topic)
            elif scale_10 >= 8.0 and topic in weak_topics:
                weak_topics.remove(topic)

            self.db.student_profiles.update_one(
                {"user_id": user_id},
                {"$set": {"interview_scores": interview_scores, "weak_topics": weak_topics}}
            )

        # 2. Save Score into Long-Term Memory
        self.ltm.save_memory(
            user_id=user_id,
            memory_type="achievement" if scale_10 >= 7.0 else "weakness",
            content=f"Scored {scale_10}/10 ({overall_score}%) in {topic} mock technical interview.",
            importance=0.85,
            source=f"interview_session:{session_id}",
            metadata={"topic": topic, "score": scale_10, "overall_score": overall_score}
        )

        final_report = None
        if is_completed:
            avg_tech = round(sum(a["technical_score"] for a in answers_hist) / max(1, len(answers_hist)), 1)
            avg_comm = round(sum(a["communication_score"] for a in answers_hist) / max(1, len(answers_hist)), 1)
            avg_ps = round(sum(a["problem_solving_score"] for a in answers_hist) / max(1, len(answers_hist)), 1)
            avg_conf = round(sum(a["confidence_score"] for a in answers_hist) / max(1, len(answers_hist)), 1)
            final_overall = round(sum(a["overall_score"] for a in answers_hist) / max(1, len(answers_hist)), 1)

            final_report = {
                "overall_score": final_overall,
                "score_10": round(final_overall / 10.0, 1),
                "technical_score": avg_tech,
                "communication_score": avg_comm,
                "problem_solving_score": avg_ps,
                "confidence_score": avg_conf,
                "strengths": [topic, "Core Programming"] if final_overall >= 70 else ["Basic Concepts"],
                "weak_areas": [] if final_overall >= 80 else [f"{topic} Advanced Formulation", "Edge-Case Handling"],
                "recommended_improvements": (
                    f"Practice implementing {topic} algorithms from scratch and deriving mathematical loss functions."
                    if final_overall < 75 else
                    f"Great performance! Proceed to high-level System Design and architectural mock interviews."
                )
            }

        next_question_text = questions_pool[next_idx]["q"] if not is_completed else None

        return {
            "agent_name": "Interview Agent",
            "session_id": session_id,
            "topic": topic,
            "question_index": curr_idx + 1,
            "total_questions": len(questions_pool),
            "is_completed": is_completed,
            "score": scale_10,
            "overall_score": overall_score,
            "technical_score": technical_score,
            "communication_score": communication_score,
            "problem_solving_score": problem_solving_score,
            "confidence_score": confidence_score,
            "feedback": feedback,
            "keywords_detected": matched_kw,
            "next_question": next_question_text,
            "final_report": final_report
        }


# Global interview agent instance
interview_agent = InterviewAgent()

