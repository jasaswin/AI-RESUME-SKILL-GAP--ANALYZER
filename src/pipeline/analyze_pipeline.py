from src.skills.resume_skill_extractor import ResumeSkillExtractor
from src.skills.jd_skill_extractor import JDSkillExtractor
from src.skills.skill_database import SkillDatabase

from src.matching.similarity_calculator import SimilarityCalculator
from src.matching.score_calculator import ScoreCalculator
from src.matching.gap_identifier import SkillGapIdentifier

from src.intelligence.skill_depth_estimator import SkillDepthEstimator
from src.intelligence.resume_signals import ResumeSignalAnalyzer
from src.intelligence.resume_archetype_detector import ResumeArchetypeDetector

from src.explainability.confidence_score import ConfidenceScorer
from src.explainability.explanation_generator import ExplanationGenerator

from src.roadmap.roadmap_generator import RoadmapGenerator


# 🔥 NEW: Skill Mapping (CRITICAL FIX)
SKILL_MAP = {
    "expressjs": "express",
    "express.js": "express",
    "node.js": "nodejs",
    "node": "nodejs",
    "mysql": "sql",
    "postgresql": "sql",
    "python3": "python"
}


def normalize(skill_db, skill):
    skill = skill.lower().strip().replace(" ", "")
    skill = SKILL_MAP.get(skill, skill)
    return skill_db.normalize_skill(skill)


def analyze_resume_jd(resume_text: str, jd_text: str) -> dict:

    skill_db = SkillDatabase()

    # ---------------- Resume Processing ----------------
    extractor = ResumeSkillExtractor()
    extracted = extractor.extract([], resume_text)

    explicit_skills = {s for s, m in extracted.items() if m["source"] == "explicit"}
    inferred_skills = {s for s, m in extracted.items() if m["source"] == "inferred"}

    resume_skills_raw = explicit_skills | inferred_skills

    # ✅ FIXED NORMALIZATION
    resume_skills = {
        normalize(skill_db, s)
        for s in resume_skills_raw
    }

    # ---- Semantic expansion ----
    semantic_resume_map = {
        "mern": {"react", "nodejs", "mongodb", "javascript"},
    }

    resume_text_lower = resume_text.lower()

    for keyword, implied_skills in semantic_resume_map.items():
        if keyword in resume_text_lower:
            resume_skills.update({
                normalize(skill_db, s)
                for s in implied_skills
            })

    # ---- Implicit promotion ----
    implicit_core_map = {
        "react": {"javascript", "html", "css"},
        "nodejs": {"javascript"},
        "express": {"nodejs", "javascript"},
    }

    for skill in list(resume_skills):
        resume_skills.update({
            normalize(skill_db, s)
            for s in implicit_core_map.get(skill, set())
        })

    # ---------------- Intelligence Layer ----------------
    skill_depths = SkillDepthEstimator().estimate(resume_text, resume_skills)
    signals = ResumeSignalAnalyzer().analyze(resume_text)
    archetype = ResumeArchetypeDetector.detect(resume_skills)

    # ---------------- JD Processing ----------------
    jd_result = JDSkillExtractor().extract_skills(jd_text)

    jd_core_raw = set(jd_result["core_skills"])
    jd_optional_raw = set(jd_result["optional_skills"])

    # ✅ FIXED NORMALIZATION
    jd_core = {
        normalize(skill_db, s)
        for s in jd_core_raw
    }

    jd_optional = {
        normalize(skill_db, s)
        for s in jd_optional_raw
    }

    # ---------------- Matching ----------------
    similarity = SimilarityCalculator.weighted_similarity_score(
        resume_vector=None,
        jd_vector=None,
        resume_skills=resume_skills,
        jd_core_skills=jd_core,
        jd_optional_skills=jd_optional,
        skill_depths=skill_depths,
        resume_archetype=archetype
    )

    final_score = ScoreCalculator.final_score(
        similarity_score=similarity,
        resume_skills=resume_skills,
        core_skills=jd_core,
        optional_skills=jd_optional,
        skill_depths=skill_depths,
        role="generic",
        inferred_skills=inferred_skills,
        jd_domain=None
    )

    # ---------------- Gap Identification ----------------
    gaps = SkillGapIdentifier.identify_gaps(
        explicit_skills=resume_skills,
        inferred_skills=set(),
        jd_core=jd_core,
        jd_optional=jd_optional
    )

    missing_core = [
        normalize(skill_db, s) for s in gaps["missing_core_skills"]
    ]

    missing_optional = [
        normalize(skill_db, s) for s in gaps["missing_optional_skills"]
    ]

    # ---------------- Roadmap ----------------
    all_missing = set(missing_core + missing_optional)

    skill_categories = {}
    skill_popularity = {}

    for skill in all_missing:
        category = skill_db.get_category(skill) or "other"
        skill_categories[skill] = category
        skill_popularity[skill] = 5 if skill in jd_core else 3

    roadmap = RoadmapGenerator().generate(
        missing_required_skills=missing_core,
        missing_optional_skills=missing_optional,
        skill_categories=skill_categories,
        skill_popularity=skill_popularity
    )

    # ---------------- ✅ FIXED MATCHING ----------------
    matched_skills = sorted(resume_skills.intersection(jd_core.union(jd_optional)))

    # ---------------- Confidence ----------------
    confidence = ConfidenceScorer().compute_confidence(
        similarity_score=similarity,
        matched_skills=matched_skills,
        total_job_skills=len(jd_core | jd_optional)
    )

    explanation = ExplanationGenerator().generate_explanation(
        matched_skills=matched_skills,
        missing_skills=sorted((jd_core | jd_optional) - resume_skills),
        core_missing_skills=missing_core,
        similarity_score=similarity
    )

    return {
        "final_match": round(final_score, 2),
        "confidence": round(confidence, 2),
        "evaluation_mode": "ml_enhanced",
        "signals": signals,
        "matched_skills": matched_skills,
        "missing_skills": missing_core,
        "roadmap": roadmap,
        "explanation": explanation
    }






