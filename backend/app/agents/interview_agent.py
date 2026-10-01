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
    """Adaptive Mock Interview Agent with scoring and memory persistence."""
    
    def __init__(self):
        self.db = db_manager
        self.ltm = long_term_memory

    def start_session(self, user_id: str, target_role: str = "AI Engineer", topic: str = "Machine Learning") -> Dict[str, Any]:
        """Initialize new mock interview session and return initial question."""
        session_id = str(uuid.uuid4())
        
        # Check previous student performance on this topic
        profile = self.db.student_profiles.find_one({"user_id": user_id}) or {}
        prev_scores = profile.get("interview_scores", {})
        topic_score = prev_scores.get(topic, 6.0)

        # Adaptive initial difficulty selection
        if topic_score >= 8.0:
            difficulty = "Hard"
        elif topic_score <= 5.0:
            difficulty = "Easy"
        else:
            difficulty = "Medium"

        # Question pool
        first_q = {
            "question_id": f"q_{topic.lower()[:3]}_01",
            "topic": topic,
            "difficulty": difficulty,
            "question": (
                "Explain the difference between L1 (Lasso) and L2 (Ridge) Regularization. "
                "How does the L1 penalty induce sparsity in learned feature weights?"
                if topic == "Machine Learning" else
                f"Explain the core algorithmic principles, trade-offs, and practical considerations of {topic}."
            ),
            "expected_keywords": ["Lasso", "Ridge", "sparsity", "penalty", "L1 norm", "feature selection", "loss"]
        }

        session_doc = {
            "session_id": session_id,
            "user_id": user_id,
            "target_role": target_role,
            "topic": topic,
            "difficulty": difficulty,
            "status": "in_progress",
            "current_question": first_q,
            "questions_answered": [],
            "total_score": 0.0,
            "created_at": datetime.utcnow().isoformat()
        }
        self.db.interview_sessions.insert_one(session_doc)

        return {
            "agent_name": "Interview Agent",
            "session_id": session_id,
            "target_role": target_role,
            "topic": topic,
            "difficulty": difficulty,
            "question": first_q["question"]
        }

    def evaluate_answer(
        self,
        session_id: str,
        user_id: str,
        student_answer: str
    ) -> Dict[str, Any]:
        """
        Evaluate student response, score 0-10, provide feedback, adjust difficulty,
        and save score into long-term memory.
        """
        session = self.db.interview_sessions.find_one({"session_id": session_id})
        topic = session.get("topic", "Machine Learning") if session else "Machine Learning"
        
        # Heuristic scoring based on keyword coverage and depth
        keywords = ["l1", "l2", "lasso", "ridge", "sparsity", "penalty", "norm", "zero", "feature", "loss", "weights"]
        ans_lower = student_answer.lower()
        matched_kw = [k for k in keywords if k in ans_lower]
        
        # Compute score out of 10
        base_score = min(10.0, max(3.0, (len(matched_kw) / 6.0) * 10.0))
        if len(student_answer.split()) < 10:
            base_score = min(base_score, 4.0)
        
        score = round(base_score, 1)

        # Construct constructive feedback
        if score >= 8.0:
            feedback = "Excellent response! You clearly articulated the geometric/mathematical mechanics and sparsity intuition."
            next_diff = "Hard"
            next_q = "How does ElasticNet regularization combine L1 and L2 to handle highly correlated feature clusters?"
        elif score >= 5.0:
            feedback = "Good foundation! You highlighted the key differences, but consider detailing why the diamond contour hits axes at zero."
            next_diff = "Medium"
            next_q = "What is the Bias-Variance Tradeoff, and how does regularization affect the model's bias and variance?"
        else:
            feedback = "Developing! Ensure you review the mathematical penalty term for L1 (|w|) vs L2 (w^2) and the concept of feature selection."
            next_diff = "Easy"
            next_q = "What is overfitting in machine learning, and why do we use a separate validation dataset?"

        # 1. Update Student Profile Scores
        profile = self.db.student_profiles.find_one({"user_id": user_id})
        if profile:
            interview_scores = profile.get("interview_scores", {})
            interview_scores[topic] = score
            self.db.student_profiles.update_one(
                {"user_id": user_id},
                {"$set": {"interview_scores": interview_scores}}
            )

        # 2. Save Score into Long-Term Memory
        self.ltm.save_memory(
            user_id=user_id,
            memory_type="achievement" if score >= 7.0 else "weakness",
            content=f"Scored {score}/10 in {topic} mock interview session.",
            importance=0.85,
            source=f"interview_session:{session_id}",
            metadata={"topic": topic, "score": score, "difficulty": next_diff}
        )

        return {
            "agent_name": "Interview Agent",
            "session_id": session_id,
            "topic": topic,
            "score": score,
            "feedback": feedback,
            "keywords_detected": matched_kw,
            "adaptive_next_difficulty": next_diff,
            "next_question": next_q
        }


# Global interview agent instance
interview_agent = InterviewAgent()
