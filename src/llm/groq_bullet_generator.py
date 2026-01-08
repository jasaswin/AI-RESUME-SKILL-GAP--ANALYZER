from src.llm.groq_client import GroqClient

class GroqBulletGenerator:
    def __init__(self, enabled=True, debug=False):
        self.enabled = enabled
        self.client = GroqClient(debug=debug)   # ✅ FIX

        # existing init code…

    def generate(
        self,
        skill: str,
        level: str,
        role: str,
        section: str | None = None   # 👈 MAKE OPTIONAL
    ) -> str | None:
        
        if not self.client:
            return None

        if not self.enabled:
            return None

        section_hint = section or "Resume"

        prompt = f"""
Generate a concise, realistic resume bullet for an {role.replace('_', ' ')} role.

Skill: {skill}
Proficiency: {level}
Context: {section_hint}

Rules:
- Do NOT invent experience
- Keep it resume-safe
- 1 bullet only
"""

        return self.client.generate(prompt)