# src/pipeline/analyze_pipeline.py

# from src.skills.resume_skill_extractor import ResumeSkillExtractor
# from src.skills.jd_skill_extractor import JDSkillExtractor
# from src.skills.skill_database import SkillDatabase

# from src.matching.similarity_calculator import SimilarityCalculator
# from src.matching.score_calculator import ScoreCalculator
# from src.matching.gap_identifier import SkillGapIdentifier

# from src.intelligence.skill_depth_estimator import SkillDepthEstimator
# from src.intelligence.resume_signals import ResumeSignalAnalyzer
# from src.intelligence.resume_archetype_detector import ResumeArchetypeDetector

# from src.explainability.confidence_score import ConfidenceScorer
# from src.explainability.explanation_generator import ExplanationGenerator

# from src.roadmap.roadmap_generator import RoadmapGenerator


# def analyze_resume_jd(resume_text: str, jd_text: str) -> dict:

#     skill_db = SkillDatabase()

#     # ---------------- Resume Processing ----------------
#     extractor = ResumeSkillExtractor()
#     extracted = extractor.extract([], resume_text)

#     explicit_skills = {s for s, m in extracted.items() if m["source"] == "explicit"}
#     inferred_skills = {s for s, m in extracted.items() if m["source"] == "inferred"}

#     resume_skills_raw = explicit_skills | inferred_skills

#     # Normalize resume skills (CRITICAL FIX)
#     resume_skills = {
#         skill_db.normalize_skill(s.strip().lower())
#         for s in resume_skills_raw
#     }

#     # ---- Semantic expansion ----
#     semantic_resume_map = {
#         "mern": {"react", "nodejs", "mongodb", "javascript"},
#     }

#     resume_text_lower = resume_text.lower()

#     for keyword, implied_skills in semantic_resume_map.items():
#         if keyword in resume_text_lower:
#             resume_skills.update({
#                 skill_db.normalize_skill(s)
#                 for s in implied_skills
#             })

