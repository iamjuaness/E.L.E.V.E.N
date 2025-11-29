import asyncio
import edge_tts
import pygame
import os
import threading
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
        
        # Threading support for non-blocking speech
        self._speaking_thread = None
        self._stop_flag = threading.Event()

    async def _generate_audio(self, text, output_file):
        """Generate audio file using edge-tts"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)

    def speak(self, text):
        """Generate and play speech (non-blocking)"""
        if not text:
            return

        # Stop any ongoing speech first
        self.stop()
        
        # Reset stop flag
        self._stop_flag.clear()
        
        # Start speaking in background thread
        self._speaking_thread = threading.Thread(
            target=self._speak_worker,
            args=(text,),
            daemon=True
        )
        self._speaking_thread.start()
    
    def _speak_worker(self, text):
        """Worker thread for speech generation and playback"""
        logger.info(f"Speaking (Neural): {text}")
        
        # Create a unique temporary file for the audio
        import uuid
        unique_filename = f"speech_{uuid.uuid4().hex}.mp3"
        temp_file = os.path.join(Settings.LOGS_DIR, unique_filename)
        
        try:
            # Generate audio (run async function synchronously)
            asyncio.run(self._generate_audio(text, temp_file))
            
            # Play audio
            if os.path.exists(temp_file):
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Wait for playback to finish, checking stop flag
                while pygame.mixer.music.get_busy() and not self._stop_flag.is_set():
                    pygame.time.Clock().tick(10)
                
                # If stopped, halt playback immediately
                if self._stop_flag.is_set():
                    pygame.mixer.music.stop()
                    logger.info("Speech interrupted by stop flag")
                
                # Unload to release file lock
                pygame.mixer.music.unload()
                
        except Exception as e:
            logger.error(f"Error in Neural TTS: {e}")
            # Fallback to print if audio fails
            print(f"ELEVEN: {text}")
            
        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_file):
                    # Small delay to ensure pygame fully released it
                    import time
                    time.sleep(0.1)
                    os.remove(temp_file)
            except Exception as e:
                logger.warning(f"Could not remove temp file: {e}")
    
    def stop(self):
        """Stop current speech immediately"""
        self._stop_flag.set()
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
            return (self._speaking_thread is not None and 
                    self._speaking_thread.is_alive() and 
                    pygame.mixer.music.get_busy())
        except:
            return False

