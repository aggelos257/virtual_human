import datetime

class EmotionState:
    """
    Εσωτερική συναισθηματική κατάσταση της Ζένια.
    Διατηρεί ενεργό συναίσθημα, ένταση και ιστορικό αλλαγών.
    """
    def __init__(self):
        self.current_emotion = "neutral"
        self.intensity = 0.0
        self.history = []

    def update(self, emotion, intensity=0.5):
        self.current_emotion = emotion
        self.intensity = max(0.0, min(1.0, intensity))
        self.history.append((datetime.datetime.now().isoformat(), emotion, intensity))
        if len(self.history) > 50:
            self.history = self.history[-50:]

    def get_emotion(self):
        return self.current_emotion, self.intensity
