
from src.skills.jd_skill_extractor import JDSkillExtractor

jd_text = """
Required skills: Python, SQL.
Must have experience with Docker.
Good to have AWS knowledge.
"""

extractor = JDSkillExtractor()
result = extractor.extract_skills("data/job_descriptions/mern_stack_developer.txt")

print("CORE SKILLS:", result["core_skills"])
print("OPTIONAL SKILLS:", result["optional_skills"])
