# core/ai_engine.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("MODEL_NAME", "gpt-4o-mini")

    def ask(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Zenia, a helpful virtual human assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Σφάλμα AI: {e}"
