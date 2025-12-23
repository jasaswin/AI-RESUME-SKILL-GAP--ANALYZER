class CareerReadinessAnalyzer:
    """
    Determines job readiness level using hybrid AI signals
    """

    def __init__(self):
        pass

    def analyze(
        self,
        final_match_percentage: float,
        confidence: float,
        missing_core_skills: list,
        missing_optional_skills: list
    ) -> dict:
        """
        Returns readiness score, readiness level, and hiring signal
        """

        readiness_score = round(
            (0.6 * final_match_percentage) + (0.4 * confidence), 2
        )

        # Readiness level logic (explainable & ATS-style)
        if readiness_score >= 70 and len(missing_core_skills) == 0:
            readiness_level = "Job Ready"
            hiring_signal = "Strong hiring signal"
        elif readiness_score >= 50:
            readiness_level = "Trainable"
            hiring_signal = "Needs targeted upskilling"
        else:
            readiness_level = "Not Ready"
            hiring_signal = "Significant skill gaps detected"

        return {
            "readiness_score": readiness_score,
            "readiness_level": readiness_level,
            "hiring_signal": hiring_signal
        }
