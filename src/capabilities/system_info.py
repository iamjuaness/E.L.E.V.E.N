import psutil
import platform
from src.utils.logger import logger

class SystemInfo:
    """
    Retrieves information about the system hardware and status.
    """
    
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)
        
    def get_memory_usage(self):
        mem = psutil.virtual_memory()
        return {
            "total": f"{mem.total / (1024**3):.2f} GB",
            "available": f"{mem.available / (1024**3):.2f} GB",
            "percent": mem.percent
        }
        
    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return {
            "total": f"{disk.total / (1024**3):.2f} GB",
            "free": f"{disk.free / (1024**3):.2f} GB",
            "percent": disk.percent
        }
        
    def get_battery_status(self):
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged
            }
        return None

    def get_system_summary(self):
        """Get a text summary of system status for the LLM"""
        cpu = self.get_cpu_usage()
        mem = self.get_memory_usage()
        disk = self.get_disk_usage()
        
        summary = f"System Status: CPU {cpu}%, RAM {mem['percent']}% used ({mem['available']} free), Disk {disk['percent']}% used."
        return summary
