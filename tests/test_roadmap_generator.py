




# tests/test_roadmap_generator.py

# from src.roadmap.roadmap_generator import RoadmapGenerator

# missing_skills = ["docker", "aws", "kubernetes"]

# generator = RoadmapGenerator()
# roadmap = generator.generate_roadmap(missing_skills)

# for item in roadmap:
#     print(
#         f"{item['skill']} → "
#         f"{item['estimated_weeks']} weeks → "
#         f"{item['resources']}"
#     )




# tests/test_roadmap_generator.py

from src.roadmap.roadmap_generator import RoadmapGenerator

missing_skills = ["docker", "aws", "kubernetes"]

generator = RoadmapGenerator()
roadmap = generator.generate_roadmap(missing_skills)

print("\nLEARNING ROADMAP (ML-BASED):\n")

for item in roadmap:
    print(
        f"Skill: {item['skill']}, "
        f"Estimated Time: {item['estimated_weeks']} weeks"
    )
    print("Resources:", ", ".join(item["resources"]))
    print("-" * 50)
