from typing import Set, Dict
from src.matching.role_profiles import ROLE_PROFILES


class RoleCompatibilityAnalyzer:
    """
    Production-grade role compatibility analyzer.

    Guarantees:
    - Explicit + inferred skills are considered
    - Equivalent skills are normalized
    - No role bias due to lexical mismatch
    """

    @staticmethod
    def analyze(
        explicit_skills: Set[str],
        inferred_skills: Set[str],
        target_role: str,
        equivalence_map: Dict[str, Set[str]] | None = None
    ) -> dict:

        profile = ROLE_PROFILES.get(target_role)
        if not profile:
            return {
                "role_fit": "Unknown",
                "compatibility_score": 0.0,
                "matched_core_skills": [],
                "partially_matched_core_skills": [],
                "missing_core_skills": [],
                "transition_feasibility": "Low"
            }

        equivalence_map = equivalence_map or {}

        core_skills = set(profile["core_skills"])
        optional_skills = set(profile.get("optional_skills", []))

        # -------------------- 1️⃣ Effective Skill Set --------------------
        effective_skills = set(explicit_skills) | set(inferred_skills)

        normalized_skills = set(effective_skills)
        for skill in effective_skills:
            normalized_skills.update(equivalence_map.get(skill, set()))

        # -------------------- 2️⃣ Core Skill Matching --------------------
        matched_core = set()
        partial_core = set()
        missing_core = set()

        for skill in core_skills:
            if skill in normalized_skills:
                matched_core.add(skill)
            else:
                # partial = semantic overlap
                for r_skill in normalized_skills:
                    if skill in r_skill or r_skill in skill:
                        partial_core.add(skill)
                        break
                else:
                    missing_core.add(skill)

        # -------------------- 3️⃣ Weighted Core Ratio --------------------
        core_ratio = (
            len(matched_core) + 0.5 * len(partial_core)
        ) / max(len(core_skills), 1)

        optional_ratio = (
            len(normalized_skills & optional_skills)
            / max(len(optional_skills), 1)
        )

        compatibility_score = round(
            (0.75 * core_ratio + 0.25 * optional_ratio) * 100, 2
        )

        # -------------------- 4️⃣ Role Fit Classification --------------------
        if core_ratio >= 0.7:
            role_fit = "High"
        elif core_ratio >= 0.4:
            role_fit = "Medium"
        else:
            role_fit = "Low"

        # -------------------- 5️⃣ Transition Feasibility --------------------
        if core_ratio >= 0.45:
            transition = "High"
        elif core_ratio >= 0.25:
            transition = "Medium"
        else:
            transition = "Low"

        return {
            "role_fit": role_fit,
            "compatibility_score": compatibility_score,
            "matched_core_skills": sorted(matched_core),
            "partially_matched_core_skills": sorted(partial_core),
            "missing_core_skills": sorted(missing_core),
            "transition_feasibility": transition,
        }

    # ==================================================
    # 🔥 MULTI-ROLE ANALYSIS (STABLE)
    # ==================================================
    @staticmethod
    def analyze_all_roles(
        explicit_skills: Set[str],
        inferred_skills: Set[str],
        equivalence_map: Dict[str, Set[str]] | None = None
    ) -> list[dict]:

        role_rankings = []

        for role in ROLE_PROFILES.keys():
            result = RoleCompatibilityAnalyzer.analyze(
                explicit_skills=explicit_skills,
                inferred_skills=inferred_skills,
                target_role=role,
                equivalence_map=equivalence_map
            )

            role_rankings.append({
                "role": role,
                "compatibility_score": result["compatibility_score"],
                "role_fit": result["role_fit"],
                "matched_core_skills": result["matched_core_skills"],
                "missing_core_skills": result["missing_core_skills"],
                "transition_feasibility": result["transition_feasibility"]
            })

        role_rankings.sort(
            key=lambda x: x["compatibility_score"],
            reverse=True
        )

        return role_rankings
