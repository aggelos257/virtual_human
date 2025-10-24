import time

class ContextManager:
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.history = []

    def add(self, role: str, text: str):
        self.history.append({"role": role, "text": text, "ts": time.time()})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history = []
