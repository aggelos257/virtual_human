# ==========================================================
# voice/voice_handler.py
# Τεχνικός χειρισμός φωνής (μικρόφωνο + ήχος εξόδου)
# ==========================================================
import threading
from voice.voice_manager import VoiceManager

class VoiceHandler:
    """
    VoiceHandler:
    --------------
    - Διαχειρίζεται την ενεργοποίηση φωνητικής λειτουργίας
    - Τρέχει σε ξεχωριστό thread
    - Συνδέει το VoiceManager με το σύστημα Zenia Core
    """

    def __init__(self, zenia_core):
        self.zenia_core = zenia_core
        self.voice_manager = VoiceManager()
        self.active = False

    def start_voice_mode(self):
        """Ενεργοποιεί τη φωνητική λειτουργία σε ξεχωριστό thread."""
        if self.active:
            print("⚠️ [Ζένια] Η φωνητική λειτουργία είναι ήδη ενεργή.")
            return

        self.active = True
        print("🎧 [Ζένια] Ενεργή φωνητική λειτουργία — μπορείς να μιλήσεις!")

        thread = threading.Thread(target=self.voice_manager.start_conversation)
        thread.daemon = True
        thread.start()

    def stop_voice_mode(self):
        """Τερματίζει τη φωνητική λειτουργία."""
        self.active = False
        print("🛑 [Ζένια] Η φωνητική λειτουργία απενεργοποιήθηκε.")
