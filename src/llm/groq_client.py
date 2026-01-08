import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:
    """
    LLM enhancer (never a hard dependency)
    """

    def __init__(self, debug=False):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.debug = debug

        self.models = [
            "llama3-70b-8192",
            "llama3-8b-8192"
        ]

    def generate(self, prompt: str) -> str | None:
        if not prompt or len(prompt.strip()) < 20:
            return None

        for model in self.models:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=300
                )

                content = response.choices[0].message.content.strip()

                # 🚨 Hard validation
                if not content or len(content) < 30:
                    raise ValueError("LLM returned weak/empty output")

                return content

            except Exception as e:
                if self.debug:
                    print(f"[Groq failed: {model}] {e}")

        # Fallback
        return None
