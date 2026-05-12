"""
CloverBot - Database Layer
SQLite-based conversation logging and lead capture.
"""

import aiosqlite
import json
import time
from config import Config


DB_PATH = Config.DB_PATH


async def init_db():
    """Initialize the database tables."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                metadata TEXT DEFAULT '{}'
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                name TEXT DEFAULT '',
                email TEXT DEFAULT '',
                company TEXT DEFAULT '',
                captured_at REAL NOT NULL,
                notes TEXT DEFAULT ''
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS escalations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                visitor_message TEXT NOT NULL,
                escalated_at REAL NOT NULL,
                resolved INTEGER DEFAULT 0
            )
        """)
        await db.execute(
            "CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id)"
        )
        await db.execute(
            "CREATE INDEX IF NOT EXISTS idx_leads_session ON leads(session_id)"
        )
        await db.commit()


async def log_message(session_id, role, content, metadata=None):
    """Log a chat message to the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO conversations (session_id, role, content, timestamp, metadata) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                session_id,
                role,
                content,
                time.time(),
                json.dumps(metadata or {}, ensure_ascii=True),
            ),
        )
        await db.commit()


async def get_conversation_history(session_id, limit=20):
    """Retrieve recent conversation history for a session."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT role, content FROM conversations "
            "WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
            (session_id, limit),
        )
        rows = await cursor.fetchall()
        # Return in chronological order
        return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]


async def save_lead(session_id, name="", email="", company="", notes=""):
    """Save lead information."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO leads (session_id, name, email, company, captured_at, notes) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, name, email, company, time.time(), notes),
        )
        await db.commit()


async def log_escalation(session_id, reason, visitor_message):
    """Log an escalation event."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO escalations (session_id, reason, visitor_message, escalated_at) "
            "VALUES (?, ?, ?, ?)",
            (session_id, reason, visitor_message, time.time()),
        )
        await db.commit()


async def get_recent_conversations(limit=50):
    """Get recent conversations for the admin dashboard."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT session_id, role, content, timestamp FROM conversations "
            "ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_leads(limit=100):
    """Get captured leads."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM leads ORDER BY captured_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
