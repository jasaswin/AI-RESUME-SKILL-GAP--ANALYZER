from typing import Set, Dict
from src.matching.role_profiles import ROLE_PROFILES
from src.intelligence.stability_engine import StabilityEngine
from src.skills.skill_database import SkillDatabase


SKILL_CATEGORY_TO_DOMAIN = {
    "language": "engineering",
    "framework": "engineering",
    "tool": "engineering",
    "concept": "engineering",
    "analytics": "analytics",
    "business": "business",
    "design": "design",
    "quality": "engineering",
}


class ScoreCalculator:
    """
    Production-grade, failure-resistant final scoring engine.

    Guarantees:
    - No score collapse
    - Entry-level fairness
    - Domain-aware weighting
    - Deterministic output
    """

    @staticmethod
    def final_score(
        similarity_score: float,
        resume_skills: Set[str],
        core_skills: Set[str],
        optional_skills: Set[str],
        skill_depths: Dict[str, str],
        role: str = "mern_stack_developer",
        inferred_skills: Set[str] | None = None,
        jd_domain: str | None = None,
    ) -> float:

        # -------------------- 0️⃣ Defensive Defaults --------------------
        resume_skills = resume_skills or set()
        core_skills = core_skills or set()
        optional_skills = optional_skills or set()
        inferred_skills = inferred_skills or set()

        effective_skills = resume_skills | inferred_skills

        profile = ROLE_PROFILES.get(role, ROLE_PROFILES["ai_ml_developer"])
        weights = profile.get("weights") or {
            "tfidf": 0.4,
            "core_coverage": 0.4,
            "optional_coverage": 0.1,
            "depth_bonus": 0.1,
        }

        # Normalize weights
        total_weight = sum(weights.values())
        weights = {k: v / total_weight for k, v in weights.items()}

        # -------------------- 1️⃣ Domain-aware Coverage --------------------
        skill_db = SkillDatabase()

        def domain_multiplier(skill: str) -> float:
            if not jd_domain:
                return 1.0

            category = skill_db.get_category(skill)
            if not category:
                return 1.0

            skill_domain = SKILL_CATEGORY_TO_DOMAIN.get(category)
            if not skill_domain or skill_domain == jd_domain:
                return 1.0

            return {
                ("engineering", "analytics"): 0.6,
                ("analytics", "engineering"): 0.6,
                ("analytics", "business"): 0.5,
                ("business", "analytics"): 0.5,
                ("engineering", "design"): 0.4,
                ("design", "engineering"): 0.4,
            }.get((skill_domain, jd_domain), 0.25)

        def weighted_coverage(skills: Set[str], target: Set[str]) -> float:
            if not target:
                return 1.0
            return sum(domain_multiplier(s) for s in skills & target) / len(target)

        core_coverage = weighted_coverage(effective_skills, core_skills)
        optional_coverage = weighted_coverage(effective_skills, optional_skills)

        # -------------------- 2️⃣ Depth Bonus (Explicit Only) --------------------
        depth_priority = profile.get("depth_priority", set())
        depth_score = 0.0

        for skill in resume_skills & depth_priority:
            depth_score += {
                "advanced": 1.0,
                "intermediate": 0.6,
                "beginner": 0.2,
            }.get(skill_depths.get(skill, "beginner"), 0.2)

        depth_bonus = depth_score / max(len(depth_priority), 1)

        # -------------------- 3️⃣ Base Score --------------------
        similarity_score = max(0.0, min(similarity_score, 1.0))

        score = (
            weights["tfidf"] * similarity_score
            + weights["core_coverage"] * core_coverage
            + weights["optional_coverage"] * optional_coverage
            + weights["depth_bonus"] * depth_bonus
        )

        # -------------------- 4️⃣ Severity-aware Penalty --------------------
        critical_defined = set(profile.get("critical_core_skills", []))
        trainable_defined = set(profile.get("trainable_core_skills", []))

        critical_missing = critical_defined - effective_skills
        trainable_missing = trainable_defined - effective_skills

        critical_ratio = len(critical_missing) / max(len(critical_defined), 1)
        trainable_ratio = len(trainable_missing) / max(len(trainable_defined), 1)

        penalty_factor = 1 - (
            0.6 * (critical_ratio ** 2)
            + 0.2 * trainable_ratio
        )

        penalty_factor = max(penalty_factor, 0.8)
        score *= penalty_factor

        # -------------------- 5️⃣ Normalize --------------------
        final_score = round(max(0.0, min(score, 1.0)) * 100, 2)

        # -------------------- 6️⃣ Entry-level Fairness Floors --------------------
        missing_core_count = len(core_skills - effective_skills)

        if missing_core_count == 1:
            final_score = max(final_score, 45.0)

        if role in {"ai_ml_developer", "business_analyst", "full_stack_developer"}:
            final_score = max(final_score, 40.0)

        return StabilityEngine.normalize_score(final_score)
