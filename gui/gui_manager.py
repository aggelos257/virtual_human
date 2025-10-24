import threading
import time

class GUIManager:
    """
    GUI Manager της Ζένιας — διαχειρίζεται οπτικές και διεπαφικές λειτουργίες.
    Υποστηρίζει reasoning_manager, audio_manager, emotion_engine και persona_profile.
    """

    def __init__(self, audio_manager=None, reasoning_manager=None, emotion_engine=None, persona_profile=None):
        """
        Αρχικοποιεί το GUI subsystem.
        """
        self.audio_manager = audio_manager
        self.reasoning_manager = reasoning_manager
        self.emotion_engine = emotion_engine
        self.persona_profile = persona_profile
        self._is_running = False
        self._gui_thread = None

    def start(self):
        """
        Εκκινεί το GUI Manager σε ξεχωριστό thread για να μην μπλοκάρει τα υπόλοιπα υποσυστήματα.
        """
        if not self._is_running:
            self._is_running = True
            self._gui_thread = threading.Thread(target=self._run, daemon=True)
            self._gui_thread.start()
            print("🖼️ [GUIManager] Το GUI ξεκίνησε επιτυχώς.")

    def _run(self):
        """
        Βασικός βρόχος λειτουργίας του GUI.
        Εδώ μπορεί να υλοποιηθεί η οπτικοποίηση συναισθημάτων, reasoning feedback κ.λπ.
        """
        while self._is_running:
            # Αν υπάρχουν δεδομένα reasoning, μπορούμε να τα εμφανίσουμε ή να τα χρησιμοποιήσουμε
            if self.reasoning_manager is not None:
                # Ενδεικτικά: μπορούμε να διαβάζουμε ενεργή κατάσταση reasoning
                pass

            if self.emotion_engine is not None:
                # Π.χ. ενημέρωση avatar με βάση το συναίσθημα
                pass

            time.sleep(0.05)  # Μικρό delay για αποφυγή υπερφόρτωσης CPU

    def stop(self):
        """
        Διακόπτει τη λειτουργία του GUI Manager.
        """
        self._is_running = False
        if self._gui_thread and self._gui_thread.is_alive():
            self._gui_thread.join(timeout=1.0)
        print("🛑 [GUIManager] Το GUI σταμάτησε.")

    def update_persona(self, new_persona):
        """
        Ενημέρωση του persona_profile δυναμικά.
        """
        self.persona_profile = new_persona
        print("👤 [GUIManager] Persona profile ενημερώθηκε.")

    def is_running(self):
        """
        Επιστρέφει True αν το GUI εκτελείται.
        """
        return self._is_running
