from src.audio.speech_recognition import SpeechRecognizer
from src.audio.neural_tts import NeuralTTS
from src.utils.sound_effects import SoundEffects
from src.utils.logger import logger

class AudioManager:
    def __init__(self):
        self.recognizer = SpeechRecognizer()
        self.tts = NeuralTTS()
        self.sfx = SoundEffects()
        
    def listen(self):
        """Listen for user input"""
        return self.recognizer.listen()
        
    def speak(self, text):
        """Speak the given text"""
        self.tts.speak(text)
        
    def play_sound(self, name):
        """Play a sound effect"""
        self.sfx.play(name)
    
    def stop_speaking(self):
        """Stop current speech"""
        self.tts.stop()
    
    def is_speaking(self):
        """Check if currently speaking"""
        return self.tts.is_speaking()

