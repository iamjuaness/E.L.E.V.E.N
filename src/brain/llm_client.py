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
        
        # Configure model with fallback
        self.model = self._configure_model()
        
        # Load recent history from DB
        history = self.memory.get_recent_history(limit=20)
        self.chat = self.model.start_chat(history=history)
        
        self.update_system_prompt()
        
    def _configure_model(self):
        """Try to configure the best available model"""
        models_to_try = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-pro-latest',
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]
        
        for model_name in models_to_try:
            try:
                logger.info(f"Attempting to use model: {model_name}")
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple prompt
                model.generate_content("Test")
                logger.info(f"Successfully connected to {model_name}")
                return model
            except Exception as e:
                logger.warning(f"Failed to connect to {model_name}: {e}")
                
        logger.error("Could not connect to any Gemini model.")
        raise RuntimeError("No available Gemini models found. Check API Key.")

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
        
        Capabilities:
        - Execute system commands
        - Manage files and windows
        - Search the web
        - Answer general knowledge questions
        """
        
    def generate_response(self, prompt, context=None):
        """
        Generate a response for the given prompt.
        """
        try:
            full_prompt = prompt
            
            if not self.chat.history:
                full_prompt = f"{self.system_prompt}\n\nUser: {prompt}"
            elif context:
                full_prompt = f"System Instructions: {self.system_prompt}\nContext: {context}\n\nUser: {prompt}"
            
            # Save user message to memory
            self.memory.add_message("user", prompt)
            
            response = self.chat.send_message(full_prompt)
            
            # Save AI response to memory
            self.memory.add_message("model", response.text)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response from LLM: {e}")
            return "Lo siento, tuve un problema al procesar tu solicitud."

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
        
        Return ONLY a JSON object in this format:
        {{
            "type": "command" or "chat",
            "command": "command_name" (if type is command),
            "parameters": "args" (if type is command),
            "confidence": 0.0-1.0
        }}
        
        Example 1: "I want to write some code" -> {{"type": "command", "command": "open_app", "parameters": "vscode", "confidence": 0.9}}
        Example 2: "Who is the president?" -> {{"type": "chat", "confidence": 1.0}}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error analyzing intent: {e}")
            return None

    def reset_chat(self):
        """Reset conversation history"""
        self.chat = self.model.start_chat(history=[])
        logger.info("Conversation history reset.")
