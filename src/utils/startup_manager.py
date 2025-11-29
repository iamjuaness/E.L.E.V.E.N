"""
Windows Startup Manager
Handles auto-start configuration via Windows Registry
"""
import winreg
import sys
import os
from src.utils.logger import logger

def get_executable_path():
    """Get the path to the current executable or script"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys.executable
    else:
        # Running as Python script
        return os.path.abspath(sys.argv[0])

def is_startup_enabled():
    """Check if auto-start is enabled in Windows Registry"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        value, _ = winreg.QueryValueEx(key, "ELEVEN")
        winreg.CloseKey(key)
        logger.info(f"Auto-start is enabled: {value}")
        return True
    except FileNotFoundError:
        logger.info("Auto-start is not enabled")
        return False
    except Exception as e:
        logger.error(f"Error checking auto-start status: {e}")
        return False

def enable_startup():
    """Enable auto-start on Windows boot (runs in headless mode)"""
    try:
        exe_path = get_executable_path()
        # Add --no-gui flag to run in headless mode on startup
        command = f'"{exe_path}" --no-gui'
        
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "ELEVEN", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        logger.info(f"Auto-start enabled: {command}")
        return True
    except Exception as e:
        logger.error(f"Error enabling auto-start: {e}")
        return False

def disable_startup():
    """Disable auto-start"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, "ELEVEN")
        winreg.CloseKey(key)
        
        logger.info("Auto-start disabled")
        return True
    except FileNotFoundError:
        logger.info("Auto-start was not enabled")
        return True
    except Exception as e:
        logger.error(f"Error disabling auto-start: {e}")
        return False
