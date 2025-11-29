import os
import subprocess
from pathlib import Path
from src.utils.logger import logger
from src.config.settings import Settings

from src.system.folder_mapper import FolderMapper

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
        self.mapper = FolderMapper()
        
        # Start periodic update automatically
        self.mapper.start_periodic_update()
        
    def search_folder(self, folder_name, max_depth=4):
        """
        Search for a folder by name.
        Uses database mapping first, falls back to os.walk if empty.
        """
        # Try DB first
        matches = self.mapper.search_folders(folder_name)
        if matches:
            return matches[0]
            
        logger.info(f"Searching for folder (fallback): {folder_name}")
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
    
    def search_folder_all(self, folder_name, max_depth=4):
        """
        Search for ALL folders matching the name.
        Uses database mapping for fast results.
        """
        # Try DB first (fast)
        matches = self.mapper.search_folders(folder_name)
        if matches:
            return matches
            
        # Fallback to slow scan if DB empty
        logger.info(f"Searching for all folders matching (fallback): {folder_name}")
        folder_name_lower = folder_name.lower()
        matches = []
        
        for base_path in self.common_paths:
            try:
                for root, dirs, _ in os.walk(base_path):
                    depth = root[len(str(base_path)):].count(os.sep)
                    if depth > max_depth:
                        continue
                        
                    for dir_name in dirs:
                        if folder_name_lower in dir_name.lower():
                            full_path = os.path.join(root, dir_name)
                            matches.append(full_path)
                            
                            if len(matches) >= 10:
                                return matches
            except (PermissionError, OSError):
                continue
        
        return matches
        
    def open_folder(self, folder_name):
        """
        Search and open a folder, with interactive selection if multiple matches.
        Returns tuple: (message, requires_selection, options)
        """
        matches = self.search_folder_all(folder_name)
        
        if not matches:
            return (f"No encontré ninguna carpeta llamada '{folder_name}'", False, [])
        
        if len(matches) == 1:
            # Only one match, open it directly
            try:
                os.startfile(matches[0])
                return (f"Abriendo carpeta: {matches[0]}", False, [])
            except Exception as e:
                logger.error(f"Error opening folder: {e}")
                return (f"No pude abrir la carpeta: {e}", False, [])
        
        # Multiple matches - return for user selection
        return (
            f"Encontré {len(matches)} carpetas. ¿Cuál quieres abrir?",
            True,
            matches
        )
            
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
