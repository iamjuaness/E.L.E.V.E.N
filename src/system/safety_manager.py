from src.config.settings import Settings
from src.utils.logger import logger

class SafetyManager:
    """
    Ensures that the assistant doesn't execute dangerous commands without approval.
    """
    
    FORBIDDEN_COMMANDS = [
        "rm -rf", "format", "del /s", "rd /s", "shutdown", "restart-computer",
        "mkfs", "dd", ":(){ :|:& };:"
    ]
    
    SENSITIVE_COMMANDS = [
        "del", "rm", "move", "install", "pip install", "npm install",
        "kill", "taskkill", "reg", "net user"
    ]

    def validate_command(self, command):
        """
        Validate if a command is safe to execute.
        Returns:
            bool: True if safe, False if dangerous/requires confirmation
            str: Reason/Warning message
        """
        if not Settings.SAFE_MODE:
            return True, "Safe mode disabled"
            
        command = command.lower()
        
        # Check for strictly forbidden commands
        for forbidden in self.FORBIDDEN_COMMANDS:
            if forbidden in command:
                logger.warning(f"Blocked forbidden command: {command}")
                return False, f"Command contains forbidden keyword: {forbidden}"
                
        # Check for sensitive commands
        for sensitive in self.SENSITIVE_COMMANDS:
            if sensitive in command:
                logger.info(f"Flagged sensitive command: {command}")
                return False, f"Command requires confirmation: {sensitive}"
                
        return True, "Command appears safe"

    def request_confirmation(self, command, reason):
        """
        Request user confirmation for a command.
        In a real GUI app, this would pop up a dialog.
        For now, we might rely on voice confirmation.
        """
        # This logic will be handled by the main loop/dialogue manager
        pass
