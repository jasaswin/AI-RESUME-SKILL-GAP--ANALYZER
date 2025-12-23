# src/intelligence/skill_priority.py

class SkillPriorityAssigner:
    """
    Assigns priority to missing skills using rule-based reasoning
    """

    def __init__(self):
        self.deployment_skills = {
            "docker", "aws", "kubernetes", "ci/cd"
        }

    def assign(
        self,
        missing_core_skills: list,
        missing_optional_skills: list,
        skill_depths: dict
    ) -> dict:

        high = set()
        medium = set()
        low = set()

        # 1️ Core skills → HIGH
        for skill in missing_core_skills:
            high.add(skill)

        # 2️ Optional skills → evaluate
        for skill in missing_optional_skills:
            depth = skill_depths.get(skill, "intermediate")

            if skill in self.deployment_skills:
                high.add(skill)
            elif depth == "beginner":
                high.add(skill)
            elif depth == "intermediate":
                medium.add(skill)
            else:
                low.add(skill)

        return {
            "high_priority": sorted(high),
            "medium_priority": sorted(medium),
            "low_priority": sorted(low)
        }
