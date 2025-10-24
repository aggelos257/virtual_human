from gtts import gTTS
import os
import pygame
import tempfile

class TextToSpeech:
    def __init__(self):
        pygame.mixer.init()

    def synthesize_and_play(self, text: str):
        """Η Ζένια μιλάει χρησιμοποιώντας gTTS (Google Text-to-Speech)."""
        try:
            print(f"🗣️ (Ζένια): {text}")

            # Δημιουργία προσωρινού αρχείου ήχου
            tts = gTTS(text=text, lang="el")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                temp_path = tmp.name
                tts.save(temp_path)

            # Αναπαραγωγή με pygame
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            # Αναμονή μέχρι να τελειώσει η φωνή
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            os.remove(temp_path)

        except Exception as e:
            print(f"⚠️ Σφάλμα στην ομιλία: {e}")
