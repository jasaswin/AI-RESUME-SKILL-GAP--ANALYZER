
import re
from collections import defaultdict
from src.skills.skill_database import SkillDatabase
from collections import defaultdict

class ResumeSkillExtractor:
    """
    Extracts explicit and inferred skills from resume text
    using token match + phrase detection + functional inference
    """

    def __init__(self):
        self.skill_db = SkillDatabase()

        # Functional → technical inference
        self.functional_inference = {
            "data analysis": {
                "analyze", "analysis", "insights", "reporting",
                "dashboard", "metrics", "kpi", "data-driven"
            },
            "machine learning": {
                "model", "prediction", "classification",
                "regression", "training", "feature"
            },
            "nlp": {
                "text", "language", "token", "sentiment", "nlp"
            },
            "problem solving": {
                "optimize", "debug", "resolve", "improve",
                "solution", "troubleshoot"
            },
            "data structures": {
                "array", "linked list", "tree", "graph",
                "stack", "queue"
            }
        }

        # Business-domain inference
        self.business_inference = {
            "business analysis": {
                "business analysis", "business analyst",
                "requirements gathering", "gap analysis"
            },
            "stakeholder management": {
                "stakeholder", "client", "interview",
                "workshop", "collaboration"
            },
            "process optimization": {
                "process optimization", "process improvement",
                "workflow", "efficiency", "productivity"
            },
            "reporting": {
                "report", "dashboard", "visualization",
                "metrics", "kpi"
            },
            "user acceptance testing": {
                "uat", "user acceptance testing",
                "validation", "test cases"
            }
        }

        # Technology dependency inference
        self.tech_dependency_inference = {
            "react": {"javascript", "html", "css"},
            "reactjs": {"javascript", "html", "css"},
            "nodejs": {"javascript"},
            "express": {"nodejs", "javascript"},
            "nextjs": {"react", "javascript"},
            "aws lambda": {"aws"},
            "github": {"git"},
            "version control": {"git"},
        }

    def extract(self, tokens: list[str], resume_text: str = "") -> dict:
      """
    Returns:
    {
        skill: {
            "source": "explicit" | "inferred"
        }
    }
    GUARANTEE:
    - Always returns a dict
    - Never returns None
    """



      skill_hits = defaultdict(lambda: {"source": "explicit"})
      text_lower = (resume_text or "").lower()

    # ---------- 1️⃣ Explicit phrase detection ----------
      for skill in self.skill_db.skills:
        if " " in skill and skill in text_lower:
            skill_hits[skill]["source"] = "explicit"

    # ---------- 2️⃣ Token-based explicit detection ----------
      for token in tokens or []:
        normalized = self.skill_db.normalize_skill(token)
        if self.skill_db.is_valid_skill(normalized):
            skill_hits[normalized]["source"] = "explicit"

      present_skills = set(skill_hits.keys())

    # ---------- 3️⃣ Functional inference ----------
      for skill, indicators in self.functional_inference.items():
        if skill in present_skills:
            continue
        if any(indicator in text_lower for indicator in indicators):
            if self.skill_db.is_valid_skill(skill):
                skill_hits[skill] = {"source": "inferred"}

    # ---------- 4️⃣ Business-domain inference ----------
      for skill, phrases in self.business_inference.items():
        if skill in present_skills:
            continue
        if any(phrase in text_lower for phrase in phrases):
            if self.skill_db.is_valid_skill(skill):
                skill_hits[skill] = {"source": "inferred"}

    # ---------- 5️⃣ Technology dependency inference ----------
      expanded_skills = dict(skill_hits)
      inferred_dependencies = set()

      for skill in expanded_skills:
        inferred_dependencies |= self.tech_dependency_inference.get(skill, set())

      for dep in inferred_dependencies:
        if dep not in expanded_skills and self.skill_db.is_valid_skill(dep):
            expanded_skills[dep] = {"source": "inferred"}

    # 🔒 FINAL GUARANTEE
      return dict(expanded_skills)
