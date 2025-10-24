# -*- coding: utf-8 -*-
import threading
import time
from typing import Optional, Dict, Any, List

from core.perception.vision.face_analyzer import FaceAnalyzer
from core.perception.vision.object_detector import ObjectDetector
from core.perception.vision.gesture_recognizer import GestureRecognizer


class VisionManager:
    """
    Ενοποιεί FaceAnalyzer, ObjectDetector, GestureRecognizer.
    Τρέχει σε δικό του thread και επιστρέφει ενοποιημένη κατάσταση όρασης.
    """

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.face = FaceAnalyzer(camera_index=camera_index)
        self.objects = ObjectDetector(camera_index=camera_index)
        self.gestures = GestureRecognizer(camera_index=camera_index)

        self._state_lock = threading.Lock()
        self._state: Dict[str, Any] = {"face": None, "objects": [], "gestures": []}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        if self._running:
            return
        self._running = True
        self.face.start()
        self.objects.start()
        self.gestures.start()
        self._thread = threading.Thread(target=self._loop, name="VisionLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        self.face.stop()
        self.objects.stop()
        self.gestures.stop()

    def _loop(self):
        while self._running:
            try:
                f = self.face.get_state()      # {"name": str|None, "emotion": str, "confidence": float}
                o = self.objects.get_state()   # [{"label": str, "conf": float}, ...]
                g = self.gestures.get_state()  # [str, str, ...]

                new_state = {"face": f, "objects": o, "gestures": g}
                with self._state_lock:
                    self._state = new_state
            except Exception:
                pass
            time.sleep(0.2)

    def get_state(self) -> Dict[str, Any]:
        with self._state_lock:
            return dict(self._state)
