"""
Python ExamDiff Pro - Main Application Entry Point
=================================================

Professional file and directory comparison tool for Windows.
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import get_config_manager
from core.diff_engine import create_diff_engine
from core.file_handler import FileHandler
from core.directory_handler import DirectoryHandler


def setup_logging():
    """Set up application logging."""
    config = get_config_manager()
    log_dir = Path(config.config_dir) / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / 'examdiff.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('PythonExamDiff')


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Python ExamDiff Pro - Professional File & Directory Comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Launch GUI
  python main.py
  
  # Compare two files
  python main.py file1.txt file2.txt
  
  # Compare directories
  python main.py --dir folder1 folder2
  
  # Three-way merge
  python main.py --merge base.txt yours.txt theirs.txt -o output.txt
  
  # Generate HTML report
  python main.py file1.txt file2.txt --html --output report.html
        '''
    )
    
    # Positional arguments
    parser.add_argument('files', nargs='*', help='Files or directories to compare')
    
    # Comparison mode
    parser.add_argument('--dir', action='store_true', help='Compare directories')
    parser.add_argument('--merge', action='store_true', help='Three-way merge mode')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--pdf', action='store_true', help='Generate PDF report')
    parser.add_argument('--unified', action='store_true', help='Generate unified diff')
    
    # Comparison options
    parser.add_argument('--ignore-case', action='store_true', help='Ignore case differences')
    parser.add_argument('--ignore-whitespace', action='store_true', help='Ignore whitespace')
    parser.add_argument('--ignore-blank-lines', action='store_true', help='Ignore blank lines')
    parser.add_argument('--syntax', help='Syntax highlighting language')
    parser.add_argument('--encoding', help='File encoding (utf-8, utf-16, etc.)')
    
    # Directory options
    parser.add_argument('--recursive', action='store_true', default=True, help='Recursive directory comparison')
    parser.add_argument('--no-recursive', action='store_false', dest='recursive', help='Non-recursive comparison')
    
    # GUI options
    parser.add_argument('--no-gui', action='store_true', help='Command-line mode only')
    parser.add_argument('--theme', choices=['light', 'dark'], default='dark', help='GUI theme')
    
    return parser.parse_args()


def cli_compare_files(file1: str, file2: str, args):
    """
    Compare two files in CLI mode.
    
    Args:
        file1: First file path
        file2: Second file path
        args: Command-line arguments
    """
    logger = logging.getLogger('PythonExamDiff')
    
    try:
        # Set up options
        options = {
            'ignore_case': args.ignore_case,
            'ignore_whitespace': args.ignore_whitespace,
            'ignore_blank_lines': args.ignore_blank_lines,
        }
        
        # Read files
        file_handler = FileHandler(encoding=args.encoding)
        lines1, info1 = file_handler.read_file(file1)
        lines2, info2 = file_handler.read_file(file2)
        
        logger.info(f"Comparing {file1} ({len(lines1)} lines) with {file2} ({len(lines2)} lines)")
        
        # Compare
        diff_engine = create_diff_engine(options)
        results = diff_engine.compare_lines(lines1, lines2)
        
        # Display results
        print(f"\n=== Comparison Results ===")
        print(f"File 1: {file1}")
        print(f"File 2: {file2}")
        print(f"\nChanges found: {len([r for r in results if r.type.value != 'equal'])}")
        
        for result in results:
            if result.type.value != 'equal':
                print(f"\n{result.type.value.upper()} at lines {result.old_start+1}-{result.old_start+result.old_count}:")
                if result.old_lines:
                    print("  OLD:", result.old_lines[:3])  # Show first 3 lines
                if result.new_lines:
                    print("  NEW:", result.new_lines[:3])
        
        # Generate output if requested
        if args.output:
            if args.html:
                print(f"\nGenerating HTML report to {args.output}...")
                # HTML generation would go here
            elif args.unified:
                from core.myers_algorithm import format_diff_unified
                unified_diff = format_diff_unified(results, file1, file2)
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(unified_diff)
                print(f"\nUnified diff saved to {args.output}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error comparing files: {e}", exc_info=True)
        print(f"ERROR: {e}")
        return 1


def cli_compare_directories(dir1: str, dir2: str, args):
    """
    Compare two directories in CLI mode.
    
    Args:
        dir1: First directory path
        dir2: Second directory path
        args: Command-line arguments
    """
    logger = logging.getLogger('PythonExamDiff')
    
    try:
        print(f"\n=== Comparing Directories ===")
        print(f"Left:  {dir1}")
        print(f"Right: {dir2}")
        print(f"Recursive: {args.recursive}\n")
        
        # Set up handler
        from core.directory_handler import CompareMode
        handler = DirectoryHandler(
            compare_mode=CompareMode.CONTENT,
            recursive=args.recursive
        )
        
        # Compare
        def progress(msg):
            print(f"  {msg}")
        
        result = handler.compare_directories(dir1, dir2, progress_callback=progress)
        
        # Display statistics
        stats = result.get_statistics()
        print(f"\n=== Statistics ===")
        print(f"Total files:     {stats['total']}")
        print(f"Identical:       {stats['identical']}")
        print(f"Different:       {stats['different']}")
        print(f"Left only:       {stats['left_only']}")
        print(f"Right only:      {stats['right_only']}")
        
        # Show some differences
        print(f"\n=== Differences ===")
        for entry in result.entries[:20]:  # Show first 20
            if entry.status.value != 'identical':
                print(f"  [{entry.status.value}] {entry.relative_path}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error comparing directories: {e}", exc_info=True)
        print(f"ERROR: {e}")
        return 1


def launch_gui(args):
    """
    Launch the GUI application.
    
    Args:
        args: Command-line arguments
    """
    try:
        import customtkinter as ctk
        from gui.main_window import MainWindow
        
        # Set appearance mode
        ctk.set_appearance_mode(args.theme)
        ctk.set_default_color_theme("blue")
        
        # Create main window
        app = MainWindow()
        
        # If files were provided, open them
        if len(args.files) == 2 and not args.dir:
            app.after(100, lambda: app.compare_files(args.files[0], args.files[1]))
        elif len(args.files) == 2 and args.dir:
            app.after(100, lambda: app.compare_directories(args.files[0], args.files[1]))
        
        # Start main loop
        app.mainloop()
        
        return 0
    
    except ImportError as e:
        print(f"ERROR: GUI dependencies not installed. Please run: pip install customtkinter")
        print(f"Details: {e}")
        return 1
    except Exception as e:
        logger = logging.getLogger('PythonExamDiff')
        logger.error(f"Error launching GUI: {e}", exc_info=True)
        print(f"ERROR: {e}")
        return 1


def main():
    """Main entry point."""
    # Set up logging
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Python ExamDiff Pro starting...")
    logger.info("=" * 60)
    
    # Parse arguments
    args = parse_arguments()
    
    try:
        # Determine mode
        if args.no_gui or args.html or args.pdf or args.unified:
            # CLI mode
            if args.merge:
                if len(args.files) != 3:
                    print("ERROR: Three-way merge requires 3 files: base, yours, theirs")
                    return 1
                print("Three-way merge not yet implemented in CLI mode.")
                return 1
            
            elif args.dir:
                if len(args.files) != 2:
                    print("ERROR: Directory comparison requires 2 directories")
                    return 1
                return cli_compare_directories(args.files[0], args.files[1], args)
            
            elif len(args.files) == 2:
                return cli_compare_files(args.files[0], args.files[1], args)
            
            else:
                print("ERROR: Please specify 2 files or directories to compare")
                return 1
        
        else:
            # GUI mode (default)
            return launch_gui(args)
    
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
