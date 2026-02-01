"""
Plugin Base - Base Class for Plugins
====================================

Provides a plugin system for extending application functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import importlib
import os
from pathlib import Path


class PluginBase(ABC):
    """
    Base class for all plugins.
    
    To create a plugin:
    1. Inherit from PluginBase
    2. Implement required methods
    3. Place plugin file in plugins/ directory
    4. Plugin will be auto-discovered and loaded
    """
    
    # Plugin metadata (override in subclass)
    name: str = "Unnamed Plugin"
    version: str = "1.0.0"
    description: str = "No description"
    author: str = "Unknown"
    
    def __init__(self):
        """Initialize plugin."""
        self.enabled = True
        self.config: Dict[str, Any] = {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the plugin.
        
        Called when plugin is loaded.
        
        Returns:
            True if initialization successful
        """
        pass
    
    @abstractmethod
    def process_diff(self, diff_result: Any) -> Any:
        """
        Process diff results.
        
        Args:
            diff_result: Diff result object
            
        Returns:
            Modified diff result
        """
        pass
    
    def on_compare_start(self, file1: str, file2: str) -> None:
        """
        Called before comparison starts.
        
        Args:
            file1: First file path
            file2: Second file path
        """
        pass
    
    def on_compare_complete(self, results: Any) -> None:
        """
        Called after comparison completes.
        
        Args:
            results: Comparison results
        """
        pass
    
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Get configuration schema for this plugin.
        
        Returns:
            Dictionary describing configuration options
        """
        return {}
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """
        Set plugin configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    def cleanup(self) -> None:
        """Cleanup when plugin is unloaded."""
        pass


class PluginManager:
    """
    Manages plugin loading, unloading, and execution.
    """
    
    def __init__(self, plugins_dir: Optional[str] = None):
        """
        Initialize plugin manager.
        
        Args:
            plugins_dir: Directory containing plugins (None for default)
        """
        if plugins_dir:
            self.plugins_dir = Path(plugins_dir)
        else:
            self.plugins_dir = Path(__file__).parent
        
        self.plugins: Dict[str, PluginBase] = {}
        self.load_all_plugins()
    
    def load_all_plugins(self) -> None:
        """Discover and load all plugins from plugins directory."""
        if not self.plugins_dir.exists():
            return
        
        for file_path in self.plugins_dir.glob("*.py"):
            if file_path.stem.startswith("_") or file_path.stem == "plugin_base":
                continue
            
            try:
                self.load_plugin(file_path.stem)
            except Exception as e:
                print(f"Error loading plugin {file_path.stem}: {e}")
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        Load a specific plugin.
        
        Args:
            plugin_name: Name of the plugin module
            
        Returns:
            True if loaded successfully
        """
        try:
            # Import plugin module
            module = importlib.import_module(f"plugins.{plugin_name}")
            
            # Find plugin class (subclass of PluginBase)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, PluginBase) and 
                    attr is not PluginBase):
                    
                    # Instantiate plugin
                    plugin = attr()
                    
                    # Initialize
                    if plugin.initialize():
                        self.plugins[plugin.name] = plugin
                        print(f"Loaded plugin: {plugin.name} v{plugin.version}")
                        return True
            
            return False
        
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            True if unloaded successfully
        """
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            plugin.cleanup()
            del self.plugins[plugin_name]
            return True
        return False
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginBase]:
        """
        Get a loaded plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin instance or None
        """
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[Dict[str, str]]:
        """
        List all loaded plugins.
        
        Returns:
            List of plugin info dictionaries
        """
        return [
            {
                'name': plugin.name,
                'version': plugin.version,
                'description': plugin.description,
                'author': plugin.author,
                'enabled': plugin.enabled
            }
            for plugin in self.plugins.values()
        ]
    
    def execute_on_compare_start(self, file1: str, file2: str) -> None:
        """
        Execute on_compare_start hook for all plugins.
        
        Args:
            file1: First file path
            file2: Second file path
        """
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_compare_start(file1, file2)
                except Exception as e:
                    print(f"Error in plugin {plugin.name}.on_compare_start: {e}")
    
    def execute_on_compare_complete(self, results: Any) -> None:
        """
        Execute on_compare_complete hook for all plugins.
        
        Args:
            results: Comparison results
        """
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_compare_complete(results)
                except Exception as e:
                    print(f"Error in plugin {plugin.name}.on_compare_complete: {e}")
    
    def process_with_plugins(self, diff_result: Any) -> Any:
        """
        Process diff result through all plugins.
        
        Args:
            diff_result: Initial diff result
            
        Returns:
            Processed diff result
        """
        result = diff_result
        
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    result = plugin.process_diff(result)
                except Exception as e:
                    print(f"Error in plugin {plugin.name}.process_diff: {e}")
        
        return result


# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """
    Get global plugin manager instance.
    
    Returns:
        PluginManager instance
    """
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager
