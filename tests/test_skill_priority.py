from src.intelligence.skill_priority import SkillPriorityAssigner

assigner = SkillPriorityAssigner()

result = assigner.assign(
    missing_core_skills=[],
    missing_optional_skills=["aws", "docker"],
    skill_depths={
        "aws": "beginner",
        "docker": "intermediate"
    }
)

print(result)
