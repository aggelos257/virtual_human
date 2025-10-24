# -*- coding: utf-8 -*-
"""
start_zenia.py
---------------
Κύριο σημείο εκκίνησης για το Virtual Human “Ζένια”.

✅ Συμβατό με τη δομή σου:
- core/reasoning/reasoning_manager.py
- voice/text_to_speech.py
- voice/voice_listener.py
"""

import sys
import traceback
import torch

# 📦 Πυρήνας
from core.system_manager import SystemManager
from core.reasoning.reasoning_manager import ReasoningManager  # ✅ σωστό import

# 🗣️ Φωνή
from voice.text_to_speech import TextToSpeech
from voice.voice_listener import VoiceListener

# 🖥️ GUI
from gui.gui_manager import GUIManager


def main():
    print("✨ Η Ζένια ενεργοποιείται...")

    # -------------------------------
    # GPU / Device
    # -------------------------------
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        print(f"⚡ GPU Detected: {gpu_name} (CUDA Enabled)")
    else:
        print("⚡ Χωρίς GPU - χρήση CPU")

    # -------------------------------
    # Managers
    # -------------------------------
    system_manager = SystemManager()
    reasoning_manager = ReasoningManager(device=device)

    # -------------------------------
    # TTS / Voice Listener / GUI
    # -------------------------------
    tts = TextToSpeech()                         # ✅ χωρίς default_voice
    listener = VoiceListener(reasoning_manager=reasoning_manager)
    gui_manager = GUIManager(
        reasoning_manager=reasoning_manager,
        tts=tts,
        listener=listener
    )

    # -------------------------------
    # Εκκίνηση υποσυστημάτων με ασφάλεια
    # -------------------------------
    system_manager.start()
    reasoning_manager.start()
    listener.start()
    gui_manager.start()

    print("✅ [Ζένια] Όλα τα υποσυστήματα φορτώθηκαν επιτυχώς.")
    tts.speak("Καλησπέρα Άγγελε!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Τερματισμός από τον χρήστη.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ [Ζένια Init Error]: {e}")
        traceback.print_exc()
        sys.exit(1)
