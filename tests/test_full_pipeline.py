from src.nlp import process_resume
from src.skills.resume_skill_extractor import ResumeSkillExtractor
from src.skills.jd_skill_extractor import JDSkillExtractor
from src.vectorizer.tfidf_vectorizer import SkillVectorizer
from src.matching.similarity_calculator import SimilarityCalculator
from src.matching.gap_identifier import SkillGapIdentifier
from src.explainability.explanation_generator import ExplanationGenerator
from src.explainability.confidence_score import ConfidenceScorer


# 1. Process resume
resume_tokens = process_resume("data/resumes/sample_resume.txt")
resume_skills = set(ResumeSkillExtractor().extract(resume_tokens))

# 2. Process JD
jd_text = open("data/job_descriptions/data_analyst.txt").read()
jd_result = JDSkillExtractor().extract_skills(jd_text)

jd_core = set(jd_result["core_skills"])
jd_optional = set(jd_result["optional_skills"])

# 3. Vectorization
resume_text = " ".join(resume_skills)
jd_text_combined = " ".join(jd_core | jd_optional)

vectorizer = SkillVectorizer()
vectors = vectorizer.fit_transform([resume_text, jd_text_combined])

# 4. Similarity
score = SimilarityCalculator.cosine_similarity_score(
    vectors[0], vectors[1]
)
match_percentage = round(score * 100, 2)

# 5. Gap detection
gaps = SkillGapIdentifier.identify_gaps(
    resume_skills, jd_core, jd_optional
)

# 6. Explainability
explanation = ExplanationGenerator.generate(match_percentage, gaps)
confidence = ConfidenceScorer.calculate(
    match_percentage, len(gaps["missing_core_skills"])
)

print("\nMATCH %:", match_percentage)
print("GAPS:", gaps)
print("CONFIDENCE:", confidence)
print("EXPLANATION:", explanation)
