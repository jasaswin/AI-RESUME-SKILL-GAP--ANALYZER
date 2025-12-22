import re
from pathlib import Path
from typing import Dict, List
from src.skills.skill_database import SkillDatabase


class JDSkillExtractor:
    def __init__(self):
        self.skill_db = SkillDatabase()
        self.core_markers = ["required", "mandatory", "must", "essential", "core skills"]
        self.optional_markers = ["good to have", "optional", "nice to have"]

    def extract_skills(self, jd_input: str) -> Dict[str, List[str]]:

        # Load JD
        if Path(jd_input).exists():
            jd_text = Path(jd_input).read_text(encoding="utf-8")
        else:
            jd_text = jd_input

        jd_text = jd_text.lower()

        core_skills = set()
        optional_skills = set()

        current_section = "optional"  # default

        # Split by lines (BEST for JDs)
        for line in jd_text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Section detection
            if any(k in line for k in self.core_markers):
                current_section = "core"
                continue

            if any(k in line for k in self.optional_markers):
                current_section = "optional"
                continue

            # Skill matching
            for skill in self.skill_db.skills.keys():
                pattern = rf"\b{re.escape(skill)}\b"
                if re.search(pattern, line):
                    normalized = self.skill_db.normalize_skill(skill)

                    if current_section == "core":
                        core_skills.add(normalized)
                        optional_skills.discard(normalized)  # 🔥 important
                    else:
                        if normalized not in core_skills:
                            optional_skills.add(normalized)

        return {
            "core_skills": sorted(core_skills),
            "optional_skills": sorted(optional_skills)
        }
