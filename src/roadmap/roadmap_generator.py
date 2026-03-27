# src/roadmap/roadmap_generator.py

# class RoadmapGenerator:
#     """
#     Simplified, real-world roadmap generator.
#     Produces ONLY actionable guidance.
#     """

#     def generate_phase_roadmap(self, priority_map: dict) -> dict:
#         """
#         priority_map = {
#             "high_priority": [...],
#             "medium_priority": [...],
#             "low_priority": [...]
#         }
#         """

#         immediate = []
#         optional = []

#         # --------------------
#         # Immediate Preparation
#         # --------------------
#         for skill in priority_map.get("high_priority", []):
#             immediate.append(self._build_step(skill))

#         for skill in priority_map.get("medium_priority", []):
#             immediate.append(self._build_step(skill))

#         # --------------------
#         # Optional Growth
#         # --------------------
#         for skill in priority_map.get("low_priority", []):
#             optional.append(self._build_step(skill))

#         # --------------------
#         # Safety Guarantee
#         # --------------------
#         if not immediate and optional:
#             immediate.append(optional.pop(0))

#         return {
#             "Immediate Preparation": immediate,
#             "Optional Growth": optional
#         }

#     # --------------------
#     # Helpers
#     # --------------------
#     def _build_step(self, skill: str) -> dict:
#         return {
#             "skill": skill,
#             "estimated_weeks": self._estimate_weeks(skill),
#             "resources": self._recommend_resources(skill)
#         }

#     def _estimate_weeks(self, skill: str) -> float:
#         return 3.0

#     def _recommend_resources(self, skill: str) -> list:
#         return ["General Online Tutorials"]




# src/roadmap/roadmap_generator.py

from src.roadmap.learning_time_model import LearningTimeEstimator
from src.roadmap.skill_difficulty import SkillDifficultyMapper
from src.roadmap.resource_mapper import ResourceMapper
from src.roadmap.skill_dependency import SkillDependencyResolver


class RoadmapGenerator:
    """
    ML-driven roadmap generator.
    Produces role-aware, dependency-aware, time-estimated learning plans.
    """

    def __init__(self):
        self.time_estimator = LearningTimeEstimator()
        self.difficulty_mapper = SkillDifficultyMapper()
        self.resource_mapper = ResourceMapper()
        self.dependency_resolver = SkillDependencyResolver()

    # -------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------
    def generate(
        self,
        missing_required_skills: list,
        missing_optional_skills: list,
        skill_categories: dict,
        skill_popularity: dict
    ) -> dict:
        """
        Generates a phased learning roadmap.

        Parameters:
        - missing_required_skills: list[str]
        - missing_optional_skills: list[str]
        - skill_categories: dict[str, str]
        - skill_popularity: dict[str, int]

        Returns:
        - dict (phased roadmap)
        """

        roadmap = {}

        # -------------------------
        # Phase 1: Core Eligibility
        # -------------------------
        phase_1_skills = self.dependency_resolver.resolve(
            missing_required_skills
        )

        roadmap["Phase 1: Core Eligibility"] = self._build_phase(
            phase_1_skills,
            skill_categories,
            skill_popularity,
            is_core=1,
            reason="Required for target role"
        )

        # -------------------------
        # Phase 2: Supporting Skills
        # -------------------------
        phase_2_skills = [
            skill for skill in missing_required_skills
            if skill not in phase_1_skills
        ]

        if phase_2_skills:
            roadmap["Phase 2: Supporting Skills"] = self._build_phase(
                phase_2_skills,
                skill_categories,
                skill_popularity,
                is_core=1,
                reason="Strengthens role readiness"
            )

        # -------------------------
        # Phase 3: Optional Growth
        # -------------------------
        if missing_optional_skills:
            roadmap["Phase 3: Optional Growth"] = self._build_phase(
                missing_optional_skills,
                skill_categories,
                skill_popularity,
                is_core=0,
                reason="Good-to-have for long-term growth"
            )

        return roadmap

    # -------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------
    def _build_phase(
        self,
        skills: list,
        skill_categories: dict,
        skill_popularity: dict,
        is_core: int,
        reason: str
    ) -> list:
        """
        Builds roadmap steps for a single phase.
        """

        steps = []

        for skill in skills:
            category = skill_categories.get(skill, "tool")
            difficulty_label = self.difficulty_mapper.map(skill)
            difficulty_score = self._difficulty_to_numeric(difficulty_label)
            popularity_score = skill_popularity.get(skill, 5)

            days = self.time_estimator.predict_days(
                category=category,
                difficulty=difficulty_score,
                popularity=popularity_score,
                is_core=is_core
            )

            step = {
                "skill": skill,
                "estimated_weeks": round(days / 7, 1),
                "difficulty": difficulty_label,
                "reason": reason,
                "resources": self.resource_mapper.get_resources(skill)
            }

            steps.append(step)

        return steps

    def _difficulty_to_numeric(self, difficulty: str) -> int:
        """
        Converts difficulty label to numeric score for ML model.
        """
        mapping = {
            "easy": 1,
            "medium": 2,
            "hard": 3
        }
        return mapping.get(difficulty, 2)
