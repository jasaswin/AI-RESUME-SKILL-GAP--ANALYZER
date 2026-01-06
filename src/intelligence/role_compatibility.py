from src.matching.role_profiles import ROLE_PROFILES


class RoleCompatibilityAnalyzer:
    """
    Determines how well a resume aligns with a given role,
    independent of ATS scoring.
    """

    @staticmethod
    def analyze(resume_skills: set, target_role: str, skill_depths: dict) -> dict:
        profile = ROLE_PROFILES.get(target_role)

        if not profile:
            raise ValueError(f"Unknown role: {target_role}")

        core_skills = set(profile["core_skills"])
        optional_skills = set(profile.get("optional_skills", []))

        matched_core = set()
        partial_core = set()
        missing_core = set()

        for skill in core_skills:
          if skill in resume_skills:
            matched_core.add(skill)
          else:
        # partial match via keyword overlap
           skill_tokens = set(skill.split())
           for r_skill in resume_skills:
             if skill_tokens & set(r_skill.split()):
                partial_core.add(skill)
                break
             else:
               missing_core.add(skill)


        # -------- WEIGHTED core ratio (FIX) --------
        total_core = len(core_skills)

        core_score = (
            len(matched_core) * 1.0 +
            len(partial_core) * 0.5
        )

        core_ratio = (
            len(matched_core) +
            0.5 * len(partial_core)
        ) / max(len(core_skills), 1)


        optional_ratio = (
            len(resume_skills & optional_skills) /
            max(len(optional_skills), 1)
        )

        compatibility_score = round(
            (0.7 * core_ratio + 0.3 * optional_ratio) * 100, 2
        )

        # -------- Role fit --------
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

        # -------- Best-fit roles --------
        best_fit_roles = []
        for role, prof in ROLE_PROFILES.items():
            role_core = set(prof["core_skills"])
            overlap = len(resume_skills & role_core) / max(len(role_core), 1)
            if overlap >= 0.5:
                best_fit_roles.append(role)

        return {
            "role_fit": role_fit,
            "compatibility_score": compatibility_score,
            "matched_core_skills": sorted(matched_core),
            "partially_matched_core_skills": sorted(partial_core),
            "missing_core_skills": sorted(missing_core),
            "best_fit_roles": best_fit_roles,
            "transition_feasibility": transition,
            "partially_matched_core_skills": sorted(partial_core),

        }
