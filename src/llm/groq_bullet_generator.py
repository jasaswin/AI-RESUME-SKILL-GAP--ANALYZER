# src/llm/groq_bullet_generator.py
from src.llm.groq_client import GroqClient

class GroqBulletGenerator:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.client = GroqClient() if enabled else None

    def generate(self, skill, level, role, section):
        if not self.enabled:
            return None  # fallback will handle

        prompt = f"""
Generate ONE professional resume bullet.

Skill: {skill}
Experience level: {level}
Target role: {role}
Resume section: {section}

Rules:
- ATS friendly
- No exaggeration
- No learning/coursework wording
- Concise, impact-focused
Return only the bullet point.
"""

        return self.client.generate(prompt)
