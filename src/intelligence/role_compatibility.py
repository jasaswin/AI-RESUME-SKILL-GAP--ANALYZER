from src.matching.role_profiles import ROLE_PROFILES


class RoleCompatibilityAnalyzer:
    """
    Determines how well a resume aligns with roles,
    independent of ATS scoring.
    """

    @staticmethod
    def analyze(resume_skills: set, target_role: str, skill_depths: dict | None = None) -> dict:
        profile = ROLE_PROFILES.get(target_role)

        if not profile:
            raise ValueError(f"Unknown role: {target_role}")

        core_skills = set(profile["core_skills"])
        optional_skills = set(profile.get("optional_skills", []))

        matched_core = set()
        partial_core = set()
        missing_core = set()

        # -------- Core skill matching --------
        for skill in core_skills:
            if skill in resume_skills:
                matched_core.add(skill)
            else:
                skill_tokens = set(skill.split())
                partial_found = False

                for r_skill in resume_skills:
                    if skill_tokens & set(r_skill.split()):
                        partial_core.add(skill)
                        partial_found = True
                        break

                if not partial_found:
                    missing_core.add(skill)

        # -------- Weighted core ratio --------
        core_ratio = (
            len(matched_core) + 0.5 * len(partial_core)
        ) / max(len(core_skills), 1)

        optional_ratio = (
            len(resume_skills & optional_skills) /
            max(len(optional_skills), 1)
        )

        compatibility_score = round(
            (0.7 * core_ratio + 0.3 * optional_ratio) * 100, 2
        )

        # -------- Role fit classification --------
        if core_ratio >= 0.65:
            role_fit = "High"
        elif core_ratio >= 0.35:
            role_fit = "Medium"
        else:
            role_fit = "Low"

        # -------- Transition feasibility --------
        if core_ratio >= 0.4:
            transition = "High"
        elif core_ratio >= 0.2:
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
    # 🧠 PHASE 3.1 — MULTI-ROLE FIT ANALYZER
    # ==================================================
    @staticmethod
    def analyze_all_roles(resume_skills: set, skill_depths: dict | None = None) -> list[dict]:
        """
        Evaluates resume against ALL known roles and ranks them.
        """

        role_rankings = []

        for role in ROLE_PROFILES.keys():
            result = RoleCompatibilityAnalyzer.analyze(
                resume_skills=resume_skills,
                target_role=role,
                skill_depths=skill_depths
            )

            role_rankings.append({
                "role": role,
                "compatibility_score": result["compatibility_score"],
                "role_fit": result["role_fit"],
                "matched_core_skills": result["matched_core_skills"],
                "missing_core_skills": result["missing_core_skills"],
                "transition_feasibility": result["transition_feasibility"]
            })

        # Sort by compatibility score (descending)
        role_rankings.sort(
            key=lambda x: x["compatibility_score"],
            reverse=True
        )

        return role_rankings
