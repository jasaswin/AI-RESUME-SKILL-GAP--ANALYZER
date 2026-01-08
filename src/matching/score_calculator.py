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
    "quality": "engineering"
}


class ScoreCalculator:
    """
    Production-grade, failure-resistant final scoring engine.
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
        jd_domain: str | None = None
    ) -> float:

        # -------------------- 0️⃣ Defaults --------------------
        resume_skills = resume_skills or set()
        core_skills = core_skills or set()
        optional_skills = optional_skills or set()
        inferred_skills = inferred_skills or set()

        profile = ROLE_PROFILES.get(role, ROLE_PROFILES["ai_ml_developer"])
        weights = profile.get("weights", {})

        # -------------------- 1️⃣ Normalize Weights --------------------
        if not weights:
            weights = {
                "tfidf": 0.4,
                "core_coverage": 0.4,
                "optional_coverage": 0.1,
                "depth_bonus": 0.1
            }

        total_weight = sum(weights.values())
        weights = {k: v / total_weight for k, v in weights.items()}

        # -------------------- 2️⃣ Skill Sets --------------------
        explicit_skills = resume_skills
        effective_skills = explicit_skills | inferred_skills

        # -------------------- 3️⃣ Domain Weighting --------------------
        skill_db = SkillDatabase()

        def domain_multiplier(skill: str) -> float:
            if not jd_domain:
                return 1.0

            skill_category = skill_db.get_category(skill)
            if not skill_category:
              return 1.0

            skill_domain = SKILL_CATEGORY_TO_DOMAIN.get(skill_category)
            if not skill_domain:
                return 1.0
            if skill_domain == jd_domain:
                return 1.0

            return {
                ("engineering", "analytics"): 0.6,
                ("analytics", "engineering"): 0.6,
                ("analytics", "business"): 0.5,
                ("business", "analytics"): 0.5,
                ("engineering", "design"): 0.4,
                ("design", "engineering"): 0.4,
            }.get((skill_category, jd_domain), 0.25)

        def weighted_coverage(skills: Set[str], target: Set[str]) -> float:
            if not target:
                return 1.0
            return sum(domain_multiplier(s) for s in skills & target) / len(target)

        core_coverage = weighted_coverage(effective_skills, core_skills)
        optional_coverage = weighted_coverage(effective_skills, optional_skills)

        # -------------------- 4️⃣ Depth Bonus --------------------
        depth_score = 0.0
        for skill in explicit_skills & profile.get("depth_priority", set()):
            depth_score += {"advanced": 1.0, "intermediate": 0.6}.get(
                skill_depths.get(skill, "beginner"), 0.2
            )

        depth_bonus = depth_score / max(len(profile.get("depth_priority", [])), 1)

        # -------------------- 5️⃣ Base Score --------------------
        similarity_score = max(0.0, min(similarity_score, 1.0))

        score = (
            weights["tfidf"] * similarity_score +
            weights["core_coverage"] * core_coverage +
            weights["optional_coverage"] * optional_coverage +
            weights["depth_bonus"] * depth_bonus
        )

        # -------------------- 6️⃣ Severity-Aware Penalty --------------------
        critical_missing = profile.get("critical_core_skills", set()) - effective_skills
        trainable_missing = profile.get("trainable_core_skills", set()) - effective_skills

        critical_ratio = len(critical_missing) / max(
            len(profile.get("critical_core_skills", [])), 1
        )
        trainable_ratio = len(trainable_missing) / max(
            len(profile.get("trainable_core_skills", [])), 1
        )

        penalty_factor = 1 - (
            0.6 * (critical_ratio ** 2) +
            0.2 * trainable_ratio
        )

        penalty_factor = max(penalty_factor, 0.8)
        score *= penalty_factor

        # -------------------- 7️⃣ Final Normalization --------------------
        final_score = round(max(0.0, min(score, 1.0)) * 100, 2)
        
    # -------------------- 8️⃣ Role Compatibility Alignment --------------------
        role_profile = ROLE_PROFILES.get(role)

        if role_profile:
    # If user is missing only 1 core skill → do not collapse score
          missing_core_count = len(core_skills - effective_skills)

        if missing_core_count == 1:
          final_score = max(final_score, 45.0)

    # If role fit is HIGH, enforce lower bound
        if role_profile and role in {"ai_ml_developer", "business_analyst", "full_stack_developer"}:
           final_score = max(final_score, 40.0)

        return StabilityEngine.normalize_score(final_score)



