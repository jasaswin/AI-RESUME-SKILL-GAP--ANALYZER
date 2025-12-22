from src.nlp import process_resume
from src.skills.resume_skill_extractor import ResumeSkillExtractor
from src.skills.jd_skill_extractor import JDSkillExtractor
from src.vectorizer.tfidf_vectorizer import SkillVectorizer
from src.matching.similarity_calculator import SimilarityCalculator
from src.matching.gap_identifier import SkillGapIdentifier
from src.explainability.explanation_generator import ExplanationGenerator
from src.explainability.confidence_score import ConfidenceScorer
from pathlib import Path
from src.roadmap.roadmap_generator import RoadmapGenerator
from src.matching.score_calculator import ScoreCalculator

# 1. Process resume
resume_tokens = process_resume("data/resumes/NilimaMishra_CSE_GITA.pdf")
resume_skills = set(ResumeSkillExtractor().extract(resume_tokens))

# 2. Process JD
jd_path = Path("data") / "job_desc" / "software_developer.txt"
jd_text = jd_path.read_text(encoding="utf-8")

jd_result = JDSkillExtractor().extract_skills(jd_text)

jd_core = set(jd_result["core_skills"])
jd_optional = set(jd_result["optional_skills"])

print("JD RESULT TYPE:", type(jd_result))
print("JD RESULT VALUE:", jd_result)



# 3. Vectorization
resume_text = " ".join(resume_skills)
jd_text_combined = " ".join(jd_core | jd_optional)

vectorizer = SkillVectorizer()
vectors = vectorizer.fit_transform([resume_text, jd_text_combined])

# 4. Similarity

tfidf_score = SimilarityCalculator.cosine_similarity_score(
    vectors[0], vectors[1]
)

final_match_percentage = ScoreCalculator.final_score(
    tfidf_score=tfidf_score,
    resume_skills=resume_skills,
    core_skills=jd_core,
    optional_skills=jd_optional
)

# 5. Gap detection
gaps = SkillGapIdentifier.identify_gaps(
    resume_skills, jd_core, jd_optional
)

# 6. Explainability
matched_skills = sorted(resume_skills & (jd_core | jd_optional))
missing_skills = sorted((jd_core | jd_optional) - resume_skills)
core_missing_skills = sorted(jd_core - resume_skills)

explainer = ExplanationGenerator()
explanation = explainer.generate_explanation(
    matched_skills=matched_skills,
    missing_skills=missing_skills,
    core_missing_skills=core_missing_skills,
    similarity_score=tfidf_score
)

confidence_scorer = ConfidenceScorer()
confidence = confidence_scorer.compute_confidence(
    similarity_score=tfidf_score,
    matched_skills=matched_skills,
    total_job_skills=len(jd_core | jd_optional)
)

# 7. Roadmap generation
roadmap_generator = RoadmapGenerator()
roadmap = roadmap_generator.generate_roadmap(missing_skills)




print("\nTF-IDF SCORE:", round(tfidf_score * 100, 2))
print("FINAL MATCH %:", final_match_percentage)
print("GAPS:", gaps)
print("CONFIDENCE:", confidence)
print("EXPLANATION:", explanation)
print("\nROADMAP:")
for step in roadmap:
    print(step)