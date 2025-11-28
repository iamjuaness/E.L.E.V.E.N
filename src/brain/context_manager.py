from src.utils.logger import logger

class ContextManager:
    def __init__(self):
        self.history = []
        self.system_state = {}
        
    def add_interaction(self, user_input, ai_response):
        """Add a turn to the conversation history"""
        self.history.append({
            "user": user_input,
            "ai": ai_response
        })
        # Keep history manageable (last 20 turns)
        if len(self.history) > 20:
            self.history.pop(0)
            
    def update_system_state(self, key, value):
        """Update a specific system state value"""
        self.system_state[key] = value
        
    def get_context_string(self):
        """Get a string representation of the current context"""
        context_str = "System State:\n"
        for k, v in self.system_state.items():
            context_str += f"- {k}: {v}\n"
        return context_str

    def clear_history(self):
        self.history = []
