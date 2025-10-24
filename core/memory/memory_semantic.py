import sqlite3
import os

class SemanticMemory:
    """
    Αποθηκεύει γενική γνώση και σημασιολογικές έννοιες.
    Π.χ. “Η Αθήνα είναι πόλη”, “Ο υπολογιστής έχει CPU”.
    """
    def __init__(self, db_path="data/memory_system.db3"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS semantic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept TEXT,
            category TEXT,
            description TEXT
        );
        """)
        self.conn.commit()

    def add_concept(self, concept, category, description):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO semantic_memory (concept, category, description)
        VALUES (?, ?, ?)
        """, (concept, category, description))
        self.conn.commit()

    def search_concept(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM semantic_memory WHERE concept LIKE ?", (f"%{keyword}%",))
        return cursor.fetchall()

    def close(self):
        self.conn.close()
