# core/context_memory.py
import time

class ContextMemory:
    """Μνήμη λογικής — θυμάται τι έγινε πρόσφατα (apps, intents, δράσεις)."""

    def __init__(self):
        self.memory = []

    def remember(self, intent: str, entity: str = None, result: str = None):
        """Αποθηκεύει τι έκανε η Ζένια."""
        self.memory.append({
            "timestamp": time.time(),
            "intent": intent or "",
            "entity": entity or "",
            "result": result or ""
        })
        if len(self.memory) > 50:
            self.memory.pop(0)

    def last_action(self):
        """Επιστρέφει την τελευταία ενέργεια."""
        return self.memory[-1] if self.memory else None

    def find_recent(self, keyword: str):
        """Βρίσκει πρόσφατη ενέργεια σχετική με λέξη."""
        for entry in reversed(self.memory):
            if keyword.lower() in entry["entity"].lower() or keyword.lower() in entry["intent"].lower():
                return entry
        return None

    def clear(self):
        self.memory.clear()
