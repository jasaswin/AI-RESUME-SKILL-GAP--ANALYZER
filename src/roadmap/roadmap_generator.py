# src/roadmap/roadmap_generator.py

from typing import Dict, List
from src.roadmap.resource_mapper import ResourceMapper
from src.roadmap.skill_difficulty import SkillDifficultyMapper
from src.intelligence.stability_engine import StabilityEngine


class RoadmapGenerator:
    """
    Phase-aware, deduplicated roadmap generator.

    Guarantees:
    - A skill appears in ONLY ONE phase (earliest applicable)
    - Phase meaning is preserved
    - Roadmap is monotonic and user-trust-safe
    """

    def __init__(self):
        self.resource_mapper = ResourceMapper()
        self.difficulty_mapper = SkillDifficultyMapper()

    def generate_phase_roadmap(
        self,
        priority_map: Dict[str, List[str]]
    ) -> Dict[str, List[dict]]:

        roadmap = {
            "Phase 1 – Job Readiness": [],
            "Phase 2 – Applied Skills & Projects": [],
            "Phase 3 – Long-term Growth": []
        }

        # 🔒 GLOBAL DEDUPLICATION LOCK
        scheduled_skills = set()

        # -------------------- PHASE 1: CORE CRITICAL --------------------
        for skill in priority_map.get("high_priority", []):
            if skill in scheduled_skills:
                continue

            roadmap["Phase 1 – Job Readiness"].append(
                self._build_step(skill)
            )
            scheduled_skills.add(skill)

        # -------------------- PHASE 2: CORE TRAINABLE --------------------
        for skill in priority_map.get("medium_priority", []):
            if skill in scheduled_skills:
                continue

            roadmap["Phase 2 – Applied Skills & Projects"].append(
                self._build_step(skill)
            )
            scheduled_skills.add(skill)

        # -------------------- PHASE 3: OPTIONAL / GROWTH --------------------
        for skill in priority_map.get("low_priority", []):
            if skill in scheduled_skills:
                continue

            roadmap["Phase 3 – Long-term Growth"].append(
                self._build_step(skill)
            )
            scheduled_skills.add(skill)

        return roadmap

    # ==================================================
    # INTERNAL HELPERS
    # ==================================================
    def _build_step(self, skill: str) -> dict:
        """
        Builds a single roadmap step with
        realistic time + action-based resources
        """
        difficulty = self.difficulty_mapper.map(skill)

        estimated_weeks = {
            "easy": 2.0,
            "medium": 3.0,
            "hard": 4.0
        }.get(difficulty, 3.0)

        resources = self.resource_mapper.get_resources(skill)

        return {
            "skill": skill,
            "estimated_weeks": round(estimated_weeks, 1),
            "resources": resources
        }
