import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # General
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "ELEVEN")
    LANGUAGE = os.getenv("LANGUAGE", "es-ES")
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Audio
    VOICE_ID = int(os.getenv("VOICE_ID", "0"))
    SPEECH_RATE = 150
    VOLUME = 1.0
    
    # Personality
    PERSONALITY = {
        "humor": 50,
        "sarcasm": 20,
        "sincerity": 100,
        "professionalism": 80
    }
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(os.path.dirname(BASE_DIR), "logs")
    
    # Safety
    SAFE_MODE = os.getenv("SAFE_MODE", "true").lower() == "true"
    
    @staticmethod
    def validate():
        if not Settings.GEMINI_API_KEY:
            print("WARNING: GEMINI_API_KEY not found in .env file")

# Create logs directory if it doesn't exist
if not os.path.exists(Settings.LOGS_DIR):
    os.makedirs(Settings.LOGS_DIR)
