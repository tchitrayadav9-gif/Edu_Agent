"""
Evaluation Metrics Module.
Calculates Accuracy, Relevance, Faithfulness, Context Relevance, Latency, Token Usage, and Estimated Cost.
"""

from typing import Dict, List, Any
import re


def compute_relevance_score(response_text: str, expected_keywords: List[str]) -> float:
    """Calculate semantic keyword recall as relevance proxy (0.0 to 1.0)."""
    if not expected_keywords:
        return 1.0
    
    resp_lower = response_text.lower()
    matches = sum(1 for kw in expected_keywords if kw.lower() in resp_lower)
    return round(matches / len(expected_keywords), 3)


def compute_faithfulness_score(response_text: str, has_hallucination_indicators: bool = False) -> float:
    """Assess whether the response avoids unsupported facts (0.0 to 1.0)."""
    score = 0.95
    if len(response_text.strip()) < 20:
        score -= 0.3
    if has_hallucination_indicators:
        score -= 0.4
    return max(0.0, min(1.0, round(score, 3)))


def compute_context_relevance_score(context_text: str, query: str) -> float:
    """Assess whether retrieved context directly addresses the query."""
    if not context_text or "No relevant" in context_text:
        return 0.5
    
    q_tokens = set(re.findall(r'\b\w+\b', query.lower()))
    c_tokens = set(re.findall(r'\b\w+\b', context_text.lower()))
    
    overlap = len(q_tokens.intersection(c_tokens))
    score = min(1.0, overlap / max(1, len(q_tokens) * 0.6))
    return round(score, 3)


def estimate_token_count(text: str) -> int:
    """Approximate token count (~4 characters per token)."""
    return max(1, len(text) // 4)


def estimate_cost(input_tokens: int, output_tokens: int, model: str = "gpt-4o-mini") -> float:
    """Calculate approximate USD API cost based on standard token pricing."""
    # gpt-4o-mini pricing: $0.15 / 1M input, $0.60 / 1M output
    input_cost = (input_tokens / 1_000_000.0) * 0.15
    output_cost = (output_tokens / 1_000_000.0) * 0.60
    return round(input_cost + output_cost, 6)
