# voice/zenia_brain.py
from core.utils.intent_classifier import IntentClassifier
from core.context_memory import ContextMemory


class ZeniaBrain:
    """Κεντρικός εγκέφαλος: κατανόηση, λογική, μνήμη, απάντηση."""

    def __init__(self):
        self.classifier = IntentClassifier()
        self.memory = ContextMemory()

    def process_input(self, text: str):
        if not text:
            return "Δεν σε άκουσα καλά."

        try:
            result = self.classifier.classify(text)

            if isinstance(result, dict):
                response = result.get("response", "")
                self.memory.remember(result.get("name", "unknown"), text, response)
                return response or "Κατάλαβα."

            return str(result)

        except Exception as e:
            return f"⚠️ Σφάλμα στον εγκέφαλο: {e}"
