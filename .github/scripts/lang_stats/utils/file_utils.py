"""
File system utilities
"""

import os
from pathlib import Path
from typing import Union


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_file_safe(path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
    """
    Safely write content to file, creating directories if needed.
    
    Args:
        path: File path
        content: Content to write
        encoding: File encoding
    """
    path = Path(path)
    ensure_directory(path.parent)
    path.write_text(content, encoding=encoding)


def read_file_safe(path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """
    Safely read file content.
    
    Args:
        path: File path
        encoding: File encoding
        
    Returns:
        File content
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(path)
    return path.read_text(encoding=encoding)


def get_project_root() -> Path:
    """
    Get project root directory.
    
    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent.parent.parent.parent

