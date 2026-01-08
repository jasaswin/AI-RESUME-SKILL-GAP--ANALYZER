class StabilityEngine:
    """
    Normalizes and stabilizes scores, gaps, and roadmap generation
    across varying resumes and JDs.
    """

    @staticmethod
    def normalize_score(score: float) -> float:
        """
        Clamp score to stable human-interpretable range
        """
        return round(min(max(score, 5.0), 95.0), 2)

    @staticmethod
    def ensure_minimum_gaps(missing_core, missing_optional):
        """
        Guarantee roadmap relevance even for strong resumes
        """
        if not missing_core and missing_optional:
            return missing_optional[:3]
        return missing_core or missing_optional[:3]

    @staticmethod
    def stabilize_priority_map(priority_map: dict):
        """
        Ensure at least Phase 1 exists
        """
        if not any(priority_map.values()):
            return {
                "high_priority": [],
                "medium_priority": [],
                "low_priority": []
            }

        if not priority_map["high_priority"]:
            priority_map["high_priority"] = (
                priority_map["medium_priority"][:2]
                or priority_map["low_priority"][:2]
            )

        return priority_map
