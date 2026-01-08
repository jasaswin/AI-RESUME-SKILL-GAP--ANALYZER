# tests/test_full_pipeline.py

from pathlib import Path

# ==================================================
# NLP & SKILLS
# ==================================================
from src.nlp import process_resume
from src.nlp.resume_text_extractor import extract_resume_text
from src.skills.resume_skill_extractor import ResumeSkillExtractor
from src.skills.jd_skill_extractor import JDSkillExtractor

# ==================================================
# MATCHING
# ==================================================
from src.vectorizer.tfidf_vectorizer import SkillVectorizer
from src.matching.similarity_calculator import SimilarityCalculator
from src.matching.score_calculator import ScoreCalculator
from src.matching.gap_identifier import SkillGapIdentifier

# ==================================================
# INTELLIGENCE
# ==================================================
from src.intelligence.skill_depth_estimator import SkillDepthEstimator
from src.intelligence.role_compatibility import RoleCompatibilityAnalyzer
from src.intelligence.resume_quality_scorer import ResumeQualityScorer
from src.intelligence.resume_signals import ResumeSignalAnalyzer
from src.intelligence.resume_archetype_detector import ResumeArchetypeDetector
from src.intelligence.resume_bullet_generator import RuleBasedBulletGenerator
from src.intelligence.career_readiness import CareerReadinessAnalyzer
from src.intelligence.resume_rewriter import ResumeRewriter

# ==================================================
# EXPLAINABILITY
# ==================================================
from src.explainability.explanation_generator import ExplanationGenerator
from src.explainability.confidence_score import ConfidenceScorer

# ==================================================
# ROADMAP
# ==================================================
from src.roadmap.roadmap_generator import RoadmapGenerator

# ==================================================
# CONFIG
# ==================================================
from src.config.settings import USE_GROQ


# ==================================================
# 1️⃣ RESUME INGESTION
# ==================================================
resume_path = "data/resumes/entry-level-data-analyst2 - Template 17.pdf"

resume_text = extract_resume_text(resume_path)
resume_tokens = process_resume(resume_path)

extractor = ResumeSkillExtractor()
extracted_skills = extractor.extract(resume_tokens, resume_text)

explicit_skills = {s for s, m in extracted_skills.items() if m["source"] == "explicit"}
inferred_skills = {s for s, m in extracted_skills.items() if m["source"] == "inferred"}

resume_skills = explicit_skills | inferred_skills


# ==================================================
# 2️⃣ DEPTH + SIGNALS + ARCHETYPE
# ==================================================
skill_depths = SkillDepthEstimator().estimate(resume_text, resume_skills)
signals = ResumeSignalAnalyzer().analyze(resume_text)
archetype = ResumeArchetypeDetector.detect(resume_skills)


# ==================================================
# 3️⃣ ROLE COMPATIBILITY
# ==================================================
all_roles = RoleCompatibilityAnalyzer.analyze_all_roles(
    explicit_skills=explicit_skills,
    inferred_skills=inferred_skills
)

print("\nTOP ROLE RECOMMENDATIONS (Resume-based career fit):")
for r in all_roles[:3]:
    print(r)


# ==================================================
# 4️⃣ JD PROCESSING
# ==================================================
jd_path = Path("data/job_desc/ai_ml_developer.txt")
jd_text = jd_path.read_text(encoding="utf-8")

jd_result = JDSkillExtractor().extract_skills(jd_text)
jd_core = set(jd_result["core_skills"])
jd_optional = set(jd_result["optional_skills"])

print("\nJD RESULT:", jd_result)

target_role = jd_path.stem

from src.intelligence.jd_domain_detector import JDDomainDetector
jd_domain = JDDomainDetector.detect(jd_text)
print("JD DOMAIN:", jd_domain)


# ==================================================
# 5️⃣ VECTOR SIMILARITY
# ==================================================
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
    skill_depths=skill_depths,
    resume_archetype=archetype
)


