import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self):
        self.enabled = os.getenv("USE_LLM", "false").lower() == "true"
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, prompt: str) -> str:
        if not self.enabled:
            return prompt  # fallback (important for safety)

        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a career guidance assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()
