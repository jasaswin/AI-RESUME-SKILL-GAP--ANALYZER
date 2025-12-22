from src.skills.skill_database import SkillDatabase


class ResumeSkillExtractor:
    """
    Extracts skills from resume tokens using SkillDatabase
    """

    def __init__(self):
        self.skill_db = SkillDatabase()

    def extract(self, tokens: list[str]) -> list[str]:
        text = " ".join(tokens)
        found_skills = set()

        # Check for multi-word skills first
        for skill in self.skill_db.skills.keys():
            if skill in text:
                found_skills.add(skill)

        # Check aliases
        for alias, actual in self.skill_db.aliases.items():
            if alias in text:
                found_skills.add(actual)

        return sorted(found_skills)
