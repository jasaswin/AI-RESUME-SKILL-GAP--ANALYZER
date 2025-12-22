

from fastapi import APIRouter
from src.api.schemas import AnalyzeRequest, AnalyzeResponse

# Import ML pipeline components
from src.skills.jd_skill_extractor import JDSkillExtractor
from src.matching.similarity_calculator import SimilarityCalculator
# from src.matching.gap_identifier import GapIdentifier
from src.matching.gap_identifier import SkillGapIdentifier

from src.roadmap.roadmap_generator import RoadmapGenerator
from src.explainability.confidence_score import ConfidenceScorer
from src.explainability.explanation_generator import ExplanationGenerator

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_resume(request: AnalyzeRequest):
    # 1️⃣ Extract JD skills
    jd_extractor = JDSkillExtractor(request.job_description)
    core_skills, optional_skills = jd_extractor.extract()

    # (Resume skills will come from Member-1 pipeline)
    resume_skills = []  # placeholder for now

    # 2️⃣ Similarity
    similarity = SimilarityCalculator()
    match_score = similarity.calculate(resume_skills, core_skills)

    # 3️⃣ Gap detection
    gap_finder = GapIdentifier()
    missing_skills = gap_finder.find(resume_skills, core_skills)

    # 4️⃣ Roadmap generation
    roadmap_gen = RoadmapGenerator()
    roadmap = roadmap_gen.generate(missing_skills)

    # 5️⃣ Confidence scoring
    confidence = ConfidenceScorer().score(
        matched=len(core_skills) - len(missing_skills),
        total=len(core_skills)
    )

    # 6️⃣ Explanation
    explanation = ExplanationGenerator().generate(
        missing_skills=missing_skills,
        match_score=match_score
    )

    return AnalyzeResponse(
        match_score=match_score,
        confidence_score=confidence,
        matched_skills=list(set(core_skills) - set(missing_skills)),
        missing_skills=missing_skills,
        roadmap=roadmap,
        explanation=explanation
    )
