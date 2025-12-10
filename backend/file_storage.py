"""
File Storage Module
Manages file storage and retrieval
"""

import os
import shutil
from typing import List, Optional
from pathlib import Path
from logger import logger


class FileStorage:
    """File storage manager"""
    
    def __init__(self, base_path: str = "./data/uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, filename: str, content: bytes) -> bool:
        """Save file to storage"""
        try:
            file_path = self.base_path / filename
            with open(file_path, 'wb') as f:
                f.write(content)
            logger.info(f"File saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save file {filename}: {str(e)}")
            return False
    
    def get_file(self, filename: str) -> Optional[bytes]:
        """Retrieve file from storage"""
        try:
            file_path = self.base_path / filename
            if not file_path.exists():
                return None
            
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {filename}: {str(e)}")
            return None
    
    def delete_file(self, filename: str) -> bool:
        """Delete file from storage"""
        try:
            file_path = self.base_path / filename
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {filename}: {str(e)}")
            return False
    
    def list_files(self) -> List[str]:
        """List all files in storage"""
        try:
            return [f.name for f in self.base_path.glob("*") if f.is_file()]
        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []
    
    def get_file_size(self, filename: str) -> int:
        """Get file size in bytes"""
        try:
            file_path = self.base_path / filename
            return file_path.stat().st_size if file_path.exists() else 0
        except Exception as e:
            logger.error(f"Failed to get file size: {str(e)}")
            return 0
    
    def clear_old_files(self, days: int = 30) -> int:
        """Clear files older than specified days"""
        import time
        cutoff_time = time.time() - (days * 86400)
        deleted = 0
        
        try:
            for file_path in self.base_path.glob("*"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted += 1
        except Exception as e:
            logger.error(f"Failed to clear old files: {str(e)}")
        
        return deleted
