import threading
import time

class GUIManager:
    """
    GUI Manager της Ζένιας — διαχειρίζεται οπτικές και διεπαφικές λειτουργίες.
    """

    def __init__(self, audio_manager=None, reasoning_manager=None, emotion_engine=None, persona_profile=None, tts=None, listener=None):
        self.audio_manager = audio_manager
        self.reasoning_manager = reasoning_manager
        self.emotion_engine = emotion_engine
        self.persona_profile = persona_profile
        self.tts = tts
        self.listener = listener
        self._is_running = False
        self._gui_thread = None

    def start_voice_interface(self, tts, stt, reasoning_manager):
        """
        Εκκινεί το GUI Voice Interface με TTS/STT/Reasoning.
        """
        self.tts = tts
        self.listener = stt
        self.reasoning_manager = reasoning_manager
        self.start()
        print("🖼️ [GUIManager] Voice interface ενεργοποιήθηκε.")

    def stop_voice_interface(self):
        """
        Σταματά το GUI Voice Interface.
        """
        self.stop()
        print("🛑 [GUIManager] Voice interface απενεργοποιήθηκε.")

    def start(self):
        """
        Εκκινεί το GUI σε ξεχωριστό thread.
        """
        if not self._is_running:
            self._is_running = True
            self._gui_thread = threading.Thread(target=self._run, daemon=True)
            self._gui_thread.start()
            print("🖼️ [GUIManager] Το GUI ξεκίνησε.")

    def _run(self):
        """
        Κυρίως βρόχος λειτουργίας GUI.
        """
        while self._is_running:
            # εδώ μπορεί να προστεθεί animation, visualization TTS/STT
            time.sleep(0.05)

    def stop(self):
        """
        Διακόπτει τη λειτουργία του GUI.
        """
        self._is_running = False
        if self._gui_thread and self._gui_thread.is_alive():
            self._gui_thread.join(timeout=1.0)
        print("🖼️ [GUIManager] Το GUI σταμάτησε.")

    def is_running(self):
        return self._is_running
