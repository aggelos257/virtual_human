# core/action_executor.py
import os
import re
import json
import psutil
import subprocess
import webbrowser
import difflib
from pathlib import Path

class ActionExecutor:
    """Πραγματικός έξυπνος εκτελεστής ενεργειών για τη Ζένια."""

    def __init__(self):
        self.memory_file = Path("core/app_memory.json")
        self.apps = self._load_memory()

        # URLs που καταλαβαίνει λογικά
        self.web_mappings = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "chatgpt": "https://chat.openai.com",
            "gmail": "https://mail.google.com",
        }

    # -----------------------------------------------------------
    def _load_memory(self):
        """Φόρτωση των γνωστών εφαρμογών που έχει μάθει η Ζένια."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.apps, f, ensure_ascii=False, indent=2)

    # -----------------------------------------------------------
    def _find_executable(self, name):
        """Αυτόματη ανίχνευση εφαρμογής στα Windows."""
        name = name.lower().strip().replace(".exe", "")
        search_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            os.path.expanduser(r"~\AppData\Local"),
        ]

        for base in search_paths:
            for root, dirs, files in os.walk(base):
                for file in files:
                    if file.lower().endswith(".exe") and name in file.lower():
                        return os.path.join(root, file)
        return None

    def _fuzzy_match(self, name):
        """Προσπαθεί να βρει κοντινή εφαρμογή (λογική ανοχή)."""
        keys = list(self.apps.keys()) + list(self.web_mappings.keys())
        match = difflib.get_close_matches(name.lower(), keys, n=1, cutoff=0.6)
        return match[0] if match else None

    # -----------------------------------------------------------
    def open_app(self, name):
        """Ανοίγει εφαρμογή ή ιστότοπο με λογική και μνήμη."""
        if not name:
            return "Τι θέλεις να ανοίξω;"

        name = re.sub(r"(το|την|τον|app|πρόγραμμα)", "", name).strip().lower()

        # 1️⃣ Αν είναι ήδη γνωστό από μνήμη
        key = self._fuzzy_match(name)
        if key:
            target = self.apps.get(key) or self.web_mappings.get(key)
            return self._launch_target(key, target)

        # 2️⃣ Αν είναι γνωστός ιστότοπος
        for w, url in self.web_mappings.items():
            if w in name:
                self.apps[name] = url
                self._save_memory()
                return self._launch_target(w, url)

        # 3️⃣ Αν δεν το ξέρει, προσπάθησε να το βρει στα Windows
        exe_path = self._find_executable(name)
        if exe_path:
            self.apps[name] = exe_path
            self._save_memory()
            return self._launch_target(name, exe_path)

        # 4️⃣ Τελευταία λύση — διαδικτυακή αναζήτηση
        webbrowser.open(f"https://www.google.com/search?q={name.replace(' ', '+')}")
        return f"Δεν βρήκα το '{name}', αλλά το αναζητώ στο διαδίκτυο."

    def _launch_target(self, key, target):
        """Ανοίγει το πρόγραμμα ή ιστότοπο."""
        if target.startswith("http"):
            webbrowser.open(target)
            return f"Άνοιξα το {key}."
        try:
            subprocess.Popen([target], shell=True)
            return f"Άνοιξα το {key}."
        except Exception as e:
            return f"⚠️ Δεν μπόρεσα να ανοίξω το {key}: {e}"

    # -----------------------------------------------------------
    def close_app(self, name):
        """Κλείνει εφαρμογή με λογική."""
        if not name:
            return "Τι θέλεις να κλείσω;"

        key = self._fuzzy_match(name)
        if not key:
            return f"Δεν γνωρίζω ακόμα πώς να κλείσω το {name}."

        exe = os.path.basename(self.apps.get(key, "") or "")
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if exe and exe.lower() in proc.info['name'].lower():
                    proc.terminate()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed:
            return f"Έκλεισα το {key}."
        else:
            return f"Δεν βρήκα ανοιχτό το {key}."

    # -----------------------------------------------------------
    def play_music(self, query):
        """Ανοίγει YouTube και παίζει μουσική."""
        if not query:
            webbrowser.open("https://www.youtube.com")
            return "Άνοιξα το YouTube. Πες μου ποιο τραγούδι να βάλω."
        else:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            return f"Αναζητώ στο YouTube το «{query}»."
