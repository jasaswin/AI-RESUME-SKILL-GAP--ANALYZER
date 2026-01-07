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
from src.intelligence.skill_gap_reasoner import SkillGapReasoner
from src.intelligence.skill_section_recommender import SkillSectionRecommender
from src.llm.groq_bullet_generator import GroqBulletGenerator
from src.llm.groq_resume_rewriter import GroqResumeRewriter
from src.intelligence.resume_bullet_generator import RuleBasedBulletGenerator
from src.config.settings import USE_GROQ


# -------------------- RESUME INGESTION --------------------
resume_path = "data/resumes/junior-python-developer2 - Template 16 .pdf"
resume_raw_text = extract_resume_text(resume_path)
resume_tokens = process_resume(resume_path)

extractor = ResumeSkillExtractor()
extracted = extractor.extract(resume_tokens, resume_raw_text)
resume_skills = set(extracted.keys())

depth_estimator = SkillDepthEstimator()
skill_depths = depth_estimator.estimate(
    resume_text=resume_raw_text,
    resume_skills=resume_skills
)

from src.intelligence.skill_confidence_promoter import SkillConfidencePromoter

inferred_skills = {
    s for s, meta in extracted.items() if meta["source"] == "inferred"
}

resume_skills |= SkillConfidencePromoter.promote(
    resume_skills, inferred_skills, skill_depths
)


# -------------------- MULTI ROLE FIT --------------------
all_roles = RoleCompatibilityAnalyzer.analyze_all_roles(
    resume_skills=resume_skills,
    skill_depths=skill_depths
)

print("\nTOP ROLE RECOMMENDATIONS:")
for r in all_roles[:3]:
    print(r)


# -------------------- JD PROCESSING --------------------
jd_path = Path("data/job_desc/ai_ml_developer.txt")
jd_text = jd_path.read_text(encoding="utf-8")

jd_result = JDSkillExtractor().extract_skills(jd_text)
jd_core = set(jd_result["core_skills"])
jd_optional = set(jd_result["optional_skills"])

print("\nJD RESULT:", jd_result)


# -------------------- VECTOR SIMILARITY --------------------
vectorizer = SkillVectorizer()
vectors = vectorizer.fit_transform([
    " ".join(resume_skills),
    " ".join(jd_core | jd_optional)
])

tfidf_score = SimilarityCalculator.weighted_similarity_score(
    resume_vector=vectors[0:1],
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
    role="python_developer"
)


# -------------------- GAP ANALYSIS --------------------
target_role = "python_developer"

gaps = SkillGapIdentifier.identify_gaps(
    resume_skills, jd_core, jd_optional
)

gap_reasoning = SkillGapReasoner.reason(
    resume_skills=resume_skills,
    inferred_skills=inferred_skills,
    skill_depths=skill_depths,
    missing_core_skills=gaps["missing_core_skills"],
    missing_optional_skills=gaps["missing_optional_skills"],
    role=target_role
)

section_guidance = SkillSectionRecommender.recommend(
    gap_reasoning=gap_reasoning,
    role=target_role
)

section_map = {
    s["skill"]: s["recommended_section"]
    for s in section_guidance
}


# -------------------- BULLET GENERATION (SAFE) --------------------
bullet_generator = GroqBulletGenerator(enabled=USE_GROQ)
rule_generator = RuleBasedBulletGenerator()

skills_section_additions = []
project_section_additions = []

for gap in gap_reasoning:
    section = section_map.get(gap["skill"], "Projects Section")

    bullet = bullet_generator.generate(
        skill=gap["skill"],
        level=skill_depths.get(gap["skill"], "beginner"),
        role=target_role,
        section=section
    )

    # ---- Normalize bullet ----
    if isinstance(bullet, str):
        bullet = {
            "skill": gap["skill"],
            "resume_bullet": bullet,
            "source": "llm"
        }

    if not bullet:
        bullet = rule_generator.generate(gap)
        bullet["source"] = "rule"

    if section == "Skills Section":
        skills_section_additions.append(bullet["resume_bullet"])
    else:
        project_section_additions.append(bullet["resume_bullet"])

# -------------------- ROADMAP GENERATION --------------------
priority_assigner = SkillPriorityAssigner()

priority_map = priority_assigner.assign(
    missing_core_skills=gaps["missing_core_skills"],
    missing_optional_skills=gaps["missing_optional_skills"],
    skill_depths=skill_depths
)

roadmap_generator = RoadmapGenerator()

roadmap = roadmap_generator.generate_roadmap(
    gaps["missing_core_skills"] + gaps["missing_optional_skills"]
)

phase_roadmap = roadmap_generator.generate_phase_roadmap(priority_map)


# -------------------- RESUME REWRITE --------------------
rewriter = GroqResumeRewriter(enabled=USE_GROQ)

rewritten_resume = rewriter.rewrite(
    resume_text=resume_raw_text,
    skills_add=skills_section_additions,
    projects_add=project_section_additions
)

if not rewritten_resume:
    rewritten_resume = {
        "skills": skills_section_additions,
        "projects": project_section_additions
    }


# -------------------- QUALITY + EXPLANATION --------------------
quality_score = ResumeQualityScorer().score(
    resume_text=resume_raw_text,
    resume_skills=resume_skills,
    skill_depths=skill_depths
)

signals = ResumeSignalAnalyzer().analyze(resume_raw_text)

explanation = ExplanationGenerator().generate_explanation(
    matched_skills=sorted(resume_skills & (jd_core | jd_optional)),
    missing_skills=sorted((jd_core | jd_optional) - resume_skills),
    core_missing_skills=sorted(jd_core - resume_skills),
    similarity_score=tfidf_score
)

confidence = ConfidenceScorer().compute_confidence(
    similarity_score=tfidf_score,
    matched_skills=list(resume_skills & jd_core),
    total_job_skills=len(jd_core | jd_optional)
)


# -------------------- OUTPUT --------------------
print("\nFINAL MATCH %:", round(final_score, 2))
print("CONFIDENCE:", round(confidence, 2))
print("RESUME QUALITY:", quality_score)
print("SIGNALS:", signals)

print("\nSKILLS TO ADD:")
for b in skills_section_additions:
    print("-", b)



print("\nPROJECT BULLETS:")
for b in project_section_additions:
    print("-", b)

print("\nPHASE-WISE ROADMAP:")
for phase, steps in phase_roadmap.items():
    print(f"\n{phase}")
    for step in steps:
        print(step)

print("\nCAREER READINESS:")
print(CareerReadinessAnalyzer().analyze(
    final_score=final_score,
    confidence=confidence,
    missing_core_skills=gaps["missing_core_skills"],
    missing_optional_skills=gaps["missing_optional_skills"]
))
