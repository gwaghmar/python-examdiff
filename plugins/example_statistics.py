"""
Example Plugin - Statistics Reporter
====================================

This is an example plugin that demonstrates the plugin system.
It reports statistics about the comparison.
"""

from plugins.plugin_base import PluginBase
from core.myers_algorithm import DiffResult, DiffType
from typing import Any, List


class StatisticsPlugin(PluginBase):
    """
    Example plugin that collects and reports comparison statistics.
    """
    
    name = "Statistics Reporter"
    version = "1.0.0"
    description = "Collects and reports detailed comparison statistics"
    author = "Python ExamDiff Pro Team"
    
    def __init__(self):
        """Initialize plugin."""
        super().__init__()
        self.stats = {}
    
    def initialize(self) -> bool:
        """Initialize the plugin."""
        print(f"[{self.name}] Plugin initialized")
        return True
    
    def on_compare_start(self, file1: str, file2: str) -> None:
        """Called before comparison starts."""
        print(f"[{self.name}] Starting comparison: {file1} vs {file2}")
        self.stats = {
            'file1': file1,
            'file2': file2,
            'total_diffs': 0,
            'additions': 0,
            'deletions': 0,
            'modifications': 0,
            'equal_blocks': 0
        }
    
    def process_diff(self, diff_result: Any) -> Any:
        """
        Process diff results and collect statistics.
        
        Args:
            diff_result: Diff result object
            
        Returns:
            Unmodified diff result (this plugin only observes)
        """
        # If diff_result is a list of DiffResult objects
        if isinstance(diff_result, list):
            for result in diff_result:
                if isinstance(result, DiffResult):
                    if result.type == DiffType.EQUAL:
                        self.stats['equal_blocks'] += 1
                    elif result.type == DiffType.INSERT:
                        self.stats['additions'] += result.new_count
                        self.stats['total_diffs'] += 1
                    elif result.type == DiffType.DELETE:
                        self.stats['deletions'] += result.old_count
                        self.stats['total_diffs'] += 1
                    elif result.type == DiffType.REPLACE:
                        self.stats['modifications'] += 1
                        self.stats['total_diffs'] += 1
        
        # Return unmodified result
        return diff_result
    
    def on_compare_complete(self, results: Any) -> None:
        """Called after comparison completes."""
        print(f"\n[{self.name}] Comparison Statistics:")
        print(f"  Total differences:  {self.stats.get('total_diffs', 0)}")
        print(f"  Lines added:        {self.stats.get('additions', 0)}")
        print(f"  Lines deleted:      {self.stats.get('deletions', 0)}")
        print(f"  Lines modified:     {self.stats.get('modifications', 0)}")
        print(f"  Equal blocks:       {self.stats.get('equal_blocks', 0)}")
        print()
    
    def get_config_schema(self) -> dict:
        """Get configuration schema."""
        return {
            'verbose': {
                'type': 'boolean',
                'default': True,
                'description': 'Print verbose statistics'
            },
            'save_to_file': {
                'type': 'boolean',
                'default': False,
                'description': 'Save statistics to file'
            },
            'output_path': {
                'type': 'string',
                'default': 'stats.txt',
                'description': 'Output file path for statistics'
            }
        }
    
    def cleanup(self) -> None:
        """Cleanup when plugin is unloaded."""
        print(f"[{self.name}] Plugin unloaded")


# Plugin is automatically discovered and loaded by the PluginManager
