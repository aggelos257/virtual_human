# core/adaptive_learner.py
import json
import difflib
from pathlib import Path

class AdaptiveLearner:
    """
    Μαθαίνει αυτόματα συνδέσεις μεταξύ λέξεων, ενεργειών και αποτελεσμάτων.
    Βασική offline “λογική μάθηση” χωρίς μοντέλο.
    """

    def __init__(self, memory_file="core/learning_memory.json"):
        self.memory_path = Path(memory_file)
        self.memory = self._load_memory()

    # -----------------------------------------------------------
    def _load_memory(self):
        if self.memory_path.exists():
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_memory(self):
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    # -----------------------------------------------------------
    def learn(self, text, intent, result):
        """Ενημερώνει τη γνώση βάσει εμπειρίας."""
        t = text.lower().strip()
        intent = intent or "unknown"

        if intent not in self.memory:
            self.memory[intent] = {"examples": [], "success": 0, "fails": 0}

        self.memory[intent]["examples"].append(t)
        self.memory[intent]["success"] += 1 if "άνοιξα" in result or "έπαιξα" in result else 0
        self.memory[intent]["fails"] += 1 if "δεν" in result or "σφάλμα" in result else 0

        self._save_memory()

    # -----------------------------------------------------------
    def suggest_intent(self, text):
        """Προσπαθεί να μαντέψει την πρόθεση από παλιές εμπειρίες."""
        t = text.lower().strip()
        best_intent = None
        best_score = 0
        for intent, data in self.memory.items():
            for example in data.get("examples", []):
                score = difflib.SequenceMatcher(None, example, t).ratio()
                if score > best_score:
                    best_intent = intent
                    best_score = score
        if best_score > 0.6:
            return best_intent, best_score
        return None, 0
