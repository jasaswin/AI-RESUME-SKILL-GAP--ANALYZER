from src.intelligence.stability_engine import StabilityEngine


class CareerReadinessAnalyzer:
    """
    Determines overall job readiness and hiring signal
    with entry-level fairness calibration.
    """

    def analyze(
        self,
        final_score: float,
        confidence: float,
        missing_core_skills: list,
        missing_optional_skills: list,
        critical_missing: set,
        trainable_missing: set,
        role: str | None = None,
        jd_level: str | None = "entry"
    ) -> dict:

        # ---------------- Phase 1: Stability-adjusted score ----------------
        adjusted_score = final_score * (0.85 + 0.15 * (confidence / 100))
        adjusted_score = round(adjusted_score, 2)

        # ---------------- Phase 2: Base readiness bands ----------------
        if adjusted_score >= 75:
            readiness_level = "Job Ready"
            hiring_signal = "Strong hiring signal"
        elif adjusted_score >= 50:
            readiness_level = "Trainable"
            hiring_signal = "Minor upskilling required"
        else:
            readiness_level = "Not Ready"
            hiring_signal = "Structured upskilling required"

# ---------------- Phase 3: Severity-based entry-level override ----------------
        if jd_level == "entry" and role in {
      "ai_ml_developer",
      "business_analyst",
      "full_stack_developer"
    }:
    #  Entry-level fairness: only trainable skills missing
          if not critical_missing and trainable_missing:
           readiness_level = "Trainable"
           hiring_signal = (
            "Entry-level candidate with strong core foundation; "
            "only trainable skills missing"
        )



        # ---------------- Phase 4: Confidence safety ----------------
        if confidence < 30 and readiness_level == "Job Ready":
            readiness_level = "Trainable"
            hiring_signal = "Low confidence in alignment despite skill match"

        return {
            "readiness_score": StabilityEngine.normalize_score(final_score),
            "adjusted_score": adjusted_score,
            "readiness_level": readiness_level,
            "hiring_signal": hiring_signal
        }
