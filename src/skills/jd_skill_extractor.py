import re
from pathlib import Path
from typing import Dict, List
from src.skills.skill_database import SkillDatabase


class JDSkillExtractor:
    def __init__(self):
        self.skill_db = SkillDatabase()
        self.core_keywords = ["required", "must", "mandatory", "essential"]

    def extract_skills(self, jd_input: str) -> Dict[str, List[str]]:

        if Path(jd_input).exists():
            jd_text = Path(jd_input).read_text(encoding="utf-8")
        else:
            jd_text = jd_input

        jd_text = jd_text.lower()

        core_skills = set()
        optional_skills = set()

        # 🔥 THIS IS THE CRITICAL FIX
        sentences = re.split(r"[.\n]", jd_text)

        for sentence in sentences:
            for skill in self.skill_db.skills.keys():
                pattern = rf"\b{re.escape(skill)}\b"

                if re.search(pattern, sentence):
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
        return any(
            word in sentence
            for word in self.core_keywords + ["required skills"]
        )
