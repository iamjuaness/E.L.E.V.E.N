import sys
import os
import time
import threading

# Add project root to sys.path to allow running as script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import Settings
from src.utils.logger import logger
from src.gui.interface import SettingsGUI

def run_assistant():
    """
    Main assistant logic to be run in a separate thread.
    """
    try:
        logger.info(f"Starting {Settings.ASSISTANT_NAME}...")
        
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
        from src.system.file_manager import FileSystemManager
        from src.audio.wake_word import WakeWordListener
        
        audio = AudioManager()
        llm = LLMClient()
        classifier = IntentClassifier(llm)
        executor = CommandExecutor()
        windows = WindowsController()
        sys_info = SystemInfo()
        browser = WebBrowser()
        vision = VisionSystem(llm)
        file_manager = FileSystemManager()
        wake_word = WakeWordListener()
        
        conversation_active = False
        last_interaction = time.time()
        
        logger.info(f"{Settings.ASSISTANT_NAME} is ready. Say 'Hey {Settings.ASSISTANT_NAME}' to start.")
        
        # Main loop
        while True:
            try:
                # 0. Wait for Wake Word
                if not conversation_active:
                    logger.info("Esperando wake word inicial...")
                    if not wake_word.listen_for_wake_word():
                        continue
                    conversation_active = True
                    last_interaction = time.time()  # Reset timer on activation
                    audio.speak("Activado. ¿En qué puedo ayudarte?")
                else:
                    logger.info("Escuchando comando continuo...")
                
                # 1. Wake up sound
                audio.play_sound("listening")
                
                # 2. Listen for actual command
                user_text = audio.listen()
                if not user_text:
                    continue
                
                # Check for sleep command BEFORE timeout
                if any(word in user_text.lower() for word in ["duerme", "duérmete", "sleep", "descansa"]):
                    conversation_active = False
                    audio.speak("Entendido. Me duermo.")
                    continue

                # Check for SHUTDOWN command
                if any(word in user_text.lower() for word in ["apagar sistema", "apágate", "cerrar programa", "shutdown system", "terminate"]):
                    audio.speak("Apagando sistemas. Hasta luego.")
                    logger.info("Shutdown command received.")
                    os._exit(0) # Force exit
                
                # Update interaction time AFTER receiving input
                last_interaction = time.time()
                
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
                        elif cmd_name == "open_folder":
                            response_text = file_manager.open_folder(params)
                        elif cmd_name == "create_folder":
                            # Parse location if provided
                            parts = params.split(" en ") if " en " in params else [params, None]
                            response_text = file_manager.create_folder(parts[0], parts[1] if len(parts) > 1 else None)
                        elif cmd_name == "open_file":
                            response_text = file_manager.open_file(params)
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
                            # Fallback: keyword detected but no handler matched - use LLM
                            logger.info("No specific handler found, using LLM for response")
                            response_text = llm.generate_response(user_text)
                
                elif intent["type"] == "chat":
                    # General conversation - use LLM to think and respond
                    logger.info("Chat mode: Using LLM for intelligent response")
                    response_text = llm.generate_response(user_text)
                
                else:
                    # Unknown intent type - default to LLM
                    logger.warning(f"Unknown intent type: {intent.get('type')}, defaulting to chat")
                    response_text = llm.generate_response(user_text)
                
                # 4. Respond with interruption support
                if response_text:
                    from threading import Thread, Event
                    
                    interruption_detected = Event()
                    new_command = [None]  # Use list to allow modification in thread
                    
                    def monitor_interruption():
                        """Monitor for user interruptions while speaking"""
                        import time
                        while audio.is_speaking() and not interruption_detected.is_set():
                            # Check for interruption every 0.1 seconds for faster response
                            time.sleep(0.1)
                            interrupt_text = audio.recognizer.listen_for_interruption()
                            if interrupt_text:
                                # Check for stop commands
                                if any(word in interrupt_text for word in ["detente", "para", "stop", "cállate", "espera", "silencio"]):
                                    logger.info("Stop command detected, halting speech")
                                    audio.stop_speaking()
                                    interruption_detected.set()
                                    break
                                else:
                                    # New command while speaking
                                    logger.info(f"New command while speaking: {interrupt_text}")
                                    audio.stop_speaking()
                                    new_command[0] = interrupt_text
                                    interruption_detected.set()
                                    break
                    
                    # Start monitoring in background
                    monitor_thread = Thread(target=monitor_interruption, daemon=True)
                    monitor_thread.start()
                    
                    # Speak the response
                    audio.speak(response_text)
                    logger.info(f"Assistant: {response_text}")
                    
                    # Wait for monitoring to finish
                    monitor_thread.join(timeout=0.5)
                    
                    # If there was a new command during speech, process it
                    if new_command[0]:
                        user_text = new_command[0]
                        continue  # Go back to process the new command
                
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                audio.speak("Lo siento, ocurrió un error. Intenta de nuevo.")
                
    except Exception as e:
        logger.critical(f"Critical error starting application: {e}")

def main():
    """Main entry point for ELEVEN"""
    # Load settings FIRST so GUI gets correct values
    try:
        Settings.load()
        Settings.validate()
    except Exception as e:
        logger.error(f"Error loading settings on startup: {e}")

    # Check if GUI is enabled (default to True now)
    enable_gui = os.getenv("ENABLE_GUI", "true").lower() == "true"
    
    if enable_gui:
        logger.info("Starting in GUI mode...")
        app = SettingsGUI(on_start_assistant=run_assistant)
        app.run()
    else:
        logger.info("Starting in Headless mode...")
        run_assistant()

if __name__ == "__main__":
    main()