#     # ---- Implicit promotion ----
#     implicit_core_map = {
#         "react": {"javascript", "html", "css"},
#         "nodejs": {"javascript"},
#         "node": {"javascript"},
#         "express": {"nodejs", "javascript"},
#     }

#     for skill in list(resume_skills):
#         resume_skills.update({
#             skill_db.normalize_skill(s)
#             for s in implicit_core_map.get(skill, set())
#         })

#     # ---------------- Intelligence Layer ----------------
#     skill_depths = SkillDepthEstimator().estimate(resume_text, resume_skills)
#     signals = ResumeSignalAnalyzer().analyze(resume_text)
#     archetype = ResumeArchetypeDetector.detect(resume_skills)

#     # ---------------- JD Processing ----------------
#     jd_result = JDSkillExtractor().extract_skills(jd_text)

#     jd_core_raw = set(jd_result["core_skills"])
#     jd_optional_raw = set(jd_result["optional_skills"])

#     # Normalize JD skills (CRITICAL FIX)
#     jd_core = {
#         skill_db.normalize_skill(s.strip().lower())
#         for s in jd_core_raw
#     }

#     jd_optional = {
#         skill_db.normalize_skill(s.strip().lower())
#         for s in jd_optional_raw
#     }

#     # ---------------- Matching ----------------
#     similarity = SimilarityCalculator.weighted_similarity_score(
#         resume_vector=None,
#         jd_vector=None,
#         resume_skills=resume_skills,
#         jd_core_skills=jd_core,
#         jd_optional_skills=jd_optional,
#         skill_depths=skill_depths,
#         resume_archetype=archetype
#     )

#     final_score = ScoreCalculator.final_score(
#         similarity_score=similarity,
#         resume_skills=resume_skills,
#         core_skills=jd_core,
#         optional_skills=jd_optional,
#         skill_depths=skill_depths,
#         role="generic",
#         inferred_skills=inferred_skills,
#         jd_domain=None
#     )

#     # ---------------- Gap Identification ----------------
#     gaps = SkillGapIdentifier.identify_gaps(
#         explicit_skills=resume_skills,
#         inferred_skills=set(),  # Already merged & normalized
#         jd_core=jd_core,
#         jd_optional=jd_optional
#     )

#     missing_core = [
#         skill_db.normalize_skill(s) for s in gaps["missing_core_skills"]
#     ]

#     missing_optional = [
#         skill_db.normalize_skill(s) for s in gaps["missing_optional_skills"]
#     ]

#     # ---------------- Roadmap Preparation ----------------
#     all_missing = set(missing_core + missing_optional)

#     skill_categories = {}
#     skill_popularity = {}

#     for skill in all_missing:
#         category = skill_db.get_category(skill) or "other"
#         skill_categories[skill] = category

#         # Core skills get higher importance
#         skill_popularity[skill] = 5 if skill in jd_core else 3

#     roadmap_generator = RoadmapGenerator()

#     roadmap = roadmap_generator.generate(
#         missing_required_skills=missing_core,
#         missing_optional_skills=missing_optional,
#         skill_categories=skill_categories,
#         skill_popularity=skill_popularity
#     )

#     # ---------------- Matched Skills ----------------
#     matched_skills = sorted(resume_skills & (jd_core | jd_optional))

#     # ---------------- Confidence & Explanation ----------------
#     confidence = ConfidenceScorer().compute_confidence(
#         similarity_score=similarity,
#         matched_skills=matched_skills,
#         total_job_skills=len(jd_core | jd_optional)
#     )

#     explanation = ExplanationGenerator().generate_explanation(
#         matched_skills=matched_skills,
#         missing_skills=sorted((jd_core | jd_optional) - resume_skills),
#         core_missing_skills=missing_core,
#         similarity_score=similarity
#     )

#     return {
#         "final_match": round(final_score, 2),
#         "confidence": round(confidence, 2),
#         "evaluation_mode": "ml_enhanced",
#         "signals": signals,
#         "matched_skills": matched_skills,
#         "missing_skills": missing_core,
#         "roadmap": roadmap,
#         "explanation": explanation
#     }