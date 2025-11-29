import os
import sqlite3
import threading
import time
from pathlib import Path
from src.config.settings import Settings
from src.utils.logger import logger

class FolderMapper:
    """
    Maps all folders on the system to database for fast searching.
    Updates periodically in background.
    """
    
    def __init__(self):
        self.db_path = Settings.DB_PATH
        self.init_db()
        self._update_thread = None
        self._stop_flag = threading.Event()
    
    def init_db(self):
        """Create folder mapping table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS folder_map (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_name TEXT,
                full_path TEXT UNIQUE,
                parent_path TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_folder_name ON folder_map(folder_name)')
        conn.commit()
        conn.close()
        logger.info("FolderMapper database initialized")
    
    def map_all_folders(self, max_depth=5):
        """
        Scan entire system and map all folders to database.
        This is a one-time operation triggered by user command.
        """
        logger.info("Starting full folder mapping...")
        
        common_paths = [
            Path.home(),
            Path("C:/"),
            Path("D:/") if Path("D:/").exists() else None,
            Path("E:/") if Path("E:/").exists() else None
        ]
        common_paths = [p for p in common_paths if p and p.exists()]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear old mappings
        cursor.execute('DELETE FROM folder_map')
        
        # System folders to exclude
        excluded_folders = {'windows', 'program files', 'program files (x86)', 'appdata', 'application data', '$recycle.bin', 'system volume information'}
        
        total_folders = 0
        for base_path in common_paths:
            try:
                for root, dirs, _ in os.walk(base_path):
                    # Filter out hidden folders and system folders
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in excluded_folders]
                    
                    # Also check if current root is inside an excluded path (e.g. inside Windows)
                    if any(ex in root.lower().split(os.sep) for ex in excluded_folders):
                        dirs.clear()
                        continue

                    depth = root[len(str(base_path)):].count(os.sep)
                    if depth > max_depth:
                        dirs.clear()  # Don't go deeper
                        continue
                    
                    for dir_name in dirs:
                        full_path = os.path.join(root, dir_name)
                        parent_path = root
                        
                        try:
                            cursor.execute(
                                'INSERT OR IGNORE INTO folder_map (folder_name, full_path, parent_path) VALUES (?, ?, ?)',
                                (dir_name.lower(), full_path, parent_path)
                            )
                            total_folders += 1
                            
                            # Commit every 1000 folders
                            if total_folders % 1000 == 0:
                                conn.commit()
                                logger.info(f"Mapped {total_folders} folders...")
                        except:
                            continue
            except (PermissionError, OSError):
                continue
        
        conn.commit()
        conn.close()
        logger.info(f"Folder mapping complete! Total: {total_folders} folders")
        return total_folders
    
    def search_folders(self, folder_name):
        """
        Fast search in database instead of os.walk()
        Returns list of matching paths.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT full_path FROM folder_map WHERE folder_name LIKE ? LIMIT 10',
            (f'%{folder_name.lower()}%',)
        )
        
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        logger.info(f"Found {len(results)} folders matching '{folder_name}' in database")
        return results
    
    def start_periodic_update(self, interval_minutes=30):
        """
        Start background thread to update mappings periodically.
        Only runs when system is idle.
        """
        if self._update_thread and self._update_thread.is_alive():
            logger.info("Periodic update already running")
            return
        
        self._stop_flag.clear()
        self._update_thread = threading.Thread(
            target=self._periodic_update_worker,
            args=(interval_minutes,),
            daemon=True
        )
        self._update_thread.start()
        logger.info(f"Started periodic folder mapping (every {interval_minutes} min)")
    
    def _periodic_update_worker(self, interval_minutes):
        """Background worker for periodic updates"""
        while not self._stop_flag.is_set():
            # Wait for interval
            self._stop_flag.wait(interval_minutes * 60)
            
            if not self._stop_flag.is_set():
                logger.info("Running periodic folder map update...")
                try:
                    self.map_all_folders()
                except Exception as e:
                    logger.error(f"Error in periodic update: {e}")
    
    def stop_periodic_update(self):
        """Stop background updates"""
        self._stop_flag.set()
        logger.info("Stopped periodic folder mapping")
