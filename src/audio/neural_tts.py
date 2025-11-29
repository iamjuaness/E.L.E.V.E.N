import asyncio
import edge_tts
import pygame
import os
import time
from src.config.settings import Settings
from src.utils.logger import logger

class NeuralTTS:
    def __init__(self):
        self.voice = Settings.VOICE_NAME
        logger.info(f"NeuralTTS initialized with voice: {self.voice}")
            
        # Initialize pygame mixer for playback
        try:
            pygame.mixer.init()
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")

    async def _generate_audio(self, text, output_file):
        """Generate audio file using edge-tts"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)

    def speak(self, text):
        """Generate and play speech"""
        if not text:
            return

        logger.info(f"Speaking (Neural): {text}")
        
        # Create a temporary file for the audio
        temp_file = os.path.join(Settings.LOGS_DIR, "speech.mp3")
        
        try:
            # Generate audio (run async function synchronously)
            asyncio.run(self._generate_audio(text, temp_file))
            
            # Play audio
            if os.path.exists(temp_file):
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                    
                # Unload to release file lock
                pygame.mixer.music.unload()
                
        except Exception as e:
            logger.error(f"Error in Neural TTS: {e}")
            # Fallback to print if audio fails
            print(f"ELEVEN: {text}")
            
        finally:
            # Cleanup temp file
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                logger.warning(f"Could not remove temp file: {e}")
    
    def stop(self):
        """Stop current speech immediately"""
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                logger.info("Speech stopped")
        except Exception as e:
            logger.error(f"Error stopping speech: {e}")
    
    def is_speaking(self):
        """Check if currently speaking"""
        try:
            return pygame.mixer.music.get_busy()
        except:
            return False

