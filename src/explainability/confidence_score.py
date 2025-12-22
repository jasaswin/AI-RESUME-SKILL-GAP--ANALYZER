
# src/explainability/confidence_score.py

import numpy as np


class ConfidenceScorer:
    """
    ML-based confidence scoring using similarity + skill coverage
    """

    def __init__(self):
        pass

    def compute_confidence(
        self,
        similarity_score: float,
        matched_skills: list,
        total_job_skills: int
    ) -> float:
        """
        Confidence is derived from:
        - cosine similarity (model output)
        - skill coverage ratio
        """

        if total_job_skills == 0:
            return 0.0

        coverage_ratio = len(matched_skills) / total_job_skills

        # Weighted confidence (ML-style scoring)
        confidence = (0.6 * similarity_score) + (0.4 * coverage_ratio)

        return round(confidence * 100, 2)

