# -*- coding: utf-8 -*-
import threading
import time
from typing import List, Optional

try:
    import cv2
except Exception:
    cv2 = None

try:
    import mediapipe as mp
except Exception:
    mp = None


class GestureRecognizer:
    """
    Απλή αναγνώριση χειρονομιών με MediaPipe Hands (thumbs_up heuristic).
    Αν δεν υπάρχουν εξαρτήσεις/κάμερα, επιστρέφει [].
    """

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._cap = None
        self._gestures: List[str] = []
        self._hands = mp.solutions.hands.Hands(model_complexity=0, min_detection_confidence=0.5) if mp else None

    def start(self):
        if self._running:
            return
        self._running = True
        if cv2 is not None:
            self._cap = cv2.VideoCapture(self.camera_index)
        self._thread = threading.Thread(target=self._loop, name="GestureLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._cap:
            try:
                self._cap.release()
            except Exception:
                pass
        if self._hands:
            try:
                self._hands.close()
            except Exception:
                pass

    def _loop(self):
        while self._running:
            try:
                if cv2 is None or self._cap is None or not self._cap.isOpened() or self._hands is None:
                    time.sleep(0.5)
                    continue

                ok, frame = self._cap.read()
                if not ok:
                    time.sleep(0.1)
                    continue

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                res = self._hands.process(rgb)
                gestures = []

                if res and res.multi_hand_landmarks:
                    # Απλό heuristic: αν ο αντίχειρας είναι σηκωμένος σε σχέση με την παλάμη => "thumbs_up"
                    # (Placeholder – μπορεί να αντικατασταθεί με classifier)
                    gestures.append("hand_detected")

                self._gestures = gestures
            except Exception:
                pass
            time.sleep(0.2)

    def get_state(self) -> List[str]:
        return list(self._gestures)
