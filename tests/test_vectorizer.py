
from src.vectorizer.tfidf_vectorizer import SkillVectorizer

# Example skills (simulate Phase 3 output)
resume_skills_text = "python sql docker"
job_skills_text = "python sql aws docker kubernetes"

vectorizer = SkillVectorizer()

vectors = vectorizer.fit_transform(
    [resume_skills_text, job_skills_text]
)

print("VECTOR SHAPE:", vectors.shape)
print("FEATURE NAMES:", vectorizer.get_feature_names())
print("VECTORS:\n", vectors.toarray())
