from src.intelligence.skill_depth_estimator import SkillDepthEstimator

resume_text = """
Developed MERN stack projects using React, Node.js, MongoDB.
Used Git and GitHub for version control.
Implemented REST APIs and deployed applications.
"""

resume_skills = {
    "javascript",
    "react",
    "nodejs",
    "git",
    "github"
}

estimator = SkillDepthEstimator()
depths = estimator.estimate(resume_text, resume_skills)

print("SKILL DEPTH ESTIMATION:")
print(depths)
