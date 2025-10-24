# core/cognitive_intent_learner.py
import re
import yaml
from pathlib import Path


class CognitiveIntentLearner:
    """
    Αυτόματο υποσύστημα μάθησης προθέσεων.
    Όταν ο classifier δεν βρίσκει intent, προσπαθεί να αναλύσει φυσικά τη φράση
    και να δημιουργήσει ένα νέο intent δυναμικά.
    """

    def __init__(self, yaml_path="core/intents.yaml"):
        self.yaml_path = Path(yaml_path)
        self.intents = self._load_yaml()

    def _load_yaml(self):
        if not self.yaml_path.exists():
            return {}
        with open(self.yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _save_yaml(self):
        with open(self.yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(self.intents, f, allow_unicode=True)

    def analyze_and_learn(self, text: str):
        """Αναλύει φράση και δημιουργεί νέο intent με βάση τη δομή της."""
        text = text.lower().strip()

        # 1️⃣ Βρες πιθανό ρήμα (δράση)
        verbs = ["άνοιξε", "κλείσε", "παίξε", "βάλε", "τρέξε", "σταμάτα", "γράψε", "δείξε", "ψάξε"]
        verb = next((v for v in verbs if v in text), None)

        # 2️⃣ Βρες το αντικείμενο
        noun = re.sub("|".join(verbs), "", text).strip()
        noun = noun.replace("το", "").replace("την", "").replace("ένα", "").strip()

        if not verb or not noun:
            return None, "Δεν κατάλαβα τη φράση για να τη μάθω."

        # 3️⃣ Δημιούργησε νέο intent name
        intent_name = f"{verb}_{noun.replace(' ', '_')}"
        if intent_name in self.intents:
            return intent_name, "Το ήξερα ήδη αυτό."

        # 4️⃣ Πρόσθεσε το στο YAML
        self.intents[intent_name] = {"examples": [text]}
        self._save_yaml()

        return intent_name, f"Το έμαθα! Από εδώ και πέρα η φράση «{text}» σημαίνει {intent_name}."
