import os
import ctypes
from src.utils.logger import logger

# Constants for Windows API
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

class WindowsController:
    """
    Controls Windows-specific features using pywin32 or ctypes.
    """
    
    def set_volume(self, level):
        """
        Set system volume (0-100).
        Note: This is a simplified implementation. 
        Precise volume control requires pycaw or comtypes.
        For now, we'll use key presses to adjust relative volume.
        """
        # TODO: Implement precise volume control
        pass
        
    def volume_up(self):
        logger.info("Increasing volume")
        ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
        
    def volume_down(self):
        logger.info("Decreasing volume")
        ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)
        
    def mute(self):
        logger.info("Muting volume")
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
        
    def open_app(self, app_name):
        """Open an application by name"""
        logger.info(f"Opening app: {app_name}")
        
        # Common aliases mapping
        app_map = {
            "vscode": "code",
            "visual studio code": "code",
            "chrome": "chrome",
            "google chrome": "chrome",
            "notepad": "notepad",
            "bloc de notas": "notepad",
            "calculator": "calc",
            "calculadora": "calc",
            "spotify": "spotify",
            "explorer": "explorer",
            "explorador": "explorer"
        }
        
        # Normalize app name
        clean_name = app_name.lower().strip()
        cmd = app_map.get(clean_name, clean_name)
        
        try:
            # Use start with empty title argument to handle quotes correctly
            # syntax: start "title" "command"
            os.system(f'start "" "{cmd}"')
        except Exception as e:
            logger.error(f"Error opening app {app_name}: {e}")
        
    def open_url(self, url):
        """Open a URL in default browser"""
        logger.info(f"Opening URL: {url}")
        os.system(f"start {url}")
