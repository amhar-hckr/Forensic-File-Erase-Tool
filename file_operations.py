import os
import shutil
from pathlib import Path
import win32api
import win32con
import win32file
from datetime import datetime
import logging
from rich.console import Console

console = Console()

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"file_operations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def is_file_locked(filepath):
    """Check if a file is locked/in use."""
    try:
        # Try to open the file in exclusive mode
        with open(filepath, 'r+b') as _:
            return False
    except IOError:
        return True

def secure_delete(filepath, passes=3):
    """Securely delete a file by overwriting it multiple times before deletion."""
    if not os.path.exists(filepath):
        return False

    try:
        file_size = os.path.getsize(filepath)
        
        # Open file in binary write mode
        with open(filepath, "r+b") as f:
            # Multiple overwrite passes
            for _ in range(passes):
                # Overwrite with zeros
                f.seek(0)
                f.write(b'\x00' * file_size)
                f.flush()
                os.fsync(f.fileno())
                
                # Overwrite with ones
                f.seek(0)
                f.write(b'\xFF' * file_size)
                f.flush()
                os.fsync(f.fileno())
                
                # Overwrite with random data
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        
        # Finally delete the file
        os.remove(filepath)
        logger.info(f"Successfully securely deleted: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to securely delete {filepath}: {str(e)}")
        return False

def create_backup(filepath):
    """Create a backup of a file before deletion."""
    try:
        backup_dir = Path("backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Preserve the relative path structure in backup
        rel_path = Path(filepath).relative_to(Path.cwd())
        backup_path = backup_dir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(filepath, backup_path)
        logger.info(f"Created backup of {filepath} at {backup_path}")
        return str(backup_path)
    except Exception as e:
        logger.error(f"Failed to create backup of {filepath}: {str(e)}")
        return None

def delete_file(filepath, secure=False, backup=True):
    """Delete a file with optional secure deletion and backup."""
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            logger.warning(f"File not found: {filepath}")
            return False
        
        # Check if file is locked
        if is_file_locked(filepath):
            logger.warning(f"File is locked/in use: {filepath}")
            return False
        
        # Create backup if requested
        if backup:
            backup_path = create_backup(filepath)
            if not backup_path:
                logger.warning(f"Failed to create backup, skipping deletion of {filepath}")
                return False
        
        # Perform deletion
        if secure:
            return secure_delete(filepath)
        else:
            os.remove(filepath)
            logger.info(f"Successfully deleted: {filepath}")
            return True
            
    except PermissionError:
        logger.error(f"Permission denied: {filepath}")
        return False
    except Exception as e:
        logger.error(f"Error deleting {filepath}: {str(e)}")
        return False
