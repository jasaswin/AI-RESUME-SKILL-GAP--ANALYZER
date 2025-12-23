from src.nlp import process_resume
from src.skills.resume_skill_extractor import ResumeSkillExtractor
from src.nlp.resume_text_extractor import extract_resume_text
from src.skills.jd_skill_extractor import JDSkillExtractor
from src.vectorizer.tfidf_vectorizer import SkillVectorizer
from src.matching.similarity_calculator import SimilarityCalculator
from src.matching.gap_identifier import SkillGapIdentifier
from src.explainability.explanation_generator import ExplanationGenerator
from src.explainability.confidence_score import ConfidenceScorer
from pathlib import Path
from src.roadmap.roadmap_generator import RoadmapGenerator
from src.matching.score_calculator import ScoreCalculator
from src.intelligence.career_readiness import CareerReadinessAnalyzer
from src.intelligence.skill_depth_estimator import SkillDepthEstimator
from src.intelligence.skill_priority import SkillPriorityAssigner
from src.intelligence.resume_quality_scorer import ResumeQualityScorer
from src.intelligence.resume_suggestions import ResumeSuggestionEngine
from src.intelligence.resume_signals import ResumeSignalAnalyzer

# 1. Process resume
resume_tokens = process_resume("data/resumes/NilimaMishra_CSE_GITA.pdf")
resume_skills = set(ResumeSkillExtractor().extract(resume_tokens))

#  Extract raw resume text
resume_raw_text = extract_resume_text(
    "data/resumes/NilimaMishra_CSE_GITA.pdf"
)

#  CREATE INSTANCE (THIS WAS MISSING)
depth_estimator = SkillDepthEstimator()

#  Skill depth estimation
skill_depths = depth_estimator.estimate(
    resume_text=resume_raw_text,
    resume_skills=resume_skills
)


# 2. Process JD
jd_path = Path("data") / "job_desc" / "mern_stack_developer.txt"
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


resume_text = resume_raw_text  # already extracted
resume_skills = resume_skills
missing_skills = gaps["missing_optional_skills"]

quality_scorer = ResumeQualityScorer()
quality_score = quality_scorer.score(
    resume_text=resume_text,
    resume_skills=resume_skills,
    skill_depths=skill_depths
)

suggestion_engine = ResumeSuggestionEngine()
suggestions = suggestion_engine.generate(
    resume_text=resume_text,
    resume_skills=resume_skills,
    missing_skills=missing_skills
)

signal_analyzer = ResumeSignalAnalyzer()
signals = signal_analyzer.analyze(resume_text)

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

readiness_analyzer = CareerReadinessAnalyzer()
career_readiness = readiness_analyzer.analyze(
    final_match_percentage=final_match_percentage,
    confidence=confidence,
    missing_core_skills=gaps["missing_core_skills"],
    missing_optional_skills=gaps["missing_optional_skills"]
)

# 7. Roadmap generation

priority_assigner = SkillPriorityAssigner()
priority_map = priority_assigner.assign(
    missing_core_skills=gaps["missing_core_skills"],
    missing_optional_skills=gaps["missing_optional_skills"],
    skill_depths=skill_depths
)

roadmap_generator = RoadmapGenerator()
roadmap = roadmap_generator.generate_roadmap(missing_skills)
phase_roadmap = roadmap_generator.generate_phase_roadmap(priority_map)


print("\nRESUME QUALITY SCORE:", quality_score)
print("\nRESUME SIGNALS:", signals)
print("\nSUGGESTIONS:")
for s in suggestions:
    print("-", s)
print("\nSKILL DEPTHS:")
print(skill_depths)
print("\nTF-IDF SCORE:", round(tfidf_score * 100, 2))
print("FINAL MATCH %:", final_match_percentage)
print("GAPS:", gaps)
print("CONFIDENCE:", confidence)
print("EXPLANATION:", explanation)
print("\nROADMAP:")
for step in roadmap:
    print(step)
print("\nPHASE-WISE ROADMAP:")
for phase, steps in phase_roadmap.items():
    print(f"\n{phase}")
    for step in steps:
        print(step)
print("\nCAREER READINESS:")
print(career_readiness)