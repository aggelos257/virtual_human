# -*- coding: utf-8 -*-
"""
tools/install_whisper_model.py
--------------------------------
Αυτόματο script εγκατάστασης Whisper (faster-whisper) για τη Ζένια.
• Κατεβάζει το multilingual small μοντέλο (~1.6GB)
• Ελέγχει GPU και βιβλιοθήκες
• Δημιουργεί data/models/whisper-small-el
• Θέτει αυτόματα τις μεταβλητές περιβάλλοντος
"""

import os
import sys
import subprocess
import shutil
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, "data", "models", "whisper-small-el")

def install_package(pkg):
    print(f"📦 Εγκατάσταση πακέτου: {pkg} ...")
    subprocess.call([sys.executable, "-m", "pip", "install", "-U", pkg])

def main():
    print("🧠 Whisper Installer for Zenia")
    print("=" * 50)

    # Βήμα 1: Έλεγχος βιβλιοθηκών
    required = ["torch", "faster-whisper", "numpy", "sounddevice", "soundfile"]
    for pkg in required:
        try:
            __import__(pkg.split("[")[0])
        except ImportError:
            install_package(pkg)

    # Βήμα 2: Δημιουργία φακέλου
    os.makedirs(MODELS_DIR, exist_ok=True)
    print(f"📁 Δημιουργήθηκε (ή υπάρχει ήδη): {MODELS_DIR}")

    # Βήμα 3: Κατέβασμα μοντέλου Whisper Small
    print("⬇️  Λήψη μοντέλου whisper-small multilingual...")
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cuda" if torch.cuda.is_available() else "cpu")
        # αποθήκευση meta
        with open(os.path.join(MODELS_DIR, "info.txt"), "w", encoding="utf-8") as f:
            f.write("Whisper small multilingual model installed.\n")
        print("✅ Whisper small εγκαταστάθηκε επιτυχώς.")
    except Exception as e:
        print("⚠️ Σφάλμα κατά τη λήψη του μοντέλου:", e)

    # Βήμα 4: Ρύθμιση περιβάλλοντος
    env_path = os.path.join(PROJECT_ROOT, ".env")
    with open(env_path, "a", encoding="utf-8") as f:
        f.write(f"\nWHISPER_MODEL_DIR={MODELS_DIR}\nWHISPER_MODEL_SIZE=small\n")
    print(f"🧩 Ενημερώθηκε το .env → WHISPER_MODEL_DIR={MODELS_DIR}")

    print("\n✨ Ολοκληρώθηκε! Μπορείς να τρέξεις τη Ζένια ξανά:")
    print("   python start_zenia.py")

if __name__ == "__main__":
    try:
        import torch
    except Exception:
        install_package("torch")
        import torch
    main()
