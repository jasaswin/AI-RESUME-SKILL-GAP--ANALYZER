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
from src.intelligence.role_compatibility import RoleCompatibilityAnalyzer



#  Extract raw resume text
resume_raw_text = extract_resume_text(
    "data/resumes/entry-level-business-analyst2 - Template 17.pdf"
)
# 1. Process resume

resume_tokens = process_resume("data/resumes/entry-level-business-analyst2 - Template 17.pdf")

extractor = ResumeSkillExtractor()
extracted_skills = extractor.extract(resume_tokens, resume_raw_text)

resume_skills = set(extracted_skills.keys())



#  CREATE INSTANCE (THIS WAS MISSING)
depth_estimator = SkillDepthEstimator()

#  Skill depth estimation
skill_depths = depth_estimator.estimate(
    resume_text=resume_raw_text,
    resume_skills=resume_skills
)

# --- Promote inferred skills with confidence ---
from src.intelligence.skill_confidence_promoter import SkillConfidencePromoter

inferred_skills = {
    s for s, meta in ResumeSkillExtractor()
    .extract(resume_tokens, resume_raw_text).items()
    if meta["source"] == "inferred"
}

promoted_skills = SkillConfidencePromoter.promote(
    resume_skills,
    inferred_skills,
    skill_depths
)

resume_skills = resume_skills | promoted_skills



# 2. Process JD
jd_path = Path("data") / "job_desc" / "business_analyst.txt"
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

compatibility = RoleCompatibilityAnalyzer.analyze(
    resume_skills=resume_skills,
    skill_depths=skill_depths,
    target_role="business_analyst"
)


# 4. Similarity

tfidf_score = SimilarityCalculator.weighted_similarity_score(
    resume_vector=vectors[0:1],  # ← slice keeps 2D
    jd_vector=vectors[1:2],
    resume_skills=resume_skills,
    jd_core_skills=jd_core,
    jd_optional_skills=jd_optional,
    skill_depths=skill_depths
)


final_score = ScoreCalculator.final_score(
    similarity_score=tfidf_score,
    resume_skills=resume_skills,
    core_skills=jd_core,
    optional_skills=jd_optional,
    skill_depths=skill_depths,
    role="ai_ml_developer"
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
    final_score=final_score,
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

print("\nROLE COMPATIBILITY:")
for k, v in compatibility.items():
    print(f"{k}: {v}")

print("\nTF-IDF SCORE:", round(tfidf_score * 100, 2))
print("FINAL MATCH %:", final_score)
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



