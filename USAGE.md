# Python ExamDiff Pro - Quick Start Guide

## Installation

### Prerequisites
- Python 3.11 or higher
- Windows 10/11 (primary support)
- pip (Python package manager)

### Step 1: Install Dependencies

Open PowerShell or Command Prompt and navigate to the project directory:

```powershell
cd "c:\Users\govind.waghmare\OneDrive - OneWorkplace\Desktop\INTERNAL TOOLS\EXAMDIFF"
```

Install all required packages:

```powershell
pip install -r requirements.txt
```

### Step 2: Run the Application

#### GUI Mode (Default)
```powershell
python main.py
```

#### Compare Two Files (GUI)
```powershell
python main.py file1.txt file2.txt
```

#### Compare Two Files (CLI with Output)
```powershell
python main.py file1.txt file2.txt --no-gui --unified --output diff.txt
```

#### Compare Directories
```powershell
python main.py --dir folder1 folder2
```

#### Generate HTML Report
```powershell
python main.py file1.txt file2.txt --html --output report.html --no-gui
```

## Common Usage Scenarios

### 1. Quick File Comparison
Launch the GUI and use File → Compare Files menu, or press Ctrl+O

### 2. Directory Comparison
File → Compare Directories, select two folders to compare recursively

### 3. Viewing Differences
- Press F8 to jump to next difference
- Press F7 to jump to previous difference
- Use the minimap on the right to see all differences at a glance

### 4. Copying Changes
- Ctrl+Right: Copy selected lines from left to right
- Ctrl+Left: Copy selected lines from right to left

### 5. Ignoring Whitespace
Tools → Options → Check "Ignore whitespace differences"

### 6. Syntax Highlighting
View → Syntax Highlighting (automatically detects language from file extension)

## Configuration

Configuration file location:
```
%APPDATA%\PythonExamDiff\config.yaml
```

Edit this file to customize:
- Colors
- Fonts
- Default ignore options
- Window size
- And more...

## Command-Line Reference

```
python main.py [FILE1] [FILE2] [OPTIONS]

Options:
  --dir                  Compare directories
  --merge                Three-way merge (requires 3 files)
  -o, --output FILE      Output file path
  --html                 Generate HTML report
  --pdf                  Generate PDF report
  --unified              Generate unified diff
  --ignore-case          Ignore case differences
  --ignore-whitespace    Ignore whitespace
  --ignore-blank-lines   Ignore blank lines
  --syntax LANG          Syntax highlighting language
  --encoding ENC         File encoding
  --no-gui               CLI mode only
  --theme THEME          GUI theme (light/dark)
```

## Keyboard Shortcuts

### File Operations
- Ctrl+O: Open/Compare files
- Ctrl+S: Save current file
- Ctrl+W: Close current tab

### Navigation
- F7: Previous difference
- F8: Next difference
- Ctrl+G: Go to line
- Ctrl+F: Find

### Editing
- Ctrl+Z: Undo
- Ctrl+Y: Redo
- Ctrl+C: Copy
- Ctrl+V: Paste

### Comparison
- Ctrl+Left: Copy right to left
- Ctrl+Right: Copy left to right
- F5: Refresh comparison

## Troubleshooting

### "customtkinter not found"
```powershell
pip install customtkinter
```

### "chardet not found"
```powershell
pip install chardet
```

### Python not found
Make sure Python is installed and added to PATH

### Import errors
Reinstall all dependencies:
```powershell
pip install -r requirements.txt --force-reinstall
```

## Creating Executable

To create a standalone .exe file:

```powershell
pyinstaller examdiff.spec
```

The executable will be in the `dist\PythonExamDiff` folder.

## Advanced Features

### Plugin Development
Create custom plugins by extending `PluginBase`:

```python
from plugins.plugin_base import PluginBase

class MyPlugin(PluginBase):
    name = "My Plugin"
    version = "1.0.0"
    
    def initialize(self):
        return True
    
    def process_diff(self, diff_result):
        # Process diff results
        return diff_result
```

Place in `plugins/` directory and restart the application.

### Session Management
Save comparison sessions: File → Save Session
Load previous sessions: File → Open Session

### Directory Synchronization
After comparing directories, use Tools → Synchronize to copy files:
- Left → Right: Make right directory match left
- Right → Left: Make left directory match right
- Bidirectional: Merge both ways

## Performance Tips

### Large Files
- Files over 100MB are processed in chunks automatically
- Disable syntax highlighting for very large files (View → Syntax Highlighting)

### Large Directories
- Use exclude patterns to skip unnecessary files
- Disable recursive comparison for faster results

### Memory Usage
- Close unused tabs to free memory
- Use "Compare by hash" for large binary files

## Getting Help

### In-Application Help
- Help → User Manual
- Help → Keyboard Shortcuts
- Help → About

### Report Issues
If you encounter issues, check the log file:
```
%APPDATA%\PythonExamDiff\logs\examdiff.log
```

## Tips and Tricks

1. **Drag and Drop**: Drag files directly onto the window to compare them

2. **Recent Files**: Access recently compared files from File → Recent Files

3. **Bookmarks**: Mark important differences with Ctrl+B for later review

4. **Search in Diffs**: Use Ctrl+F and check "Search in differences only"

5. **Custom Color Schemes**: Edit config.yaml to change diff colors

6. **Quick Compare**: Right-click files in Windows Explorer and select "Compare with ExamDiff"

7. **Batch Processing**: Use command-line mode with batch scripts for automated comparisons

8. **Export Reports**: Generate HTML reports for sharing comparison results

9. **Three-Way Merge**: Use --merge for resolving conflicts in version control

10. **Ignore Patterns**: Set regex patterns to ignore specific lines (e.g., timestamps)

## Examples

### Example 1: Compare Two Python Files
```powershell
python main.py script1.py script2.py --syntax python
```

### Example 2: Compare Directories with Filtering
```powershell
python main.py --dir project1 project2 --no-gui
```

### Example 3: Generate Report
```powershell
python main.py old_version.txt new_version.txt --html --output comparison_report.html --no-gui
```

### Example 4: Ignore Whitespace and Case
```powershell
python main.py file1.txt file2.txt --ignore-whitespace --ignore-case
```

### Example 5: Three-Way Merge
```powershell
python main.py --merge base.txt mine.txt theirs.txt -o merged.txt
```

---

**Enjoy using Python ExamDiff Pro!**

For more information, see README.md or visit the documentation.
