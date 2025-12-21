
from src.matching.gap_identifier import SkillGapIdentifier

resume_skills = {"python", "sql"}
jd_core = {"python", "sql", "docker"}
jd_optional = {"aws"}

gaps = SkillGapIdentifier.identify_gaps(
    resume_skills,
    jd_core,
    jd_optional
)

print("GAPS FOUND:")
print(gaps)
