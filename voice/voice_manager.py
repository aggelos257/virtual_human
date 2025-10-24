# voice/voice_manager.py
import time
import traceback
from core.reasoning.reasoner import Reasoner
from core.runtime_monitor import RuntimeMonitor
from core.utils.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech


class VoiceManager:
    """
    Ο κύριος ελεγκτής φωνής της Ζένιας.
    Συνδυάζει: ακρόαση, λογική, απάντηση και προσαρμοστική επίγνωση χρόνου.
    """

    def __init__(self):
        print("🎧 [Ζένια] Ενεργή φωνητική λειτουργία — μπορείς να μιλήσεις!")

        # Υποσυστήματα
        self.speech_to_text = SpeechToText()
        self.tts = TextToSpeech()
        self.reasoner = Reasoner()
        self.runtime_monitor = RuntimeMonitor(timeout=10)

        # Ενεργή λειτουργία
        self.active = True

    # ------------------------------------------------------------
    def run(self):
        """Κύρια βρόχος φωνητικής λειτουργίας."""
        while self.active:
            try:
                # Έλεγχος καθυστέρησης χρήστη
                timeout_response = self.runtime_monitor.check_timeout()
                if timeout_response:
                    print(f"[Ζένια]: {timeout_response}")
                    self.tts.speak(timeout_response)

                # Ακούει φράση
                text = self.speech_to_text.listen()

                if not text:
                    continue

                self.runtime_monitor.update_activity()
                print(f"[Αναγνώριση]: {text}")

                # Επεξεργασία πρόθεσης
                response = self.reasoner.reason(text)
                if response:
                    print(f"[Ζένια]: {response}")
                    self.tts.speak(response)

                # Αν τερματιστεί από τη λογική
                if "τερματίζω" in response.lower() or "αντίο" in response.lower():
                    self.active = False
                    break

            except KeyboardInterrupt:
                print("\n🛑 [Ζένια] Διακόπηκε χειροκίνητα.")
                break
            except Exception as e:
                print(f"⚠️ [VoiceManager] Σφάλμα: {e}")
                traceback.print_exc()
                time.sleep(1)
