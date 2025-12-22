class ScoreCalculator:
    """
    Combines TF-IDF similarity with skill coverage logic
    """

    @staticmethod
    def final_score(
        tfidf_score: float,
        resume_skills: set,
        core_skills: set,
        optional_skills: set
    ) -> float:

        core_match_ratio = (
            len(resume_skills & core_skills) / max(len(core_skills), 1)
        )

        optional_match_ratio = (
            len(resume_skills & optional_skills) / max(len(optional_skills), 1)
        )

        # Hybrid weighted score (ATS-style)
        final = (
            0.5 * tfidf_score +
            0.4 * core_match_ratio +
            0.1 * optional_match_ratio
        )

        return round(final * 100, 2)
