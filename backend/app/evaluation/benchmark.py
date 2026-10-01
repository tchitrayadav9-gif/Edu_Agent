"""
Evaluation Benchmark Runner.
Executes the full 50-question benchmark suite against EduMind Agent, computes quantitative metrics,
and persists benchmark run logs to MongoDB.
"""

import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from .dataset_50 import EVALUATION_DATASET_50
from .metrics import (
    compute_relevance_score,
    compute_faithfulness_score,
    compute_context_relevance_score,
    estimate_token_count,
    estimate_cost
)
from ..database.mongodb import db_manager
from ..agents.main_agent import main_agent
from ..database.models import ChatRequest

logger = logging.getLogger("edumind.evaluation")


class BenchmarkRunner:
    """Automated benchmark test suite execution engine."""
    
    def __init__(self):
        self.dataset = EVALUATION_DATASET_50
        self.db = db_manager

    async def run_full_benchmark(self, sample_size: int = 50, provider: str = "auto") -> Dict[str, Any]:
        """Execute benchmark evaluation and return aggregate performance metrics."""
        test_cases = self.dataset[:sample_size]
        results_breakdown = []
        
        total_latency_ms = 0.0
        total_input_tokens = 0
        total_output_tokens = 0
        relevance_scores = []
        faithfulness_scores = []
        context_relevance_scores = []

        demo_user_id = "eval_student_user"

        for tc in test_cases:
            t_start = time.perf_counter()
            req = ChatRequest(message=tc["question"], provider=provider)
            
            chat_resp = await main_agent.process_message(demo_user_id, req)
            elapsed_ms = (time.perf_counter() - t_start) * 1000
            total_latency_ms += elapsed_ms

            # Compute metrics
            rel_score = compute_relevance_score(chat_resp.response, tc.get("expected_keywords", []))
            faith_score = compute_faithfulness_score(chat_resp.response)
            ctx_score = compute_context_relevance_score(chat_resp.response, tc["question"])

            relevance_scores.append(rel_score)
            faithfulness_scores.append(faith_score)
            context_relevance_scores.append(ctx_score)

            in_tok = estimate_token_count(tc["question"])
            out_tok = estimate_token_count(chat_resp.response)
            total_input_tokens += in_tok
            total_output_tokens += out_tok

            results_breakdown.append({
                "id": tc["id"],
                "category": tc["category"],
                "question": tc["question"],
                "relevance_score": rel_score,
                "faithfulness_score": faith_score,
                "context_relevance_score": ctx_score,
                "latency_ms": round(elapsed_ms, 2),
                "intent_detected": chat_resp.intent,
                "response_preview": chat_resp.response[:120] + "..."
            })

        n = len(test_cases)
        avg_relevance = round(sum(relevance_scores) / n, 3) if n else 0.0
        avg_faithfulness = round(sum(faithfulness_scores) / n, 3) if n else 0.0
        avg_context_relevance = round(sum(context_relevance_scores) / n, 3) if n else 0.0
        avg_latency = round(total_latency_ms / n, 2) if n else 0.0
        
        # Accuracy composite: (relevance * 0.5) + (faithfulness * 0.3) + (context_rel * 0.2)
        accuracy_score = round((avg_relevance * 0.5) + (avg_faithfulness * 0.3) + (avg_context_relevance * 0.2), 3)
        
        total_tokens = total_input_tokens + total_output_tokens
        est_cost = estimate_cost(total_input_tokens, total_output_tokens)

        eval_doc = {
            "eval_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "provider": provider,
            "total_questions": n,
            "accuracy_score": accuracy_score,
            "relevance_score": avg_relevance,
            "faithfulness_score": avg_faithfulness,
            "context_relevance_score": avg_context_relevance,
            "avg_latency_ms": avg_latency,
            "total_tokens": total_tokens,
            "estimated_cost_usd": est_cost,
            "results_breakdown": results_breakdown
        }

        self.db.evaluation_results.insert_one(eval_doc)
        logger.info(f"Evaluation benchmark complete ({n} questions): Accuracy {accuracy_score}, Avg Latency {avg_latency}ms")

        return eval_doc

    def get_latest_results(self) -> Optional[Dict[str, Any]]:
        """Retrieve the most recent evaluation benchmark from database."""
        docs = self.db.evaluation_results.find()
        return docs[-1] if docs else None


# Global benchmark runner instance
benchmark_runner = BenchmarkRunner()
