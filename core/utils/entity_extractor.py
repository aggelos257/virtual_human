# core/entity_extractor.py
import re


class EntityExtractor:
    """
    Εξαγωγέας οντοτήτων για προτάσεις φυσικής γλώσσας.
    Εντοπίζει εφαρμογές, τραγούδια, ενέργειες, ονόματα κ.λπ.
    """

    def __init__(self):
        # Προκαθορισμένες οντότητες για apps, websites και κατηγορίες
        self.known_entities = {
            "apps": [
                "youtube", "spotify", "chrome", "browser", "vlc", "word",
                "excel", "notepad", "explorer", "photoshop", "obs"
            ],
            "actions": [
                "άνοιξε", "κλείσε", "τερμάτισε", "παίξε", "βάλε", "σταμάτα", "γράψε"
            ],
            "media": ["μουσική", "τραγούδι", "ταινία", "βίντεο"]
        }

    def extract(self, text: str):
        text = text.lower().strip()

        entities = {"apps": [], "actions": [], "media": [], "other": []}

        for category, items in self.known_entities.items():
            for item in items:
                if item in text:
                    entities[category].append(item)

        # Αν δεν βρεθεί τίποτα, προσπαθεί να πιάσει τίτλους τραγουδιών
        match = re.search(r"(παίξε|βάλε)\s+(.*)", text)
        if match:
            entities["media"].append(match.group(2).strip())

        return entities

    def extract_main(self, text: str):
        """Επιστρέφει την πιο πιθανή κύρια οντότητα."""
        ents = self.extract(text)
        for key in ["apps", "media", "actions"]:
            if ents[key]:
                return ents[key][0]
        return None
