import re


class SkillDepthEstimator:
    """
    Estimates skill proficiency using resume context
    """

    def __init__(self):
        pass

    def estimate(
        self,
        resume_text: str,
        resume_skills: set
    ) -> dict:
        """
        Returns skill → depth mapping
        """

        resume_text = resume_text.lower()
        depth_map = {}

        for skill in resume_skills:
            occurrences = len(re.findall(rf"\b{re.escape(skill)}\b", resume_text))

            in_projects = "project" in resume_text and skill in resume_text
            used_with_tools = any(
                tool in resume_text
                for tool in ["react", "node", "docker", "aws", "sql", "flask"]
            )

            # Depth logic (explainable)
            if occurrences >= 3 or in_projects:
                depth = "advanced"
            elif occurrences == 2 or used_with_tools:
                depth = "intermediate"
            else:
                depth = "beginner"

            depth_map[skill] = depth

        return depth_map
