# virtual_human/core/openai_engine.py
from openai import OpenAI


class OpenAIEngine:
    """Ενότητα χειρισμού απαντήσεων AI"""

    def __init__(self):
        self.client = None
        self.model = "gpt-4o-mini"  # fallback

    def generate_response(self, user_prompt: str):
        if not user_prompt:
            return "Δεν έλαβα είσοδο για απάντηση."

        try:
            t = str(user_prompt).lower()
        except Exception:
            t = ""

        if "ζένια" in t:
            return "Ναι, είμαι εδώ! Σε ακούω."
        elif "πώς είσαι" in t:
            return "Είμαι καλά, ευχαριστώ που ρωτάς!"
        else:
            return "Δεν είμαι σίγουρη για αυτό, αλλά μπορώ να το ψάξω."

    # --- ΝΕΑ μέθοδος συμβατότητας ---
    def chat(self, message: str):
        """Συμβατότητα με παλαιότερες κλήσεις"""
        return self.generate_response(message)
