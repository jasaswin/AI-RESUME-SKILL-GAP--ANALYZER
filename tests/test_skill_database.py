
from src.skills.skill_database import SkillDatabase

db = SkillDatabase()

print(db.normalize_skill("py"))        # python
print(db.is_valid_skill("python"))     # True
print(db.is_valid_skill("golang"))     # False
print(db.get_category("docker"))       # tool
