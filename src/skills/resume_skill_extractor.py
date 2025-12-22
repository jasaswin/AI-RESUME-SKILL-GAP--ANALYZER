import re
from src.skills.skill_database import SkillDatabase


class ResumeSkillExtractor:
    def __init__(self):
        self.skill_db = SkillDatabase()

    def extract(self, tokens: list[str]) -> list[str]:
        # Step 1: normalize tokens using aliases
        normalized_tokens = []

        for token in tokens:
            token = token.lower()
            token = re.sub(r"[^a-z0-9+#]", "", token)  # clean punctuation
            token = self.skill_db.normalize_skill(token)  # APPLY ALIAS HERE
            normalized_tokens.append(token)

        text = " ".join(normalized_tokens)

        found_skills = set()

        # Step 2: match ONLY against master skills
        for skill in self.skill_db.skills.keys():
            pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, text):
                found_skills.add(skill)

        return sorted(found_skills)
