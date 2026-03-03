"""
data/database.py - SQLite storage for session history and stats
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime


DB_PATH = Path.home() / ".smart_file_organizer" / "history.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                folder      TEXT NOT NULL,
                files_moved INTEGER NOT NULL,
                bytes_moved INTEGER NOT NULL,
                moves_json  TEXT NOT NULL,
                created_at  TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()


def save_session(folder: str, files_moved: int, bytes_moved: int, moves: list):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO sessions (folder, files_moved, bytes_moved, moves_json, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (folder, files_moved, bytes_moved, json.dumps(moves), datetime.now().isoformat()))
        # Update cumulative stats
        _increment_stat(conn, "total_files", files_moved)
        _increment_stat(conn, "total_bytes", bytes_moved)
        _increment_stat(conn, "total_sessions", 1)
        conn.execute("INSERT OR REPLACE INTO stats (key, value) VALUES (?, ?)",
                     ("last_run", datetime.now().strftime("%d %b %Y %H:%M")))
        conn.commit()


def _increment_stat(conn, key: str, delta: int):
    row = conn.execute("SELECT value FROM stats WHERE key = ?", (key,)).fetchone()
    current = int(row["value"]) if row else 0
    conn.execute("INSERT OR REPLACE INTO stats (key, value) VALUES (?, ?)", (key, str(current + delta)))


def get_stats() -> dict:
    with get_connection() as conn:
        rows = conn.execute("SELECT key, value FROM stats").fetchall()
        return {r["key"]: r["value"] for r in rows}


def get_recent_sessions(limit: int = 10) -> list:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT folder, files_moved, bytes_moved, created_at FROM sessions ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_last_moves() -> list:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT moves_json FROM sessions ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if row:
            return json.loads(row["moves_json"])
        return []
