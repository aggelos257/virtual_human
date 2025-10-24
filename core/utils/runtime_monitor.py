# core/runtime_monitor.py
import time
import random

class RuntimeMonitor:
    """
    Παρακολουθεί τη ροή της ομιλίας και αντιδρά λογικά σε timeouts ή παύσεις.
    """

    def __init__(self, timeout=8):
        self.last_input_time = time.time()
        self.timeout = timeout
        self.last_event = None

    # ----------------------------------------------------------
    def update_activity(self):
        """Καλείται κάθε φορά που ο χρήστης μιλά."""
        self.last_input_time = time.time()
        self.last_event = "user_speaking"

    # ----------------------------------------------------------
    def check_timeout(self):
        """Αν περάσει πολύς χρόνος χωρίς είσοδο, επιστρέφει φυσική απάντηση."""
        now = time.time()
        diff = now - self.last_input_time

        if diff > self.timeout:
            self.last_input_time = now
            self.last_event = "timeout"

            responses = [
                "Μάλλον σταμάτησες να μιλάς… Είσαι καλά;",
                "Δεν σε άκουσα για λίγο, θέλεις να συνεχίσουμε;",
                "Έκανες παύση. Σκέφτεσαι κάτι;",
                "Αν θέλεις, μπορώ να περιμένω λίγο ακόμα."
            ]
            return random.choice(responses)

        return None
