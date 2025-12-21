

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SimilarityCalculator:
    """
    Computes similarity between resume and job skill vectors
    """

    @staticmethod
    def cosine_similarity_score(resume_vector, jd_vector) -> float:
        """
        Returns cosine similarity score between two vectors
        """
        if resume_vector.shape != jd_vector.shape:
            raise ValueError("Vectors must have same shape")

        score = cosine_similarity(resume_vector, jd_vector)[0][0]
        return round(float(score), 4)
