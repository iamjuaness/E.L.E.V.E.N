import os
import sys
import sqlite3
import json
from dotenv import load_dotenv

# Load environment variables (fallback/initial defaults)
load_dotenv()

class Settings:
    # General
    VERSION = "1.2.0"
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "ELEVEN")
    LANGUAGE = os.getenv("LANGUAGE", "es-ES")
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Audio
    VOICE_ID = int(os.getenv("VOICE_ID", "0"))
    VOICE_NAME = os.getenv("VOICE_NAME", "es-ES-AlvaroNeural")
    SPEECH_RATE = 500
    VOLUME = 1.0
    
    # Personality
    PERSONALITY = {
        "humor": 50,
        "sarcasm": 20,
        "sincerity": 80,
        "professionalism": 80
    }
    
    # Paths - Use AppData for persistence when running as .exe
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use AppData for persistence
        APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'eleven')
        BASE_DIR = APP_DATA_DIR
        LOGS_DIR = os.path.join(APP_DATA_DIR, "logs")
        DB_PATH = os.path.join(APP_DATA_DIR, "brain", "memory.db")
    else:
        # Running as Python script - use project directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        LOGS_DIR = os.path.join(os.path.dirname(BASE_DIR), "logs")
        DB_PATH = os.path.join(BASE_DIR, "brain", "memory.db")
    
    # Safety
    SAFE_MODE = os.getenv("SAFE_MODE", "true").lower() == "true"
    
    @staticmethod
    def _get_db_connection():
        return sqlite3.connect(Settings.DB_PATH)

    @staticmethod
    def init_db():
        """Initialize settings table"""
        try:
            # Ensure the brain directory exists
            db_dir = os.path.dirname(Settings.DB_PATH)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            conn = Settings._get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing settings DB: {e}")

    @staticmethod
    def load():
        """Load settings from database, overriding defaults"""
        Settings.init_db()
        try:
            conn = Settings._get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT key, value FROM app_settings')
            rows = cursor.fetchall()
            conn.close()
            
            for key, value in rows:
                if key == "ASSISTANT_NAME":
                    Settings.ASSISTANT_NAME = value
                elif key == "LANGUAGE":
                    Settings.LANGUAGE = value
                elif key == "GEMINI_API_KEY":
                    Settings.GEMINI_API_KEY = value
                elif key == "VOICE_NAME":
                    Settings.VOICE_NAME = value
                elif key == "PERSONALITY":
                    try:
                        Settings.PERSONALITY = json.loads(value)
                    except:
                        pass
            
            print("Settings loaded from database.")
        except Exception as e:
            print(f"Error loading settings from DB: {e}")

    @staticmethod
    def save():
        """Save current settings to database"""
        try:
            conn = Settings._get_db_connection()
            cursor = conn.cursor()
            
            settings_to_save = {
                "ASSISTANT_NAME": Settings.ASSISTANT_NAME,
                "LANGUAGE": Settings.LANGUAGE,
                "GEMINI_API_KEY": Settings.GEMINI_API_KEY,
                "VOICE_NAME": Settings.VOICE_NAME,
                "PERSONALITY": json.dumps(Settings.PERSONALITY)
            }
            
            for key, value in settings_to_save.items():
                cursor.execute(
                    'INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)',
                    (key, value)
                )
            
            conn.commit()
            conn.close()
            print("Settings saved to database.")
        except Exception as e:
            print(f"Error saving settings to DB: {e}")

    @staticmethod
    def validate():
        if not Settings.GEMINI_API_KEY:
            print("WARNING: GEMINI_API_KEY not found in settings")

# Create logs directory if it doesn't exist
if not os.path.exists(Settings.LOGS_DIR):
    os.makedirs(Settings.LOGS_DIR)
