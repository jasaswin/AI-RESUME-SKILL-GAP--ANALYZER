import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:
    def __init__(self, debug=False):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.debug = debug

        # Priority list — auto fallback
        self.models = [
    "llama3-8b-8192",
    "llama3-70b-8192"
        ]

        

    def generate(self, prompt: str) -> str | None:
        for model in self.models:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                    max_tokens=200
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                if self.debug:
                 print(f"[Groq model failed: {model}] {e}")


        # All models failed → fallback triggered
        return None
