import sys
import os
import time

# Add project root to sys.path to allow running as script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import Settings
from src.utils.logger import logger

def main():
    """Main entry point for ELEVEN"""
    try:
        logger.info(f"Starting {Settings.ASSISTANT_NAME}...")
        Settings.validate()
        
        logger.info("Initializing components...")
        
        # Initialize components
        from src.audio.audio_manager import AudioManager
        from src.brain.llm_client import LLMClient
        from src.brain.intent_classifier import IntentClassifier
        from src.system.command_executor import CommandExecutor
        from src.system.windows_controller import WindowsController
        from src.capabilities.system_info import SystemInfo
        from src.capabilities.web_browser import WebBrowser
        from src.capabilities.vision import VisionSystem
        
        audio = AudioManager()
        llm = LLMClient()
        classifier = IntentClassifier(llm)
        executor = CommandExecutor()
        windows = WindowsController()
        sys_info = SystemInfo()
        browser = WebBrowser()
        vision = VisionSystem(llm)
        
        logger.info(f"{Settings.ASSISTANT_NAME} is ready and listening.")
        audio.speak(f"Hola, soy {Settings.ASSISTANT_NAME}. Estoy listo.")
        
        # Main loop
        while True:
            try:
                # 1. Listen for input
                # audio.play_sound("listening") # Optional: might be too repetitive
                user_text = audio.listen()
                
                if not user_text:
                    continue
                
                audio.play_sound("processing")    
                logger.info(f"User said: {user_text}")
                
                # 2. Classify intent
                intent = classifier.classify(user_text)
                
                # 3. Handle action
                response_text = ""
                
                if intent["type"] == "command":
                    # 1. Try LLM-based command first
                    cmd_name = intent.get("command")
                    params = intent.get("parameters")
                    
                    if cmd_name:
                        logger.info(f"Executing LLM command: {cmd_name} with params: {params}")
                        if cmd_name == "open_app":
                            windows.open_app(params)
                            response_text = f"Abriendo {params}"
                        elif cmd_name == "search_web":
                            response_text = browser.search_google(params)
                        elif cmd_name == "system_control":
                            if params == "volume_up":
                                windows.volume_up()
                                response_text = "Subiendo volumen"
                            elif params == "volume_down":
                                windows.volume_down()
                                response_text = "Bajando volumen"
                            elif params == "mute":
                                windows.mute()
                                response_text = "Silenciando"
                        elif cmd_name == "system_info":
                            response_text = sys_info.get_system_summary()
                        elif cmd_name == "analyze_screen":
                            # Vision capability
                            prompt = params if params else "Describe lo que ves en mi pantalla."
                            audio.speak("Déjame ver...")
                            response_text = vision.analyze_screen(prompt)
                        else:
                            # Unknown LLM command
                            response_text = "No estoy seguro de cómo ejecutar ese comando."

                    # 2. Fallback to Legacy/Keyword matching
                    else:
                        cmd = intent.get("keyword", "")
                        logger.info(f"Executing Legacy command: {cmd}")
                        
                        if any(k in cmd for k in ["ver", "mira", "pantalla", "screen"]):
                             audio.speak("Analizando pantalla...")
                             response_text = vision.analyze_screen("Describe detalladamente qué hay en mi pantalla.")
                        
                        elif any(k in cmd for k in ["abrir", "abre", "open"]):
                            target = user_text.replace("abrir", "").replace("abre", "").replace("open", "").strip()
                            if "google" in target:
                                response_text = browser.open_url("google.com")
                            elif "youtube" in target:
                                response_text = browser.open_url("youtube.com")
                            else:
                                windows.open_app(target)
                                response_text = f"Abriendo {target}"
                                
                        elif any(k in cmd for k in ["buscar", "busca", "search"]):
                            query = user_text.replace("buscar", "").replace("busca", "").replace("search", "").strip()
                            response_text = browser.search_google(query)
                            
                        elif "volumen" in cmd or "volume" in cmd:
                            if "subir" in user_text or "up" in user_text:
                                windows.volume_up()
                                response_text = "Subiendo volumen"
                            elif "bajar" in user_text or "down" in user_text:
                                windows.volume_down()
                                response_text = "Bajando volumen"
                                
                        elif "sistema" in cmd or "system" in cmd:
                            response_text = sys_info.get_system_summary()
    
                        elif any(k in cmd for k in ["configurar", "ajustar", "humor", "sarcasmo", "sinceridad", "set"]):
                            # Parse personality command
                            import re
                            traits = {
                                "humor": "humor", "sarcasmo": "sarcasm", "sarcasm": "sarcasm",
                                "sinceridad": "sincerity", "sincerity": "sincerity",
                                "profesionalismo": "professionalism", "professionalism": "professionalism"
                            }
                            target_trait = None
                            for word, key in traits.items():
                                if word in user_text.lower():
                                    target_trait = key
                                    break
                            
                            value_match = re.search(r'(\d+)%', user_text) or re.search(r'(\d+)', user_text)
                                
                            if target_trait and value_match:
                                new_value = max(0, min(100, int(value_match.group(1))))
                                Settings.PERSONALITY[target_trait] = new_value
                                llm.update_system_prompt()
                                llm.reset_chat()
                                response_text = f"Entendido. He ajustado mi {target_trait} al {new_value}%."
                            else:
                                response_text = "No entendí qué parámetro ajustar."
                        
                        else:
                            # Fallback if keyword detected but no handler matched
                            context = sys_info.get_system_summary()
                            response_text = llm.generate_response(user_text, context=context)
                        
                else:
                    # Chat intent
                    context = sys_info.get_system_summary()
                    response_text = llm.generate_response(user_text, context=context)
                
                # 4. Speak response
                if response_text:
                    audio.speak(response_text)
                
            except KeyboardInterrupt:
                logger.info("Stopping by user request...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                audio.speak("Lo siento, ocurrió un error.")
                
    except Exception as e:
        logger.critical(f"Critical error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
