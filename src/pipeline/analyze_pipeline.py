# src/pipeline/analyze_pipeline.py

from src.skills.resume_skill_extractor import ResumeSkillExtractor
from src.skills.jd_skill_extractor import JDSkillExtractor

from src.matching.similarity_calculator import SimilarityCalculator
from src.matching.score_calculator import ScoreCalculator
from src.matching.gap_identifier import SkillGapIdentifier

from src.intelligence.skill_depth_estimator import SkillDepthEstimator
from src.intelligence.resume_signals import ResumeSignalAnalyzer
from src.intelligence.resume_archetype_detector import ResumeArchetypeDetector
from src.intelligence.resume_quality_scorer import ResumeQualityScorer
from src.intelligence.career_readiness import CareerReadinessAnalyzer

from src.explainability.confidence_score import ConfidenceScorer
from src.explainability.explanation_generator import ExplanationGenerator

from src.roadmap.roadmap_generator import RoadmapGenerator


def analyze_resume_jd(resume_text: str, jd_text: str) -> dict:
    # ---------------- Resume processing ----------------
    extractor = ResumeSkillExtractor()
    extracted = extractor.extract([], resume_text)

    explicit_skills = {s for s, m in extracted.items() if m["source"] == "explicit"}
    inferred_skills = {s for s, m in extracted.items() if m["source"] == "inferred"}
    resume_skills = explicit_skills | inferred_skills

    # ---- CONTROLLED SEMANTIC EXPANSION (API SAFE) ----
    semantic_resume_map = {
    "mern": {"react", "nodejs", "mongodb", "javascript"},
}

    resume_text_lower = resume_text.lower()

    for keyword, implied_skills in semantic_resume_map.items():
       if keyword in resume_text_lower:
        for skill in implied_skills:
            resume_skills.add(skill)


    # ---- IMPLICIT CORE SKILL PROMOTION (CRITICAL FIX) ----
    implicit_core_map = {
    "react": {"javascript", "html", "css"},
    "nodejs": {"javascript"},
    "node": {"javascript"},
    "express": {"nodejs", "javascript"},
}

    for skill in list(resume_skills):
        for implied in implicit_core_map.get(skill, set()):
            resume_skills.add(implied)

    skill_depths = SkillDepthEstimator().estimate(resume_text, resume_skills)
    signals = ResumeSignalAnalyzer().analyze(resume_text)
    archetype = ResumeArchetypeDetector.detect(resume_skills)

    # ---------------- JD processing ----------------
    jd_result = JDSkillExtractor().extract_skills(jd_text)
    jd_core = set(jd_result["core_skills"])
    jd_optional = set(jd_result["optional_skills"])

    # ---------------- Matching ----------------
    similarity = SimilarityCalculator.weighted_similarity_score(
        resume_vector=None,  # TF-IDF optional in API
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

    # ---------------- Gaps & roadmap ----------------
    gaps = SkillGapIdentifier.identify_gaps(
        explicit_skills=explicit_skills,
        inferred_skills=inferred_skills,
        jd_core=jd_core,
        jd_optional=jd_optional
    )

    roadmap = RoadmapGenerator().generate_phase_roadmap({
        "high_priority": gaps["missing_core_skills"][:1],
        "medium_priority": gaps["missing_optional_skills"][:1],
        "low_priority": []
    })

    # ---------------- Explanation & confidence ----------------
    confidence = ConfidenceScorer().compute_confidence(
        similarity_score=similarity,
        matched_skills=list(resume_skills & jd_core),
        total_job_skills=len(jd_core | jd_optional)
    )

    explanation = ExplanationGenerator().generate_explanation(
        matched_skills=sorted(resume_skills & (jd_core | jd_optional)),
        missing_skills=sorted((jd_core | jd_optional) - resume_skills),
        core_missing_skills=gaps["missing_core_skills"],
        similarity_score=similarity
    )

    return {
        "final_match": round(final_score, 2),
        "confidence": round(confidence, 2),
        "evaluation_mode": "conservative_api",
        "signals": signals,
        "matched_skills": sorted(resume_skills & jd_core),
        "missing_skills": gaps["missing_core_skills"],
        "roadmap": roadmap,
        "explanation": explanation
    }
