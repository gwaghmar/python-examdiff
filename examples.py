"""
API Usage Examples
==================

This file demonstrates how to use the Python ExamDiff Pro API programmatically.
"""

# Example 1: Basic File Comparison
def example_basic_comparison():
    """Compare two files and print results."""
    from core.file_handler import FileHandler
    from core.diff_engine import create_diff_engine
    from core.myers_algorithm import DiffType
    
    # Read files
    handler = FileHandler()
    lines1, info1 = handler.read_file('file1.txt')
    lines2, info2 = handler.read_file('file2.txt')
    
    # Create diff engine
    engine = create_diff_engine()
    
    # Compare
    results = engine.compare_lines(lines1, lines2)
    
    # Print results
    print(f"Comparing {info1.path} with {info2.path}")
    print(f"File 1: {len(lines1)} lines, {info1.encoding}")
    print(f"File 2: {len(lines2)} lines, {info2.encoding}")
    print()
    
    for result in results:
        if result.type != DiffType.EQUAL:
            print(f"{result.type.value.upper()} at line {result.old_start + 1}")
            if result.old_lines:
                print(f"  OLD: {result.old_lines[0]}")
            if result.new_lines:
                print(f"  NEW: {result.new_lines[0]}")
            print()


# Example 2: Comparison with Options
def example_comparison_with_options():
    """Compare files with ignore options."""
    from core.file_handler import read_file_lines
    from core.diff_engine import create_diff_engine
    
    # Read files
    lines1 = read_file_lines('file1.txt')
    lines2 = read_file_lines('file2.txt')
    
    # Create engine with options
    options = {
        'ignore_case': True,
        'ignore_whitespace': True,
        'ignore_blank_lines': True,
        'fuzzy_matching': True
    }
    engine = create_diff_engine(options)
    
    # Compare
    results = engine.compare_lines(lines1, lines2)
    
    # Count differences
    diff_count = len([r for r in results if r.type.value != 'equal'])
    print(f"Found {diff_count} differences (with ignore options)")


# Example 3: Word-Level Comparison
def example_word_level_diff():
    """Compare two lines at word level."""
    from core.diff_engine import create_diff_engine
    
    engine = create_diff_engine()
    
    line1 = "The quick brown fox jumps"
    line2 = "The slow brown fox leaps"
    
    word_diffs = engine.compare_words(line1, line2)
    
    print("Word-level differences:")
    for diff in word_diffs:
        if diff.type.value != 'equal':
            print(f"  {diff.type.value}: '{diff.word}' at position {diff.start_pos}")


# Example 4: Directory Comparison
def example_directory_comparison():
    """Compare two directories."""
    from core.directory_handler import DirectoryHandler, CompareMode
    
    handler = DirectoryHandler(
        compare_mode=CompareMode.CONTENT,
        recursive=True,
        include_patterns=['*.py', '*.txt'],
        exclude_patterns=['*.pyc', '__pycache__']
    )
    
    result = handler.compare_directories('dir1', 'dir2')
    
    # Print statistics
    stats = result.get_statistics()
    print("Directory Comparison Results:")
    print(f"  Total files: {stats['total']}")
    print(f"  Identical: {stats['identical']}")
    print(f"  Different: {stats['different']}")
    print(f"  Left only: {stats['left_only']}")
    print(f"  Right only: {stats['right_only']}")


# Example 5: Generate HTML Report
def example_html_report():
    """Generate an HTML comparison report."""
    from core.file_handler import read_file_lines
    from core.diff_engine import create_diff_engine
    from utils.report_generator import create_html_report
    
    # Compare files
    lines1 = read_file_lines('old_version.py')
    lines2 = read_file_lines('new_version.py')
    
    engine = create_diff_engine()
    results = engine.compare_lines(lines1, lines2)
    
    # Generate report
    create_html_report(
        'old_version.py',
        'new_version.py',
        lines1,
        lines2,
        results,
        'comparison_report.html'
    )
    
    print("HTML report generated: comparison_report.html")


# Example 6: Syntax Highlighting
def example_syntax_highlighting():
    """Use syntax highlighting."""
    from utils.syntax_highlighter import create_highlighter
    
    # Create highlighter
    highlighter = create_highlighter(language='python', theme='dark')
    
    # Highlight code
    code = """
def hello_world():
    print("Hello, World!")
    return 42
"""
    
    tokens = highlighter.highlight_text(code)
    
    print("Highlighted tokens:")
    for token in tokens[:10]:  # Show first 10 tokens
        print(f"  '{token.text}' ({token.token_type}): {token.color}")


