from fastapi import APIRouter
from src.api.schemas import AnalyzeRequest, AnalyzeResponse
from src.pipeline.analyze_pipeline import analyze_resume_jd

router = APIRouter(prefix="/analyze", tags=["Resume Analysis"])

@router.post("/", response_model=AnalyzeResponse)
def analyze_resume(request: AnalyzeRequest):
    result = analyze_resume_jd(
        resume_text=request.resume_text,
        jd_text=request.job_description
    )

    return AnalyzeResponse(**result)
