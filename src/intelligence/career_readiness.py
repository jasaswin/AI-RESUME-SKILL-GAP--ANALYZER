class CareerReadinessAnalyzer:
    """
    Determines overall job readiness and hiring signal
    using role-aware final score and confidence
    """

    def analyze(
        self,
        final_score: float,
        confidence: float,
        missing_core_skills: list,
        missing_optional_skills: list
    ) -> dict:

        # -------- Base readiness from score --------
        if final_score >= 75:
            readiness_level = "Job Ready"
            hiring_signal = "Strong hiring signal"
        elif final_score >= 55:
            readiness_level = "Trainable"
            hiring_signal = "Needs targeted upskilling"
        else:
            readiness_level = "Not Ready"
            hiring_signal = "Significant skill gaps detected"

        # -------- Core skill override (critical) --------
        if missing_core_skills:
            if final_score >= 75:
                readiness_level = "Trainable"
                hiring_signal = "Strong profile but missing core skills"
            elif final_score >= 55:
                readiness_level = "Not Ready"
                hiring_signal = "Core skills missing"

        # -------- Confidence-based adjustment --------
        if confidence < 40 and readiness_level == "Job Ready":
            readiness_level = "Trainable"
            hiring_signal = "Low confidence in skill alignment"

        return {
            "readiness_score": round(final_score, 2),
            "readiness_level": readiness_level,
            "hiring_signal": hiring_signal
        }