# ==================================================
# 6️⃣ FINAL SCORE
# ==================================================
final_score = ScoreCalculator.final_score(
    similarity_score=tfidf_score,
    resume_skills=resume_skills,
    core_skills=jd_core,
    optional_skills=jd_optional,
    skill_depths=skill_depths,
    role=target_role,
    inferred_skills=inferred_skills,
    jd_domain=jd_domain
)


# ==================================================
# 7️⃣ GAP ANALYSIS
# ==================================================
gaps = SkillGapIdentifier.identify_gaps(
    explicit_skills=explicit_skills,
    inferred_skills=inferred_skills,
    jd_core=jd_core,
    jd_optional=jd_optional
)


# ==================================================
# 8️⃣ BULLET GENERATION (FAIL-SAFE)
# ==================================================
rule_generator = RuleBasedBulletGenerator()
bullet_suggestions = []

# 🔒 ALWAYS show at least ONE core skill
core_for_resume = gaps["missing_core_skills"][:1]

for skill in core_for_resume:
    bullet = rule_generator.generate(
        gap={"skill": skill, "severity": "High"},
        section="Skills Section"
    )
    bullet_suggestions.append({
        "resume_bullet": bullet["resume_bullet"],
        "priority": "High",
        "section": "Skills Section"
    })

# Optional → Projects only
for skill in gaps["missing_optional_skills"]:
    bullet = rule_generator.generate(
        gap={"skill": skill, "severity": "Medium"},
        section="Projects Section"
    )
    bullet_suggestions.append({
        "resume_bullet": bullet["resume_bullet"],
        "priority": "Medium",
        "section": "Projects Section"
    })


# ==================================================
# 9️⃣ RESUME REWRITE
# ==================================================
rewritten = ResumeRewriter.rewrite(
    original_text=resume_text,
    bullet_suggestions=bullet_suggestions,
    archetype=archetype
)


# ==================================================
# 🔟 ROADMAP (NON-EMPTY GUARANTEE)
# ==================================================
high = gaps["missing_core_skills"][:1]
medium = gaps["missing_core_skills"][1:]
low = gaps["missing_optional_skills"]

if not high and medium:
    high = [medium.pop(0)]

priority_map = {
    "high_priority": high,
    "medium_priority": medium,
    "low_priority": low
}

roadmap = RoadmapGenerator().generate_phase_roadmap(priority_map)


# ==================================================
# 1️⃣1️⃣ QUALITY + EXPLANATION + CONFIDENCE
# ==================================================
quality_score = ResumeQualityScorer().score(
    resume_text=resume_text,
    resume_skills=resume_skills,
    skill_depths=skill_depths
)

explanation = ExplanationGenerator().generate_explanation(
    matched_skills=sorted(resume_skills & (jd_core | jd_optional)),
    missing_skills=sorted((jd_core | jd_optional) - resume_skills),
    core_missing_skills=gaps["missing_core_skills"],
    similarity_score=tfidf_score
)

confidence = ConfidenceScorer().compute_confidence(
    similarity_score=tfidf_score,
    matched_skills=list(resume_skills & jd_core),
    total_job_skills=len(jd_core | jd_optional)
)


# ==================================================
# 1️⃣2️⃣ FINAL OUTPUT
# ==================================================
print("\nFINAL MATCH %:", round(final_score, 2))
print("CONFIDENCE:", round(confidence, 2))
print("RESUME QUALITY:", quality_score)
print("SIGNALS:", signals)

print("\nSKILLS TO ADD:")
for b in rewritten["skills_section_additions"]:
    print("-", b)

print("\nPROJECT BULLETS:")
for b in rewritten["project_section_additions"]:
    print("-", b)

print("\nPHASE-WISE ROADMAP:")
for phase, steps in roadmap.items():
    print(f"\n{phase}")
    for step in steps:
        print(step)

print("\nCAREER READINESS:")
print(
CareerReadinessAnalyzer().analyze(
    final_score=final_score,
    confidence=confidence,
    missing_core_skills=gaps["missing_core_skills"],
    missing_optional_skills=gaps["missing_optional_skills"],
    critical_missing=set(),
    trainable_missing=set(gaps["missing_core_skills"]),
    role=target_role,
    jd_level="entry"
)

)
