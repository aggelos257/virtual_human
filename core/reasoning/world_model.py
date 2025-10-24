# -*- coding: utf-8 -*-
import os
import sqlite3
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime


class WorldModel:
    """
    Επιμένον world model με SQLite (world_model.db3):
    - entities(id, name, type, attrs_json)
    - relations(id, src_id, rel_type, dst_id, attrs_json)
    - states(id, key, value, updated_at)
    """

    def __init__(self, db_path: Optional[str] = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # default: <project_root>/data/db/world_model.db3
        default_db = os.path.join(base_dir, "data", "db", "world_model.db3")
        self.db_path = db_path or default_db
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS entities(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            type TEXT,
            attrs_json TEXT
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS relations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src_id INTEGER,
            rel_type TEXT,
            dst_id INTEGER,
            attrs_json TEXT,
            UNIQUE(src_id, rel_type, dst_id)
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS states(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT,
            updated_at TEXT
        )""")
        self.conn.commit()

    # ------------- Entities -------------
    def upsert_entity(self, name: str, type_: str = "", attrs_json: str = "{}") -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM entities WHERE name=?", (name,))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE entities SET type=?, attrs_json=? WHERE id=?", (type_, attrs_json, row["id"]))
            self.conn.commit()
            return int(row["id"])
        cur.execute("INSERT INTO entities(name, type, attrs_json) VALUES(?,?,?)", (name, type_, attrs_json))
        self.conn.commit()
        return int(cur.lastrowid)

    def get_entity(self, name: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM entities WHERE name=?", (name,))
        row = cur.fetchone()
        return dict(row) if row else None

    def list_entities(self, type_: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        if type_:
            cur.execute("SELECT * FROM entities WHERE type=? LIMIT ?", (type_, limit))
        else:
            cur.execute("SELECT * FROM entities LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]

    # ------------- Relations -------------
    def upsert_relation(self, src_id: int, rel_type: str, dst_id: int, attrs_json: str = "{}") -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM relations WHERE src_id=? AND rel_type=? AND dst_id=?", (src_id, rel_type, dst_id))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE relations SET attrs_json=? WHERE id=?", (attrs_json, row["id"]))
            self.conn.commit()
            return int(row["id"])
        cur.execute("INSERT INTO relations(src_id, rel_type, dst_id, attrs_json) VALUES(?,?,?,?)",
                    (src_id, rel_type, dst_id, attrs_json))
        self.conn.commit()
        return int(cur.lastrowid)

    def get_relations(self, src_id: Optional[int] = None, rel_type: Optional[str] = None) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        query = "SELECT * FROM relations WHERE 1=1"
        args: Tuple[Any, ...] = tuple()
        if src_id is not None:
            query += " AND src_id=?"
            args += (src_id,)
        if rel_type is not None:
            query += " AND rel_type=?"
            args += (rel_type,)
        cur.execute(query, args)
        return [dict(r) for r in cur.fetchall()]

    # ------------- States -------------
    def set_state(self, key: str, value: str):
        cur = self.conn.cursor()
        now = datetime.utcnow().isoformat()
        cur.execute("INSERT INTO states(key, value, updated_at) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at", (key, value, now))
        self.conn.commit()

    def get_state(self, key: str) -> Optional[str]:
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM states WHERE key=?", (key,))
        row = cur.fetchone()
        return row["value"] if row else None

    def snapshot(self) -> Dict[str, Any]:
        return {
            "entities": self.list_entities(limit=500),
            "relations": self.get_relations(),
            "states": self._all_states()
        }

    def _all_states(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM states")
        return [dict(r) for r in cur.fetchall()]

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
