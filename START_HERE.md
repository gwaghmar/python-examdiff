# 🎉 WELCOME TO PYTHON EXAMDIFF PRO

## You're Ready to Go! Here's How to Start:

### 📦 STEP 1: Install Dependencies (One Time Only)

Open PowerShell in this directory and run:

```powershell
.\install.ps1
```

**OR** manually install:

```powershell
pip install -r requirements.txt
```

---

### 🚀 STEP 2: Launch the Application

#### Option A: GUI Mode (Recommended for First Time)
```powershell
python main.py
```

#### Option B: Compare Two Files Directly
```powershell
python main.py file1.txt file2.txt
```

#### Option C: Compare Directories
```powershell
python main.py --dir folder1 folder2
```

---

### ✨ WHAT YOU GET

This is a **production-ready professional diff tool** with:

✅ **Myers' Diff Algorithm** - Industry-standard comparison
✅ **Modern GUI** - CustomTkinter Windows 11 style  
✅ **Syntax Highlighting** - 25+ programming languages
✅ **Directory Comparison** - Recursive with filtering
✅ **HTML Reports** - Beautiful interactive reports
✅ **Plugin System** - Extend with custom features
✅ **CLI Mode** - Automate with command-line
✅ **Three-Way Merge** - Conflict resolution
✅ **Binary Files** - Hex dump comparison
✅ **Large Files** - Handles files over 1GB

---

### 📚 QUICK LINKS

- **Full Documentation**: [README.md](README.md)
- **Usage Guide**: [USAGE.md](USAGE.md)
- **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **API Examples**: [examples.py](examples.py)
- **Project Overview**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

### ⌨️ ESSENTIAL KEYBOARD SHORTCUTS

| Key | Action |
|-----|--------|
| `Ctrl+O` | Compare Files |
| `F8` | Next Difference |
| `F7` | Previous Difference |
| `Ctrl+G` | Go to Line |
| `F5` | Refresh |

---

### 🔧 CONFIGURATION

Config file location:
```
%APPDATA%\PythonExamDiff\config.yaml
```

Customize:
- Colors (diff highlighting)
- Fonts (family and size)
- Ignore options (whitespace, case, etc.)
- Theme (dark/light)
- Window size

---

### 📋 COMMON COMMANDS

```powershell
# Basic comparison
python main.py file1.txt file2.txt

# Ignore whitespace
python main.py file1.txt file2.txt --ignore-whitespace

# Generate HTML report
python main.py old.py new.py --html --output report.html --no-gui

# Compare directories
python main.py --dir C:\project1 C:\project2

# With syntax highlighting
python main.py script1.py script2.py --syntax python

# Get help
python main.py --help
```

---

### 🎯 TRY THESE EXAMPLES

1. **Test the CLI**:
   ```powershell
   python examples.py
   ```

2. **Run Tests**:
   ```powershell
   pytest tests/ -v
   ```

3. **Compare This README**:
   Create two versions of a file and compare:
   ```powershell
   python main.py README.md USAGE.md
   ```

---

### 🐛 TROUBLESHOOTING

**"Module not found" error?**
```powershell
pip install -r requirements.txt --force-reinstall
```

**GUI not working?**
```powershell
pip install customtkinter
```

**Check logs**:
```
%APPDATA%\PythonExamDiff\logs\examdiff.log
```

---

### 📦 BUILD EXECUTABLE

Want a standalone .exe?

```powershell
pip install pyinstaller
pyinstaller examdiff.spec
```

Output: `dist\PythonExamDiff\PythonExamDiff.exe`

---

### 🌟 WHAT MAKES THIS SPECIAL

1. **Real Algorithm Implementation**: Not just a wrapper around difflib
2. **Production Quality**: Error handling, logging, testing
3. **Fully Extensible**: Plugin system for custom features
4. **Well Documented**: 1000+ lines of documentation
5. **Modern Stack**: Python 3.11+, CustomTkinter, Pygments
6. **Enterprise Grade**: Handles edge cases, large files, binary files

---

### 🎓 LEARNING THE CODE

The codebase includes extensive comments explaining:

- **Myers' Algorithm**: Step-by-step implementation
- **Design Patterns**: MVC, Factory, Plugin patterns  
- **Best Practices**: Type hints, error handling, logging
- **Python Features**: Dataclasses, Enums, ABC, pathlib

Great for learning professional Python development!

---

### 🔌 EXTENDING WITH PLUGINS

See `plugins/example_statistics.py` for a working example.

Create your own:

```python
from plugins.plugin_base import PluginBase

class MyPlugin(PluginBase):
    name = "My Plugin"
    version = "1.0.0"
    
    def initialize(self):
        return True
    
    def process_diff(self, diff_result):
        # Your custom logic
        return diff_result
```

Save in `plugins/` and it auto-loads!

---

### 💡 PRO TIPS

1. Drag files onto the GUI window to compare
2. Use `--no-gui` for batch processing
3. Save comparison sessions (File → Save Session)
4. Create custom color schemes in config.yaml
5. Use plugins for project-specific logic
6. Generate HTML reports for sharing
7. Set up Windows Explorer context menu integration

---

### 🚀 YOU'RE ALL SET!

To get started right now:

```powershell
python main.py
```

Then click **"Compare Files"** or press `Ctrl+O`.

---

### 📬 NEED HELP?

- Check the log file: `%APPDATA%\PythonExamDiff\logs\examdiff.log`
- Read [USAGE.md](USAGE.md) for detailed examples
- See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture
- Run `python main.py --help` for command-line options

---

**Happy Comparing! 🎉**

*Python ExamDiff Pro - Professional File & Directory Comparison*
*Version 1.0.0 | MIT License*
