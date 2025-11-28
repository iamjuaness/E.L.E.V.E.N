
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
        text = text.lower()
        
        # 1. Check for configuration commands (fast path)
        if any(k in text for k in ["configurar", "ajustar", "humor", "sarcasmo", "sinceridad", "set"]):
             return {"type": "config", "confidence": 1.0}

        # 2. LLM Classification (Smarter, for natural language)
        # We try this first for complex queries, or we can use it as fallback.
        # Given the user wants "natural instructions", we prioritize LLM for ambiguous cases.
        
        try:
            logger.info("Analyzing intent with LLM...")
            analysis = self.llm.analyze_intent(text)
            
            if analysis:
                import json
                # Clean up json string if needed (remove markdown code blocks)
                analysis = analysis.replace("```json", "").replace("```", "").strip()
                
                result = json.loads(analysis)
                if result.get("type") == "command":
                    logger.info(f"LLM identified command: {result}")
                    return result
        except Exception as e:
            logger.error(f"LLM classification failed: {e}")
        
        # 3. Fallback to Keyword Matching (Fast but dumb)
        for keyword in self.SYSTEM_KEYWORDS:
            if keyword in text:
                logger.info(f"Intent classified as COMMAND via keyword: {keyword}")
                return {"type": "command", "confidence": 0.8, "keyword": keyword}
    
        logger.info("Intent classified as CHAT")
        return {"type": "chat", "confidence": 0.9}
