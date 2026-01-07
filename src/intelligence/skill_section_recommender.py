from src.matching.role_profiles import ROLE_PROFILES


class SkillSectionRecommender:
    """
    Recommends WHERE a skill should be added or strengthened
    in the resume.
    """

    @staticmethod
    def recommend(
        gap_reasoning: list,
        role: str
    ) -> list:
        profile = ROLE_PROFILES.get(role, {})
        role_core = set(profile.get("core_skills", []))

        recommendations = []

        for item in gap_reasoning:
            skill = item["skill"]
            gap_type = item["gap_type"]
            severity = item["severity"]

            if gap_type == "missing":
                if skill in role_core:
                    section = "Projects Section"
                else:
                    section = "Skills Section"

            elif gap_type == "implicit_only":
                section = "Skills Section (explicit mention)"

            else:  # weak evidence
                section = "Experience or Projects Section"

            recommendations.append({
                "skill": skill,
                "recommended_section": section,
                "priority": severity
            })

        return recommendations
