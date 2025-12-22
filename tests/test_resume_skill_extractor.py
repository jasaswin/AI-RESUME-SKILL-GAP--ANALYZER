from src.nlp import process_resume
from src.skills.resume_skill_extractor import ResumeSkillExtractor

extractor = ResumeSkillExtractor()

tokens = process_resume("data/resumes/sample_resume.txt")
skills = extractor.extract(tokens)

print("Resume Skills:", skills)
