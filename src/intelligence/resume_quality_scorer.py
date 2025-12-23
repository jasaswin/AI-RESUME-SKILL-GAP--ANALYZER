class ResumeQualityScorer:
    """
    Scores resume quality based on structure, skills, and clarity
    """

    def score(
        self,
        resume_text: str,
        resume_skills: set,
        skill_depths: dict
    ) -> float:

        score = 50  # base score

        # 1️⃣ Skill richness
        if len(resume_skills) >= 10:
            score += 15
        elif len(resume_skills) >= 6:
            score += 10
        else:
            score += 5

        # 2️⃣ Advanced skills presence
        advanced_count = sum(
            1 for level in skill_depths.values() if level == "advanced"
        )

        if advanced_count >= 5:
            score += 15
        elif advanced_count >= 3:
            score += 10

        # 3️⃣ Resume length signal
        word_count = len(resume_text.split())
        if word_count >= 300:
            score += 10
        elif word_count >= 200:
            score += 5

        return min(score, 100)
