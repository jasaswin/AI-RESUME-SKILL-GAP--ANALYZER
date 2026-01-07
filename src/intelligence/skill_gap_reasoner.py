from src.matching.role_profiles import ROLE_PROFILES


class SkillGapReasoner:
    """
    Explains WHY a skill gap exists and HOW to fix it
    """

    @staticmethod
    def reason(
        resume_skills: set,
        inferred_skills: set,
        skill_depths: dict,
        missing_core_skills: list,
        missing_optional_skills: list,
        role: str
    ) -> list:
        profile = ROLE_PROFILES.get(role, {})
        role_priority = set(profile.get("core_skills", []))

        explanations = []

        all_missing = set(missing_core_skills) | set(missing_optional_skills)

        for skill in all_missing:
            explanation = {
                "skill": skill,
                "gap_type": None,
                "severity": None,
                "reason": None,
                "recommended_fix": None
            }

            # ---------- Gap Type ----------
            if skill in inferred_skills:
                explanation["gap_type"] = "implicit_only"
                explanation["reason"] = (
                    "Skill inferred from context but not explicitly stated"
                )
            elif skill in resume_skills:
                explanation["gap_type"] = "weak_evidence"
                explanation["reason"] = (
                    "Skill mentioned but lacks project or experience usage"
                )
            else:
                explanation["gap_type"] = "missing"
                explanation["reason"] = (
                    "No evidence of this skill found in the resume"
                )

            # ---------- Severity ----------
            if skill in role_priority:
                explanation["severity"] = "High"
            elif explanation["gap_type"] == "weak_evidence":
                explanation["severity"] = "Medium"
            else:
                explanation["severity"] = "Low"

            # ---------- Fix Recommendation ----------
            if explanation["gap_type"] == "missing":
                explanation["recommended_fix"] = (
                    f"Add at least one project or experience demonstrating {skill}"
                )
            elif explanation["gap_type"] == "implicit_only":
                explanation["recommended_fix"] = (
                    f"Explicitly mention {skill} in skills or project descriptions"
                )
            else:
                explanation["recommended_fix"] = (
                    f"Strengthen {skill} with measurable outcomes or tools used"
                )

            explanations.append(explanation)

        return explanations
