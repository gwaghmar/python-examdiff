"""
Configuration Management
=======================

Handles application configuration, settings, and user preferences.
"""

import os
import yaml
import json
from typing import Any, Dict, Optional
from pathlib import Path
from dataclasses import dataclass, asdict, field


@dataclass
class AppConfig:
    """Application configuration."""
    
    # General settings
    theme: str = "dark"
    language: str = "en"
    
    # Comparison settings
    ignore_case: bool = False
    ignore_whitespace: bool = False
    ignore_blank_lines: bool = False
    ignore_leading_whitespace: bool = False
    ignore_trailing_whitespace: bool = False
    ignore_comments: bool = False
    
    # Syntax highlighting
    syntax_highlighting_enabled: bool = True
    syntax_theme: str = "default"
    
    # Display settings
    font_family: str = "Consolas"
    font_size: int = 10
    tab_size: int = 4
    show_line_numbers: bool = True
    show_whitespace: bool = False
    wrap_lines: bool = False
    
    # Colors
    color_added: str = "#90EE90"
    color_deleted: str = "#FFB6C1"
    color_modified: str = "#FFD700"
    color_unchanged: str = "#F0F0F0"
    
    # Window settings
    window_width: int = 1400
    window_height: int = 900
    window_maximized: bool = False
    
    # Recent files
    max_recent_files: int = 10
    recent_files: list = field(default_factory=list)
    recent_dirs: list = field(default_factory=list)
    
    # Advanced
    fuzzy_matching: bool = False
    moving_block_detection: bool = False
    auto_save_sessions: bool = True
    check_for_updates: bool = True
    
    # Directory comparison
    dir_compare_mode: str = "content"  # content, size, timestamp
    dir_recursive: bool = True
    dir_include_patterns: list = field(default_factory=lambda: ["*"])
    dir_exclude_patterns: list = field(default_factory=lambda: ["*.pyc", "__pycache__", ".git", ".svn"])
    
    # Performance
    large_file_threshold: int = 100 * 1024 * 1024  # 100 MB
    chunk_size: int = 10 * 1024 * 1024  # 10 MB


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Custom config directory (None for default)
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Use AppData on Windows
            appdata = os.getenv('APPDATA') or os.path.expanduser('~')
            self.config_dir = Path(appdata) / 'PythonExamDiff'
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / 'config.yaml'
        self.sessions_dir = self.config_dir / 'sessions'
        self.sessions_dir.mkdir(exist_ok=True)
        
        self.config = AppConfig()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        # Update config with loaded values
                        for key, value in data.items():
                            if hasattr(self.config, key):
                                setattr(self.config, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(asdict(self.config), f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value
        """
        return getattr(self.config, key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: New value
        """
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            self.save_config()
    
    def add_recent_file(self, filepath: str) -> None:
        """
        Add file to recent files list.
        
        Args:
            filepath: File path to add
        """
        if filepath in self.config.recent_files:
            self.config.recent_files.remove(filepath)
        
        self.config.recent_files.insert(0, filepath)
        
        # Limit list size
        if len(self.config.recent_files) > self.config.max_recent_files:
            self.config.recent_files = self.config.recent_files[:self.config.max_recent_files]
        
        self.save_config()
    
    def add_recent_dir(self, dirpath: str) -> None:
        """
        Add directory to recent directories list.
        
        Args:
            dirpath: Directory path to add
        """
        if dirpath in self.config.recent_dirs:
            self.config.recent_dirs.remove(dirpath)
        
        self.config.recent_dirs.insert(0, dirpath)
        
        # Limit list size
        if len(self.config.recent_dirs) > self.config.max_recent_files:
            self.config.recent_dirs = self.config.recent_dirs[:self.config.max_recent_files]
        
        self.save_config()
    
    def save_session(self, session_name: str, session_data: Dict[str, Any]) -> None:
        """
        Save a comparison session.
        
        Args:
            session_name: Name of the session
            session_data: Session data to save
        """
        session_file = self.sessions_dir / f"{session_name}.json"
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def load_session(self, session_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a comparison session.
        
        Args:
            session_name: Name of the session
            
        Returns:
            Session data or None
        """
        session_file = self.sessions_dir / f"{session_name}.json"
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading session: {e}")
        return None
    
    def list_sessions(self) -> list:
        """
        List all saved sessions.
        
        Returns:
            List of session names
        """
        return [f.stem for f in self.sessions_dir.glob('*.json')]
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = AppConfig()
        self.save_config()


# Global config manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """
    Get global configuration manager instance.
    
    Returns:
        ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
