from core.memory.memory_episodic import EpisodicMemory
from core.memory.memory_semantic import SemanticMemory
from core.emotion.memory_emotional import EmotionalMemory

class MemoryConsolidator:
    """
    Συνδυάζει τις μνήμες της Ζένιας — μετατρέπει εμπειρίες σε γνώση.
    Π.χ. “Όταν ο Άγγελος είναι κουρασμένος, του αρέσει η ήσυχη μουσική.”
    """
    def __init__(self):
        self.epi = EpisodicMemory()
        self.sem = SemanticMemory()
        self.em = EmotionalMemory()

    def consolidate(self):
        recent = self.epi.recall_recent(20)
        for _, t, u, etype, content, emotion, imp in recent:
            if "μουσική" in content and emotion == "χαρά":
                self.sem.add_concept("μουσική", "προτίμηση", "Η Ζένια συνδέει τη μουσική με ευχαρίστηση.")
            if "κουρασμένος" in content:
                self.sem.add_concept("ξεκούραση", "ανάγκη", "Η Ζένια έμαθε ότι ο Άγγελος χρειάζεται ξεκούραση όταν είναι κουρασμένος.")

    def shutdown(self):
        self.epi.close()
        self.sem.close()
        self.em.close()
