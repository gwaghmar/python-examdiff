"""
Main Window - Primary Application Window
========================================

The main application window with menu bar, toolbar, and tabbed interface.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, List, Tuple
import os

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    import tkinter.ttk as ttk

from config import get_config_manager
from core.diff_engine import create_diff_engine
from core.file_handler import FileHandler
from core.directory_handler import DirectoryHandler
from gui.file_select_dialog import FileSelectDialog


class MainWindow(ctk.CTk if CTK_AVAILABLE else tk.Tk):
    """Main application window."""
    
    # Theme definitions
    LIGHT_THEME = {
        'bg': '#ffffff',
        'fg': '#000000',
        'toolbar_bg': '#e8e8e8',
        'header_bg': '#d0d0d0',
        'header_fg': '#000000',
        'button_bg': '#0078d4',
        'button_fg': '#ffffff',
        'text_bg': '#ffffff',
        'text_fg': '#000000',
        'linenumber_bg': '#f0f0f0',
        'linenumber_fg': '#666666',
    }
    
    DARK_THEME = {
        'bg': '#2b2b2b',
        'fg': '#ffffff',
        'toolbar_bg': '#1e1e1e',
        'header_bg': '#2b5278',
        'header_fg': '#ffffff',
        'button_bg': '#0078d4',
        'button_fg': '#ffffff',
        'text_bg': '#3c3c3c',
        'text_fg': '#ffffff',
        'linenumber_bg': '#2b2b2b',
        'linenumber_fg': '#666666',
    }
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        self.config_manager = get_config_manager()
        
        # Theme state
        self.current_theme = self.config_manager.get('theme', 'light')
        self.theme = self.LIGHT_THEME if self.current_theme == 'light' else self.DARK_THEME
        
        # Window setup
        self.title("ExamDiff")
        self.geometry(f"{self.config_manager.get('window_width', 1400)}x{self.config_manager.get('window_height', 900)}")
        
        # Set appearance based on theme
        if CTK_AVAILABLE:
            ctk.set_appearance_mode("light" if self.current_theme == 'light' else "dark")
        else:
            try:
                self.configure(bg=self.theme['bg'])
            except:
                pass
        
        # State
        self.current_tab = None
        self.tabs = []
        self.comparison_active = False
        self.left_text = None
        self.right_text = None
        self.left_line_text = None
        self.right_line_text = None
        self.comparison_frame = None
        self.header_frame = None
        self.left_header = None
        self.right_header = None
        self.theme_btn = None
        
        # Build UI
        self._create_menu()
        self._create_toolbar()
        self._create_main_area()
        self._create_statusbar()
        
        # Bind events
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Keyboard shortcuts
        self._setup_shortcuts()
        
        # Show file selection dialog on startup
        self.after(100, self.show_file_select_dialog)
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        menubar.configure(bg=self.theme['toolbar_bg'], fg=self.theme['fg'])
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Compare Files...", command=self.on_compare_files, accelerator="Ctrl+O")
        file_menu.add_command(label="Compare Directories...", command=self.on_compare_directories)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.on_save, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.on_save_as)
        file_menu.add_separator()
        
        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self._update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Alt+F4")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.on_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.on_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", command=self.on_find, accelerator="Ctrl+F")
        edit_menu.add_command(label="Go to Line...", command=self.on_goto_line, accelerator="Ctrl+G")
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy Left to Right", command=self.on_copy_left_to_right, accelerator="Ctrl+Right")
        edit_menu.add_command(label="Copy Right to Left", command=self.on_copy_right_to_left, accelerator="Ctrl+Left")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Next Difference", command=self.on_next_diff, accelerator="F8")
        view_menu.add_command(label="Previous Difference", command=self.on_prev_diff, accelerator="F7")
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Line Numbers")
        view_menu.add_checkbutton(label="Show Whitespace")
        view_menu.add_checkbutton(label="Syntax Highlighting")
        view_menu.add_separator()
        view_menu.add_command(label="Refresh", command=self.on_refresh, accelerator="F5")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Options...", command=self.on_options)
        tools_menu.add_command(label="Generate Report...", command=self.on_generate_report)
        tools_menu.add_separator()
        tools_menu.add_command(label="Plugins...", command=self.on_plugins)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Manual", command=self.on_help)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.on_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.on_about)
    
    def _create_toolbar(self):
        """Create toolbar."""
        toolbar = tk.Frame(self, bg=self.theme['toolbar_bg'], height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        toolbar.pack_propagate(False)
        
        # Buttons
        btn_compare = self._create_toolbar_button(toolbar, "Compare Files", self.on_compare_files)
        btn_compare_dir = self._create_toolbar_button(toolbar, "Compare Dirs", self.on_compare_directories)
        btn_save = self._create_toolbar_button(toolbar, "Save", self.on_save)
        btn_prev = self._create_toolbar_button(toolbar, "◀ Prev", self.on_prev_diff)
        btn_next = self._create_toolbar_button(toolbar, "Next ▶", self.on_next_diff)
        btn_refresh = self._create_toolbar_button(toolbar, "Refresh", self.on_refresh)
        btn_theme = self._create_toolbar_button(toolbar, "☀️ Light" if self.current_theme == 'light' else "🌙 Dark", self.toggle_theme)
        
        # Pack buttons
        for btn in [btn_compare, btn_compare_dir, btn_save, btn_prev, btn_next, btn_refresh]:
            btn.pack(side=tk.LEFT, padx=2, pady=5)
        
        # Pack theme button on the right
        btn_theme.pack(side=tk.RIGHT, padx=5, pady=5)
        self.theme_btn = btn_theme
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.theme = self.LIGHT_THEME if self.current_theme == 'light' else self.DARK_THEME
        self.config_manager.set('theme', self.current_theme)
        
        # Update CTK appearance mode
        if CTK_AVAILABLE:
            ctk.set_appearance_mode("light" if self.current_theme == 'light' else "dark")
        
        # Update button text
        self.theme_btn.configure(text="☀️ Light" if self.current_theme == 'light' else "🌙 Dark")
        
        # Update main window
        try:
            self.configure(bg=self.theme['bg'])
        except:
            pass
        
        # Update toolbar and other frames
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                try:
                    child.configure(bg=self.theme['toolbar_bg'])
                except:
                    pass
        
        # Refresh comparison view if active
        if self.comparison_active:
            self._refresh_theme_colors()
    
    def _create_toolbar_button(self, parent, text, command):
        """Create a toolbar button."""
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=12,
            bg=self.theme['button_bg'],
            fg=self.theme['button_fg'],
            font=("Arial", 9),
            relief=tk.RAISED,
            bd=1
        )
    
    def _create_main_area(self):
        """Create main content area with tabs."""
        if CTK_AVAILABLE:
            self.notebook = ctk.CTkTabview(self)
        else:
            self.notebook = ttk.Notebook(self)
        
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    def show_file_select_dialog(self):
        """Show file selection dialog."""
        dialog = FileSelectDialog(self)
        result = dialog.show()
        
        if result:
            file1, file2 = result
            self.compare_files(file1, file2)
        else:
            # User cancelled - close application
            self.on_closing()
    
    def _create_statusbar(self):
        """Create status bar."""
        self.statusbar = tk.Label(self, text="Ready", anchor=tk.W,
                                 bg=self.theme['toolbar_bg'], fg=self.theme['fg'],
                                 font=("Arial", 9))
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)
    
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        self.bind("<Control-o>", lambda e: self.on_compare_files())
        self.bind("<Control-s>", lambda e: self.on_save())
        self.bind("<Control-w>", lambda e: self.on_close_tab())
        self.bind("<F5>", lambda e: self.on_refresh())
        self.bind("<F7>", lambda e: self.on_prev_diff())
        self.bind("<F8>", lambda e: self.on_next_diff())
        self.bind("<Control-g>", lambda e: self.on_goto_line())
        self.bind("<Control-f>", lambda e: self.on_find())
        self.bind("<Control-z>", lambda e: self.on_undo())
        self.bind("<Control-y>", lambda e: self.on_redo())
        self.bind("<Control-Left>", lambda e: self.on_copy_right_to_left())
        self.bind("<Control-Right>", lambda e: self.on_copy_left_to_right())
    
    def _update_recent_menu(self):
        """Update recent files menu."""
        self.recent_menu.delete(0, tk.END)
        
        recent_pairs = self.config_manager.get('recent_pairs', [])
        if not recent_pairs:
            self.recent_menu.add_command(label="(No recent comparisons)", state=tk.DISABLED)
        else:
            for i, (file1, file2) in enumerate(recent_pairs[:10]):
                label = f"{os.path.basename(file1)} ↔ {os.path.basename(file2)}"
                self.recent_menu.add_command(
                    label=label,
                    command=lambda f1=file1, f2=file2: self._open_recent_pair(f1, f2)
                )
    
    def _open_recent(self, filepath):
        """Open a recent file."""
        # Implementation depends on how files are paired
        messagebox.showinfo("Info", f"Opening {filepath}")
    
    def _open_recent_pair(self, file1: str, file2: str):
        """Open and compare a recent file pair."""
        try:
            if not os.path.exists(file1):
                messagebox.showerror("File Not Found", f"File no longer exists:\n{file1}")
                return
            if not os.path.exists(file2):
                messagebox.showerror("File Not Found", f"File no longer exists:\n{file2}")
                return
            self.compare_files(file1, file2)
        except Exception as e:
            messagebox.showerror("Error", f"Error opening recent pair:\n{e}")
    
    # Menu/Toolbar command handlers
    
    def on_compare_files(self):
        """Handle compare files command."""
        file1 = filedialog.askopenfilename(title="Select First File")
        if not file1:
            return
        
        file2 = filedialog.askopenfilename(title="Select Second File")
        if not file2:
            return
        
        self.compare_files(file1, file2)
    
    def compare_files(self, file1: str, file2: str):
        """
        Compare two files.
        
        Args:
            file1: First file path
            file2: Second file path
        """
        try:
            self.set_status(f"Comparing {os.path.basename(file1)} with {os.path.basename(file2)}...")
            
            # Add to recent file pairs
            recent_pairs = self.config_manager.get('recent_pairs', [])
            # Remove if already exists, then add to front
            recent_pairs = [(f1, f2) for f1, f2 in recent_pairs if not (f1 == file1 and f2 == file2)]
            recent_pairs.insert(0, (file1, file2))
            # Keep only last 20 pairs
            recent_pairs = recent_pairs[:20]
            self.config_manager.set('recent_pairs', recent_pairs)
            self._update_recent_menu()
            
            # Read files
            file_handler = FileHandler()
            lines1, info1 = file_handler.read_file(file1)
            lines2, info2 = file_handler.read_file(file2)
            
            # Compare
            diff_engine = create_diff_engine({
                'ignore_case': self.config_manager.get('ignore_case', False),
                'ignore_whitespace': self.config_manager.get('ignore_whitespace', False),
                'ignore_blank_lines': self.config_manager.get('ignore_blank_lines', False),
            })
            
            results = diff_engine.compare_lines(lines1, lines2)
            
            # Create comparison tab
            self._create_comparison_tab(file1, file2, lines1, lines2, results)
            
            diff_count = len([r for r in results if r.type.value != 'equal'])
            self.set_status(f"Comparison complete. {diff_count} differences found.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error comparing files:\n{e}")
            self.set_status("Error comparing files")
    
    def _create_comparison_tab(self, file1, file2, lines1, lines2, results):
        """Create a tab showing file comparison with synchronized scrolling."""
        self.comparison_active = True
        
        # Update window title
        self.title(f"ExamDiff - {os.path.basename(file1)} | {os.path.basename(file2)}")
        
        # Clear any existing tabs
        if CTK_AVAILABLE:
            self.notebook.destroy()
            self.notebook = ctk.CTkTabview(self)
            self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        else:
            for tab in self.notebook.tabs():
                self.notebook.forget(tab)
        
        # Create main comparison frame
        if CTK_AVAILABLE:
            self.notebook.add("Diff 1")
            frame = self.notebook.tab("Diff 1")
        else:
            frame = tk.Frame(self.notebook, bg=self.theme['bg'])
            self.notebook.add(frame, text="Diff 1")
        
        self.comparison_frame = frame
        
        # Create header with file paths
        header = tk.Frame(frame, bg=self.theme['header_bg'], height=30)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        left_header = tk.Label(header, text=f"  {file1}", bg=self.theme['header_bg'], 
                              fg=self.theme['header_fg'], anchor=tk.W, font=("Arial", 10))
        left_header.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        separator = tk.Frame(header, bg=self.theme['header_bg'], width=1)
        separator.pack(side=tk.LEFT, fill=tk.Y)
        
        right_header = tk.Label(header, text=f"  {file2}", bg=self.theme['header_bg'], 
                               fg=self.theme['header_fg'], anchor=tk.W, font=("Arial", 10))
        right_header.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Store reference for theme updates
        self.header_frame = header
        self.left_header = left_header
        self.right_header = right_header
        
        # Create container for both panes and scrollbars
        content_frame = tk.Frame(frame, bg=self.theme['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Shared vertical scrollbar
        shared_scroll_y = tk.Scrollbar(content_frame, orient=tk.VERTICAL)
        shared_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Left pane (File 1)
        left_frame = tk.Frame(content_frame, bg=self.theme['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Line numbers for left
        left_lines_frame = tk.Frame(left_frame, width=50, bg=self.theme['linenumber_bg'])
        left_lines_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_lines_frame.pack_propagate(False)
        
        left_line_text = tk.Text(left_lines_frame, width=5, bg=self.theme['linenumber_bg'], 
                                fg=self.theme['linenumber_fg'], font=("Courier New", 10), 
                                state=tk.DISABLED, takefocus=0, bd=0, padx=3, pady=0,
                                highlightthickness=0)
        left_line_text.pack(fill=tk.BOTH, expand=True)
        
        # Left text
        left_text = tk.Text(left_frame, wrap=tk.NONE, font=("Courier New", 10),
                           bg=self.theme['text_bg'], fg=self.theme['text_fg'], 
                           padx=5, pady=0, highlightthickness=0,
                           yscrollcommand=shared_scroll_y.set)
        left_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Left horizontal scrollbar
        left_scroll_x = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=left_text.xview)
        left_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        left_text.config(xscrollcommand=left_scroll_x.set)
        
        # Divider between panes
        divider = tk.Frame(content_frame, bg=self.theme['header_bg'], width=2)
        divider.pack(side=tk.LEFT, fill=tk.Y)
        divider.pack_propagate(False)
        
        # Right pane (File 2)
        right_frame = tk.Frame(content_frame, bg=self.theme['bg'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Line numbers for right
        right_lines_frame = tk.Frame(right_frame, width=50, bg=self.theme['linenumber_bg'])
        right_lines_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_lines_frame.pack_propagate(False)
        
        right_line_text = tk.Text(right_lines_frame, width=5, bg=self.theme['linenumber_bg'], 
                                 fg=self.theme['linenumber_fg'], font=("Courier New", 10), 
                                 state=tk.DISABLED, takefocus=0, bd=0, padx=3, pady=0,
                                 highlightthickness=0)
        right_line_text.pack(fill=tk.BOTH, expand=True)
        
        # Right text
        right_text = tk.Text(right_frame, wrap=tk.NONE, font=("Courier New", 10),
                            bg=self.theme['text_bg'], fg=self.theme['text_fg'], 
                            padx=5, pady=0, highlightthickness=0,
                            yscrollcommand=shared_scroll_y.set)
        right_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right horizontal scrollbar
        right_scroll_x = tk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=right_text.xview)
        right_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        right_text.config(xscrollcommand=right_scroll_x.set)
        
        # Configure shared scrollbar to control both text widgets
        def shared_scroll_command(first, last):
            shared_scroll_y.set(first, last)
            left_text.yview_moveto(first)
            right_text.yview_moveto(first)
            left_line_text.yview_moveto(first)
            right_line_text.yview_moveto(first)
        
        left_text.config(yscrollcommand=shared_scroll_command)
        right_text.config(yscrollcommand=shared_scroll_command)
        
        # Configure shared scrollbar
        shared_scroll_y.config(command=lambda *args: (
            left_text.yview(*args),
            right_text.yview(*args),
            left_line_text.yview(*args),
            right_line_text.yview(*args)
        ))
        
        # Configure tags for highlighting
        left_text.tag_config("added", background="#90EE90")
        left_text.tag_config("deleted", background="#FFB6C1")
        left_text.tag_config("changed", background="#FFD700")
        left_text.tag_config("blank_added", background="#E8F5E9")  # Light green for blank lines
        left_text.tag_config("blank_deleted", background="#FCE4EC")  # Light red for blank lines
        
        right_text.tag_config("added", background="#90EE90")
        right_text.tag_config("deleted", background="#FFB6C1")
        right_text.tag_config("changed", background="#FFD700")
        right_text.tag_config("blank_added", background="#E8F5E9")  # Light green for blank lines
        right_text.tag_config("blank_deleted", background="#FCE4EC")  # Light red for blank lines
        
        # Store references for theme updates
        self.left_text = left_text
        self.right_text = right_text
        self.left_line_text = left_line_text
        self.right_line_text = right_line_text
        
        # Populate with content - keep both sides visually aligned
        for result in results:
            if result.type.value == 'equal':
                for line in result.old_lines:
                    left_text.insert(tk.END, line + "\n")
                    right_text.insert(tk.END, line + "\n")
            
            elif result.type.value == 'delete':
                # Add deleted lines on left, blank lines on right (with light red highlighting)
                for line in result.old_lines:
                    line_start = left_text.index("end-1c")
                    left_text.insert(tk.END, line + "\n")
                    line_end = left_text.index("end-1c")
                    left_text.tag_add("deleted", line_start, line_end)
                    
                    # Add blank line on right with light red highlighting
                    blank_start = right_text.index("end-1c")
                    right_text.insert(tk.END, "\n")
                    blank_end = right_text.index("end-1c")
                    right_text.tag_add("blank_deleted", blank_start, blank_end)
            
            elif result.type.value == 'insert':
                # Add inserted lines on right, blank lines on left (with light green highlighting)
                for line in result.new_lines:
                    # Add blank line on left with light green highlighting
                    blank_start = left_text.index("end-1c")
                    left_text.insert(tk.END, "\n")
                    blank_end = left_text.index("end-1c")
                    left_text.tag_add("blank_added", blank_start, blank_end)
                    
                    line_start = right_text.index("end-1c")
                    right_text.insert(tk.END, line + "\n")
                    line_end = right_text.index("end-1c")
                    right_text.tag_add("added", line_start, line_end)
            
            elif result.type.value == 'replace':
                # Add changed lines, padding with blank lines to keep alignment
                max_lines = max(len(result.old_lines), len(result.new_lines))
                
                # Add old lines (changed)
                for i in range(max_lines):
                    if i < len(result.old_lines):
                        line_start = left_text.index("end-1c")
                        left_text.insert(tk.END, result.old_lines[i] + "\n")
                        line_end = left_text.index("end-1c")
                        left_text.tag_add("changed", line_start, line_end)
                    else:
                        blank_start = left_text.index("end-1c")
                        left_text.insert(tk.END, "\n")
                        blank_end = left_text.index("end-1c")
                        left_text.tag_add("blank_deleted", blank_start, blank_end)
                    
                    if i < len(result.new_lines):
                        line_start = right_text.index("end-1c")
                        right_text.insert(tk.END, result.new_lines[i] + "\n")
                        line_end = right_text.index("end-1c")
                        right_text.tag_add("changed", line_start, line_end)
                    else:
                        blank_start = right_text.index("end-1c")
                        right_text.insert(tk.END, "\n")
                        blank_end = right_text.index("end-1c")
                        right_text.tag_add("blank_deleted", blank_start, blank_end)
        
        # Now populate line numbers based on actual content
        left_lines = left_text.get('1.0', 'end').split('\n')
        right_lines = right_text.get('1.0', 'end').split('\n')
        
        left_line_num = 1
        for i, line in enumerate(left_lines[:-1]):  # Skip last empty line
            left_line_text.config(state=tk.NORMAL)
            left_line_text.insert(tk.END, f"{left_line_num}\n")
            left_line_text.config(state=tk.DISABLED)
            left_line_num += 1
        
        right_line_num = 1
        for i, line in enumerate(right_lines[:-1]):  # Skip last empty line
            right_line_text.config(state=tk.NORMAL)
            right_line_text.insert(tk.END, f"{right_line_num}\n")
            right_line_text.config(state=tk.DISABLED)
            right_line_num += 1
        
        left_text.config(state=tk.DISABLED)
        right_text.config(state=tk.DISABLED)
    
    def _refresh_theme_colors(self):
        """Refresh theme colors for active comparison view."""
        if not (self.left_text and self.right_text):
            return
        
        # Update text widgets
        self.left_text.config(bg=self.theme['text_bg'], fg=self.theme['text_fg'])
        self.right_text.config(bg=self.theme['text_bg'], fg=self.theme['text_fg'])
        self.left_line_text.config(bg=self.theme['linenumber_bg'], fg=self.theme['linenumber_fg'])
        self.right_line_text.config(bg=self.theme['linenumber_bg'], fg=self.theme['linenumber_fg'])
        
        # Update header
        if self.header_frame:
            self.header_frame.config(bg=self.theme['header_bg'])
        if self.left_header:
            self.left_header.config(bg=self.theme['header_bg'], fg=self.theme['header_fg'])
        if self.right_header:
            self.right_header.config(bg=self.theme['header_bg'], fg=self.theme['header_fg'])
        
        # Update comparison frame background
        if self.comparison_frame:
            self.comparison_frame.config(bg=self.theme['bg'])
    
    def on_compare_directories(self):
        """Handle compare directories command."""
        dir1 = filedialog.askdirectory(title="Select First Directory")
        if not dir1:
            return
        
        dir2 = filedialog.askdirectory(title="Select Second Directory")
        if not dir2:
            return
        
        self.compare_directories(dir1, dir2)
    
    def compare_directories(self, dir1: str, dir2: str):
        """
        Compare two directories.
        
        Args:
            dir1: First directory path
            dir2: Second directory path
        """
        try:
            self.set_status(f"Comparing directories...")
            
            # Add to recent
            self.config_manager.add_recent_dir(dir1)
            self.config_manager.add_recent_dir(dir2)
            
            # Compare
            from core.directory_handler import CompareMode
            handler = DirectoryHandler(
                compare_mode=CompareMode.CONTENT,
                recursive=self.config_manager.get('dir_recursive', True)
            )
            
            result = handler.compare_directories(dir1, dir2, 
                progress_callback=lambda msg: self.set_status(msg))
            
            # Show results
            stats = result.get_statistics()
            self.set_status(f"Directory comparison complete. {stats['different']} differences found.")
            
            messagebox.showinfo("Directory Comparison", 
                f"Total files: {stats['total']}\n" +
                f"Identical: {stats['identical']}\n" +
                f"Different: {stats['different']}\n" +
                f"Left only: {stats['left_only']}\n" +
                f"Right only: {stats['right_only']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error comparing directories:\n{e}")
            self.set_status("Error comparing directories")
    
    def on_save(self):
        """Handle save command."""
        messagebox.showinfo("Info", "Save functionality")
    
    def on_save_as(self):
        """Handle save as command."""
        messagebox.showinfo("Info", "Save As functionality")
    
    def on_close_tab(self):
        """Handle close tab command."""
        pass
    
    def on_undo(self):
        """Handle undo command."""
        pass
    
    def on_redo(self):
        """Handle redo command."""
        pass
    
    def on_find(self):
        """Handle find command."""
        messagebox.showinfo("Info", "Find functionality")
    
    def on_goto_line(self):
        """Handle go to line command."""
        messagebox.showinfo("Info", "Go to Line functionality")
    
    def on_copy_left_to_right(self):
        """Handle copy left to right command."""
        pass
    
    def on_copy_right_to_left(self):
        """Handle copy right to left command."""
        pass
    
    def on_next_diff(self):
        """Handle next difference command."""
        pass
    
    def on_prev_diff(self):
        """Handle previous difference command."""
        pass
    
    def on_refresh(self):
        """Handle refresh command."""
        messagebox.showinfo("Info", "Refresh functionality")
    
    def on_options(self):
        """Handle options command."""
        messagebox.showinfo("Info", "Options dialog will open here")
    
    def on_generate_report(self):
        """Handle generate report command."""
        messagebox.showinfo("Info", "Report generation functionality")
    
    def on_plugins(self):
        """Handle plugins command."""
        messagebox.showinfo("Info", "Plugins manager")
    
    def on_help(self):
        """Handle help command."""
        messagebox.showinfo("Help", "Python ExamDiff Pro User Manual\n\nFor full documentation, see README.md")
    
    def on_shortcuts(self):
        """Handle shortcuts command."""
        shortcuts = """
