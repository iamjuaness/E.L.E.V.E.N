import speech_recognition as sr
from src.config.settings import Settings
from src.utils.logger import logger

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            logger.info("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Ready to listen.")

    def listen(self):
        """Listen for audio input and return text"""
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            logger.info("Processing audio...")
            # Recognize speech using Google Speech Recognition (free tier)
            # Note: For production, we might want to use a local model (Whisper) or Cloud API
            text = self.recognizer.recognize_google(audio, language=Settings.LANGUAGE)
            logger.info(f"Heard: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            logger.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Speech Recognition service; {e}")
            return None
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None
    
    def listen_for_interruption(self):
        """Quick listen to detect if user is trying to interrupt (non-blocking)"""
        try:
            with self.microphone as source:
                # Increased timeout to 0.5s for better detection
                # phrase_time_limit=3 allows slightly longer stop commands
                audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=3)
                
            # Try to recognize what was said
            text = self.recognizer.recognize_google(audio, language=Settings.LANGUAGE)
            logger.info(f"Interruption detected: {text}")
            return text.lower()
            
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except Exception as e:
            # Don't log every timeout/error to avoid spamming logs during monitoring
            return None


