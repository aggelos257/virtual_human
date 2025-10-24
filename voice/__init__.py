# -*- coding: utf-8 -*-
"""
voice package initializer
-------------------------
Υποσύστημα φωνής για τη Ζένια.
Φορτώνει αυτόματα τα modules TextToSpeech και SpeechToText.
"""

from .text_to_speech import TextToSpeech
from .speech_to_text import SpeechToText

__all__ = ["TextToSpeech", "SpeechToText"]
