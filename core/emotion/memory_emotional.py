import sqlite3
import os
import datetime

class EmotionalMemory:
    """
    Συνδέει γεγονότα με συναισθήματα και μαθαίνει πώς να αντιδρά συναισθηματικά.
    """
    def __init__(self, db_path="data/memory_system.db3"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emotional_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_ref TEXT,
            emotion TEXT,
            intensity REAL,
            timestamp TEXT
        );
        """)
        self.conn.commit()

    def record_emotion(self, event_ref, emotion, intensity=0.5):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO emotional_memory (event_ref, emotion, intensity, timestamp)
        VALUES (?, ?, ?, ?)
        """, (event_ref, emotion, intensity, datetime.datetime.now().isoformat()))
        self.conn.commit()

    def recall_emotions(self, emotion=None):
        cursor = self.conn.cursor()
        if emotion:
            cursor.execute("SELECT * FROM emotional_memory WHERE emotion=?", (emotion,))
        else:
            cursor.execute("SELECT * FROM emotional_memory ORDER BY id DESC LIMIT 10")
        return cursor.fetchall()

    def close(self):
        self.conn.close()
