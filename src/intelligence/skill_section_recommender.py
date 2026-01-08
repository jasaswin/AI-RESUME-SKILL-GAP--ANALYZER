class SkillSectionRecommender:

    @staticmethod
    def recommend(gap_reasoning: list, role: str) -> list:
        recommendations = []

        for gap in gap_reasoning:
            skill = gap["skill"]

            # 🔥 USE GAP TYPE — NOT SEVERITY
            gap_type = gap.get("type", "core")  
            # expected: "core", "optional", "tool"

            if gap_type == "core":
                section = "Skills Section"
            else:
                section = "Projects Section"

            recommendations.append({
                "skill": skill,
                "recommended_section": section
            })

        return recommendations
