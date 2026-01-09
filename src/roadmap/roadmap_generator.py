# src/roadmap/roadmap_generator.py

class RoadmapGenerator:
    """
    Simplified, real-world roadmap generator.
    Produces ONLY actionable guidance.
    """

    def generate_phase_roadmap(self, priority_map: dict) -> dict:
        """
        priority_map = {
            "high_priority": [...],
            "medium_priority": [...],
            "low_priority": [...]
        }
        """

        immediate = []
        optional = []

        # --------------------
        # Immediate Preparation
        # --------------------
        for skill in priority_map.get("high_priority", []):
            immediate.append(self._build_step(skill))

        for skill in priority_map.get("medium_priority", []):
            immediate.append(self._build_step(skill))

        # --------------------
        # Optional Growth
        # --------------------
        for skill in priority_map.get("low_priority", []):
            optional.append(self._build_step(skill))

        # --------------------
        # Safety Guarantee
        # --------------------
        if not immediate and optional:
            immediate.append(optional.pop(0))

        return {
            "Immediate Preparation": immediate,
            "Optional Growth": optional
        }

    # --------------------
    # Helpers
    # --------------------
    def _build_step(self, skill: str) -> dict:
        return {
            "skill": skill,
            "estimated_weeks": self._estimate_weeks(skill),
            "resources": self._recommend_resources(skill)
        }

    def _estimate_weeks(self, skill: str) -> float:
        return 3.0

    def _recommend_resources(self, skill: str) -> list:
        return ["General Online Tutorials"]
