<div align="center">

# 🚀 Python ExamDiff Pro

**Professional File & Directory Comparison Tool for Windows**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

*A production-ready, feature-rich file and directory comparison application with modern GUI, syntax highlighting, and advanced diff algorithms.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Plugin System](#-plugin-system)
- [Project Structure](#-project-structure)
- [Building from Source](#-building-from-source)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

**Python ExamDiff Pro** is a professional-grade file and directory comparison tool built for Windows. It combines the power of industry-standard diff algorithms with a modern, intuitive interface to help developers, content creators, and technical professionals efficiently compare files and directories.

### Why Python ExamDiff Pro?

- ✅ **Production-Ready**: Built with enterprise-grade code quality and error handling
- ✅ **Modern UI**: Beautiful CustomTkinter interface with dark/light themes
- ✅ **Powerful Engine**: Implements Myers' diff algorithm for accurate comparisons
- ✅ **Extensible**: Plugin system for custom functionality
- ✅ **Comprehensive**: File comparison, directory comparison, three-way merge, and more
- ✅ **Developer-Friendly**: Full CLI support, Git integration, and automation-ready

---

## ✨ Features

### 🔍 Core Comparison Engine

| Feature | Description |
|---------|-------------|
| **Myers' Diff Algorithm** | Industry-standard O(ND) complexity algorithm for accurate line-by-line comparison |
| **Multi-Mode Comparison** | Two-way diff, three-way diff, and three-way merge with conflict resolution |
| **Text & Binary Support** | Compare text files with multiple encodings or binary files byte-by-byte |
| **Large File Support** | Efficiently handle files up to 1GB with chunked processing |
| **Smart Ignore Options** | Ignore whitespace, case, blank lines, comments, and custom regex patterns |

### 🎨 Visual Interface

| Feature | Description |
|---------|-------------|
| **Dual-Pane View** | Side-by-side comparison with synchronized scrolling |
| **Color-Coded Highlighting** | 🟢 Green (added), 🔴 Red (deleted), 🟡 Yellow (modified), ⚪ Gray (unchanged) |
| **Three-Level Diff** | Line-level, word-level, and character-level highlighting |
| **Diff Navigation** | Previous/Next/Current with keyboard shortcuts (F7/F8) |
| **Minimap Overview** | Vertical bar showing all differences at a glance |
| **Jump to Line** | Quick navigation to specific line numbers (Ctrl+G) |

### 📁 Directory Comparison

| Feature | Description |
|---------|-------------|
| **Recursive Tree Comparison** | Full directory tree comparison with file status indicators |
| **File Status Indicators** | ✅ Identical, ⚠️ Different, ⬅️ Left only, ➡️ Right only, 🕒 Newer/Older |
| **Flexible Views** | Tree view or flat list with smart filtering |
| **Mass Operations** | Copy, delete, synchronize between directories |
| **Directory Snapshots** | Save comparison state as XML for later review |

### 💻 Syntax Highlighting

| Feature | Description |
|---------|-------------|
| **25+ Languages** | Python, JavaScript, Java, C++, C#, HTML, CSS, SQL, XML, JSON, and more |
| **Multiple Themes** | Light and dark color schemes |
| **Auto-Detection** | Automatic language detection from file extension |
| **Powered by Pygments** | Professional syntax highlighting library |

### 🔧 Advanced Features

| Feature | Description |
|---------|-------------|
| **Inline Editing** | Edit files directly in comparison panes |
| **Copy Operations** | Left→Right or Right→Left (whole file or selected lines) |
| **Merge Changes** | Select and merge specific changes with conflict resolution |
| **Undo/Redo** | Full undo/redo support for all edits |
| **Tabbed Interface** | Multiple comparisons simultaneously |
| **Git Integration** | Compare Git commits and branches |
| **Bookmark System** | Mark important differences for later review |
| **Comparison History** | Save and reload comparison sessions |

### 📊 Reporting & Export

| Feature | Description |
|---------|-------------|
| **HTML Reports** | Interactive navigation with clickable differences |
| **PDF Reports** | Print-ready documents with professional formatting |
| **Unix Diff Format** | Standard diff output for version control |
| **Statistics** | Lines added/deleted/changed with detailed metrics |
| **Print Preview** | Print directly from the application |

### 🪟 Windows Integration

| Feature | Description |
|---------|-------------|
| **Explorer Context Menu** | Right-click to compare files from Windows Explorer |
| **File Associations** | Handle .diff and .patch files |
| **System Tray Icon** | Quick access from system tray |
| **Command-Line Interface** | Full CLI for automation and scripting |
| **Drag & Drop** | Drop files/folders directly onto the window |

---

## 📸 Screenshots

> **Note**: Add screenshots of the application to showcase its features. Recommended screenshots:
> - Main window with file comparison
> - Directory comparison view
> - Syntax highlighting example
> - Three-way merge interface
> - HTML report output

### Main Interface
![Main Window](docs/screenshots/main-window.png)
*Main comparison window showing side-by-side file comparison with syntax highlighting*

### Directory Comparison
![Directory View](docs/screenshots/directory-view.png)
*Directory comparison with tree view and file status indicators*

### Syntax Highlighting
![Syntax Highlighting](docs/screenshots/syntax-highlighting.png)
*Code comparison with Python syntax highlighting enabled*

### Three-Way Merge
![Three-Way Merge](docs/screenshots/three-way-merge.png)
*Three-way merge interface for conflict resolution*

### HTML Report
![HTML Report](docs/screenshots/html-report.png)
*Interactive HTML report with navigation*

---

## 📦 Installation

### Prerequisites

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Windows 10/11** - Primary platform support
- **pip** - Python package manager (included with Python)

### Method 1: Quick Install (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/python-examdiff.git
   cd python-examdiff
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Method 2: PowerShell Installation Script

On Windows, you can use the provided installation script:

```powershell
.\install.ps1
```

This script will:
- Check Python installation
- Create a virtual environment (optional)
- Install all dependencies
- Verify installation

### Method 3: Standalone Executable

Download the pre-built executable from [Releases](https://github.com/yourusername/python-examdiff/releases) and run `PythonExamDiff.exe` directly.

### Building Executable from Source

To create your own standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller examdiff.spec
```

The executable will be in the `dist/PythonExamDiff` folder.

---

## 🚀 Quick Start

### GUI Mode

Launch the application:
```bash
python main.py
```

Then:
1. Click **File → Compare Files** or press `Ctrl+O`
2. Select two files or directories
3. View the comparison results

### Command-Line Mode

**Compare two files:**
```bash
python main.py file1.txt file2.txt
```

**Compare directories:**
```bash
python main.py --dir folder1 folder2
```

**Three-way merge:**
```bash
python main.py --merge base.txt yours.txt theirs.txt -o output.txt
```

**Generate HTML report:**
```bash
python main.py file1.txt file2.txt --html --output report.html --no-gui
```

---

## 📖 Usage

### GUI Mode

#### File Comparison

1. **Open Files**: `File → Compare Files` or `Ctrl+O`
2. **Navigate Differences**: Use `F7` (previous) and `F8` (next)
3. **Copy Changes**: `Ctrl+Right` (left to right) or `Ctrl+Left` (right to left)
4. **Save**: `Ctrl+S` to save changes

#### Directory Comparison

1. **Open Directories**: `File → Compare Directories`
2. **Filter Files**: Use the filter toolbar to show only differences
3. **Synchronize**: `Tools → Synchronize` to copy files between directories
4. **Export**: `File → Export` to save comparison results

#### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open files/directories |
| `Ctrl+S` | Save current file |
| `Ctrl+W` | Close current tab |
| `F5` | Refresh/Re-compare |
| `F7` | Previous difference |
| `F8` | Next difference |
| `Ctrl+G` | Go to line |
| `Ctrl+F` | Find |
| `Ctrl+H` | Find and replace |
| `Ctrl+Left` | Copy to left pane |
| `Ctrl+Right` | Copy to right pane |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+Tab` | Next tab |
| `Ctrl+Shift+Tab` | Previous tab |

### Command-Line Options

```bash
python main.py [FILE1] [FILE2] [OPTIONS]

Positional Arguments:
  files                 Files or directories to compare

Comparison Mode:
  --dir                 Compare directories
  --merge               Three-way merge mode

Output Options:
  -o, --output FILE     Output file path
  --html                Generate HTML report
  --pdf                 Generate PDF report
  --unified             Generate unified diff

Comparison Options:
  --ignore-case         Ignore case differences
  --ignore-whitespace   Ignore whitespace
  --ignore-blank-lines  Ignore blank lines
  --syntax LANG         Syntax highlighting language
  --encoding ENC        File encoding (utf-8, utf-16, etc.)

Directory Options:
  --recursive           Recursive directory comparison (default)
  --no-recursive        Non-recursive comparison

GUI Options:
  --no-gui              Command-line mode only
  --theme THEME         GUI theme (light/dark)
```

### Examples

**Compare Python files with syntax highlighting:**
```bash
python main.py script1.py script2.py --syntax python
```

**Compare directories and generate HTML report:**
```bash
python main.py --dir project1 project2 --html --output report.html --no-gui
```

**Ignore whitespace and case:**
```bash
python main.py file1.txt file2.txt --ignore-whitespace --ignore-case
```

**Three-way merge:**
```bash
python main.py --merge base.txt mine.txt theirs.txt -o merged.txt
```

---

## ⚙️ Configuration

The application uses a YAML configuration file stored at:
```
%APPDATA%\PythonExamDiff\config.yaml
```

### Customization Options

You can customize:

- **Colors**: Diff highlighting colors (added, deleted, modified, unchanged)
- **Fonts**: Font family and size for text display
- **Default Ignore Options**: Case, whitespace, blank lines, comments
- **Keyboard Shortcuts**: Customize key bindings
- **Window Settings**: Size, position, theme preferences
- **Plugin Settings**: Configure loaded plugins
- **Recent Files**: Limit for recent files list

### Editing Configuration

1. **Via GUI**: `Settings → Preferences`
2. **Manually**: Edit `%APPDATA%\PythonExamDiff\config.yaml` directly

### Example Configuration

```yaml
appearance:
  theme: dark
  font_family: Consolas
  font_size: 11

colors:
  added: "#00ff00"
  deleted: "#ff0000"
  modified: "#ffff00"
  unchanged: "#808080"

comparison:
  ignore_case: false
  ignore_whitespace: false
  ignore_blank_lines: false
  ignore_comments: true

window:
  width: 1200
  height: 800
  maximized: false
```

---

## 🔌 Plugin System

Python ExamDiff Pro includes a powerful plugin system for extending functionality.

### Creating a Plugin

1. **Create a plugin file** in the `plugins/` directory:

```python
# plugins/my_plugin.py
from plugins.plugin_base import PluginBase

class MyPlugin(PluginBase):
    name = "My Custom Plugin"
    version = "1.0.0"
    description = "Adds custom functionality"
    
    def initialize(self):
        """Initialize the plugin."""
        return True
    
    def process_diff(self, diff_result):
        """Process diff results."""
        # Your custom processing logic
        return diff_result
    
    def cleanup(self):
        """Cleanup when plugin is unloaded."""
        pass
```

2. **Place the plugin** in the `plugins/` directory
3. **Restart the application** - plugins are auto-loaded on startup

### Plugin API

Plugins can:
- Process diff results before display
- Add custom menu items
- Register keyboard shortcuts
- Generate custom reports
- Integrate with external tools

See `plugins/plugin_base.py` for the complete API documentation.

---

## 📁 Project Structure

```
python-examdiff/
├── core/                          # Core comparison engine
│   ├── __init__.py
│   ├── myers_algorithm.py         # Myers' diff implementation
│   ├── diff_engine.py             # Main diff engine
│   ├── file_handler.py            # File I/O operations
│   └── directory_handler.py       # Directory operations
│
├── gui/                           # GUI components
│   ├── __init__.py
│   ├── main_window.py             # Main application window
│   └── file_select_dialog.py      # File selection dialogs
│
├── utils/                         # Utility modules
│   ├── __init__.py
│   ├── syntax_highlighter.py     # Syntax highlighting
│   ├── report_generator.py        # Report generation
│   └── helpers.py                 # Helper functions
│
├── plugins/                       # Plugin system
│   ├── __init__.py
│   ├── plugin_base.py            # Plugin base class
│   └── example_statistics.py     # Example plugin
│
├── tests/                         # Unit tests
│   ├── __init__.py
│   ├── test_myers.py             # Myers algorithm tests
│   └── test_file_handler.py     # File handler tests
│
├── docs/                          # Documentation
│   └── screenshots/              # Screenshot images
│
├── main.py                        # Application entry point
├── config.py                      # Configuration management
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Package configuration
├── examdiff.spec                  # PyInstaller specification
├── install.ps1                    # Installation script
├── LICENSE                        # MIT License
└── README.md                      # This file
```

---

## 🔨 Building from Source

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/python-examdiff.git
   cd python-examdiff
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies**
   ```bash
   pip install -r requirements.txt[dev]
   ```

### Building Executable

```bash
pip install pyinstaller
pyinstaller examdiff.spec
```

The executable will be in `dist/PythonExamDiff/`.

---

## 🧪 Testing

### Run Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest --cov=. tests/
```

### Run Specific Test

```bash
pytest tests/test_myers.py -v
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** with tests
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for all classes and functions
- Add tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Eugene Myers** - For the Myers diff algorithm
- **ExamDiff Pro** - Inspiration for features and design
- **CustomTkinter** - Modern GUI framework
- **Pygments** - Syntax highlighting library
- **All Contributors** - Thanks to everyone who has contributed!

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/python-examdiff/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/python-examdiff/discussions)
- **Documentation**: See [USAGE.md](USAGE.md) for detailed usage guide

---

## 🗺️ Roadmap

- [ ] Cloud storage integration (Google Drive, OneDrive, Dropbox)
- [ ] Real-time collaboration features
- [ ] AI-powered smart merge suggestions
- [ ] Image comparison with visual diff
- [ ] Multi-language UI (i18n)
- [ ] Web-based interface
- [ ] Integration with more version control systems
- [ ] Performance optimizations for very large files
- [ ] Custom diff algorithm implementations
- [ ] Plugin marketplace

---

<div align="center">

**Made with ❤️ for developers who need powerful comparison tools**

[⭐ Star this repo](https://github.com/yourusername/python-examdiff) • [🐛 Report Bug](https://github.com/yourusername/python-examdiff/issues) • [💡 Request Feature](https://github.com/yourusername/python-examdiff/issues)

</div>
