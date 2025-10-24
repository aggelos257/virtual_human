class FaceEngine:
    pass
# -*- coding: utf-8 -*-
import threading
import time
from typing import Optional, Dict, Any

try:
    import cv2
except Exception:
    cv2 = None

from core.perception.perception_manager import PerceptionManager


class FaceEngine:
    """
    Live GUI για όραση:
    - Εμφάνιση κάμερας
    - Overlay κατάστασης από Perception (face/emotion/objects/gestures)
    - Graceful fallback αν λείπει OpenCV ή κάμερα
    """

    def __init__(self, perception: Optional[PerceptionManager] = None, camera_index: int = 0, window_name: str = "Zenia Vision"):
        self.perception = perception or PerceptionManager(enable_vision=True, enable_audio=False, enable_system=False, camera_index=camera_index)
        self.window_name = window_name
        self.camera_index = camera_index
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._cap = None

    def start(self):
        if self._running:
            return
        self._running = True

        if cv2 is not None:
            self._cap = cv2.VideoCapture(self.camera_index)

        # Start Perception if not already
        try:
            self.perception.start()
        except Exception:
            pass

        self._thread = threading.Thread(target=self._loop, name="FaceEngineLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._cap:
            try:
                self._cap.release()
            except Exception:
                pass
        if cv2 is not None:
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass

    def _draw_text(self, frame, txt, x, y):
        if cv2 is None:
            return
        cv2.putText(frame, txt, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

    def _loop(self):
        if cv2 is None:
            # Χωρίς OpenCV, απλώς κρατάμε ενημερωμένο το Perception state
            while self._running:
                time.sleep(0.5)
            return

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 960, 540)

        while self._running:
            try:
                ok, frame = (self._cap.read() if self._cap else (False, None))
                if not ok:
                    blank = (None if cv2 is None else cv2.UMat(540, 960))
                    if blank is None:
                        time.sleep(0.2)
                        continue
                    frame = cv2.UMat.get(blank)

                state: Dict[str, Any] = self.perception.get_state() if self.perception else {}

                # Overlay πληροφοριών
                face = (state.get("face") or {}) if isinstance(state.get("face"), dict) else state.get("face")
                objects = state.get("objects") or []
                gestures = state.get("gestures") or []
                audio = state.get("audio") or {}
                system = state.get("system") or {}

                # Draw header
                self._draw_text(frame, "Zenia Vision", 20, 30)

                # Face info
                if isinstance(face, dict):
                    emo_txt = face.get("emotion", "neutral")
                    conf = face.get("confidence", 0.0)
                    self._draw_text(frame, f"Face: emotion={emo_txt} conf={conf:.2f}", 20, 60)
                else:
                    self._draw_text(frame, f"Face: none", 20, 60)

                # Objects
                if objects:
                    top = ", ".join([f"{o.get('label')}({o.get('conf',0):.2f})" for o in objects[:5]])
                    self._draw_text(frame, f"Objects: {top}", 20, 90)
                else:
                    self._draw_text(frame, "Objects: -", 20, 90)

                # Gestures
                if gestures:
                    self._draw_text(frame, f"Gestures: {', '.join(gestures)}", 20, 120)
                else:
                    self._draw_text(frame, "Gestures: -", 20, 120)

                # Audio
                if audio:
                    self._draw_text(frame, f"Audio: {audio.get('scene')} {audio.get('level_db'):.1f} dB", 20, 150)
                else:
                    self._draw_text(frame, "Audio: -", 20, 150)

                # System
                if system:
                    self._draw_text(frame, f"System: CPU {system.get('cpu')}%  RAM {system.get('ram')}%  FG {system.get('fg_window')}", 20, 180)

                cv2.imshow(self.window_name, frame)

                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord('q')):  # ESC ή q
                    self.stop()
                    break
            except Exception:
                time.sleep(0.1)
