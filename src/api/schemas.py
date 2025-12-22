

from pydantic import BaseModel
from typing import List, Dict


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class AnalyzeResponse(BaseModel):
    match_score: float
    confidence_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    roadmap: Dict
    explanation: str
