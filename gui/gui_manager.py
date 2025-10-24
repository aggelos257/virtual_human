import threading
import traceback
import time
import sys
import gc

from voice.text_to_speech import TextToSpeech
from voice.speech_to_text import SpeechToText
from core.reasoning.reasoning_manager import ReasoningManager

class GUIManager:
    """
    Ζένια - Γραφικό & Φωνητικό Υποσύστημα
    Διαχειρίζεται τη φωνητική διεπαφή (TTS/STT) και συνδέεται με το reasoning core.
    """

    def __init__(self):
        self.tts = None
        self.stt = None
        self.reasoning_manager = None
        self.voice_thread = None
        self.is_running = False
        print("🎨 [GUIManager] Ενεργοποιήθηκε.")

    # ------------------------------------------------------
    # ΑΣΦΑΛΕΙΑ: Διασφαλίζει ότι η SpeechToText έχει listen_once
    # ------------------------------------------------------
    def _verify_stt_integrity(self):
        try:
            if not hasattr(self.stt, "listen_once"):
                print("⚠️ [GUIManager] Το SpeechToText δεν έχει listen_once(). Δημιουργία fallback.")
                def listen_once_stub():
                    print("[SpeechToText] (stub) fallback ενεργό — επιστρέφει κενό string.")
                    return ""
                setattr(self.stt, "listen_once", listen_once_stub)
        except Exception as e:
            print("⚠️ [GUIManager] Σφάλμα κατά τον έλεγχο STT:", e)

    # ------------------------------------------------------
    # Εκκίνηση φωνητικής διεπαφής
    # ------------------------------------------------------
    def start_voice_interface(self, tts: TextToSpeech, stt: SpeechToText, reasoning_manager: ReasoningManager):
        """Ενεργοποιεί το φωνητικό υποσύστημα σε ξεχωριστό νήμα."""
        self.tts = tts
        self.stt = stt
        self.reasoning_manager = reasoning_manager

        self._verify_stt_integrity()

        if not self.stt or not self.tts:
            print("⚠️ [GUIManager] Δεν υπάρχει STT ή TTS instance — ακύρωση φωνητικής διεπαφής.")
            return

        if self.is_running:
            print("ℹ️ [GUIManager] Η φωνητική διεπαφή είναι ήδη ενεργή.")
            return

        self.is_running = True
        print("🎧 [Ζένια] Ενεργή φωνητική διεπαφή — μπορείς να μιλήσεις!")

        def voice_loop():
            try:
                while self.is_running:
                    try:
                        user_text = self.stt.listen_once()
                        if not user_text:
                            continue

                        print(f"👂 [Χρήστης]: {user_text}")
                        response = self.reasoning_manager.process(user_text)
                        if response:
                            print(f"🤖 [Ζένια]: {response}")
                            self.tts.speak(response)
                        else:
                            print("🤖 [Ζένια]: (χωρίς απάντηση)")
                    except Exception as e:
                        print(f"⚠️ [GUIManager] Σφάλμα στο voice loop: {e}")
                        traceback.print_exc()
                        time.sleep(1)
            except KeyboardInterrupt:
                print("🛑 [GUIManager] Voice loop διακόπηκε χειροκίνητα.")
            except Exception as e:
                print("❌ [GUIManager] Σφάλμα:", e)
                traceback.print_exc()
            finally:
                self.is_running = False
                print("🔚 [GUIManager] Voice loop τερματίστηκε.")

        self.voice_thread = threading.Thread(target=voice_loop, daemon=True)
        self.voice_thread.start()
        print("🎤 [GUIManager] Voice loop ξεκίνησε σε ξεχωριστό νήμα.")

    # ------------------------------------------------------
    # Διακοπή φωνητικής διεπαφής
    # ------------------------------------------------------
    def stop_voice_interface(self):
        """Σταματά τη φωνητική διεπαφή και καθαρίζει threads."""
        if not self.is_running:
            print("ℹ️ [GUIManager] Δεν υπάρχει ενεργό voice loop.")
            return

        self.is_running = False
        try:
            if self.voice_thread and self.voice_thread.is_alive():
                print("🛑 [GUIManager] Διακοπή voice thread...")
                self.voice_thread.join(timeout=2)
        except Exception as e:
            print("⚠️ [GUIManager] Σφάλμα κατά τη διακοπή:", e)

        try:
            gc.collect()
        except:
            pass

        print("🔇 [GUIManager] Η φωνητική διεπαφή απενεργοποιήθηκε.")

    # ------------------------------------------------------
    # Απενεργοποίηση GUI συστήματος
    # ------------------------------------------------------
    def shutdown(self):
        """Πλήρης απενεργοποίηση GUI και φωνής."""
        print("🔻 [GUIManager] Τερματισμός GUI Manager...")
        self.stop_voice_interface()
        self.tts = None
        self.stt = None
        self.reasoning_manager = None
        print("✅ [GUIManager] Τερματίστηκε πλήρως χωρίς σφάλματα.")