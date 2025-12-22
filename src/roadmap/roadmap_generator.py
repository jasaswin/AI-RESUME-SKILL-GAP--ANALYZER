




# src/roadmap/roadmap_generator.py

# import numpy as np
# from sklearn.linear_model import LinearRegression

# from src.roadmap.skill_difficulty import SkillDifficultyMapper
# from src.roadmap.resource_mapper import ResourceMapper


# class RoadmapGenerator:
#     """
#     Generates ML-based learning roadmap with time estimation
#     """

#     def __init__(self):
#         self.difficulty_mapper = SkillDifficultyMapper()
#         self.resource_mapper = ResourceMapper()
#         self.model = self._train_time_model()

#     def _train_time_model(self):
#         """
#         Train regression model:
#         Features:
#         - difficulty
#         - category_weight (proxy for complexity)
#         Target:
#         - learning time (weeks)
#         """

#         # Training data (synthetic but realistic)
#         # [difficulty, category_weight]
#         X = np.array([
#             [1, 1],   # python
#             [1, 1],   # sql
#             [2, 2],   # docker
#             [3, 3],   # aws
#             [3, 3],   # kubernetes
#             [3, 4],   # ml
#             [4, 4]    # dl
#         ])

#         # Target learning time in weeks
#         y = np.array([2, 2, 4, 6, 6, 8, 12])

#         model = LinearRegression()
#         model.fit(X, y)
#         return model

#     def _category_weight(self, skill: str) -> int:
#         """
#         Approximate category complexity
#         """
#         infra = {"docker", "aws", "kubernetes"}
#         ai = {"machine learning", "deep learning"}

#         if skill in infra:
#             return 3
#         if skill in ai:
#             return 4
#         return 1

#     def estimate_learning_time(self, skill: str) -> float:
#         """
#         Predict learning time using ML regression
#         """
#         difficulty = self.difficulty_mapper.get_difficulty(skill)
#         category_weight = self._category_weight(skill)

#         features = np.array([[difficulty, category_weight]])
#         predicted_weeks = self.model.predict(features)[0]

#         return round(predicted_weeks, 1)

#     def generate_roadmap(self, missing_skills: list) -> list:
#         """
#         Create ordered roadmap with time & resources
#         """

#         roadmap = []

#         for skill in missing_skills:
#             time_required = self.estimate_learning_time(skill)
#             resources = self.resource_mapper.get_resources(skill)

#             roadmap.append({
#                 "skill": skill,
#                 "estimated_weeks": time_required,
#                 "resources": resources
#             })

#         # Sort by learning time (easy → hard)
#         roadmap.sort(key=lambda x: x["estimated_weeks"])
#         return roadmap



# src/roadmap/roadmap_generator.py

import numpy as np
from sklearn.linear_model import LinearRegression

from src.roadmap.skill_difficulty import SkillDifficulty
from src.roadmap.resource_mapper import ResourceMapper


class RoadmapGenerator:
    """
    Generates ML-based personalized learning roadmap
    """

    def __init__(self):
        self.difficulty_engine = SkillDifficulty()
        self.resource_mapper = ResourceMapper()
        self.model = self._train_learning_time_model()

    def _train_learning_time_model(self):
        """
        Train regression model on synthetic learning-time data
        """

        # Features: [difficulty_level]
        X = np.array([
            [1], [1], [2], [2], [3], [3]
        ])

        # Target: learning time in weeks
        y = np.array([2, 3, 5, 6, 9, 10])

        model = LinearRegression()
        model.fit(X, y)
        return model

    def estimate_learning_time(self, skill: str) -> float:
        """
        Predict learning time (weeks) using ML regression
        """
        difficulty_level = self.difficulty_engine.get_difficulty_level(skill)
        predicted_time = self.model.predict([[difficulty_level]])[0]
        return round(predicted_time, 1)

    def generate_roadmap(self, missing_skills: list) -> list:
        """
        Generate ordered roadmap with ML-based time estimates
        """

        roadmap = []

        for skill in missing_skills:
            weeks = self.estimate_learning_time(skill)
            resources = self.resource_mapper.get_resources(skill)

            roadmap.append({
                "skill": skill,
                "estimated_weeks": weeks,
                "resources": resources
            })

        # Sort by estimated learning time (ascending)
        roadmap.sort(key=lambda x: x["estimated_weeks"])

        return roadmap
