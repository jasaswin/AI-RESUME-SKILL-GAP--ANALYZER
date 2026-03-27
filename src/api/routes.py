


from fastapi import APIRouter, UploadFile, File, Form
from src.pipeline.analyze_pipeline import analyze_resume_jd
from src.utils.pdf_reader import extract_text_from_pdf
from pydantic import BaseModel
from src.chatbot.chatbot_engine import ChatbotEngine

router = APIRouter()


@router.post("/analyze/")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Accepts:
    - Resume PDF file
    - JD as text

    Returns:
    - AI analysis result
    """

    # Validate file type
    if not resume_file.filename.endswith(".pdf"):
        return {"error": "Resume must be a PDF file."}

    # Extract resume text
    resume_text = extract_text_from_pdf(resume_file.file)

    # Run pipeline
    result = analyze_resume_jd(
        resume_text=resume_text,
        jd_text=job_description
    )

    return result


# ✅ Request model
class ChatRequest(BaseModel):
    question: str
    analysis: dict


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        engine = ChatbotEngine(request.analysis)
        response = engine.ask(request.question)

        return {
            "answer": response
        }

    except Exception as e:
        return {"error": str(e)}