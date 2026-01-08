from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """
    Computes TF-IDF similarity with role-aware weighting
    and Phase-5 stability safeguards.
    """

    @staticmethod
    def weighted_similarity_score(
        resume_vector,
        jd_vector,
        resume_skills: set,
        jd_core_skills: set,
        jd_optional_skills: set,
        skill_depths: dict,
        resume_archetype: str = "general"
    ) -> float:

        # -------- Base cosine similarity (ALWAYS initialize) --------
        similarity = cosine_similarity(resume_vector, jd_vector)[0][0]

        # -------- Defensive clamp --------
        similarity = max(0.0, min(similarity, 1.0))

        # -------- Weighted core skill amplification --------
        weighted_score = 0.0

        for skill in resume_skills & jd_core_skills:
            weight = SimilarityCalculator.get_skill_weight(
                skill, resume_archetype, skill_depths
            )
            weighted_score += weight

        if jd_core_skills:
            amplification = min(weighted_score / len(jd_core_skills), 1.2)
            similarity *= amplification

        # -------- Final clamp --------
        return round(float(max(0.0, min(similarity, 1.0))), 4)

    @staticmethod
    def get_skill_weight(skill: str, archetype: str, skill_depths: dict) -> float:
        """
        Role + depth aware weighting
        """

        base_weight = {
            "advanced": 1.2,
            "intermediate": 1.0,
            "beginner": 0.8
        }.get(skill_depths.get(skill, "beginner"), 0.8)

        archetype_boost = {
            "frontend": ["react", "javascript", "css"],
            "backend": ["python", "java", "nodejs"],
            "data": ["sql", "python", "machine learning"]
        }

        if skill in archetype_boost.get(archetype, []):
            base_weight *= 1.15

        return base_weight
