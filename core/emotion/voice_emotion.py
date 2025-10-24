# -*- coding: utf-8 -*-
"""
voice_emotion.py
----------------
Αναλυτής συναισθήματος βασισμένος στο περιεχόμενο φωνής ή κειμένου.
Προς το παρόν text-based (θα επεκταθεί σε ανάλυση ήχου στο μέλλον).
"""

from typing import Tuple

class VoiceEmotionAnalyzer:
    """
    Αναγνωρίζει βασικά συναισθήματα (χαρά, λύπη, θυμός, φόβος, έκπληξη)
    με βάση λέξεις–κλειδιά στο κείμενο ή από υποσύστημα φωνής.
    Επιστρέφει (emotion, intensity).
    """

    def __init__(self):
        self.patterns = {
            "joy": [
                "χαρά", "χαίρομαι", "τέλεια", "φανταστικά", "υπέροχα", "τέλειο",
                "χαρούμενος", "ευτυχία", "σούπερ"
            ],
            "sadness": [
                "λυπάμαι", "στεναχωρήθηκα", "θλίψη", "κουρασμένος", "κατάθλιψη",
                "μόνος", "βαριέμαι", "δεν μπορώ"
            ],
            "anger": [
                "θυμός", "θυμωμένος", "εκνευρισμένος", "νεύρα", "γαμώ", "σκατά",
                "άι", "άντε", "παλιο"
            ],
            "fear": [
                "φοβάμαι", "ανησυχώ", "τρομάζω", "πανικός", "άγχος"
            ],
            "surprise": [
                "ουάου", "σοβαρά", "πραγματικά", "απίστευτο", "δεν το πιστεύω"
            ]
        }

    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Ανάλυση συναισθήματος με βάση το κείμενο.
        Επιστρέφει (emotion, intensity).
        """
        text_lower = text.lower()
        scores = {emotion: 0 for emotion in self.patterns}

        for emotion, words in self.patterns.items():
            for w in words:
                if w in text_lower:
                    scores[emotion] += 1

        # εύρεση του πιο πιθανού συναισθήματος
        emotion = max(scores, key=scores.get)
        intensity = min(1.0, scores[emotion] / 3.0)

        if scores[emotion] == 0:
            emotion, intensity = "neutral", 0.0

        return emotion, intensity
