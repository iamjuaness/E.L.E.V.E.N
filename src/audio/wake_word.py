import speech_recognition as sr
from src.utils.logger import logger
from src.config.settings import Settings

class WakeWordListener:
    """
    Simple Wake Word detection using SpeechRecognition.
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_words = [Settings.ASSISTANT_NAME.lower(), "hey " + Settings.ASSISTANT_NAME.lower(), "oye " + Settings.ASSISTANT_NAME.lower()]
        
        # Adjust for ambient noise on init
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def listen_for_wake_word(self):
        """
        Listen continuously until the wake word is detected.
        Returns:
            bool: True if wake word detected
        """
        logger.info(f"Waiting for wake word: {self.wake_words}...")
        
        with self.microphone as source:
            try:
                # Short timeout to keep loop responsive
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                try:
                    # Use Google for now (online) - simplest for prototype
                    # For production, we'd use Vosk or Porcupine (offline)
                    text = self.recognizer.recognize_google(audio, language=Settings.LANGUAGE).lower()
                    logger.debug(f"Heard in standby: {text}")
                    
                    if any(word in text for word in self.wake_words):
                        logger.info("Wake word detected!")
                        return True
                        
                except sr.UnknownValueError:
                    pass # Silence
                except sr.RequestError:
                    logger.warning("Network error in wake word detection")
                    
            except sr.WaitTimeoutError:
                pass
                
        return False
