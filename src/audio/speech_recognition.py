import speech_recognition as sr
from src.config.settings import Settings
from src.utils.logger import logger

import threading

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._lock = threading.Lock()
        
        # Adjust for ambient noise
        with self.microphone as source:
            logger.info("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Ready to listen.")

    def listen(self):
        """Listen for audio input and return text"""
        if not self._lock.acquire(blocking=False):
            # If microphone is busy (e.g. interruption thread), skip
            return None
            
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            logger.info("Processing audio...")
            # Recognize speech using Google Speech Recognition (free tier)
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
        finally:
            self._lock.release()
    
    def listen_for_interruption(self):
        """Ultra-fast listen to detect interruptions"""
        # Try to acquire lock, but don't block if main thread is using it
        if not self._lock.acquire(blocking=False):
            return None
            
        try:
            with self.microphone as source:
                # OPTIMIZED: Reduced timeout for faster interruption detection
                audio = self.recognizer.listen(source, timeout=0.2, phrase_time_limit=1)
                
            # Try to recognize what was said
            text = self.recognizer.recognize_google(audio, language=Settings.LANGUAGE)
            logger.info(f"Interruption detected: {text}")
            return text.lower()
            
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except Exception:
            return None
        finally:
            self._lock.release()


