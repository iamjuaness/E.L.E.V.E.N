import pyttsx3
from src.config.settings import Settings
from src.utils.logger import logger

class TextToSpeech:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.configure_voice()
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None

    def configure_voice(self):
        """Configure voice settings based on preferences"""
        if not self.engine:
            return
            
        try:
            voices = self.engine.getProperty('voices')
            # Try to find a voice that matches the language
            selected_voice = None
            
            # Simple heuristic to find a Spanish or English voice
            lang_code = "ES" if "es" in Settings.LANGUAGE.lower() else "EN"
            
            for voice in voices:
                if lang_code in voice.id.upper():
                    selected_voice = voice
                    break
            
            if selected_voice:
                self.engine.setProperty('voice', selected_voice.id)
                logger.info(f"Selected voice: {selected_voice.name}")
            else:
                # Fallback to the configured index if specific language not found
                if len(voices) > Settings.VOICE_ID:
                    self.engine.setProperty('voice', voices[Settings.VOICE_ID].id)
            
            self.engine.setProperty('rate', Settings.SPEECH_RATE)
            self.engine.setProperty('volume', Settings.VOLUME)
            
        except Exception as e:
            logger.error(f"Error configuring voice: {e}")

    def speak(self, text):
        """Convert text to speech"""
        if not self.engine:
            logger.warning("TTS Engine not available. Printing text instead.")
            print(f"ELEVEN: {text}")
            return

        try:
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error during speech: {e}")
