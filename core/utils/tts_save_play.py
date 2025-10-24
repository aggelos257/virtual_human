# tts_save_play.py
import pyttsx3
import tempfile
import os
import winsound
import time

def save_and_play(text="Δοκιμή αποθήκευσης σε WAV"):
    engine = pyttsx3.init()
    fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        engine.save_to_file(text, wav_path)
        engine.runAndWait()
        print("Saved to:", wav_path)
        # play synchronously
        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
    except Exception as e:
        print("Error saving/playing:", e)
    finally:
        try:
            os.remove(wav_path)
        except Exception:
            pass

if __name__ == "__main__":
    save_and_play()
