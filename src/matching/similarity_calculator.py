from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """
    Computes similarity between resume and JD.

    Supports:
    - API mode (skill overlap only, no vectors)
    - Research mode (TF-IDF cosine similarity)

    🔒 LOCKED INVARIANT:
    - Always returns a normalized score (0.0 – 1.0)
    - Never crashes on None vectors
    """

    @staticmethod
    def weighted_similarity_score(
        resume_vector,
        jd_vector,
        resume_skills,
        jd_core_skills,
        jd_optional_skills,
        skill_depths,
        resume_archetype
    ):
        # ==============================
        # 🛑 API MODE (NO VECTORS)
        # ==============================
        if resume_vector is None or jd_vector is None:
            if not jd_core_skills:
                return 0.5  # neutral baseline

            core_overlap = len(resume_skills & jd_core_skills)
            optional_overlap = len(resume_skills & jd_optional_skills)

            core_score = core_overlap / max(len(jd_core_skills), 1)
            optional_score = optional_overlap / max(len(jd_optional_skills), 1)

            # Core skills dominate ATS behavior
            similarity = (0.75 * core_score) + (0.25 * optional_score)

            return round(similarity, 4)  # 🔒 0–1 ONLY

        # ==============================
        # 🧪 RESEARCH MODE (TF-IDF)
        # ==============================
        similarity = cosine_similarity(resume_vector, jd_vector)[0][0]
        return round(float(similarity), 4)
