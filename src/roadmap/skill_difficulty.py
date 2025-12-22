




# # src/roadmap/skill_difficulty.py

# class SkillDifficultyMapper:
#     """
#     Maps skills to difficulty levels (used as ML feature)
#     """

#     def __init__(self):
#         self.difficulty_map = {
#             "python": 1,
#             "sql": 1,
#             "java": 2,
#             "docker": 2,
#             "aws": 3,
#             "kubernetes": 3,
#             "machine learning": 3,
#             "deep learning": 4
#         }

#     def get_difficulty(self, skill: str) -> int:
#         """
#         Returns numeric difficulty (default = 2)
#         """
#         return self.difficulty_map.get(skill.lower(), 2)




# src/roadmap/skill_difficulty.py

class SkillDifficulty:
    """
    Encodes skill difficulty as numerical ML-friendly values
    """

    def __init__(self):
        self.difficulty_map = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3
        }

        # Default difficulty for known skills
        self.skill_difficulty = {
            "python": "beginner",
            "sql": "beginner",
            "docker": "intermediate",
            "aws": "intermediate",
            "kubernetes": "advanced",
            "machine learning": "advanced"
        }

    def get_difficulty_level(self, skill: str) -> int:
        """
        Returns numerical difficulty level
        """
        level = self.skill_difficulty.get(skill, "intermediate")
        return self.difficulty_map[level]

