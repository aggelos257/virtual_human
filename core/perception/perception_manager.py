# -*- coding: utf-8 -*-
import threading
import time
from typing import Optional, Dict, Any

from core.perception.vision.vision_manager import VisionManager
from core.perception.audio.audio_manager import AudioManager
from core.perception.system.system_monitor import SystemMonitor
from core.memory.memory_manager import MemoryManager


class PerceptionManager:
    """
    Ενιαίος ενορχηστρωτής Αντίληψης.
    - Εκκινεί/σταματά Vision, Audio, System awareness
    - Συγχρονίζει τα σήματα σε ενιαίο state
    - Καταγράφει σημαντικά ευρήματα στη μνήμη
    """

    def __init__(self,
                 enable_vision: bool = True,
                 enable_audio: bool = True,
                 enable_system: bool = True,
                 camera_index: int = 0):
        self.enable_vision = enable_vision
        self.enable_audio = enable_audio
        self.enable_system = enable_system
        self.camera_index = camera_index

        self.memory = MemoryManager()

        self.vision: Optional[VisionManager] = None
        self.audio: Optional[AudioManager] = None
        self.system: Optional[SystemMonitor] = None

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._state_lock = threading.Lock()
        self._state: Dict[str, Any] = {
            "face": None,          # {"name": "Angelos", "emotion": "neutral", "confidence": 0.87}
            "objects": [],         # [{"label": "cup", "conf": 0.71}, ...]
            "gestures": [],        # ["thumbs_up", ...]
            "audio": None,         # {"scene": "silence|music|speech|noise", "level_db": float}
            "system": None         # {"fg_window": "chrome.exe", "cpu": 14.2, "ram": 57.3}
        }

    # ---------------- Lifecycle ----------------
    def start(self):
        if self._running:
            return
        self._running = True

        if self.enable_vision:
            self.vision = VisionManager(camera_index=self.camera_index)
            self.vision.start()

        if self.enable_audio:
            self.audio = AudioManager()
            self.audio.start()

        if self.enable_system:
            self.system = SystemMonitor()
            self.system.start()

        self._thread = threading.Thread(target=self._loop, name="PerceptionLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self.vision:
            self.vision.stop()
        if self.audio:
            self.audio.stop()
        if self.system:
            self.system.stop()
        try:
            self.memory.shutdown()
        except Exception:
            pass

    # ---------------- Internal Loop ----------------
    def _loop(self):
        """
        Συγχωνεύει περιοδικά τα σήματα αισθητήρων σε ένα κοινό state και καταγράφει σημαντικά συμβάντα.
        """
        while self._running:
            try:
                aggregated = {}

                if self.vision:
                    v = self.vision.get_state()
                    aggregated["face"] = v.get("face")
                    aggregated["objects"] = v.get("objects", [])
                    aggregated["gestures"] = v.get("gestures", [])

                    # Καταγραφή σημαντικών ευρημάτων
                    if v.get("face") and v["face"].get("name"):
                        self.memory.store_event(
                            event_type="vision_face",
                            content=f"Detected face: {v['face']}",
                            emotion="neutral",
                            importance=0.6
                        )
                    if v.get("objects"):
                        self.memory.store_event(
                            event_type="vision_objects",
                            content=str(v["objects"][:3]),
                            emotion="neutral",
                            importance=0.4
                        )

                if self.audio:
                    a = self.audio.get_state()
                    aggregated["audio"] = a
                    if a and a.get("scene") in ("music", "speech"):
                        self.memory.store_event(
                            event_type="audio_scene",
                            content=f"Audio scene: {a}",
                            emotion="neutral",
                            importance=0.3
                        )

                if self.system:
                    s = self.system.get_state()
                    aggregated["system"] = s

                with self._state_lock:
                    self._state.update(aggregated)

            except Exception:
                # Δεν ρίχνουμε το loop — συνεχίζουμε ανθεκτικά
                pass

            time.sleep(0.33)  # ~3 Hz update rate

    # ---------------- Public API ----------------
    def get_state(self) -> Dict[str, Any]:
        with self._state_lock:
            return dict(self._state)
