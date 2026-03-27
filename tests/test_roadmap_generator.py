




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

# from src.roadmap.roadmap_generator import RoadmapGenerator

# missing_skills = ["docker", "aws", "kubernetes"]

# generator = RoadmapGenerator()
# roadmap = generator.generate_roadmap(missing_skills)

# print("\nLEARNING ROADMAP (ML-BASED):\n")

# for item in roadmap:
#     print(
#         f"Skill: {item['skill']}, "
#         f"Estimated Time: {item['estimated_weeks']} weeks"
#     )
#     print("Resources:", ", ".join(item["resources"]))
#     print("-" * 50)





# from src.roadmap.roadmap_generator import RoadmapGenerator


# def test_generic_gap_roadmap():
#     """
#     Test roadmap for ANY JD vs resume mismatch
#     """

#     # Simulated extracted skills
#     jd_required = [
#         "javascript", "react", "nodejs", "mongodb", "html", "css"
#     ]
#     jd_optional = [
#         "aws", "docker"
#     ]
#     resume_skills = [
#         "python", "sql", "machine learning"
#     ]

#     # Compute gaps (same logic as pipeline)
#     missing_required = list(set(jd_required) - set(resume_skills))
#     missing_optional = list(set(jd_optional) - set(resume_skills))

#     generator = RoadmapGenerator()
#     roadmap = generator.generate(
#         missing_required=missing_required,
#         missing_optional=missing_optional
#     )

#     print("\n===== ROADMAP OUTPUT =====")
#     for k, v in roadmap.items():
#         print(f"\n{k}:")
#         for item in v:
#             print(item)

#     assert len(roadmap["Core Skill Roadmap"]) > 0
#     assert any("javascript" in s["skill"] for s in roadmap["Core Skill Roadmap"])




from src.roadmap.roadmap_generator import RoadmapGenerator


def test_mearn_stack_roadmap():
    generator = RoadmapGenerator()

    # Simulated output from earlier phases
    missing_required_skills = [
        "javascript", "react", "nodejs", "mongodb"
    ]

    missing_optional_skills = [
        "aws", "docker", "ci/cd"
    ]

    # Skill categories (normally from skill DB)
    skill_categories = {
        "javascript": "language",
        "react": "framework",
        "nodejs": "framework",
        "mongodb": "database",
        "aws": "tool",
        "docker": "tool",
        "ci/cd": "tool"
    }

    # Popularity scores (1–10, mock values)
    skill_popularity = {
        "javascript": 9,
        "react": 8,
        "nodejs": 8,
        "mongodb": 7,
        "aws": 9,
        "docker": 8,
        "ci/cd": 6
    }

    roadmap = generator.generate(
        missing_required_skills,
        missing_optional_skills,
        skill_categories,
        skill_popularity
    )

    print("\nGENERATED ROADMAP\n")
    for phase, steps in roadmap.items():
        print(f"\n{phase}")
        for step in steps:
            print(step)


if __name__ == "__main__":
    test_mearn_stack_roadmap()
