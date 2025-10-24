import os
import torch
from TTS.api import TTS
import pygame
import tempfile

class CoquiTTS:
    """Offline φωνητικός κινητήρας της Ζένιας με χρήση Coqui TTS."""

    def __init__(self):
        print("🔊 Φόρτωση φωνής Ζένιας (Coqui TTS)...")

        # Επιλογή συσκευής (GPU αν υπάρχει)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Ελληνικό offline μοντέλο Coqui
        self.tts = TTS(model_name="tts_models/el/cv/vits", progress_bar=False).to(self.device)

    def speak(self, text: str):
        """Μετατρέπει το κείμενο σε φωνή και το αναπαράγει."""
        try:
            print(f"🗣️ (Ζένια): {text}")

            # Δημιουργία προσωρινού αρχείου ήχου
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                output_path = tmp.name

            # Δημιουργία ήχου
            self.tts.tts_to_file(text=text, file_path=output_path)

            # Αναπαραγωγή με pygame
            pygame.mixer.init()
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()

            # Περιμένει να ολοκληρωθεί η αναπαραγωγή
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()
            os.remove(output_path)

        except Exception as e:
            print(f"⚠️ Σφάλμα στην εκφώνηση: {e}")
