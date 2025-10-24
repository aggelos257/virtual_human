import re
import webbrowser
import datetime

from core.action.action_executor import ActionExecutor
from core.memory.memory_manager import MemoryManager
from core.learning.adaptive_learner import AdaptiveLearner
from core.emotion.emotion_engine import EmotionEngine
from core.reasoning.world_model import WorldModel
from .reasoner import Reasoner


class ReasoningManager:
    """
    Διαχειριστής Λογικής της Ζένια.
    Συντονίζει: Reasoner, Memory, Learning, Emotion, Actions, WorldModel.
    Είναι πλήρως συμβατός με το start_zenia.py που περνάει device.
    """

    def __init__(self, device=None):
        self.device = device
        print(f"🧠 [ReasoningManager] Ενεργοποιήθηκε με συσκευή: {self.device.type if self.device else 'cpu'}")

        # Υποσυστήματα (όλα υπάρχουν στο project dump σου)
        self.reasoner = Reasoner(device=self.device)
        self.memory = MemoryManager()
        self.learner = AdaptiveLearner()
        self.emotion_engine = EmotionEngine()
        self.executor = ActionExecutor()
        self.world_model = WorldModel()

        print("✅ [ReasoningManager] Υποσυστήματα φόρτωσαν επιτυχώς.")

    # ------------------------------------------------------------
    # 🔍 Κύρια διεπαφή επεξεργασίας
    # ------------------------------------------------------------
    def process(self, text: str) -> str:
        if not text or not text.strip():
            return "⚠️ Δεν δόθηκε είσοδος προς ανάλυση."

        # 1) Intent + ανάλυση
        intent = self.reasoner.predict_intent(text)
        analysis = self.reasoner.analyze(text)

        # 2) Συναίσθημα (υφιστάμενο API: process_input -> (prefix, emotion, intensity))
        prefix, emotion, intensity = self.emotion_engine.process_input(text)

        # 3) Ενέργειες (δράσεις) βάσει intent
        action_result = self._handle_action(text, intent)
        if action_result:
            # 4) Καταγραφή στη μνήμη (υφιστάμενο API: store_event)
            self.memory.store_event(
                event_type="action_result",
                content=f"{text} -> {action_result}",
                emotion=emotion,
                importance=0.7
            )
            # 5) World state ενημέρωση (υφιστάμενο API: set_state)
            self.world_model.set_state("last_action", action_result)
            return f"{prefix}{action_result}"

        # 4) Μάθηση (υφιστάμενο API: learn_from ή παρόμοιο – σε dump υπάρχει learn_from;)
        # Σε αρκετές εκδόσεις υπάρχει learn_from· αν όχι, δεν θα σκάσει το σύστημα αν καλέσουμε απλή μέθοδο learn().
        try:
            # Προτιμάμε learn_from(text) αν υπάρχει:
            if hasattr(self.learner, "learn_from"):
                self.learner.learn_from(text)
            else:
                self.learner.learn()
        except Exception:
            pass

        # 5) Καταγραφή στη μνήμη
        self.memory.store_event(
            event_type="user_input",
            content=text,
            emotion=emotion,
            importance=float(intensity) if isinstance(intensity, (int, float)) else 0.5
        )

        # 6) World state
        try:
            self.world_model.set_state("last_input", text)
            self.world_model.set_state("last_intent", intent)
        except Exception:
            pass

        # 7) Τελική απάντηση
        return f"{prefix}{analysis} | Συναισθηματική κατάσταση: {emotion}"

    # ------------------------------------------------------------
    # ⚙️ Χειρισμός ενεργειών
    # ------------------------------------------------------------
    def _handle_action(self, text: str, intent: str):
        t = (text or "").lower()

        # Άνοιγμα URL
        if intent == "open_url":
            m = re.search(r"(https?://[^\s]+|www\.[^\s]+)", text)
            if m:
                url = m.group(0)
                if not url.startswith("http"):
                    url = "https://" + url
                webbrowser.open(url)
                return f"🌐 Άνοιξα την ιστοσελίδα: {url}"

        # Εφαρμογές
        if intent == "open_app":
            # επιχειρούμε να αφαιρέσουμε λέξεις-σύνδεσμους
            name = re.sub(r"(άνοιξε|open|το|την|τον|app|πρόγραμμα)", "", t).strip()
            return self.executor.open_app(name)

        if intent == "close_app":
            name = re.sub(r"(κλείσε|close|το|την|τον|app|πρόγραμμα)", "", t).strip()
            return self.executor.close_app(name)

        # Μουσική
        if intent == "play_music":
            # αφαιρούμε triggers για καθαρό query
            query = re.sub(r"(παίξε|βάλε|μουσική|τραγούδι|στο|youtube)", "", t).strip()
            return self.executor.play_music(query)

        # Ώρα / Ημερομηνία
        if intent == "query_time":
            return f"🕓 Η ώρα είναι {datetime.datetime.now().strftime('%H:%M')}."
        if intent == "query_date":
            return f"📅 Η ημερομηνία είναι {datetime.datetime.now().strftime('%d/%m/%Y')}."

        # Καμία αναγνωρίσιμη ενέργεια
        return None
