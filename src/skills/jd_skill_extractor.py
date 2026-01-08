import re
from pathlib import Path
from typing import Dict, List
from src.skills.skill_database import SkillDatabase


class JDSkillExtractor:
    """
    High-recall, precision-safe JD skill extractor.
    Designed to favor recall over strict lexical matching.
    """

    CORE_MARKERS = {
        "required",
        "mandatory",
        "must",
        "must have",
        "core skills",
        "required skills",
        "must have experience",
    }

    OPTIONAL_MARKERS = {
        "good to have",
        "optional",
        "nice to have",
        "preferred",
    }

    def __init__(self):
        self.skill_db = SkillDatabase()

        # JD-only semantic expansion (DO NOT use for resumes)
        self.jd_semantic_map = {
            "numpy": "data analysis",
            "pandas": "data analysis",
            "scikit-learn": "machine learning",
            "sklearn": "machine learning",
            "model evaluation": "machine learning",
            "statistics": "data analysis",
        }

    def extract_skills(self, jd_input: str) -> Dict[str, List[str]]:

        # -------- Load JD --------
        if Path(jd_input).exists():
            jd_text = Path(jd_input).read_text(encoding="utf-8")
        else:
            jd_text = jd_input

        jd_text = jd_text.lower()

        core_skills = set()
        optional_skills = set()

        current_section = "optional"

        # -------- Line-wise parsing --------
        for line in jd_text.splitlines():
            line = line.strip()
            if not line:
                continue

            # -------- Section detection --------
            if any(marker in line for marker in self.CORE_MARKERS):
                current_section = "core"
                continue

            if any(marker in line for marker in self.OPTIONAL_MARKERS):
                current_section = "optional"
                continue

            # -------- Explicit skill detection --------
            for skill in self.skill_db.skills.keys():
                pattern = rf"\b{re.escape(skill)}\b"
                if re.search(pattern, line):
                    normalized = self.skill_db.normalize_skill(skill)

                    if current_section == "core":
                        core_skills.add(normalized)
                        optional_skills.discard(normalized)
                    else:
                        if normalized not in core_skills:
                            optional_skills.add(normalized)

            # -------- JD semantic expansion --------
            for token, inferred in self.jd_semantic_map.items():
                if token in line:
                    if current_section == "core":
                        core_skills.add(inferred)
                        optional_skills.discard(inferred)
                    else:
                        if inferred not in core_skills:
                            optional_skills.add(inferred)

        # -------- JD-side cluster inference --------
# -------- Domain-safe cluster inference --------
        jd_domain = self.skill_db.detect_domain(core_skills | optional_skills)

        if jd_domain:
            inferred_from_clusters = {
            s for s in self.skill_db.infer_related_skills(core_skills | optional_skills)
            if self.skill_db.get_domain(s) == jd_domain
       }
        core_skills |= inferred_from_clusters


        return {
            "core_skills": sorted(core_skills),
            "optional_skills": sorted(optional_skills - core_skills),
        }
