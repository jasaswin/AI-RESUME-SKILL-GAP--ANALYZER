# src/api/schemas.py

from pydantic import BaseModel
from typing import List, Dict, Any


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class AnalyzeResponse(BaseModel):
    final_match: float
    confidence: float
    evaluation_mode: str
    signals: Dict[str, bool]
    matched_skills: List[str]
    missing_skills: List[str]
    roadmap: Dict[str, Any]
    explanation: Dict[str, Any]

