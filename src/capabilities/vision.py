import pyautogui
import os
from PIL import Image
from src.config.settings import Settings
from src.utils.logger import logger

class VisionSystem:
    """
    Handles screen capture and visual analysis using Gemini.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.screenshot_path = os.path.join(Settings.LOGS_DIR, "screen_capture.png")
        
    def capture_screen(self):
        """Capture the current screen and save to file"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(self.screenshot_path)
            return self.screenshot_path
        except Exception as e:
            logger.error(f"Failed to capture screen: {e}")
            return None
            
    def analyze_screen(self, prompt="Describe what you see on the screen"):
        """
        Analyze the screen content using Gemini Vision capabilities.
        """
        image_path = self.capture_screen()
        if not image_path:
            return "No pude capturar la pantalla."
            
        try:
            logger.info(f"Analyzing screen with prompt: {prompt}")
            
            # Load image for Gemini
            img = Image.open(image_path)
            
            # Use the LLM client's model directly if exposed, or add a method in LLMClient
            # We'll assume LLMClient has a method for multimodal generation or we access the model
            response = self.llm.generate_vision_response(prompt, img)
            
            return response
        except Exception as e:
            logger.error(f"Error analyzing screen: {e}")
            return "Tuve un problema analizando la imagen."
