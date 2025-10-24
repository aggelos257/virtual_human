# -*- coding: utf-8 -*-
import threading
import time
from typing import Optional, Dict, Any

try:
    import cv2  # OpenCV
except Exception:
    cv2 = None

try:
    import mediapipe as mp
except Exception:
    mp = None


class FaceAnalyzer:
    """
    Βασική αναγνώριση/εντοπισμός προσώπου + απλή απόδοση συναισθήματος (heuristics).
    Σχεδιασμένο ώστε να λειτουργεί *ακόμη κι αν* λείπουν εξαρτήσεις: κάνει graceful degradation.
    """

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._state: Dict[str, Any] = {"name": None, "emotion": "neutral", "confidence": 0.0}
        self._cap = None
        self._mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) if mp else None

    def start(self):
        if self._running:
            return
        self._running = True
        if cv2 is not None:
            self._cap = cv2.VideoCapture(self.camera_index)
        self._thread = threading.Thread(target=self._loop, name="FaceAnalyzerLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._cap:
            try:
                self._cap.release()
            except Exception:
                pass
        if self._mp_face:
            try:
                self._mp_face.close()
            except Exception:
                pass

    def _loop(self):
        while self._running:
            try:
                if cv2 is None or self._cap is None or not self._cap.isOpened() or self._mp_face is None:
                    # Χωρίς κάμερα/βιβλιοθήκες, παραμένουμε ουδέτεροι
                    time.sleep(0.5)
                    continue

                ok, frame = self._cap.read()
                if not ok:
                    time.sleep(0.1)
                    continue

                # Mediapipe face detection
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                res = self._mp_face.process(rgb)

                if res and res.detections:
                    # Δεν κάνουμε identification (privacy). Θεωρούμε default "Angelos?" αν ένα πρόσωπο είναι σταθερό.
                    conf = float(res.detections[0].score[0])
                    emotion = "neutral"
                    # Πολύ απλά heuristics συναισθήματος βάσει bbox size (placeholder – μπορεί να αντικατασταθεί με μοντέλο)
                    if conf > 0.8:
                        emotion = "calm"
                    state = {"name": None, "emotion": emotion, "confidence": conf}
                else:
                    state = {"name": None, "emotion": "neutral", "confidence": 0.0}

                self._state = state

            except Exception:
                pass
            time.sleep(0.1)

    def get_state(self) -> Dict[str, Any]:
        return dict(self._state)
