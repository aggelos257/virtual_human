import torch

class Reasoner:
    """
    Πυρήνας Λογικής της Ζένια.
    - Δέχεται device (GPU/CPU) ώστε να μην σκάει ο ReasoningManager.
    - Παρέχει ανάλυση και αναγνώριση πρόθεσης (intent).
    """

    def __init__(self, device=None):
        self.device = device or torch.device("cpu")
        print(f"🧩 [Reasoner] Ενεργοποιήθηκε με συσκευή: {self.device.type}")
        # Placeholder για μελλοντικά νευρωνικά μοντέλα
        self.model = None

    # ------------------------------------------------------------
    # 🔍 Ανάλυση κειμένου
    # ------------------------------------------------------------
    def analyze(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return "⚠️ Άκυρη είσοδος προς ανάλυση."
        return f"🔍 Ανάλυση: «{text.strip().capitalize()}»"

    # ------------------------------------------------------------
    # 🧭 Πρόβλεψη πρόθεσης (intent)
    # ------------------------------------------------------------
    def predict_intent(self, text: str) -> str:
        t = (text or "").lower()
        if any(w in t for w in ["άνοιξε", "open "]):
            return "open_app"
        if any(w in t for w in ["κλείσε", "close "]):
            return "close_app"
        if any(w in t for w in ["παίξε", "βάλε"]) and "μουσ" in t:
            return "play_music"
        if "ώρα" in t:
            return "query_time"
        if "ημερομηνία" in t or "μέρα" in t:
            return "query_date"
        if "www." in t or "http" in t:
            return "open_url"
        return "general_reasoning"

    # ------------------------------------------------------------
    # 🧠 Συλλογισμός βάσει context (προαιρετικό API)
    # ------------------------------------------------------------
    def infer(self, context: dict) -> str:
        if not context:
            return "⚠️ Δεν υπάρχει διαθέσιμο context."
        parts = ", ".join(f"{k}: {v}" for k, v in context.items())
        return f"🧠 Συλλογισμός βάσει δεδομένων: {parts}"
