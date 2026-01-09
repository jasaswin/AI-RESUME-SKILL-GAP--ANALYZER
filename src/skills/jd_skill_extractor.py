import re
from typing import Set
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

    # ==================================================
    # ✅ MAIN EXTRACTION METHOD (ERROR-PROOF)
    # ==================================================
    def extract_skills(self, jd_text: str) -> dict:
        """
        Extract core and optional skills from a Job Description.
        Guarantees:
        - No crashes
        - No empty unsafe outputs
        - Entry-level fairness
        """

        # ----------------------------
        # 0️⃣ ALWAYS-SAFE INITIALIZATION
        # ----------------------------
        core_skills: Set[str] = set()
        optional_skills: Set[str] = set()
        inferred_from_clusters: Set[str] = set()

        if not jd_text or not jd_text.strip():
            return {
                "core_skills": [],
                "optional_skills": []
            }

        jd_text_lower = jd_text.lower()

        # ----------------------------
        # 1️⃣ RAW SKILL DETECTION
        # ----------------------------
        detected_skills = self._extract_raw_skills(jd_text_lower)

        # ----------------------------
        # 1.5️⃣ DOMAIN-BASED FALLBACK (CRITICAL)
        # ----------------------------
        if not detected_skills:
            domain_fallback = {
                "analytics": {"data analysis", "reporting"},
                "engineering": {"python", "sql"},
                "business": {"business analysis"},
                "design": {"ux design"}
            }

            inferred_domain = None
            if any(k in jd_text_lower for k in ["analysis", "analytics", "reporting"]):
                inferred_domain = "analytics"
            elif any(k in jd_text_lower for k in ["engineer", "developer", "backend"]):
                inferred_domain = "engineering"
            elif any(k in jd_text_lower for k in ["business", "stakeholder"]):
                inferred_domain = "business"
            elif any(k in jd_text_lower for k in ["design", "ux", "ui"]):
                inferred_domain = "design"

            fallback_skills = domain_fallback.get(inferred_domain, set())

            return {
                "core_skills": sorted(fallback_skills),
                "optional_skills": []
            }

        # ----------------------------
        # 2️⃣ CORE vs OPTIONAL CLASSIFICATION
        # ----------------------------
        for skill in detected_skills:
            if self._is_core_skill(skill, jd_text_lower):
                core_skills.add(skill)
            else:
                optional_skills.add(skill)

        # ----------------------------
        # 3️⃣ CLUSTER INFERENCE (SAFE)
        # ----------------------------
        if core_skills:
            inferred_from_clusters = self.skill_db.infer_related_skills(core_skills)

        # ----------------------------
        # 4️⃣ MERGE INFERRED CORE SKILLS
        # ----------------------------
        core_skills |= inferred_from_clusters

        # ----------------------------
        # 5️⃣ DEDUPLICATION
        # ----------------------------
        optional_skills -= core_skills

        # ----------------------------
        # 6️⃣ FINAL SAFETY GUARD
        # ----------------------------
        if not core_skills and optional_skills:
            promoted = sorted(optional_skills)[0]
            core_skills.add(promoted)
            optional_skills.remove(promoted)

        return {
            "core_skills": sorted(core_skills),
            "optional_skills": sorted(optional_skills)
        }

    # ==================================================
    # INTERNAL HELPERS
    # ==================================================
    def _extract_raw_skills(self, text: str) -> Set[str]:
        """
        Extract raw skills using master skill DB + JD semantic aliases
        """
        found = set()

        for skill in self.skill_db.skills.keys():
            if re.search(rf"\b{re.escape(skill)}\b", text):
                found.add(skill)

        for alias, canonical in self.jd_semantic_map.items():
            if alias in text:
                found.add(canonical)

        return found

    def _is_core_skill(self, skill: str, text: str) -> bool:
        """
        Decide if a detected skill is core or optional
        """

        for marker in self.CORE_MARKERS:
            if marker in text:
                return True

        for marker in self.OPTIONAL_MARKERS:
            if marker in text:
                return False

        # Default: entry-level safe assumption
        return True
