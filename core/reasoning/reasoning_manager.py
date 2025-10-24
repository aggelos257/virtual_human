# -*- coding: utf-8 -*-
"""
core/reasoning/reasoning_manager.py
-----------------------------------
Διαχειριστής Λογικής της Ζένια.
Συντονίζει: Reasoner, Memory, Learning, Emotion, Actions, WorldModel.
Είναι πλήρως συμβατός με το start_zenia.py που περνάει device.
"""

import re
import webbrowser
import datetime
import threading

from core.action.action_executor import ActionExecutor
from core.memory.memory_manager import MemoryManager
from core.learning.adaptive_learner import AdaptiveLearner
from core.emotion.emotion_engine import EmotionEngine
from core.reasoning.world_model import WorldModel
from .reasoner import Reasoner


class ReasoningManager:
    def __init__(self, device=None):
        self.device = device
        print(f"🧠 [ReasoningManager] Ενεργοποιήθηκε με συσκευή: {self.device.type if self.device else 'cpu'}")

        # Υποσυστήματα
        self.reasoner = Reasoner(device=self.device)
        self.memory = MemoryManager()
        self.learner = AdaptiveLearner()
        self.emotion_engine = EmotionEngine()
        self.executor = ActionExecutor()
        self.world_model = WorldModel()

        # Κατάσταση λειτουργίας
        self._is_running = False
        self._loop_thread = None

        print("✅ [ReasoningManager] Υποσυστήματα φόρτωσαν επιτυχώς.")

    # ------------------------------------------------------------
    # 🧠 Εκκίνηση reasoning loop (ώστε να είναι συμβατό με start_zenia.py)
    # ------------------------------------------------------------
    def start(self):
        """Εκκινεί το reasoning loop (προαιρετικά background λογική)."""
        if not self._is_running:
            self._is_running = True
            self._loop_thread = threading.Thread(target=self._loop, daemon=True)
            self._loop_thread.start()
            print("🧠 [ReasoningManager] Το reasoning ξεκίνησε.")

    def _loop(self):
        """Background loop αν χρειαστεί μελλοντική συνεχή λογική."""
        while self._is_running:
            # Εδώ μπορεί να μπει μελλοντικά monitoring, world updates κ.λπ.
            # Προς το παρόν δεν κάνει κάτι.
            import time
            time.sleep(0.1)

    # ------------------------------------------------------------
    # 🛑 Τερματισμός reasoning
    # ------------------------------------------------------------
    def shutdown(self):
        self._is_running = False
        if self._loop_thread and self._loop_thread.is_alive():
            self._loop_thread.join(timeout=1.0)
        print("🧠 [ReasoningManager] Το reasoning τερματίστηκε.")

    def is_running(self):
        return self._is_running

    # ------------------------------------------------------------
    # 🔍 Κύρια διεπαφή επεξεργασίας
    # ------------------------------------------------------------
    def process(self, text: str) -> str:
        if not text or not text.strip():
            return "⚠️ Δεν δόθηκε είσοδος προς ανάλυση."

        # 1) Intent + ανάλυση
        intent = self.reasoner.predict_intent(text)
        analysis = self.reasoner.analyze(text)

        # 2) Συναίσθημα
        prefix, emotion, intensity = self.emotion_engine.process_input(text)

        # 3) Ενέργειες
        action_result = self._handle_action(text, intent)
        if action_result:
            self.memory.store_event(
                event_type="action_result",
                content=f"{text} -> {action_result}",
                emotion=emotion,
                importance=0.7
            )
            self.world_model.set_state("last_action", action_result)
            return f"{prefix}{action_result}"

        # 4) Μάθηση
        try:
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
            name = re.sub(r"(άνοιξε|open|το|την|τον|app|πρόγραμμα)", "", t).strip()
            return self.executor.open_app(name)

        if intent == "close_app":
            name = re.sub(r"(κλείσε|close|το|την|τον|app|πρόγραμμα)", "", t).strip()
            return self.executor.close_app(name)

        # Μουσική
        if intent == "play_music":
            query = re.sub(r"(παίξε|βάλε|μουσική|τραγούδι|στο|youtube)", "", t).strip()
            return self.executor.play_music(query)

        # Ώρα / Ημερομηνία
        if intent == "query_time":
            return f"🕓 Η ώρα είναι {datetime.datetime.now().strftime('%H:%M')}."
        if intent == "query_date":
            return f"📅 Η ημερομηνία είναι {datetime.datetime.now().strftime('%d/%m/%Y')}."

        return None
