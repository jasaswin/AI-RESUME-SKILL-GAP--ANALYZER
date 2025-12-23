import os
from dotenv import load_dotenv
from src.config.settings import USE_LLM, LLM_PROVIDER

load_dotenv()


# ---------- Base Interface ----------
class BaseLLM:
    def generate(self, text: str) -> str:
        raise NotImplementedError


# ---------- Fallback (No LLM) ----------
class RuleBasedLLM(BaseLLM):
    def generate(self, text: str) -> str:
        return text.strip()


# ---------- Groq LLM ----------
class GroqLLM(BaseLLM):
    def __init__(self):
        from groq import Groq
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, text: str) -> str:
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly career mentor. "
                        "Rewrite the response in a conversational, encouraging tone. "
                        "Keep it short and clear."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.4,
            max_tokens=200,
        )

        return completion.choices[0].message.content.strip()


# ---------- Formatter ----------
class LLMFormatter:
    """
    Feature-flagged LLM phrasing layer (SAFE)
    """

    def __init__(self):
        # ALWAYS initialize safely
        self.llm = RuleBasedLLM()

        if not USE_LLM:
            return

        if LLM_PROVIDER == "groq":
            try:
                self.llm = GroqLLM()
            except Exception as e:
                print("[LLM WARNING] Falling back to rule-based:", e)
                self.llm = RuleBasedLLM()
