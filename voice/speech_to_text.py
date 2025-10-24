# -*- coding: utf-8 -*-
"""
speech_to_text.py
-----------------
Διαχείριση φωνητικής εισόδου — online (OpenAI Whisper) ή offline (faster_whisper).
Υποστηρίζει επιλογή μικροφώνου μέσω μεταβλητής περιβάλλοντος MIC_DEVICE_INDEX.
"""

import os
import sys
import queue
import numpy as np
import sounddevice as sd
import soundfile as sf
import tempfile
import traceback
import torch

# === OpenAI API ===
try:
    import openai
    _OPENAI_OK = True
except Exception:
    _OPENAI_OK = False

# === Faster Whisper ===
try:
    from faster_whisper import WhisperModel
    _FW_OK = True
except Exception:
    _FW_OK = False

# === ΡΥΘΜΙΣΕΙΣ ===
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_MS = 30

# Επιλογή μικροφώνου μέσω μεταβλητής περιβάλλοντος
ENV_MIC_INDEX = os.environ.get("MIC_DEVICE_INDEX")
if ENV_MIC_INDEX and ENV_MIC_INDEX.isdigit():
    device_index = int(ENV_MIC_INDEX)
    print(f"🎧 [Audio] MIC_DEVICE_INDEX από περιβάλλον: {device_index}")
else:
    # Αν δεν υπάρχει, χρησιμοποιεί το πρώτο διαθέσιμο μικρόφωνο
    device_index = 0
    print(f"🎚️ [Audio] Πρώτο διαθέσιμο input -> #{device_index} (default)")

USE_OPENAI = True if _OPENAI_OK else False
USE_FASTER_WHISPER = True if _FW_OK else False

LANGUAGE = "el"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# === ΔΗΜΙΟΥΡΓΙΑ ΜΟΝΤΕΛΟΥ ===
if USE_FASTER_WHISPER:
    try:
        whisper_model = WhisperModel("small", device=DEVICE)
        print(f"🧠 [FasterWhisper] Φορτώθηκε επιτυχώς ({DEVICE})")
    except Exception as e:
        print(f"⚠️ [FasterWhisper] Σφάλμα φόρτωσης: {e}")
        whisper_model = None
        USE_FASTER_WHISPER = False
else:
    whisper_model = None

# === ΣΥΝΑΡΤΗΣΗ ΕΓΓΡΑΦΗΣ ===
def _record_once(duration=5):
    """Καταγραφή φωνής για συγκεκριμένη διάρκεια."""
    try:
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            device=device_index
        )
        sd.wait()
        return np.squeeze(audio)
    except Exception as e:
        print(f"⚠️ [Audio Record] Σφάλμα: {e}")
        return None

# === ΚΥΡΙΑ ΚΛΑΣΗ ===
class SpeechToText:
    def __init__(self):
        self.online = USE_OPENAI
        self.offline = USE_FASTER_WHISPER
        self.client = openai if _OPENAI_OK else None

        if self.online:
            print("🌐 [STT Online] OpenAI Whisper έτοιμο.")
        elif self.offline:
            print("🧠 [STT Offline] Faster Whisper έτοιμο.")
        else:
            print("⚠️ [STT] Δεν υπάρχει ενεργό μοντέλο — χρησιμοποιείται stub fallback.")

    def listen_once(self, duration=5):
        """Καταγραφή και μετατροπή φωνής σε κείμενο."""
        audio = _record_once(duration=duration)
        if audio is None:
            print("[SpeechToText] (stub) fallback ενεργό — επιστρέφει κενό string.")
            return ""

        # Αποθήκευση προσωρινού WAV
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                sf.write(f.name, audio, SAMPLE_RATE)
                wav_path = f.name
        except Exception as e:
            print(f"⚠️ [STT] Σφάλμα αποθήκευσης αρχείου: {e}")
            return ""

        text = ""
        if self.online and self.client:
            try:
                with open(wav_path, "rb") as af:
                    resp = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=af,
                        language=LANGUAGE
                    )
                text = resp.text.strip()
                return text
            except Exception as e:
                print(f"⚠️ [STT Online] Σφάλμα: {e}")

        if self.offline and whisper_model:
            try:
                segments, _ = whisper_model.transcribe(wav_path, language=LANGUAGE)
                text = " ".join([seg.text for seg in segments]).strip()
                return text
            except Exception as e:
                print(f"⚠️ [STT Offline] Σφάλμα: {e}")

        print("[SpeechToText] (stub) fallback ενεργό — επιστρέφει κενό string.")
        return ""