# Example 7: Three-Way Merge
def example_three_way_merge():
    """Perform a three-way merge."""
    from core.file_handler import read_file_lines
    from core.diff_engine import create_diff_engine
    
    # Read three versions
    base = read_file_lines('base.txt')
    yours = read_file_lines('yours.txt')
    theirs = read_file_lines('theirs.txt')
    
    # Merge
    engine = create_diff_engine()
    merged, conflicts = engine.three_way_merge(base, yours, theirs)
    
    print(f"Merge complete. {len(conflicts)} conflicts found.")
    
    if conflicts:
        print("\nConflicts:")
        for conflict in conflicts:
            print(f"  Line {conflict['line']}")
            print(f"    Yours: {conflict['yours_lines']}")
            print(f"    Theirs: {conflict['theirs_lines']}")


# Example 8: Using Plugins
def example_using_plugins():
    """Use the plugin system."""
    from plugins.plugin_base import get_plugin_manager
    
    # Get plugin manager
    manager = get_plugin_manager()
    
    # List loaded plugins
    plugins = manager.list_plugins()
    print(f"Loaded plugins: {len(plugins)}")
    
    for plugin in plugins:
        print(f"  - {plugin['name']} v{plugin['version']}")
        print(f"    {plugin['description']}")
    
    # Execute plugin hooks
    manager.execute_on_compare_start('file1.txt', 'file2.txt')
    
    # Process with plugins
    # result = manager.process_with_plugins(diff_result)


# Example 9: Binary File Comparison
def example_binary_comparison():
    """Compare two binary files."""
    from core.file_handler import FileHandler
    
    handler = FileHandler()
    
    differences = handler.compare_binary('file1.bin', 'file2.bin')
    
    print(f"Binary comparison: {len(differences)} byte differences")
    
    # Show first few differences
    for offset, byte1, byte2 in differences[:10]:
        print(f"  Offset {offset:08X}: {byte1:02X} -> {byte2:02X}")


# Example 10: Custom Configuration
def example_custom_configuration():
    """Use custom configuration."""
    from config import ConfigManager
    
    # Create config manager
    config = ConfigManager()
    
    # Get settings
    theme = config.get('theme', 'dark')
    font_size = config.get('font_size', 10)
    
    print(f"Current theme: {theme}")
    print(f"Font size: {font_size}")
    
    # Change settings
    config.set('theme', 'light')
    config.set('font_size', 12)
    
    # Add recent file
    config.add_recent_file('myfile.txt')
    
    # Save session
    session_data = {
        'file1': 'path/to/file1.txt',
        'file2': 'path/to/file2.txt',
        'options': {'ignore_case': True}
    }
    config.save_session('my_comparison', session_data)


# Example 11: Progress Tracking
def example_progress_tracking():
    """Track progress of long operations."""
    from utils.helpers import ProgressTracker
    import time
    
    # Create progress tracker
    total_items = 100
    progress = ProgressTracker(total_items)
    
    for i in range(total_items):
        # Do some work
        time.sleep(0.01)
        
        # Update progress
        progress.update(1, f"Processing item {i+1}")
        
        # Check progress
        percent = progress.get_percentage()
        eta = progress.get_eta()
        
        if i % 10 == 0:
            print(f"Progress: {percent:.1f}% (ETA: {eta:.1f}s)")


# Example 12: Unified Diff Format
def example_unified_diff():
    """Generate unified diff format."""
    from core.file_handler import read_file_lines
    from core.myers_algorithm import myers_diff, format_diff_unified
    
    lines1 = read_file_lines('file1.txt')
    lines2 = read_file_lines('file2.txt')
    
    results = myers_diff(lines1, lines2)
    
    unified = format_diff_unified(results, 'file1.txt', 'file2.txt')
    
    print(unified)


# Main demonstration
if __name__ == '__main__':
    print("=" * 60)
    print("Python ExamDiff Pro - API Usage Examples")
    print("=" * 60)
    print()
    
    print("Example 1: Basic File Comparison")
    print("-" * 60)
    # example_basic_comparison()
    
    print("\nExample 2: Comparison with Options")
    print("-" * 60)
    # example_comparison_with_options()
    
    print("\nExample 3: Word-Level Diff")
    print("-" * 60)
    example_word_level_diff()
    
    print("\nExample 6: Syntax Highlighting")
    print("-" * 60)
    example_syntax_highlighting()
    
    print("\nExample 11: Progress Tracking")
    print("-" * 60)
    example_progress_tracking()
    
    print("\n" + "=" * 60)
    print("For more examples, uncomment the function calls above")
    print("=" * 60)
