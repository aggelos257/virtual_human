import datetime
from core.memory.memory_episodic import EpisodicMemory
from core.memory.memory_semantic import SemanticMemory
from core.emotion.memory_emotional import EmotionalMemory
from core.memory.memory_consolidator import MemoryConsolidator

class MemoryManager:
    """
    Κεντρική μονάδα μνήμης — συντονίζει όλες τις υπομνήμες της Ζένιας.
    """
    def __init__(self):
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.emotional = EmotionalMemory()
        self.consolidator = MemoryConsolidator()

    def store_event(self, event_type, content, emotion="neutral", importance=0.5):
        self.episodic.store_event(
            user="Angelos",
            event_type=event_type,
            content=content,
            emotion=emotion,
            importance=importance
        )

    def learn(self):
        """Εκτελεί ενοποίηση μνήμης (σαν 'ύπνος' για τη Ζένια)."""
        self.consolidator.consolidate()

    def shutdown(self):
        self.episodic.close()
        self.semantic.close()
        self.emotional.close()
