import threading
import time

class GUIManager:
    """
    GUI Manager της Ζένιας — διαχειρίζεται οπτικές και διεπαφικές λειτουργίες.
    Υποστηρίζει reasoning_manager, audio_manager, emotion_engine, persona_profile, tts και listener.
    """

    def __init__(self, audio_manager=None, reasoning_manager=None, emotion_engine=None, persona_profile=None, tts=None, listener=None):
        """
        Αρχικοποιεί το GUI subsystem.
        """
        self.audio_manager = audio_manager
        self.reasoning_manager = reasoning_manager
        self.emotion_engine = emotion_engine
        self.persona_profile = persona_profile
        self.tts = tts
        self.listener = listener
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
        Εδώ μπορεί να υλοποιηθεί η οπτικοποίηση reasoning, συναισθημάτων, TTS και Listener.
        """
        while self._is_running:
            if self.reasoning_manager is not None:
                # Reasoning visualization
                pass

            if self.emotion_engine is not None:
                # Visualization συναισθημάτων
                pass

            if self.tts is not None:
                # Ενέργειες κατά την εκφώνηση
                pass

            if self.listener is not None:
                # Ενέργειες κατά την ακρόαση μικροφώνου
                pass

            time.sleep(0.05)

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
