from typing import Set, Dict


class SkillGapIdentifier:
    """
    Production-grade skill gap identifier.

    Guarantees:
    - Inferred skills are respected
    - Equivalent skills are normalized
    - Optional skills never block readiness
    - No duplicate or fake gaps
    """

    @staticmethod
    def identify_gaps(
        explicit_skills: Set[str],
        inferred_skills: Set[str],
        jd_core: Set[str],
        jd_optional: Set[str],
        equivalence_map: Dict[str, Set[str]] | None = None
    ) -> Dict[str, list]:
        """
        Returns missing core and optional skills
        """

        explicit_skills = explicit_skills or set()
        inferred_skills = inferred_skills or set()
        jd_core = jd_core or set()
        jd_optional = jd_optional or set()
        equivalence_map = equivalence_map or {}

        # -------------------- 1️⃣ Effective Skill Set --------------------
        effective_skills = set(explicit_skills) | set(inferred_skills)

        # -------------------- 2️⃣ Apply Equivalence --------------------
        normalized_skills = set(effective_skills)

        for skill in list(effective_skills):
            equivalents = equivalence_map.get(skill, set())
            normalized_skills.update(equivalents)

        # -------------------- 3️⃣ True Gaps --------------------
        missing_core = sorted(
            skill for skill in jd_core
            if skill not in normalized_skills
        )

        missing_optional = sorted(
            skill for skill in jd_optional
            if skill not in normalized_skills
        )

        return {
            "missing_core_skills": missing_core,
            "missing_optional_skills": missing_optional
        }
