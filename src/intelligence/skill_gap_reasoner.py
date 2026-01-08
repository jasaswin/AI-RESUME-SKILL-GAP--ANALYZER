class SkillGapReasoner:
    """
    Determines severity and intent of missing skills.
    This is the semantic bridge between gaps and actions.
    """

    @staticmethod
    def reason(
        resume_skills: set,
        inferred_skills: set,
        skill_depths: dict,
        missing_core_skills: list,
        missing_optional_skills: list,
        role: str | None = None
    ) -> list[dict]:

        reasoning = []

        # ---------------- Core skill gaps (HIGH severity) ----------------
        for skill in missing_core_skills:
            reasoning.append({
                "skill": skill,
                "severity": "High",
                "reason": "Required core skill missing"
            })

        # ---------------- Optional skill gaps (MEDIUM / LOW) ----------------
        for skill in missing_optional_skills:
            depth = skill_depths.get(skill, "none")

            severity = (
                "Medium" if depth in {"none", "beginner"} else "Low"
            )

            reasoning.append({
                "skill": skill,
                "severity": severity,
                "reason": "Optional or growth skill"
            })

        return reasoning