Keyboard Shortcuts:

Ctrl+O       - Compare Files
Ctrl+S       - Save
Ctrl+W       - Close Tab
F5           - Refresh
F7           - Previous Difference
F8           - Next Difference
Ctrl+G       - Go to Line
Ctrl+F       - Find
Ctrl+Z       - Undo
Ctrl+Y       - Redo
Ctrl+Left    - Copy Right to Left
Ctrl+Right   - Copy Left to Right
        """
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    
    def on_about(self):
        """Handle about command."""
        about_text = """
Python ExamDiff Pro
Version 1.0.0

Professional File & Directory Comparison Tool

© 2026 - MIT License

Features:
• Myers' Diff Algorithm
• Syntax Highlighting
• Directory Comparison
• Three-Way Merge
• And much more!

Built with Python and CustomTkinter
        """
        messagebox.showinfo("About", about_text)
    
    def set_status(self, message: str):
        """
        Update status bar.
        
        Args:
            message: Status message
        """
        if hasattr(self, 'statusbar'):
            self.statusbar.configure(text=message)
            self.update_idletasks()
    
    def on_closing(self):
        """Handle window closing."""
        # Save window size
        self.config_manager.set('window_width', self.winfo_width())
        self.config_manager.set('window_height', self.winfo_height())
        
        # Close
        self.destroy()


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
