# -*- coding: utf-8 -*-
import threading
import time
from typing import Optional, Dict, Any

try:
    import psutil
except Exception:
    psutil = None

# Προαιρετικά, για ενεργό παράθυρο στα Windows
try:
    import pygetwindow as gw
except Exception:
    gw = None


class SystemMonitor:
    """
    Ελαφρύ system awareness: CPU/RAM και ενεργό παράθυρο (Windows).
    Αν λείπουν βιβλιοθήκες, γίνεται graceful degradation.
    """

    def __init__(self, interval_sec: float = 1.5):
        self.interval = interval_sec
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._state: Optional[Dict[str, Any]] = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, name="SystemMonitorLoop", daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            try:
                cpu = float(psutil.cpu_percent(interval=None)) if psutil else None
                ram = float(psutil.virtual_memory().percent) if psutil else None
                fg_window = None
                if gw:
                    try:
                        w = gw.getActiveWindow()
                        fg_window = w.title if w else None
                    except Exception:
                        fg_window = None

                self._state = {"cpu": cpu, "ram": ram, "fg_window": fg_window}
            except Exception:
                pass
            time.sleep(self.interval)

    def get_state(self) -> Optional[Dict[str, Any]]:
        return dict(self._state) if self._state else None
