import sqlite3
import json
from datetime import datetime, timezone
from app.core.config import settings

def get_connection():
    # Remove sqlite:/// prefix if it exists for standard sqlite3
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            status TEXT DEFAULT 'ACTIVE',
            created_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL,
            rationale TEXT NOT NULL,
            sources TEXT NOT NULL,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidate_history (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            title TEXT NOT NULL,
            source_url TEXT NOT NULL,
            fingerprint TEXT,
            decision TEXT NOT NULL,
            score REAL,
            reason TEXT,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    """)
    
    conn.commit()
    conn.close()
