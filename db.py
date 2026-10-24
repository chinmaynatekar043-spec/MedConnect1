import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("medical_help.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            provider_type TEXT NOT NULL CHECK(provider_type IN ('Medical Contact', 'Doctor', 'Hospital')),
            specialty TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            emergency INTEGER NOT NULL DEFAULT 0,
            experience_years INTEGER DEFAULT 0,
            qualification TEXT,
            availability TEXT,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS conditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            severity TEXT NOT NULL CHECK(severity IN ('minor', 'major')),
            recommended_specialty TEXT NOT NULL,
            keywords TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            selected_severity TEXT,
            detected_severity TEXT,
            latitude REAL,
            longitude REAL,
            results_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    # Backward-compatible migration for older databases.
    columns = [row[1] for row in cur.execute("PRAGMA table_info(providers)").fetchall()]
    if "is_available" not in columns:
        cur.execute("ALTER TABLE providers ADD COLUMN is_available INTEGER NOT NULL DEFAULT 1")

    conn.commit()
    conn.close()
