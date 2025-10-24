# -*- coding: utf-8 -*-
from typing import Tuple

from core.emotion.voice_emotion import VoiceEmotionAnalyzer


class EmotionEngine:
    """
    Ενοποιημένος αναλυτής συναισθήματος:
    - προς το παρόν text-based (VoiceEmotionAnalyzer)
    - μελλοντικά: συνδυασμός με ακουστικά/οπτικά σήματα
    API: process_input(text) -> (prefix_response, emotion, intensity)
    """

    def __init__(self):
        self.text_analyzer = VoiceEmotionAnalyzer()

    def process_input(self, text: str) -> Tuple[str, str, float]:
        emotion, intensity = self.text_analyzer.analyze(text)

        # Επιλογή affective prefix
        if emotion == "joy":
            prefix = "Χαίρομαι που το λες! "
        elif emotion == "sadness":
            prefix = "Σε καταλαβαίνω... "
        elif emotion == "anger":
            prefix = "Ας το λύσουμε ήρεμα. "
        else:
            prefix = ""

        return prefix, emotion, float(intensity)
