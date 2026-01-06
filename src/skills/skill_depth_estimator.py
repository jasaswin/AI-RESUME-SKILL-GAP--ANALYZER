from collections import defaultdict
from src.skills.skill_database import SkillDatabase


class SkillDepthEstimator:
    """
    Evidence-based skill depth estimator
    """

    def __init__(self):
        self.skill_db = SkillDatabase()

        # Action verbs = strong evidence
        self.action_verbs = {
            "built", "developed", "implemented", "designed",
            "analyzed", "created", "optimized", "deployed",
            "trained", "evaluated"
        }

        # Weak indicators (still useful)
        self.weak_indicators = {
            "familiar", "exposed", "knowledge", "basic"
        }

        self.skill_proxies = {
    "machine learning": {
        "model", "prediction", "classification", "regression",
        "training", "accuracy", "feature", "algorithm"
    },
    "data analysis": {
        "analysis", "insights", "dashboard", "metrics",
        "visualization", "report"
    },
    "nlp": {
        "text", "token", "sentiment", "language",
        "embedding", "tf-idf"
    },
}


    def estimate(
        self,
        explicit_skills: set[str],
        inferred_skills: set[str],
        resume_text: str = ""
    ) -> dict:
        depths = {}

        text = resume_text.lower()

        # ---------- Explicit skills ----------
        for skill in explicit_skills:
            depths[skill] = self._estimate_depth(skill, text, explicit=True)

        # ---------- Inferred skills ----------
        for skill in inferred_skills:
            if skill in depths:
                continue
            depths[skill] = self._estimate_depth(skill, text, explicit=False)

        return depths

    # ===============================
    # Core logic
    # ===============================

    def _estimate_depth(self, skill: str, text: str, explicit: bool) -> str:
      skill = skill.lower()
      score = 0

    # 1️⃣ Frequency signal
      occurrences = text.count(skill)
      score += min(occurrences, 3)

    # 1.5️⃣ Proxy evidence
      proxies = self.skill_proxies.get(skill, set())
      score += min(sum(1 for p in proxies if p in text), 3)

    # 2️⃣ Action verb context
      if skill in text and any(v in text for v in self.action_verbs):
        score += 2

    # 3️⃣ Project / experience context
      if skill in text and any(
        kw in text for kw in ["project", "experience", "internship"]
      ):
        score += 2

    # 4️⃣ Tool coupling
      category = self.skill_db.get_category(skill)
      if category in {"machine learning", "data", "ai"}:
        if any(t in text for t in ["python", "pandas", "numpy", "sklearn"]):
            score += 2

    # ---------- Final depth ----------
      if score >= 7:
        return "advanced"

      if score >= 4:
        return "intermediate"

      if explicit:
        return "intermediate"

      return "beginner"
 