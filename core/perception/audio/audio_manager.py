# -*- coding: utf-8 -*-
"""
audio_manager.py
----------------
Υποσύστημα Αντίληψης Ήχου (Audio Perception)
Διαχειρίζεται τη βασική παρακολούθηση μικροφώνου & ανάλυση ήχου.
"""

import sounddevice as sd
import numpy as np
import threading
import time

class AudioManager:
    """
    Διαχειρίζεται ακουστική είσοδο — ενεργοποιεί το μικρόφωνο,
    υπολογίζει ένταση και επιστρέφει βασικά χαρακτηριστικά.
    """

    def __init__(self, sample_rate=16000, block_size=1024):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.current_volume = 0.0
        self.active = False
        self._thread = None

    # -------------------------------------------------------
    def _listen_loop(self):
        """Κύριος βρόχος ακρόασης ήχου (τρέχει σε ξεχωριστό νήμα)."""
        try:
            while self.active:
                audio_data = sd.rec(
                    self.block_size, samplerate=self.sample_rate, channels=1, dtype="float32"
                )
                sd.wait()
                volume = np.linalg.norm(audio_data) * 10
                self.current_volume = round(float(volume), 3)
                time.sleep(0.1)
        except Exception as e:
            print("⚠️ [AudioManager] Σφάλμα ακρόασης:", e)

    # -------------------------------------------------------
    def start(self):
        """Εκκίνηση ακρόασης ήχου."""
        if not self.active:
            self.active = True
            self._thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._thread.start()
            print("🎧 [AudioManager] Ξεκίνησε επιτυχώς.")

    def stop(self):
        """Τερματισμός ακρόασης ήχου."""
        if self.active:
            self.active = False
            print("🛑 [AudioManager] Σταμάτησε η ακρόαση.")

    def get_state(self):
        """Επιστρέφει βασική κατάσταση ήχου για perception manager."""
        return {"volume": self.current_volume, "active": self.active}
