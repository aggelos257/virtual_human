# -*- coding: utf-8 -*-
import threading
import time
from typing import Optional, Dict, Any

try:
    import sounddevice as sd
    import numpy as np
except Exception:
    sd = None
    np = None


class AudioManager:
    """
    Ελαφριά ανάλυση ηχητικού περιβάλλοντος (RMS level + απλή κατηγοριοποίηση).
    Αν δεν υπάρχουν βιβλιοθήκες/μικρόφωνο, επιστρέφει None state.
    """

    def __init__(self, sample_rate: int = 16000, block_size: int = 1024):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._state: Optional[Dict[str, Any]] = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, name="AudioLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        if sd is None or np is None:
            # Χωρίς βιβλιοθήκες, δεν κάνουμε capture
            while self._running:
                time.sleep(0.5)
            return

        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, blocksize=self.block_size, dtype="float32") as stream:
                while self._running:
                    data, _ = stream.read(self.block_size)
                    if data is None:
                        time.sleep(0.1)
                        continue
                    # RMS level
                    rms = float(np.sqrt(np.mean(np.square(data))))
                    level_db = 20.0 * np.log10(max(rms, 1e-7))

                    # Πολύ απλή κατηγοριοποίηση περιβάλλοντος
                    if level_db < -45:
                        scene = "silence"
                    elif level_db < -25:
                        scene = "quiet"
                    elif level_db < -10:
                        scene = "speech"
                    else:
                        scene = "loud"

                    self._state = {"scene": scene, "level_db": float(level_db)}
        except Exception:
            # Αν κάτι πάει στραβά, μένουμε σιωπηλοί αλλά δεν ρίχνουμε το σύστημα
            while self._running:
                time.sleep(0.5)

    def get_state(self) -> Optional[Dict[str, Any]]:
        return dict(self._state) if self._state else None
