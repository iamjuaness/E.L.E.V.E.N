import subprocess
from src.utils.logger import logger
from src.system.safety_manager import SafetyManager

class CommandExecutor:
    def __init__(self):
        self.safety = SafetyManager()
        
    def execute(self, command, confirm=False):
        """
        Execute a system command.
        Args:
            command (str): The command to execute
            confirm (bool): Whether the user has explicitly confirmed it
        """
        # Validate safety
        is_safe, reason = self.safety.validate_command(command)
        
        if not is_safe and not confirm:
            logger.warning(f"Command blocked: {reason}")
            return f"I cannot execute that command without confirmation. Reason: {reason}"
            
        try:
            logger.info(f"Executing command: {command}")
            
            # Execute command
            # using shell=True is necessary for many commands but has security risks
            # handled by SafetyManager
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                logger.info(f"Command output: {output}")
                return output if output else "Command executed successfully."
            else:
                error = result.stderr.strip()
                logger.error(f"Command failed: {error}")
                return f"Error executing command: {error}"
                
        except subprocess.TimeoutExpired:
            logger.error("Command timed out")
            return "Command timed out."
        except Exception as e:
            logger.error(f"Exception executing command: {e}")
            return f"Failed to execute command: {e}"
