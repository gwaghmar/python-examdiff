"""
Helper Utilities
===============

Common utility functions used throughout the application.
"""

import os
import time
from typing import List, Tuple, Optional, Any
from datetime import datetime
import hashlib


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_timestamp(timestamp: float) -> str:
    """
    Format timestamp in human-readable format.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted string
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity between two strings (0.0 to 1.0).
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Similarity ratio
    """
    if str1 == str2:
        return 1.0
    
    if not str1 or not str2:
        return 0.0
    
    # Simple Levenshtein distance ratio
    from difflib import SequenceMatcher
    return SequenceMatcher(None, str1, str2).ratio()


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        text: Input string
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def normalize_path(path: str) -> str:
    """
    Normalize file path.
    
    Args:
        path: Input path
        
    Returns:
        Normalized path
    """
    return os.path.normpath(os.path.abspath(path))


def ensure_dir(directory: str) -> None:
    """
    Ensure directory exists, create if not.
    
    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)


def safe_read_file(filepath: str, default: str = "") -> str:
    """
    Safely read file content.
    
    Args:
        filepath: File path
        default: Default value if read fails
        
    Returns:
        File content or default
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception:
        return default


def safe_write_file(filepath: str, content: str) -> bool:
    """
    Safely write file content.
    
    Args:
        filepath: File path
        content: Content to write
        
    Returns:
        True if successful
    """
    try:
        ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False


def get_relative_path(path: str, base: str) -> str:
    """
    Get relative path from base.
    
    Args:
        path: Full path
        base: Base path
        
    Returns:
        Relative path
    """
    try:
        return os.path.relpath(path, base)
    except ValueError:
        return path


def is_text_file(filepath: str) -> bool:
    """
    Check if file is likely a text file.
    
    Args:
        filepath: File path
        
    Returns:
        True if likely text file
    """
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(8192)
        
        # Check for null bytes
        if b'\x00' in chunk:
            return False
        
        # Check printable ratio
        printable = sum(32 <= b < 127 or b in (9, 10, 13) for b in chunk)
        return printable / len(chunk) > 0.75
    
    except Exception:
        return False


def timer(func):
    """
    Decorator to time function execution.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper


class ProgressTracker:
    """Track progress of long-running operations."""
    
    def __init__(self, total: int, callback=None):
        """
        Initialize progress tracker.
        
        Args:
            total: Total number of items
            callback: Optional callback function(current, total, message)
        """
        self.total = total
        self.current = 0
        self.callback = callback
        self.start_time = time.time()
    
    def update(self, increment: int = 1, message: str = ""):
        """
        Update progress.
        
        Args:
            increment: Amount to increment
            message: Optional message
        """
        self.current += increment
        if self.callback:
            self.callback(self.current, self.total, message)
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        return time.time() - self.start_time
    
    def get_percentage(self) -> float:
        """Get completion percentage."""
        if self.total == 0:
            return 100.0
        return (self.current / self.total) * 100.0
    
    def get_eta(self) -> Optional[float]:
        """Get estimated time to completion in seconds."""
        if self.current == 0:
            return None
        
        elapsed = self.get_elapsed_time()
        rate = self.current / elapsed
        remaining = self.total - self.current
        
        return remaining / rate if rate > 0 else None


def batch_process(items: List[Any], batch_size: int = 100):
    """
    Generator that yields items in batches.
    
    Args:
        items: List of items
        batch_size: Size of each batch
        
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Recursively merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result
