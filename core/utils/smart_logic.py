# core/smart_logic.py
import re
from core.action_executor import ActionExecutor


class SmartLogic:
    """Ενδιάμεση λογική της Ζένιας: κατανοεί φυσική γλώσσα και αποφασίζει ενέργειες."""

    def __init__(self):
        self.executor = ActionExecutor()
        self.last_action = None

    def interpret(self, text: str):
        text = text.lower().strip()

        # === 1️⃣ Γενικές λογικές κατηγορίες ===
        if any(w in text for w in ["άνοιξε", "ξεκίνα", "εκκίνησε"]):
            app = self._extract_app_name(text)
            if not app:
                if "μουσική" in text or "τραγούδι" in text:
                    return self.executor.play_music("")
                if "browser" in text or "διαδίκτυο" in text:
                    return self.executor.open_app("browser")
                return "Τι θέλεις να ανοίξω;"

            self.last_action = ("open", app)
            return self.executor.open_app(app)

        elif any(w in text for w in ["κλείσε", "τερμάτισε", "σταμάτα"]):
            if "όλα" in text or "ό,τι άνοιξες" in text:
                if self.last_action:
                    kind, app = self.last_action
                    if kind == "open":
                        return self.executor.close_app(app)
                return "Δεν θυμάμαι να έχω κάτι ανοιχτό."
            elif "μουσική" in text or "youtube" in text:
                return self.executor.close_youtube()

            app = self._extract_app_name(text)
            if app:
                return self.executor.close_app(app)
            return "Δεν κατάλαβα τι να κλείσω."

        elif any(w in text for w in ["παίξε", "βάλε"]):
            query = self._extract_music_query(text)
            self.last_action = ("music", query)
            return self.executor.play_music(query)

        elif any(w in text for w in ["σταμάτησε", "παύση", "παύσε"]):
            return self.executor.close_youtube()

        elif any(w in text for w in ["γράψε", "ντοκουμέντο", "κείμενο"]):
            self.last_action = ("open", "word")
            return self.executor.open_app("word")

        elif "υπολογιστή" in text and any(w in text for w in ["κλείσε", "τερμάτισε", "σβήσε"]):
            return self.executor.shutdown()

        # === 2️⃣ Αν δεν ξέρει, απαντά φυσικά ===
        return "Δεν είμαι σίγουρη, αλλά μπορώ να το ψάξω."

    # === Εξαγωγή ονόματος εφαρμογής ===
    def _extract_app_name(self, text: str):
        apps = [
            "youtube", "browser", "chrome", "spotify", "vlc",
            "word", "excel", "notepad", "explorer", "photoshop", "obs"
        ]
        for app in apps:
            if app in text:
                return app
        return None

    # === Εξαγωγή τίτλου τραγουδιού ===
    def _extract_music_query(self, text: str):
        match = re.search(r"(παίξε|βάλε)\s+(.*)", text)
        if match:
            return match.group(2).strip()
        return ""
