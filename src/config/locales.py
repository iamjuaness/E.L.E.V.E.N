# Localization strings for ELEVEN

TRANSLATIONS = {
    "es-ES": {
        # Responses
        "wake_response": "Activado. ¿En qué puedo ayudarte?",
        "sleep_response": "Entendido. Me duermo.",
        "shutdown_response": "Apagando sistemas. Hasta luego.",
        "stopped_response": "Detenido.",
        "mapping_start": "Iniciando mapeo de carpetas. Esto puede tomar varios minutos.",
        "mapping_end": "Mapeo completo. {} carpetas indexadas.",
        "open_gui": "Abriendo interfaz de configuración.",
        "gui_error": "Lo siento, no pude abrir la interfaz.",
        "error_generic": "Lo siento, ocurrió un error.",
        "analyzing_screen": "Analizando pantalla...",
        "vision_prompt": "Describe lo que ves en mi pantalla.",
        "volume_up": "Subiendo volumen",
        "volume_down": "Bajando volumen",
        "mute": "Silenciando",
        "opening": "Abriendo {}",
        "searching": "Buscando {}",
        "option_prefix": "Opción {}: {} en {}",
        "ask_selection": "Di el número de la opción que quieres",
        "invalid_selection": "Número inválido.",
        "no_selection": "No escuché respuesta",
        
        # Keywords (Lowercase)
        "stop_words": ["detente", "detén", "para", "stop", "cállate", "silencio", "basta", "quiet", "shut up"],
        "sleep_words": ["duerme", "duérmete", "sleep", "descansa", "rest"],
        "shutdown_words": ["apagar sistema", "apágate", "cerrar programa", "shutdown", "terminate", "turn off"],
        "map_words": ["mapear carpetas", "map folders", "update index", "actualizar indice"],
        "gui_words": ["mostrar interfaz", "abre la configuración", "show interface", "open settings"],
    },
    "en-US": {
        # Responses
        "wake_response": "Online. How can I help you?",
        "sleep_response": "Understood. Going to sleep.",
        "shutdown_response": "Shutting down systems. Goodbye.",
        "stopped_response": "Stopped.",
        "mapping_start": "Starting folder mapping. This may take a few minutes.",
        "mapping_end": "Mapping complete. {} folders indexed.",
        "open_gui": "Opening settings interface.",
        "gui_error": "Sorry, I couldn't open the interface.",
        "error_generic": "Sorry, an error occurred.",
        "analyzing_screen": "Analyzing screen...",
        "vision_prompt": "Describe what you see on my screen.",
        "volume_up": "Volume up",
        "volume_down": "Volume down",
        "mute": "Muting",
        "opening": "Opening {}",
        "searching": "Searching for {}",
        "option_prefix": "Option {}: {} in {}",
        "ask_selection": "Say the number of the option you want",
        "invalid_selection": "Invalid number.",
        "no_selection": "I didn't hear a response",
        
        # Keywords (Lowercase)
        "stop_words": ["stop", "halt", "silence", "quiet", "shut up", "detente", "para"],
        "sleep_words": ["sleep", "go to sleep", "rest", "duerme"],
        "shutdown_words": ["shutdown", "turn off", "terminate", "apagar"],
        "map_words": ["map folders", "index folders", "update index", "mapear carpetas"],
        "gui_words": ["show interface", "open settings", "open config", "mostrar interfaz"],
    }
}

def get_text(key, lang="es-ES", *args):
    """Get translated text formatted with args"""
    # Fallback to English if lang not found
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en-US"])
    text = lang_dict.get(key, key)
    
    if args:
        try:
            return text.format(*args)
        except:
            return text
    return text

def get_keywords(key, lang="es-ES"):
    """Get list of keywords for a specific action"""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en-US"])
    return lang_dict.get(key, [])
