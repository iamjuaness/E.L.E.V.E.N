import speech_recognition as sr
from difflib import SequenceMatcher
from src.utils.logger import logger
from src.config.settings import Settings

class WakeWordListener:
    """
    Improved Wake Word detection with fuzzy matching and phonetic variations.
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Phonetic variations for better recognition
        self.wake_word_variations = {
            'eleven': ['eleven', 'ileven', 'elevan', 'eleben', 'ilebén', 'ileben', 'lebén'],
            'once': ['once', 'onse', 'onze', '11'],
            'hey': ['hey', 'ei', 'ay', 'he', 'ey'],
            'oye': ['oye', 'oi', 'hoye', 'olle', 'oy']
        }
        
        # Build all possible wake word combinations
        assistant_variations = self.wake_word_variations.get(Settings.ASSISTANT_NAME.lower(), [Settings.ASSISTANT_NAME.lower()])
        # Also include 'once' variations if assistant name is Eleven
        if Settings.ASSISTANT_NAME.lower() == 'eleven':
            assistant_variations.extend(self.wake_word_variations['once'])

        self.wake_words = []
        
        # Solo el nombre
        self.wake_words.extend(assistant_variations)
        
        # Con "hey" / "oye"
        for prefix in ['hey', 'oye', 'ei', 'oi']:
            for variation in assistant_variations:
                self.wake_words.append(f"{prefix} {variation}")
        
        # Optimized energy threshold for faster detection
        self.recognizer.energy_threshold = 400  # Less sensitive (was 300) to avoid noise
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.2 # More damping (was 0.15)
        self.recognizer.dynamic_energy_ratio = 1.5
        
        # Adjust for ambient noise on init
        with self.microphone as source:
            logger.info("Ajustando para ruido ambiental...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            logger.info(f"Wake words configurados: {list(set(assistant_variations))}")

    def fuzzy_match(self, text, target, threshold=0.7):
        """
        Check if text fuzzy matches target with given threshold.
        Returns True if similarity >= threshold.
        """
        ratio = SequenceMatcher(None, text.lower(), target.lower()).ratio()
        return ratio >= threshold

    def check_wake_word(self, text):
        """
        Check if text contains wake word using fuzzy matching.
        Returns True if wake word is detected.
        """
        text = text.lower().strip()
        
        # First try exact matching (fastest)
        for wake_word in self.wake_words:
            if wake_word in text:
                logger.info(f"✓ Wake word detectado (exacto): '{wake_word}' en '{text}'")
                return True
        
        # Then try fuzzy matching with 70% similarity
        for wake_word in self.wake_words:
            # Check each word in the text
            words = text.split()
            for word in words:
                if self.fuzzy_match(word, wake_word, threshold=0.7):
                    logger.info(f"✓ Wake word detectado (fuzzy): '{wake_word}' ≈ '{word}' en '{text}'")
                    return True
            
            # Also check full phrases for multi-word wake words
            if ' ' in wake_word and self.fuzzy_match(text, wake_word, threshold=0.7):
                logger.info(f"✓ Wake word detectado (fuzzy phrase): '{wake_word}' ≈ '{text}'")
                return True
        
        logger.debug(f"✗ No wake word en: '{text}'")
        return False

    def listen_for_wake_word(self):
        """
        Listen continuously until the wake word is detected.
        Returns:
            bool: True if wake word detected
        """
        with self.microphone as source:
            try:
                # Reduced timeout for faster response
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)
                
                try:
                    # Use Google for recognition
                    text = self.recognizer.recognize_google(audio, language=Settings.LANGUAGE).lower()
                    logger.debug(f"Escuchado en standby: '{text}'")
                    
                    if self.check_wake_word(text):
                        return True
                        
                except sr.UnknownValueError:
                    pass  # Silence or unclear audio
                except sr.RequestError as e:
                    logger.warning(f"Error de red en detección: {e}")
                    
            except sr.WaitTimeoutError:
                pass  # Normal timeout, keep listening
                
        return False
