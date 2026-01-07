# src/llm/groq_resume_rewriter.py
from src.llm.groq_client import GroqClient

class GroqResumeRewriter:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.client = GroqClient() if enabled else None

    def rewrite(self, resume_text, skills_add, projects_add):
        if not self.enabled:
            return None

        prompt = f"""
Rewrite the resume below.

Rules:
- Do NOT remove existing content
- Insert bullets into correct sections
- Maintain professional ATS tone
- Do not add new skills

Resume:
{resume_text}

Skills Section Additions:
{skills_add}

Projects Section Additions:
{projects_add}
"""

        return self.client.generate(prompt)
