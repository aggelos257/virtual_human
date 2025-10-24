# -*- coding: utf-8 -*-
"""
voice_listener.py
-----------------
Συνεχής ακρόαση, αναγνώριση φωνητικών εντολών για αλλαγή γλώσσας/φύλου,
και προώθηση υπολοίπων αιτημάτων στο ReasoningManager.
"""

import re
import threading
import traceback
import time

try:
    import speech_recognition as sr
except Exception:
    sr = None

from voice.text_to_speech import TextToSpeech


class VoiceListener:
    def __init__(self, reasoning_manager=None):
        self.reasoning_manager = reasoning_manager
        self.running = False

        self.tts = TextToSpeech()

        self.recognizer = sr.Recognizer() if sr else None
        self.microphone = sr.Microphone() if sr else None

        # Εντολές τύπου: "μίλα ελληνικά γυναίκα", "μίλα αγγλικά άντρας"
        self.voice_cmd_pattern = re.compile(
            r"(?:μίλα|μιλα)\s+(ελληνικά|αγγλικά)\s+(γυναίκα|άντρας)",
            re.IGNORECASE
        )

    def start(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self._listen_loop, daemon=True).start()
        print("🎧 [VoiceListener] Ξεκίνησε η φωνητική ακρόαση...")

    def stop(self):
        self.running = False

    def _listen_loop(self):
        if not self.recognizer or not self.microphone:
            print("⚠️ [VoiceListener] Δεν βρέθηκε μικρόφωνο ή SpeechRecognition.")
            return

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        while self.running:
            try:
                with self.microphone as source:
                    print("🎤 [VoiceListener] Ακούω...")
                    audio = self.recognizer.listen(source, phrase_time_limit=6)

                # Αναγνώριση στα ελληνικά (μπορείς να αλλάξεις σε en-US αν μιλάς αγγλικά)
                text = self.recognizer.recognize_google(audio, language="el-GR").lower().strip()
                if not text:
                    continue
                print(f"🗣️ [VoiceListener] Άκουσα: {text}")

                # Εντολή αλλαγής φωνής;
                if self._check_voice_command(text):
                    continue

                # Αλλιώς, προώθηση στο Reasoning
                if self.reasoning_manager:
                    # αν έχεις μέθοδο handle_voice_input, διαφορετικά process
                    if hasattr(self.reasoning_manager, "handle_voice_input"):
                        self.reasoning_manager.handle_voice_input(text)
                    else:
                        reply = self.reasoning_manager.process(text)
                        if reply:
                            self.tts.speak(reply)

            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"⚠️ [VoiceListener] Σφάλμα: {e}")
                traceback.print_exc()
                time.sleep(1)

    def _check_voice_command(self, text: str) -> bool:
        m = self.voice_cmd_pattern.search(text)
        if not m:
            return False

        lang_word, gender_word = m.groups()
        lang_word = lang_word.lower()
        gender_word = gender_word.lower()

        lang_map = {"ελληνικά": "el", "αγγλικά": "en"}
        gender_map = {"γυναίκα": "female", "άντρας": "male"}

        lang_code = lang_map.get(lang_word)
        gender_code = gender_map.get(gender_word)
        if not lang_code or not gender_code:
            return False

        self.tts.set_voice(lang_code, gender_code)
        self.tts.speak(f"Η φωνή άλλαξε σε {lang_word} {gender_word}.")
        return True
