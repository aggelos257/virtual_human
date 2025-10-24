# -*- coding: utf-8 -*-
"""
text_to_speech.py
-----------------
Ενιαίο TTS:
- Online: Edge TTS (Athina/Nestoras/Aria/Guy)
- Offline: Coqui TTS (multilingual)
- Fallback: pyttsx3 (Windows)
- Voice switching + αποθήκευση/φόρτωση μνήμης (voice_memory.json)
"""

import os
import asyncio
import socket
import traceback
import json
from pathlib import Path
from typing import Optional

# Optional imports
try:
    import edge_tts
    _EDGE_OK = True
except Exception:
    _EDGE_OK = False

try:
    from TTS.api import TTS as COQUI_TTS
    _COQUI_OK = True
except Exception:
    _COQUI_OK = False

try:
    import pyttsx3
    _PYTTSX3_OK = True
except Exception:
    _PYTTSX3_OK = False

try:
    from playsound import playsound
    _PLAYSOUND_OK = True
except Exception:
    _PLAYSOUND_OK = False


VOICE_MAP = {
    "el": {
        "female": {"online": "el-GR-AthinaNeural",  "offline": "el_female"},
        "male":   {"online": "el-GR-NestorasNeural", "offline": "el_male"},
    },
    "en": {
        "female": {"online": "en-US-AriaNeural",     "offline": "en_female"},
        "male":   {"online": "en-US-GuyNeural",      "offline": "en_male"},
    }
}

BASE_DIR = Path(__file__).resolve().parent.parent
TMP_DIR = BASE_DIR / "tmp_tts"
TMP_DIR.mkdir(exist_ok=True, parents=True)

MEM_FILE = BASE_DIR / "voice" / "voice_memory.json"
COQUI_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"


def _has_internet(timeout=1.5) -> bool:
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=timeout)
        return True
    except OSError:
        return False


class TextToSpeech:
    def __init__(self):
        self.lang = "el"
        self.gender = "female"
        self.coqui_tts = None
        self._init_coqui_once = False

        self._load_memory()

        self.pytts_engine = None
        if _PYTTSX3_OK:
            try:
                self.pytts_engine = pyttsx3.init()
                for v in self.pytts_engine.getProperty("voices"):
                    name = (v.name or "").lower()
                    lang = "".join(v.languages).lower() if hasattr(v, "languages") else ""
                    if "stefanos" in name or "el" in lang or "greek" in name:
                        self.pytts_engine.setProperty("voice", v.id)
                        break
            except Exception:
                self.pytts_engine = None

        print(f"🗣️ [TTS] Έτοιμο με φωνή: {self.lang}/{self.gender}")

    # ---------- Memory ----------
    def _save_memory(self):
        try:
            MEM_FILE.parent.mkdir(exist_ok=True, parents=True)
            with open(MEM_FILE, "w", encoding="utf-8") as f:
                json.dump({"lang": self.lang, "gender": self.gender}, f)
        except Exception as e:
            print(f"⚠️ [TTS Memory] Σφάλμα αποθήκευσης: {e}")

    def _load_memory(self):
        if MEM_FILE.exists():
            try:
                with open(MEM_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.lang = data.get("lang", "el")
                    self.gender = data.get("gender", "female")
                print(f"🧠 [TTS Memory] Φορτώθηκε: {self.lang}/{self.gender}")
            except Exception as e:
                print(f"⚠️ [TTS Memory] Σφάλμα ανάγνωσης: {e}")

    # ---------- Voice Switching ----------
    def set_voice(self, lang: str, gender: str):
        lang = (lang or "").lower()
        gender = (gender or "").lower()
        if lang not in VOICE_MAP:
            print(f"⚠️ [TTS] Μη υποστηριζόμενη γλώσσα '{lang}'. Επιλογές: {list(VOICE_MAP.keys())}")
            return
        if gender not in ("male", "female"):
            print("⚠️ [TTS] Το φύλο πρέπει να είναι 'male' ή 'female'.")
            return
        self.lang = lang
        self.gender = gender
        self._save_memory()
        print(f"🔄 [TTS] Νέα φωνή -> {self.lang}/{self.gender}")

    # ---------- Public ----------
    def speak(self, text: str):
        if not text or not text.strip():
            return

        # 1) Online: Edge TTS
        if _EDGE_OK and _PLAYSOUND_OK and _has_internet():
            try:
                out_mp3 = self._edge_tts_to_mp3(text)
                if out_mp3:
                    self._play_file(out_mp3)
                    return
            except Exception as e:
                print(f"⚠️ [TTS Online] Edge TTS αποτυχία: {e}")
                traceback.print_exc()

        # 2) Offline: Coqui
        if _COQUI_OK:
            try:
                out_wav = self._coqui_tts_to_wav(text)
                if out_wav:
                    self._play_file(out_wav)
                    return
            except Exception as e:
                print(f"⚠️ [TTS Offline:Coqui] Αποτυχία: {e}")
                traceback.print_exc()

        # 3) Fallback: pyttsx3
        if self.pytts_engine:
            try:
                self.pytts_engine.say(text)
                self.pytts_engine.runAndWait()
                return
            except Exception as e:
                print(f"⚠️ [TTS Fallback pyttsx3] {e}")

        print("❌ [TTS] Καμία διαθέσιμη μηχανή ομιλίας.")

    # ---------- Edge TTS ----------
    def _edge_tts_voice(self) -> Optional[str]:
        try:
            return VOICE_MAP[self.lang][self.gender]["online"]
        except Exception:
            return None

    def _edge_tts_to_mp3(self, text: str) -> Optional[str]:
        """Διορθωμένη μέθοδος για Edge TTS χωρίς stream_to_file (χρήση stream)."""
        voice = self._edge_tts_voice()
        if not voice:
            return None
        out_path = str(TMP_DIR / "edge_tts_out.mp3")

        async def _run():
            communicate = edge_tts.Communicate(text, voice)
            with open(out_path, "wb") as f:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])

        try:
            asyncio.run(_run())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(_run())
            finally:
                loop.close()

        return out_path if os.path.exists(out_path) else None

    # ---------- Coqui ----------
    def _init_coqui(self):
        if self._init_coqui_once:
            return
        self._init_coqui_once = True
        try:
            print(f"🧠 [Coqui] Φόρτωση μοντέλου {COQUI_MODEL}...")
            self.coqui_tts = COQUI_TTS(COQUI_MODEL)
            print("✅ [Coqui] Έτοιμο.")
        except Exception as e:
            self.coqui_tts = None
            print(f"⚠️ [Coqui] Αποτυχία: {e}")

    def _coqui_voice_tag(self):
        return "female" if self.gender == "female" else "male"

    def _coqui_tts_to_wav(self, text: str) -> Optional[str]:
        self._init_coqui()
        if not self.coqui_tts:
            return None
        out_path = str(TMP_DIR / "coqui_tts_out.wav")
        lang = "el" if self.lang == "el" else "en"
        try:
            self.coqui_tts.tts_to_file(
                text=text,
                file_path=out_path,
                language=lang,
                speaker=self._coqui_voice_tag()
            )
            return out_path if os.path.exists(out_path) else None
        except TypeError:
            self.coqui_tts.tts_to_file(
                text=text,
                file_path=out_path,
                language=lang
            )
            return out_path if os.path.exists(out_path) else None

    # ---------- Playback ----------
    def _play_file(self, path: str):
        if not _PLAYSOUND_OK:
            print("⚠️ [TTS] Το playsound δεν είναι διαθέσιμο.")
            return
        try:
            playsound(path)
        except Exception as e:
            print(f"⚠️ [TTS Playback] {e}")
