

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# class ResourceMapper:
#     """
#     ML-based resource recommendation
#     """

#     def __init__(self, resources: dict):
#         """
#         resources = {
#           "docker": ["Docker Docs", "Docker Tutorial"],
#           "aws": ["AWS Free Tier", "AWS Cloud Practitioner"]
#         }
#         """
#         self.resources = resources
#         self.vectorizer = TfidfVectorizer()

#     def recommend(self, skill: str) -> list[str]:
#         if skill not in self.resources:
#             return []

#         texts = [skill] + self.resources[skill]
#         vectors = self.vectorizer.fit_transform(texts)

#         scores = cosine_similarity(vectors[0:1], vectors[1:])[0]
#         ranked = sorted(
#             zip(self.resources[skill], scores),
#             key=lambda x: x[1],
#             reverse=True
#         )

#         return [res for res, _ in ranked]





# src/roadmap/resource_mapper.py

# class ResourceMapper:
#     """
#     Maps skills to learning resources
#     """

#     def __init__(self):
#         self.resources = {
#             "python": ["Python Docs", "freeCodeCamp Python"],
#             "sql": ["SQLZoo", "Mode SQL Tutorial"],
#             "docker": ["Docker Docs", "TechWorld with Nana"],
#             "aws": ["AWS Free Tier", "AWS Skill Builder"],
#             "kubernetes": ["Kubernetes Docs", "KodeKloud"],
#             "machine learning": ["Andrew Ng ML Course"],
#             "deep learning": ["DeepLearning.AI"]
#         }

#     def get_resources(self, skill: str) -> list:
#         return self.resources.get(skill.lower(), ["Google + Practice"])




# src/roadmap/resource_mapper.py

class ResourceMapper:
    """
    Maps skills to learning resources
    """

    def __init__(self):
        self.resources = {
            "python": [
                "Python Official Docs",
                "Automate the Boring Stuff"
            ],
            "sql": [
                "W3Schools SQL",
                "Mode SQL Tutorial"
            ],
            "docker": [
                "Docker Official Docs",
                "Docker for Beginners (YouTube)"
            ],
            "aws": [
                "AWS Free Tier",
                "AWS Cloud Practitioner Course"
            ],
            "kubernetes": [
                "Kubernetes Docs",
                "Kubernetes Hands-on Labs"
            ]
        }

    def get_resources(self, skill: str) -> list:
        """
        Return learning resources for a skill
        """
        return self.resources.get(skill, ["General Online Tutorials"])
