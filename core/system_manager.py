# -*- coding: utf-8 -*-
"""
core/system_manager.py
----------------------
Κεντρικός Διαχειριστής Συστήματος για τη Ζένια (Zenia AI Virtual Human)
"""

import os
import sys
import gc
import time
import socket
import traceback
import threading

# === GPU / CPU Detection ===
try:
    import torch
except Exception:
    torch = None


def detect_device():
    """Ανιχνεύει αν υπάρχει GPU CUDA ή επιστρέφει CPU."""
    try:
        if torch and torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(f"⚡ [SystemManager] GPU Ανιχνεύθηκε: {device_name} (CUDA ενεργό)")
            return torch.device("cuda")
        else:
            print("🧠 [SystemManager] Λειτουργία CPU (χωρίς GPU)")
            return torch.device("cpu") if torch else "cpu"
    except Exception:
        print("⚠️ [SystemManager] Αδυναμία εντοπισμού συσκευής - fallback σε CPU.")
        return "cpu"


def internet_available():
    """Ελέγχει αν υπάρχει σύνδεση στο Internet."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


# === Imports των υποσυστημάτων ===
try:
    from core.reasoning.reasoning_manager import ReasoningManager
    from gui.gui_manager import GUIManager
    from voice import TextToSpeech, SpeechToText
except Exception as e:
    print("⚠️ [SystemManager] Σφάλμα κατά τη φόρτωση βασικών modules:", e)
    traceback.print_exc()


class SystemManager:
    """Κεντρικός Διαχειριστής Ζένια – ενοποιεί όλα τα υποσυστήματα."""

    def __init__(self):
        self.device = detect_device()
        self.reasoning_manager = None
        self.gui_manager = None
        self.tts = None
        self.stt = None
        self.is_active = False
        self._lock = threading.Lock()
        print("🧠 [SystemManager] Εκκίνηση...")

    # ------------------------------------------------------
    # Δημόσια μέθοδος για εκκίνηση (συμβατή με start_zenia.py)
    # ------------------------------------------------------
    def start(self):
        """Συμβατή συντόμευση που καλεί το start_all()."""
        self.start_all()

    # ------------------------------------------------------
    # Εκκίνηση όλων των υποσυστημάτων
    # ------------------------------------------------------
    def start_all(self):
        """Εκκινεί Reasoning, TTS, STT και GUI."""
        with self._lock:
            try:
                # === Reasoning Manager ===
                print("🧩 [SystemManager] Εκκινείται το ReasoningManager...")
                self.reasoning_manager = ReasoningManager(device=self.device)
                print("✅ [SystemManager] ReasoningManager ενεργό.")

                # === Text To Speech ===
                print("🔊 [SystemManager] Εκκινείται το TTS...")
                self.tts = TextToSpeech()

                if internet_available():
                    print("🌐 [SystemManager] Internet διαθέσιμο — Online TTS ενεργό.")
                    self.tts.online_enabled = True
                else:
                    print("💻 [SystemManager] Offline λειτουργία — χρήση XTTS v2.")
                    self.tts.online_enabled = False

                print("✅ [SystemManager] TextToSpeech έτοιμο.")

                # === Speech To Text ===
                print("🎙️ [SystemManager] Εκκινείται το STT...")
                self.stt = SpeechToText()
                print("✅ [SystemManager] SpeechToText ενεργό.")

                # === GUI Manager ===
                print("🎨 [SystemManager] Εκκινείται το GUI...")
                self.gui_manager = GUIManager()
                self.gui_manager.start_voice_interface(self.tts, self.stt, self.reasoning_manager)
                print("✅ [SystemManager] GUI έτοιμο.")

                # === Ενεργοποίηση κατάστασης ===
                self.is_active = True
                print("🤖 [SystemManager] Όλα τα υποσυστήματα ενεργοποιήθηκαν επιτυχώς.\n")

            except Exception as e:
                print("❌ [SystemManager] Σφάλμα κατά την εκκίνηση υποσυστημάτων:", e)
                traceback.print_exc()
                self.is_active = False

    # ------------------------------------------------------
    # Διακοπή όλων των υποσυστημάτων
    # ------------------------------------------------------
    def stop_all(self):
        """Ασφαλής τερματισμός όλων των modules."""
        with self._lock:
            try:
                print("🛑 [SystemManager] Τερματισμός υποσυστημάτων...")
                if self.gui_manager:
                    try:
                        self.gui_manager.stop_voice_interface()
                    except Exception:
                        pass
                if self.tts and hasattr(self.tts, "stop"):
                    try:
                        self.tts.stop()
                    except Exception:
                        pass
                if self.reasoning_manager:
                    try:
                        self.reasoning_manager.shutdown()
                    except Exception:
                        pass
                self.is_active = False
                gc.collect()
                print("✅ [SystemManager] Όλα τα υποσυστήματα τερματίστηκαν.")
            except Exception as e:
                print("⚠️ [SystemManager] Σφάλμα κατά το shutdown:", e)
                traceback.print_exc()

    # ------------------------------------------------------
    # Επανεκκίνηση
    # ------------------------------------------------------
    def restart(self):
        """Επανεκκινεί τη Ζένια."""
        print("🔄 [SystemManager] Επανεκκίνηση όλων των modules...")
        self.stop_all()
        time.sleep(1)
        self.start_all()
        print("✅ [SystemManager] Επανεκκινήθηκε επιτυχώς.")

    # ------------------------------------------------------
    # Έλεγχος κατάστασης
    # ------------------------------------------------------
    def status(self):
        """Επιστρέφει την κατάσταση όλων των modules."""
        return {
            "reasoning": bool(self.reasoning_manager),
            "gui": bool(self.gui_manager),
            "tts": bool(self.tts),
            "stt": bool(self.stt),
            "active": self.is_active,
            "device": str(self.device),
        }


# === Αυτόνομη εκτέλεση (αν τρέξει μόνο του) ===
if __name__ == "__main__":
    system = SystemManager()
    system.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        system.stop_all()
        print("👋 [SystemManager] Τερματισμός Ζένια.")
