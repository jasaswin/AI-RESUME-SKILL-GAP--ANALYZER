from src.matching.role_profiles import ROLE_PROFILES


class ScoreCalculator:
    """
    Role-aware final scoring engine (production-grade)
    """

    @staticmethod
    def final_score(
        similarity_score: float,
        resume_skills: set,
        core_skills: set,
        optional_skills: set,
        skill_depths: dict,
        role: str = "ai_ml_developer"
    ) -> float:

        profile = ROLE_PROFILES.get(role, ROLE_PROFILES["ai_ml_developer"])
        weights = profile["weights"]

        # -------- Normalize weights (CRITICAL) --------
        total_weight = sum(weights.values())
        weights = {k: v / total_weight for k, v in weights.items()}

        # -------- Coverage --------
        core_coverage = len(resume_skills & core_skills) / max(len(core_skills), 1)
        optional_coverage = len(resume_skills & optional_skills) / max(len(optional_skills), 1)

        # -------- Depth bonus (role-aware amplification) --------
        depth_score = 0.0
        priority_skills = profile["depth_priority"]

        for skill in resume_skills & priority_skills:
            depth = skill_depths.get(skill, "beginner")
            depth_score += {
                "advanced": 1.0,
                "intermediate": 0.6,
                "beginner": 0.2
            }.get(depth, 0)

        depth_bonus = depth_score / max(len(priority_skills), 1)

        # -------- Base score --------
        score = (
            weights["tfidf"] * similarity_score +
            weights["core_coverage"] * core_coverage +
            weights["optional_coverage"] * optional_coverage +
            weights["depth_bonus"] * depth_bonus
        )

        # -------- Graduated core penalty --------
        missing_core_count = len(core_skills - resume_skills)
        total_core = max(len(core_skills), 1)

        penalty_factor = 1 - (
            profile["missing_core_penalty"] * (missing_core_count / total_core)
        )

        score *= max(penalty_factor, 0.6)  # never fully destroy score

        return round(min(score, 1.0) * 100, 2)
