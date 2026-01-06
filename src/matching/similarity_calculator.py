from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """
    Computes similarity between resume and job skill vectors
    """

    @staticmethod
    def weighted_similarity_score(
        resume_vector,
        jd_vector,
        resume_skills: set,
        jd_core_skills: set,
        jd_optional_skills: set,
        skill_depths: dict
    ) -> float:
        """
        Returns a clean TF-IDF cosine similarity score.
        Role-awareness is handled in ScoreCalculator, NOT here.
        """

        # ---- SAFETY: Ensure 2D matrices ----
        if resume_vector.ndim == 1:
            resume_vector = resume_vector.reshape(1, -1)

        if jd_vector.ndim == 1:
            jd_vector = jd_vector.reshape(1, -1)

        # ---- Base cosine similarity ----
        similarity = cosine_similarity(resume_vector, jd_vector)[0][0]

        return round(float(similarity), 4)
