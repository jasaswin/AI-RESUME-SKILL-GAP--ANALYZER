

from typing import Dict, List
from src.skills.skill_database import SkillDatabase


class JDSkillExtractor:
    """
    Extracts required skills from Job Description text
    """

    def __init__(self):
        self.skill_db = SkillDatabase()

        # Words indicating MUST / CORE requirement
        self.core_keywords = [
            "required", "must", "mandatory", "essential"
        ]

    def extract_skills(self, jd_text: str) -> Dict[str, List[str]]:
        """
        Extract core and optional skills from JD text
        """
        jd_text = jd_text.lower()

        core_skills = set()
        optional_skills = set()

        # Split JD into sentences (simple approach)
        sentences = jd_text.split(".")

        for sentence in sentences:
            for skill in self.skill_db.skills.keys():
                if skill in sentence:
                    normalized = self.skill_db.normalize_skill(skill)

                    if self._is_core_sentence(sentence):
                        core_skills.add(normalized)
                    else:
                        optional_skills.add(normalized)

        return {
            "core_skills": sorted(core_skills),
            "optional_skills": sorted(optional_skills)
        }

    def _is_core_sentence(self, sentence: str) -> bool:
        """
        Check if sentence implies mandatory skill
        """
        return any(word in sentence for word in self.core_keywords)
