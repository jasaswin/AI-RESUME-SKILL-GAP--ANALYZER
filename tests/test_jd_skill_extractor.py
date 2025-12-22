from src.skills.jd_skill_extractor import JDSkillExtractor

print(">>> TEST STARTED <<<")

# jd_text = """
# Required skills:
# python
# machine learning
# data analysis
# nlp

# Must have experience with:
# sql

# Good to have:
# aws
# docker
# """

extractor = JDSkillExtractor()
result = extractor.extract_skills("data/job_desc/mern_stack_developer.txt")

print("CORE SKILLS:", result["core_skills"])
print("OPTIONAL SKILLS:", result["optional_skills"])

print(">>> TEST FINISHED <<<")
