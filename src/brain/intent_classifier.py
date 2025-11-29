
import re
from src.utils.logger import logger

class IntentClassifier:
    """
    Simple rule-based and LLM-assisted intent classifier.
    """
    
    SYSTEM_KEYWORDS = [
        "abrir", "abre", "cerrar", "cierra", "ejecutar", "ejecuta", "buscar", "busca", 
        "reproducir", "pon", "volumen", "brillo", "apagar", "reiniciar", "carpeta", "archivo",
        "open", "close", "run", "search", "play", "volume", "shutdown",
        "configurar", "ajustar", "humor", "sarcasmo", "sinceridad", "configure", "set",
        "ver", "mira", "pantalla", "screen", "look", "see"
    ]
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
    def classify(self, text):
        """
        Classify the user intent.
        Returns:
            dict: {'type': 'command'|'chat', 'confidence': float, 'action': str}
        """
        text_lower = text.lower()
        
        # 1. LLM Classification FIRST (Smarter, handles natural language)
        # This allows the assistant to understand requests like "cuéntame un chiste"
        try:
            logger.info("Analyzing intent with LLM...")
            analysis = self.llm.analyze_intent(text)
            
            if analysis:
                import json
                # Clean up json string if needed (remove markdown code blocks)
                analysis = analysis.replace("```json", "").replace("```", "").strip()
                
                result = json.loads(analysis)
                logger.info(f"LLM classification result: {result}")
                return result
                
        except Exception as e:
            logger.error(f"LLM classification failed: {e}, falling back to keyword matching")
        
        # 2. Fallback to Keyword Matching (only if LLM fails)
        for keyword in self.SYSTEM_KEYWORDS:
            if keyword in text_lower:
                logger.info(f"Intent classified as COMMAND via keyword: {keyword}")
                return {"type": "command", "confidence": 0.7, "keyword": keyword}
    
        # 3. Default to chat if nothing else matches
        logger.info("Intent classified as CHAT (default)")
        return {"type": "chat", "confidence": 0.9}

