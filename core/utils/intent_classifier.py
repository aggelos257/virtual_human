# core/intent_classifier.py
import yaml
from pathlib import Path
from core.cognitive_intent_learner import CognitiveIntentLearner
from core.reasoning.reasoner import Reasoner


class IntentClassifier:
    """Αναγνωρίζει ή μαθαίνει προθέσεις του χρήστη (intents)."""

    def __init__(self, yaml_path="core/intents.yaml"):
        self.yaml_path = Path(yaml_path)
        self.reasoner = Reasoner()
        self.intents = self._load_yaml()
        print(f"✅ [IntentClassifier] Φορτώθηκαν {len(self.intents)} προθέσεις από YAML.")

    def _load_yaml(self):
        if not self.yaml_path.exists():
            return {}
        with open(self.yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}

    def _save_yaml(self):
        with open(self.yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(self.intents, f, allow_unicode=True)

    # -----------------------------------------------------------
    def classify(self, text: str):
        """Αναγνωρίζει ή μαθαίνει και εκτελεί αυτόματα το intent."""
        t = text.lower().strip()

        # === 1️⃣ Έλεγχος γνωστής πρόθεσης ===
        for intent, data in self.intents.items():
            examples = data.get("examples", []) if isinstance(data, dict) else []
            for ex in examples:
                if ex in t:
                    reasoned_response = self.reasoner.reason(t)
                    return {
                        "name": intent,
                        "response": reasoned_response,
                        "confidence": 0.95,
                    }

        # === 2️⃣ Αν δεν υπάρχει, προσπάθησε να τη μάθεις ===
        learner = CognitiveIntentLearner(self.yaml_path)
        new_intent, message = learner.analyze_and_learn(t)
        if new_intent:
            print(f"🧩 [AutoLearn] {message}")
            reasoned_response = self.reasoner.reason(t)
            return {
                "name": new_intent,
                "response": reasoned_response,
                "confidence": 0.9,
            }

        # === 3️⃣ Fallback στη Reasoner ===
        try:
            reasoned_response = self.reasoner.reason(t)
            return {
                "name": "reasoned_action",
                "response": reasoned_response,
                "confidence": 0.8,
            }
        except Exception as e:
            return {
                "name": "unknown",
                "response": f"⚠️ Σφάλμα Reasoner: {e}",
                "confidence": 0.1,
            }
