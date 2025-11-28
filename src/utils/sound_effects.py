import os
import pygame
import time
import numpy as np
from src.config.settings import Settings
from src.utils.logger import logger

class SoundEffects:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds_dir = os.path.join(Settings.BASE_DIR, "assets", "sounds")
            if not os.path.exists(self.sounds_dir):
                os.makedirs(self.sounds_dir)
        except Exception as e:
            logger.error(f"Failed to initialize SoundEffects: {e}")

    def _generate_beep(self, frequency=440, duration=0.1):
        """Generate a synthesized beep using numpy and pygame"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        # Generate sine wave
        tone = np.sin(2 * np.pi * frequency * t)
        
        # Fade out
        tone *= np.linspace(1, 0, n_samples)
        
        # Convert to 16-bit integer
        audio = (tone * 32767).astype(np.int16)
        
        # Stereo
        audio = np.column_stack((audio, audio))
        
        return pygame.sndarray.make_sound(audio)

    def play(self, sound_name):
        """
        Play a sound effect.
        Args:
            sound_name (str): 'listening', 'processing', 'success', 'error'
        """
        try:
            # Try to load from file first
            file_path = os.path.join(self.sounds_dir, f"{sound_name}.wav")
            
            if os.path.exists(file_path):
                pygame.mixer.Sound(file_path).play()
            else:
                # Fallback to synthesized sounds
                if sound_name == "listening":
                    self._generate_beep(880, 0.1).play()
                elif sound_name == "processing":
                    self._generate_beep(440, 0.05).play()
                elif sound_name == "success":
                    self._generate_beep(1200, 0.15).play()
                elif sound_name == "error":
                    self._generate_beep(200, 0.3).play()
                    
        except Exception as e:
            logger.error(f"Error playing sound {sound_name}: {e}")
