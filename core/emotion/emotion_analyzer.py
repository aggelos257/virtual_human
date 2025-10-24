import re
import numpy as np

class EmotionAnalyzer:
    """
    Αναλύει το περιεχόμενο του λόγου και προσεγγίζει το πιθανό συναίσθημα.
    Συνδυάζει λέξεις, τόνους και απλούς ηχητικούς δείκτες.
    """
    def __init__(self):
        self.keywords = {
            "χαρά": ["χαίρομαι", "τέλεια", "φανταστικά", "υπέροχα"],
            "λύπη": ["λυπάμαι", "στενοχωρημένος", "θλιμμένος"],
            "θυμός": ["θυμός", "νεύρα", "εκνευρίστηκα"],
            "φόβος": ["φοβάμαι", "ανησυχώ", "αγχώνομαι"],
            "έκπληξη": ["τι;", "αλήθεια;", "ουάου"],
            "ηρεμία": ["ήρεμα", "χαλαρά", "όλα καλά"],
            "κούραση": ["κουράστηκα", "κουρασμένος", "νυστάζω"]
        }

    def analyze_text(self, text):
        text = text.lower()
        scores = {k: 0 for k in self.keywords.keys()}

        for emotion, words in self.keywords.items():
            for w in words:
                if re.search(rf"\b{w}\b", text):
                    scores[emotion] += 1

        if not any(scores.values()):
            return "neutral", 0.0

        dominant = max(scores, key=scores.get)
        intensity = np.clip(scores[dominant] / 3.0, 0.1, 1.0)
        return dominant, float(intensity)
