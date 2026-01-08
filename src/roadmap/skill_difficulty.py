# src/roadmap/skill_difficulty.py

class SkillDifficultyMapper:
    """
    Maps skills to realistic difficulty levels.
    This is intentionally conservative for entry-level roles.
    """

    EASY = {
        "html", "css", "sql", "excel", "power bi", "tableau"
    }

    MEDIUM = {
        "python", "java", "javascript", "data analysis",
        "nodejs", "flask", "django"
    }

    HARD = {
        "machine learning", "deep learning", "nlp",
        "docker", "aws", "kubernetes"
    }

    def map(self, skill: str) -> str:
        skill = skill.lower().strip()

        if skill in self.EASY:
            return "easy"
        if skill in self.MEDIUM:
            return "medium"
        if skill in self.HARD:
            return "hard"

        # Safe fallback
        return "medium"
