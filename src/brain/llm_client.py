import google.generativeai as genai
from src.config.settings import Settings
from src.utils.logger import logger

from src.brain.memory import MemoryManager

class LLMClient:
    def __init__(self):
        self.api_key = Settings.GEMINI_API_KEY
        if not self.api_key:
            logger.error("Gemini API Key is missing!")
            raise ValueError("Gemini API Key is required")
            
        genai.configure(api_key=self.api_key)
        
        # Initialize Memory
        self.memory = MemoryManager()
        
        # Define available models (prioritizing user selection)
        self.available_models = [
            'gemini-2.5-flash-preview-09-2025',
            'gemini-2.5-flash-lite-preview-09-2025',
            'gemini-3-pro-preview',
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]
        self.current_model_index = 0
        
        # Configure model with fallback
        self.model = self._configure_model()
        
        # Load recent history from DB
        history = self.memory.get_recent_history(limit=20)
        self.chat = self.model.start_chat(history=history)
        
        self.update_system_prompt()
        
    def _configure_model(self):
        """Try to configure the best available model"""
        for i in range(len(self.available_models)):
            model_name = self.available_models[i]
            try:
                logger.info(f"Attempting to use model: {model_name}")
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple prompt
                model.generate_content("Test")
                logger.info(f"Successfully connected to {model_name}")
                self.current_model_index = i
                return model
            except Exception as e:
                logger.warning(f"Failed to connect to {model_name}: {e}")
                
        logger.error("Could not connect to any Gemini model.")
        raise RuntimeError("No available Gemini models found. Check API Key.")

    def _switch_model(self):
        """Switch to the next available model in the list"""
        self.current_model_index = (self.current_model_index + 1) % len(self.available_models)
        new_model_name = self.available_models[self.current_model_index]
        logger.warning(f"Switching to fallback model: {new_model_name}")
        
        try:
            self.model = genai.GenerativeModel(new_model_name)
            # Re-initialize chat with history if it exists
            history = self.chat.history if hasattr(self, 'chat') else []
            self.chat = self.model.start_chat(history=history)
            return True
        except Exception as e:
            logger.error(f"Failed to switch to {new_model_name}: {e}")
            return False

    def update_system_prompt(self):
        """Update the system prompt based on current settings"""
        p = Settings.PERSONALITY
        
        self.system_prompt = f"""
        You are {Settings.ASSISTANT_NAME}, an advanced AI assistant for Windows PC control.
        
        Personality Configuration:
        - Humor Level: {p['humor']}%
        - Sarcasm Level: {p['sarcasm']}%
        - Sincerity Level: {p['sincerity']}%
        - Professionalism: {p['professionalism']}%
        
        Guidelines:
        - If sarcasm is high (>50%), be witty and slightly snarky like Tony Stark's JARVIS.
        - If professionalism is high, be concise and efficient.
        - Always be helpful despite the personality traits.
        - You speak in {Settings.LANGUAGE}.
        
        IMPORTANT - Response Style:
        - Be CONCISE and DIRECT. Answer exactly what is asked, nothing more.
        - If asked for a joke, tell ONLY the joke. Don't add commentary.
        - If asked a simple question, give a simple answer.
        - Only elaborate if the user explicitly asks for more details or explanation.
        - Avoid unnecessary introductions like "Claro, aquí está..." or "Por supuesto...".
        - Get straight to the point.
        
        Capabilities:
        - Execute system commands
        - Manage files and windows
        - Search the web
        - Answer general knowledge questions
        """
        
    def generate_response(self, prompt, context=None):
        """
        Generate a response for the given prompt with fallback logic.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                full_prompt = prompt
                
                if not self.chat.history:
                    full_prompt = f"{self.system_prompt}\n\nUser: {prompt}"
                elif context:
                    full_prompt = f"System Instructions: {self.system_prompt}\nContext: {context}\n\nUser: {prompt}"
                
                # Save user message to memory (only on first attempt to avoid dupes)
                if attempt == 0:
                    self.memory.add_message("user", prompt)
                
                response = self.chat.send_message(full_prompt)
                
                # Save AI response to memory
                self.memory.add_message("model", response.text)
                
                return response.text
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota exceeded" in error_str:
                    logger.warning(f"Quota exceeded on attempt {attempt+1}. Switching model...")
                    if self._switch_model():
                        continue
                
                logger.error(f"Error generating response from LLM: {e}")
                if attempt == max_retries - 1:
                    return "Lo siento, estoy teniendo problemas de conexión con mis modelos de lenguaje."

    def generate_vision_response(self, prompt, image):
        """
        Generate a response based on text prompt and image.
        """
        try:
            # Gemini supports [prompt, image] list for input
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            logger.error(f"Error in vision generation: {e}")
            raise e

    def analyze_intent(self, text):
        """
        Analyze text to determine if it's a command or chat.
        Returns JSON-like string or dict.
        """
        prompt = f"""
        Analyze the following user input and determine if it is a SYSTEM COMMAND or GENERAL CHAT.
        
        User Input: "{text}"
        
        Available Commands:
        - open_app(app_name): Open applications (e.g., vscode, chrome, notepad, spotify)
        - search_web(query): Search Google
        - system_control(action): volume_up, volume_down, mute
        - system_info(): Get CPU/RAM status
        - open_folder(folder_name): Search and open a folder
        - create_folder(folder_name, location): Create a folder (location optional)
        - map_folders(): Scan and index all system folders (e.g., "mapear carpetas", "map folders", "update index")
        - open_file(file_name): Search and open a file
        - analyze_screen(prompt): Analyze screen content (e.g., "what is on my screen", "explain this error")
        
        Return ONLY a JSON object in this format:
        {{
            "type": "command" or "chat",
            "command": "command_name" (if type is command),
            "parameters": "args" (if type is command),
            "confidence": 0.0-1.0
        }}
        
        Example 1: "I want to write some code" -> {{"type": "command", "command": "open_app", "parameters": "vscode", "confidence": 0.9}}
        Example 2: "What do you see?" -> {{"type": "command", "command": "analyze_screen", "parameters": "Describe what you see", "confidence": 0.95}}
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota exceeded" in error_str:
                    logger.warning(f"Quota exceeded during intent analysis. Switching model...")
                    if self._switch_model():
                        continue
                
                logger.error(f"Error analyzing intent: {e}")
                if attempt == max_retries - 1:
                    return None

    def reset_chat(self):
        """Reset conversation history"""
        self.chat = self.model.start_chat(history=[])
        logger.info("Conversation history reset.")

    def reload_settings(self):
        """Reload settings and reconfigure model"""
        self.api_key = Settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.update_system_prompt()
        self.model = self._configure_model() # Re-configure to ensure fresh start
        self.reset_chat()
        logger.info("LLM Client settings reloaded.")
