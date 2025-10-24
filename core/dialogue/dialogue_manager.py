# core/dialogue_manager.py
from core.utils.zenia_brain import ZeniaBrain
from core.utils.entity_extractor import EntityExtractor


class DialogueManager:
    """
    Διαχειριστής διαλόγου μεταξύ του χρήστη και της Ζένιας.
    Συντονίζει κατανόηση, φυσική λογική και απάντηση.
    """

    def __init__(self):
        self.brain = ZeniaBrain()          # Χρησιμοποιεί IntentClassifier + SmartLogic + ActionExecutor
        self.extractor = EntityExtractor()  # Για εξαγωγή οντοτήτων (apps, media, actions)
        self.last_intent = None
        self.last_entity = None

    def process_user_input(self, text: str) -> str:
        """Παίρνει κείμενο από STT και επιστρέφει τελική απάντηση (μία φορά)."""
        if not text or not isinstance(text, str):
            return "Δεν σε άκουσα καλά. Μπορείς να επαναλάβεις;"

        # 1) Αναλύουμε οντότητες για πιθανό αυτόματο συμπλήρωμα
        entities = self.extractor.extract(text)

        # 2) Ζητάμε από τον εγκέφαλο την απάντηση (εδώ γίνεται όλη η λογική/εκτέλεση actions)
        response = self.brain.process_input(text)

        # 3) Ενημέρωση απλού context
        self.last_entity = self.extractor.extract_main(text)
        self.last_intent = response

        # 4) Αν ο εγκέφαλος ζητά διευκρίνιση (“Τι θέλεις να ανοίξω;”)
        #    και έχουμε βρει app entity, δοκίμασε αυτόματα
        if "Τι θέλεις να ανοίξω" in response and entities["apps"]:
            app = entities["apps"][0]
            response = self.brain.process_input(f"άνοιξε {app}")

        return response

    def terminate(self):
        """Κλείσιμο συνεδρίας (αν χρειάζεται στο μέλλον)."""
        # εδώ μπορούμε να τερματίσουμε πόρους/μνήμη κτλ
        pass
