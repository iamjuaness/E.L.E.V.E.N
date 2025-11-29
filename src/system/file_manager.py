import os
import subprocess
from pathlib import Path
from src.utils.logger import logger
from src.config.settings import Settings

class FileSystemManager:
    """
    Advanced file system operations with intelligent search.
    """
    
    def __init__(self):
        self.common_paths = [
            Path.home() / "Desktop",
            Path.home() / "Documents",
            Path.home() / "Downloads",
            Path.home() / "Pictures",
            Path.home() / "Videos",
            Path("C:/"),
            Path("D:/") if Path("D:/").exists() else None
        ]
        self.common_paths = [p for p in self.common_paths if p and p.exists()]
        
    def search_folder(self, folder_name, max_depth=4):
        """
        Search for a folder by name across common locations.
        Returns the first match found.
        """
        logger.info(f"Searching for folder: {folder_name}")
        folder_name_lower = folder_name.lower()
        
        for base_path in self.common_paths:
            try:
                for root, dirs, _ in os.walk(base_path):
                    # Limit depth
                    depth = root[len(str(base_path)):].count(os.sep)
                    if depth > max_depth:
                        continue
                        
                    for dir_name in dirs:
                        if folder_name_lower in dir_name.lower():
                            full_path = os.path.join(root, dir_name)
                            logger.info(f"Found folder: {full_path}")
                            return full_path
            except (PermissionError, OSError) as e:
                continue
                
        return None
        
    def open_folder(self, folder_name):
        """
        Search and open a folder in Windows Explorer.
        """
        folder_path = self.search_folder(folder_name)
        
        if folder_path:
            try:
                os.startfile(folder_path)
                return f"Abriendo carpeta: {folder_path}"
            except Exception as e:
                logger.error(f"Error opening folder: {e}")
                return f"No pude abrir la carpeta: {e}"
        else:
            return f"No encontré ninguna carpeta llamada '{folder_name}'"
            
    def create_folder(self, folder_name, location=None):
        """
        Create a folder at the specified location or Desktop by default.
        """
        if location:
            # Try to resolve location
            base_path = self.search_folder(location)
            if not base_path:
                base_path = Path.home() / "Desktop"
        else:
            base_path = Path.home() / "Desktop"
            
        new_folder_path = Path(base_path) / folder_name
        
        try:
            new_folder_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created folder: {new_folder_path}")
            return f"Carpeta creada en: {new_folder_path}"
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return f"No pude crear la carpeta: {e}"
            
    def search_file(self, file_name, max_depth=4):
        """
        Search for a file by name.
        """
        logger.info(f"Searching for file: {file_name}")
        file_name_lower = file_name.lower()
        
        for base_path in self.common_paths:
            try:
                for root, _, files in os.walk(base_path):
                    depth = root[len(str(base_path)):].count(os.sep)
                    if depth > max_depth:
                        continue
                        
                    for file in files:
                        if file_name_lower in file.lower():
                            full_path = os.path.join(root, file)
                            logger.info(f"Found file: {full_path}")
                            return full_path
            except (PermissionError, OSError):
                continue
                
        return None
        
    def open_file(self, file_name):
        """
        Search and open a file with default application.
        """
        file_path = self.search_file(file_name)
        
        if file_path:
            try:
                os.startfile(file_path)
                return f"Abriendo archivo: {file_path}"
            except Exception as e:
                logger.error(f"Error opening file: {e}")
                return f"No pude abrir el archivo: {e}"
        else:
            return f"No encontré ningún archivo llamado '{file_name}'"
