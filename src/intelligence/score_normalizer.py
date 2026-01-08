class ScoreNormalizer:
    """
    Calibrates raw scores into stable, human-expected scores.
    """

    @staticmethod
    def normalize(
        raw_score: float,
        confidence: float,
        resume_archetype: str,
        target_archetype: str
    ) -> float:

        confidence_factor = 0.85 + min(confidence, 80) / 100 * 0.3

        archetype_alignment = 1.1 if resume_archetype == target_archetype else 0.9

        normalized = raw_score * confidence_factor * archetype_alignment

        return round(min(normalized, 100), 2)
