class IntentClassifier:
    """
    Classifies user questions into predefined career-related intents
    """

    def classify(self, question: str) -> str:
        q = question.lower()

        # 1️⃣ Career readiness
        if any(kw in q for kw in ["job ready", "am i ready", "ready for job"]):
            return "READINESS"

        # 2️⃣ Score explanation
        if "why" in q and any(kw in q for kw in ["score", "match", "percentage"]):
            return "WHY_SCORE_LOW"

        # 3️⃣ Learning priority
        if any(kw in q for kw in ["learn first", "start with", "what should i learn"]):
            return "WHAT_TO_LEARN_FIRST"

        # 4️⃣ Time estimate
        if any(kw in q for kw in ["how long", "when can i apply", "time"]):
            return "TIME_ESTIMATE"

        # 5️⃣ Skill comparison
        if " vs " in q or "better than" in q:
            return "SKILL_COMPARISON"

        # Default
        return "UNKNOWN"
