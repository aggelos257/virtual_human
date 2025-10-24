# -*- coding: utf-8 -*-
import re
import datetime
import webbrowser
from typing import Any

from core.action.action_executor import ActionExecutor


class ReasonerAdvanced:
    """
    Advanced Reasoner της Ζένια: απλά intents + αξιοποίηση WorldModel.
    Χρησιμοποιείται από ReasoningManager.process_input(user_text).
    """

    def __init__(self, online_mode: bool = True):
        self.online_mode = online_mode
        self.executor = ActionExecutor()

    def process(self, user_text: str, world_model: Any) -> str:
        t = (user_text or "").strip().lower()
        if not t:
            return "Δεν σε άκουσα καθαρά. Μπορείς να το επαναλάβεις;"

        # Μικρά κοινωνικά
        if any(x in t for x in ["γεια", "καλημέρα", "καλησπέρα"]):
            world_model.set_state("last_greeting", datetime.datetime.utcnow().isoformat())
            return "Γεια! Πώς μπορώ να βοηθήσω;"

        # Χρόνος/Ημερομηνία
        if "ώρα" in t:
            now = datetime.datetime.now().strftime("%H:%M")
            world_model.set_state("last_time_check", now)
            return f"Η ώρα είναι {now}."
        if "ημερομηνία" in t or "μέρα" in t:
            today = datetime.datetime.now().strftime("%d/%m/%Y")
            world_model.set_state("last_date_check", today)
            return f"Σήμερα είναι {today}."

        # Αναζήτηση
        if any(x in t for x in ["ψάξε", "bρες", "αναζήτησε", "τι είναι", "googl", "google"]):
            query = re.sub(r"(ψάξε|βρες|αναζήτησε|τι είναι|google|googl)", "", t).strip()
            if self.online_mode and query:
                webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
                return f"Ανοίγω αναζήτηση για «{query}»."
            return "Πες μου τι να ψάξω."

        # Άνοιγμα/Κλείσιμο εφαρμογών
        if any(x in t for x in ["άνοιξε", "ξεκίνα", "open", "launch"]):
            app = re.sub(r"(άνοιξε|ξεκίνα|open|launch|το|την|τον)", "", t).strip()
            return self.executor.open_app(app) if app else "Ποια εφαρμογή να ανοίξω;"
        if any(x in t for x in ["κλείσε", "τερμάτισε", "shutdown", "σταμάτα", "σβήσε"]):
            app = re.sub(r"(κλείσε|τερμάτισε|shutdown|σταμάτα|σβήσε|το|την|τον)", "", t).strip()
            return self.executor.close_app(app) if app else "Ποια εφαρμογή να κλείσω;"

        # Μουσική
        if any(x in t for x in ["παίξε", "βάλε", "μουσική", "youtube", "τραγούδι"]):
            song = re.sub(r"(παίξε|βάλε|μουσική|youtube|τραγούδι|στο)", "", t).strip()
            return self.executor.play_music(song)

        # Ταυτότητα
        if any(x in t for x in ["πως σε λένε", "όνομά σου", "ποιο είναι το όνομά σου"]):
            world_model.set_state("assistant_name", "Ζένια")
            return "Με λένε Ζένια — ο ψηφιακός σου άνθρωπος."

        if any(x in t for x in ["πως με λένε", "το όνομά μου", "ποιος είμαι"]):
            e = world_model.get_entity("Angelos")
            if not e:
                world_model.upsert_entity("Angelos", type_="person", attrs_json='{"role":"owner"}')
            return "Σε λένε Άγγελο — είσαι ο δημιουργός μου. 😊"

        return "Το σημείωσα. Πες μου αν θες να το ψάξω ή να εκτελέσω κάτι."
