"""
Bayesian Reasoning & Uncertainty Module for Career Guidance.
Applies Bayesian probability theory to calculate career suitability distributions under uncertainty,
integrating prior career distribution, conditional likelihood of student skills, and evidence updating.
"""

from typing import Dict, List, Any, Optional
import math


class BayesianCareerNetwork:
    """Bayesian Belief Network for Career Suitability Assessment."""
    
    def __init__(self):
        # 1. Prior probabilities for candidate career roles P(Career)
        self.priors: Dict[str, float] = {
            "AI Engineer": 0.25,
            "Machine Learning Engineer": 0.25,
            "Data Scientist": 0.25,
            "Software Engineer (Backend)": 0.25
        }

        # 2. Conditional Likelihoods P(Skill | Career)
        # Represents how strongly each skill is required / expected in that career track
        self.conditional_skill_likelihood: Dict[str, Dict[str, float]] = {
            "AI Engineer": {
                "Python": 0.95,
                "Machine Learning": 0.90,
                "Deep Learning": 0.92,
                "Statistics": 0.85,
                "AI Agents": 0.90,
                "Data Structures": 0.75,
                "SQL": 0.70,
                "System Design": 0.80
            },
            "Machine Learning Engineer": {
                "Python": 0.92,
                "Machine Learning": 0.95,
                "Deep Learning": 0.88,
                "Statistics": 0.90,
                "AI Agents": 0.70,
                "Data Structures": 0.80,
                "SQL": 0.75,
                "System Design": 0.82
            },
            "Data Scientist": {
                "Python": 0.90,
                "Machine Learning": 0.85,
                "Deep Learning": 0.65,
                "Statistics": 0.95,
                "AI Agents": 0.50,
                "Data Structures": 0.65,
                "SQL": 0.95,
                "System Design": 0.60
            },
            "Software Engineer (Backend)": {
                "Python": 0.90,
                "Machine Learning": 0.40,
                "Deep Learning": 0.30,
                "Statistics": 0.50,
                "AI Agents": 0.45,
                "Data Structures": 0.95,
                "SQL": 0.90,
                "System Design": 0.95
            }
        }

    def calculate_career_probabilities(
        self,
        student_skills: Dict[str, int],  # skill -> score (0-100)
        weak_topics: Optional[List[str]] = None,
        career_interest: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compute posterior probabilities P(Career | Evidence) using Bayes' Rule.
        Evidence: observed skill proficiencies, reported weaknesses, and stated interest.
        """
        weak_topics = weak_topics or []
        posteriors: Dict[str, float] = {}
        explanation_breakdown: Dict[str, List[str]] = {}

        for career, prior in self.priors.items():
            likelihood_log = 0.0
            reasons = []

            # Factor in stated interest prior boost
            if career_interest and career_interest.lower() in career.lower():
                likelihood_log += math.log(1.5)
                reasons.append(f"Direct student career interest in '{career_interest}' boosts prior likelihood.")

            cond_probs = self.conditional_skill_likelihood.get(career, {})

            for skill_name, req_weight in cond_probs.items():
                student_score = student_skills.get(skill_name, 50)
                is_weak = any(w.lower() in skill_name.lower() for w in weak_topics)
                
                if is_weak:
                    student_score = min(student_score, 35)

                # Likelihood factor: how well student's score matches the career requirement
                # Normalized between 0.2 and 1.0
                match_prob = 0.3 + 0.7 * (1.0 - abs((student_score / 100.0) - req_weight))
                likelihood_log += math.log(match_prob)

                if student_score >= 75 and req_weight >= 0.8:
                    reasons.append(f"Strong proficiency in {skill_name} ({student_score}%) satisfies key prerequisite ({round(req_weight*100)}% importance).")
                elif is_weak and req_weight >= 0.8:
                    reasons.append(f"Weakness in {skill_name} lowers current confidence for {career} (requires {round(req_weight*100)}% mastery).")

            # P(Career | Evidence) ~ P(Evidence | Career) * P(Career)
            unnormalized_posterior = math.exp(likelihood_log) * prior
            posteriors[career] = unnormalized_posterior
            explanation_breakdown[career] = reasons

        # Normalize posteriors to sum to 100%
        total_prob = sum(posteriors.values()) or 1.0
        normalized_results = []
        for career, unnorm in posteriors.items():
            percentage = round((unnorm / total_prob) * 100, 1)
            normalized_results.append({
                "career_role": career,
                "confidence_percentage": percentage,
                "confidence_score": round(percentage / 100.0, 3),
                "key_evidence": explanation_breakdown[career][:3]
            })

        # Sort descending by confidence percentage
        normalized_results.sort(key=lambda x: x["confidence_percentage"], reverse=True)

        return {
            "recommendations": normalized_results,
            "top_career": normalized_results[0]["career_role"],
            "disclaimer": (
                "Bayesian confidence scores represent probabilistic suitability based on current evidence (skills, weaknesses, and interests). "
                "These are not guaranteed outcomes and can be enhanced through targeted study."
            )
        }


# Global bayesian network instance
bayesian_career_network = BayesianCareerNetwork()
