# 🚀 Python ExamDiff Pro - Quick Reference Card

## Installation (One-Time Setup)
```powershell
cd "C:\Users\govind.waghmare\OneDrive - OneWorkplace\Desktop\INTERNAL TOOLS\EXAMDIFF"
.\install.ps1
```

## Quick Start Commands

### Launch GUI
```powershell
python main.py
```

### Compare Two Files
```powershell
# In GUI
python main.py file1.txt file2.txt

# In CLI with unified diff output
python main.py file1.txt file2.txt --no-gui --unified --output diff.txt
```

### Compare Directories
```powershell
python main.py --dir C:\folder1 C:\folder2
```

### Generate HTML Report
```powershell
python main.py old.py new.py --html --output report.html --no-gui
```

## Essential Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+O` | Open/Compare Files |
| `Ctrl+S` | Save Current File |
| `F5` | Refresh Comparison |
| `F7` | Previous Difference |
| `F8` | Next Difference |
| `Ctrl+G` | Go to Line |
| `Ctrl+F` | Find |
| `Ctrl+→` | Copy Left to Right |
| `Ctrl+←` | Copy Right to Left |

## Command-Line Options

```
python main.py [file1] [file2] [options]

Options:
  --dir                 Compare directories instead of files
  --no-gui              Run in command-line mode only
  --html                Generate HTML report
  --unified             Generate unified diff format
  -o FILE               Output to file
  --ignore-case         Ignore case differences
  --ignore-whitespace   Ignore whitespace differences
  --syntax LANG         Enable syntax highlighting
  --theme dark|light    Set GUI theme
```

## Common Tasks

### 1. Quick File Comparison
```powershell
python main.py file1.txt file2.txt
```
- Opens in GUI
- Shows differences side-by-side
- Press F8 to jump between differences

### 2. Compare with Ignore Options
```powershell
python main.py file1.txt file2.txt --ignore-whitespace --ignore-case
```

### 3. Directory Sync
```powershell
python main.py --dir C:\source C:\backup
```
- Shows all file differences
- Identifies missing files
- Can copy or sync directories

### 4. Generate Report for Review
```powershell
python main.py old_version.py new_version.py --html --output review.html --no-gui
```
- Creates beautiful HTML report
- Can be shared via email
- Interactive navigation

### 5. Batch Processing
Create `compare.bat`:
```batch
@echo off
for %%f in (*.txt) do (
    python main.py original\%%f modified\%%f --unified --output diffs\%%~nf.diff --no-gui
)
```

## Configuration File Location
```
%APPDATA%\PythonExamDiff\config.yaml
```

Edit to change:
- Colors
- Fonts
- Default options
- Window size

## Troubleshooting

### Import Error
```powershell
pip install -r requirements.txt --force-reinstall
```

### GUI Not Working
```powershell
pip install customtkinter
```

### Encoding Issues
```powershell
python main.py file1.txt file2.txt --encoding utf-8
```

## Project Structure
```
EXAMDIFF/
├── main.py              ← Entry point
├── config.py            ← Configuration
├── core/                ← Comparison engine
│   ├── myers_algorithm.py
│   ├── diff_engine.py
│   ├── file_handler.py
│   └── directory_handler.py
├── gui/                 ← User interface
│   └── main_window.py
├── utils/               ← Utilities
├── plugins/             ← Plugin system
└── tests/               ← Unit tests
```

## Quick Examples

### Python Files
```powershell
python main.py script_v1.py script_v2.py --syntax python
```

### Configuration Files
```powershell
python main.py old_config.json new_config.json --syntax json
```

### Large Files
```powershell
python main.py large1.log large2.log --no-gui --unified --output diff.txt
```

### Websites (HTML)
```powershell
python main.py site_old.html site_new.html --syntax html --html --output comparison.html --no-gui
```

## Tips & Tricks

1. **Drag & Drop**: Drag files onto window to compare
2. **Recent Files**: File → Recent Files for quick access
3. **Search in Diffs**: Ctrl+F, check "Search in differences only"
4. **Dark Mode**: Edit config.yaml, set `theme: dark`
5. **Custom Colors**: Edit color values in config.yaml
6. **Plugin Development**: See `plugins/example_statistics.py`

## Getting Help

### In-Application
- Help → User Manual
- Help → Keyboard Shortcuts
- Help → About

### Documentation Files
- `README.md` - Full documentation
- `USAGE.md` - Detailed usage guide
- `PROJECT_SUMMARY.md` - Project overview

### Check Logs
```
%APPDATA%\PythonExamDiff\logs\examdiff.log
```

## Build Executable

```powershell
pyinstaller examdiff.spec
```

Output: `dist\PythonExamDiff\PythonExamDiff.exe`

---

## Need More Help?

📖 **Full Documentation**: See README.md
📘 **Usage Guide**: See USAGE.md
🔧 **Developer Guide**: See PROJECT_SUMMARY.md
🐛 **Issues**: Check examdiff.log in AppData

---

**Python ExamDiff Pro** - Professional File & Directory Comparison
Version 1.0.0 | MIT License
