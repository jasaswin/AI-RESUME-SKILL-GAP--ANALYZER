
from pathlib import Path

# ==================================================
# 🧠 CONSOLE UI HELPERS
# ==================================================
def hr():
    print("═" * 54)

def sr():
    print("─" * 54)

def title(text):
    hr()
    print(text.center(54))
    hr()

def section(text):
    print(f"\n{text}")
    sr()

def print_bullet(text):
    print(f"• {text}")

def check(label, value):
    icon = "✔" if value else "✖"
    print(f"{icon} {label.replace('_', ' ').title()}")

def badge(text):
    return {
        "Shortlist": "✅ SHORTLIST",
        "Trainable / Consider": "🟡 TRAINABLE",
        "Not Suitable Currently": "🔴 NOT READY"
    }.get(text, text)


# ==================================================
# NLP & SKILLS
# ==================================================
from src.nlp import process_resume
from src.nlp.resume_text_extractor import extract_resume_text
from src.skills.resume_skill_extractor import ResumeSkillExtractor
from src.skills.jd_skill_extractor import JDSkillExtractor
from src.skills.skill_database import SkillDatabase

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
from src.intelligence.resume_rewriter import ResumeRewriter
from src.intelligence.jd_skill_prioritizer import JDSkillPrioritizer
from src.intelligence.jd_domain_detector import JDDomainDetector

# ==================================================
# ROADMAP & CONFIG
# ==================================================
from src.roadmap.roadmap_generator import RoadmapGenerator
from src.matching.role_profiles import ROLE_PROFILES
from src.explainability.confidence_score import ConfidenceScorer


# ==================================================
# 1️⃣ RESUME INGESTION
# ==================================================
resume_path = "data/resumes/sample_resume.txt"

resume_text = extract_resume_text(str(resume_path))
resume_tokens = process_resume(str(resume_path))

extractor = ResumeSkillExtractor()
extracted = extractor.extract(resume_tokens, resume_text)

explicit_skills = {s for s, m in extracted.items() if m["source"] == "explicit"}
inferred_skills = {s for s, m in extracted.items() if m["source"] == "inferred"}
resume_skills = explicit_skills | inferred_skills


# ==================================================
# 2️⃣ DEPTH + SIGNALS
# ==================================================
skill_depths = SkillDepthEstimator().estimate(resume_text, resume_skills)
signals = ResumeSignalAnalyzer().analyze(resume_text)
archetype = ResumeArchetypeDetector.detect(resume_skills)


# ==================================================
# 3️⃣ JD PROCESSING
# ==================================================
jd_path = Path("data/job_desc/mern_stack_developer.txt")
jd_text = jd_path.read_text(encoding="utf-8")

jd_result = JDSkillExtractor().extract_skills(jd_text)
jd_core = set(jd_result["core_skills"])
jd_optional = set(jd_result["optional_skills"])

target_role = jd_path.stem
profile = ROLE_PROFILES.get(target_role, {})

prioritized = JDSkillPrioritizer.prioritize(
    jd_core=jd_core,
    jd_optional=jd_optional,
    role_profile=profile
)

jd_domain = JDDomainDetector.detect(jd_text)


# ==================================================
# 4️⃣ VECTOR SIMILARITY
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
# 5️⃣ FINAL SCORE
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
# 6️⃣ GAP ANALYSIS
# ==================================================
gaps = SkillGapIdentifier.identify_gaps(
    explicit_skills=explicit_skills,
    inferred_skills=inferred_skills,
    jd_core=jd_core,
    jd_optional=jd_optional
)

missing_required = gaps["missing_core_skills"]
missing_optional = gaps["missing_optional_skills"]


# ==================================================
# 7️⃣ BUILD SKILL METADATA (NEW CLEAN PART)
# ==================================================
skill_db = SkillDatabase()

skill_categories = {}
skill_popularity = {}

all_missing = missing_required + missing_optional

for skill in all_missing:
    category = skill_db.get_category(skill)
    skill_categories[skill] = category if category else "tool"

    # simple importance weighting
    skill_popularity[skill] = 8 if skill in missing_required else 5


# ==================================================
# 8️⃣ ROADMAP (FULL ML VERSION)
# ==================================================
roadmap = RoadmapGenerator().generate(
    missing_required_skills=missing_required,
    missing_optional_skills=missing_optional,
    skill_categories=skill_categories,
    skill_popularity=skill_popularity
)


# ==================================================
# 9️⃣ QUALITY + CONFIDENCE
# ==================================================
quality_score = ResumeQualityScorer().score(
    resume_text=resume_text,
    resume_skills=resume_skills,
    skill_depths=skill_depths
)

confidence = ConfidenceScorer().compute_confidence(
    similarity_score=tfidf_score,
    matched_skills=list(resume_skills & jd_core),
    total_job_skills=len(jd_core | jd_optional)
)


# ==================================================
# 🔒 FINAL DECISION
# ==================================================
def hiring_decision(score: float) -> str:
    if score >= 60:
        return "Shortlist"
    elif score >= 45:
        return "Trainable / Consider"
    return "Not Suitable Currently"

decision = hiring_decision(final_score)


# ==================================================
# 🎯 OUTPUT
# ==================================================
title("🧠 AI RESUME–JD EVALUATION REPORT")

print(f"\n📌 TARGET ROLE        : {target_role.replace('_', ' ').title()}")
print(f"📊 FINAL MATCH        : {round(final_score, 2)}%")
print(f"🎯 CONFIDENCE         : {round(confidence, 2)}%")
print(f"📝 RESUME QUALITY     : {quality_score} / 100")
print(f"\n🚦 HIRING DECISION    : {badge(decision)}")

section("🔍 KEY SIGNALS")
for k, v in signals.items():
    check(k, v)

section("📚 ROADMAP")

for phase, steps in roadmap.items():
    print(f"\n{phase}")
    for step in steps:
        print(f"  • {step['skill']} ({step['estimated_weeks']} weeks)")
        print(f"    - {step['reason']}")
        print(f"    - Resources: {', '.join(step['resources'])}")

hr()
