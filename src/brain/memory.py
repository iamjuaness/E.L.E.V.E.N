import sqlite3
import json
import os
from datetime import datetime
from src.config.settings import Settings
from src.utils.logger import logger

class MemoryManager:
    """
    Manages long-term memory using SQLite.
    Stores conversation history and user preferences.
    """
    
    def __init__(self):
        self.db_path = os.path.join(Settings.BASE_DIR, "brain", "memory.db")
        self._init_db()
        
    def _init_db(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    role TEXT,
                    content TEXT
                )
            ''')
            
            # User Preferences/Facts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS facts (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Memory database initialized.")
        except Exception as e:
            logger.error(f"Failed to init memory DB: {e}")

    def add_message(self, role, content):
        """Add a message to history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO conversations (role, content) VALUES (?, ?)',
                (role, content)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error adding message to memory: {e}")

    def get_recent_history(self, limit=10):
        """Get recent conversation history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?',
                (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            
            # Return in chronological order
            history = [{"role": row[0], "parts": [row[1]]} for row in reversed(rows)]
            return history
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            return []

    def remember_fact(self, key, value):
        """Store a specific fact or preference"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO facts (key, value) VALUES (?, ?)',
                (key, json.dumps(value))
            )
            conn.commit()
            conn.close()
            logger.info(f"Remembered fact: {key} = {value}")
        except Exception as e:
            logger.error(f"Error remembering fact: {e}")

    def recall_fact(self, key):
        """Recall a specific fact"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM facts WHERE key = ?', (key,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            logger.error(f"Error recalling fact: {e}")
            return None
