import sqlite3
import os
import datetime

class EpisodicMemory:
    """
    Καταγράφει εμπειρίες της Ζένιας: γεγονότα, context, συναισθήματα, συμμετέχοντες.
    """
    def __init__(self, db_path="data/memory_system.db3"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            event_type TEXT,
            content TEXT,
            emotion TEXT,
            importance REAL
        );
        """)
        self.conn.commit()

    def store_event(self, user, event_type, content, emotion="neutral", importance=0.5):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO episodic_memory (timestamp, user, event_type, content, emotion, importance)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.datetime.now().isoformat(), user, event_type, content, emotion, importance))
        self.conn.commit()

    def recall_recent(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM episodic_memory ORDER BY id DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()
