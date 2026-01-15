from pathlib import Path

# ==================================================
# 🧠 CONSOLE UI HELPERS (PURE PRESENTATION LAYER)
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
# 1️⃣ RESUME INGESTION (REAL PDF – EXISTS)
# ==================================================
resume_path = Path("data/resumes/NilimaMishra_Resume_1P.pdf")

# resume_text = extract_resume_text(resume_path)
# resume_tokens = process_resume(resume_path)

resume_text = extract_resume_text(str(resume_path))
resume_tokens = process_resume(str(resume_path))


extractor = ResumeSkillExtractor()
extracted = extractor.extract(resume_tokens, resume_text)

explicit_skills = {s for s, m in extracted.items() if m["source"] == "explicit"}
inferred_skills = {s for s, m in extracted.items() if m["source"] == "inferred"}
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


# ==================================================
# 4️⃣ JD PROCESSING
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
# 8️⃣ BULLET GENERATION
# ==================================================
rule_generator = RuleBasedBulletGenerator()
bullet_suggestions = []

if gaps["missing_core_skills"]:
    skill = gaps["missing_core_skills"][0]
    bullet = rule_generator.generate(
        gap={"skill": skill, "severity": "High", "type": "core"},
        section="Skills Section"
    )
    bullet_suggestions.append({
        "resume_bullet": bullet["resume_bullet"],
        "priority": "High",
        "section": "Skills Section"
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
# 🔟 ROADMAP
# ==================================================
priority_map = {
    "high_priority": gaps["missing_core_skills"][:1],
    "medium_priority": gaps["missing_optional_skills"][:1],
    "low_priority": []
}

roadmap = RoadmapGenerator().generate_phase_roadmap(priority_map)


# ==================================================
# 1️⃣1️⃣ QUALITY + CONFIDENCE
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
# 🔒 FINAL HIRING DECISION
# ==================================================
def hiring_decision(score: float) -> str:
    if score >= 60:
        return "Shortlist"
    elif score >= 45:
        return "Trainable / Consider"
    return "Not Suitable Currently"

decision = hiring_decision(final_score)


# ==================================================
# 🎯 FINAL OUTPUT
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

if rewritten["skills_section_additions"]:
    section("🧩 SKILLS TO ADD")
    for b in rewritten["skills_section_additions"]:
        print_bullet(b)

section("🛠 IMMEDIATE NEXT STEP")
for phase, steps in roadmap.items():
    if steps:
        step = steps[0]
        print(f"Skill     : {step['skill']}")
        print(f"Duration  : {step['estimated_weeks']} Weeks")
        print(f"Resources : {', '.join(step['resources'])}")
        break

hr()
