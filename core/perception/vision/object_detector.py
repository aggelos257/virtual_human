# -*- coding: utf-8 -*-
import threading
import time
from typing import List, Dict, Any, Optional

try:
    import cv2
except Exception:
    cv2 = None

# Προαιρετικό YOLO (ultralytics). Αν λείπει, γυρνάει κενή λίστα.
try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


class ObjectDetector:
    """
    Ανίχνευση αντικειμένων (YOLO). Αν λείπουν οι εξαρτήσεις, απλά επιστρέφει [].
    """

    def __init__(self, camera_index: int = 0, model_name: str = "yolov8n.pt"):
        self.camera_index = camera_index
        self.model_name = model_name
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._cap = None
        self._state: List[Dict[str, Any]] = []

        self._model = None
        if YOLO is not None:
            try:
                self._model = YOLO(model_name)
            except Exception:
                self._model = None

    def start(self):
        if self._running:
            return
        self._running = True
        if cv2 is not None:
            self._cap = cv2.VideoCapture(self.camera_index)
        self._thread = threading.Thread(target=self._loop, name="ObjectDetectorLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._cap:
            try:
                self._cap.release()
            except Exception:
                pass

    def _loop(self):
        while self._running:
            try:
                if cv2 is None or self._cap is None or not self._cap.isOpened() or self._model is None:
                    time.sleep(0.5)
                    continue

                ok, frame = self._cap.read()
                if not ok:
                    time.sleep(0.1)
                    continue

                results = self._model(frame, verbose=False)
                objs = []
                try:
                    for r in results:
                        for b in r.boxes:
                            cls_id = int(b.cls[0])
                            conf = float(b.conf[0])
                            label = r.names.get(cls_id, f"cls_{cls_id}")
                            if conf >= 0.4:
                                objs.append({"label": label, "conf": conf})
                except Exception:
                    pass

                self._state = objs
            except Exception:
                pass
            time.sleep(0.2)

    def get_state(self) -> List[Dict[str, Any]]:
        return list(self._state)
