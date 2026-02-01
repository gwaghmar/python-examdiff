"""
File Selection Dialog
=====================

Initial dialog for selecting files to compare.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False


class FileSelectDialog(tk.Toplevel):
    """Dialog for selecting files to compare."""
    
    def __init__(self, parent):
        """Initialize the dialog."""
        super().__init__(parent)
        
        self.title("Compare")
        self.geometry("700x170")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.winfo_screenheight() // 2) - (170 // 2)
        self.geometry(f"700x170+{x}+{y}")
        
        # Configure style
        self.configure(bg="#f0f0f0")
        
        # Result
        self.result = None
        self.file1 = tk.StringVar()
        self.file2 = tk.StringVar()
        
        # Build UI
        self._create_widgets()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Title label
        title_label = tk.Label(
            self, 
            text="Select files to compare:",
            font=("Arial", 11),
            bg="#f0f0f0"
        )
        title_label.pack(pady=(15, 10), padx=20, anchor=tk.W)
        
        # File 1 row
        file1_frame = tk.Frame(self, bg="#f0f0f0")
        file1_frame.pack(fill=tk.X, padx=20, pady=5)
        
        file1_label = tk.Label(file1_frame, text="File 1:", width=8, bg="#f0f0f0", font=("Arial", 10))
        file1_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.file1_entry = tk.Entry(
            file1_frame,
            textvariable=self.file1,
            width=70,
            font=("Arial", 10)
        )
        self.file1_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        btn1 = tk.Button(
            file1_frame,
            text="...",
            width=3,
            command=self.browse_file1,
            font=("Arial", 10)
        )
        btn1.pack(side=tk.LEFT)
        
        # File 2 row
        file2_frame = tk.Frame(self, bg="#f0f0f0")
        file2_frame.pack(fill=tk.X, padx=20, pady=5)
        
        file2_label = tk.Label(file2_frame, text="File 2:", width=8, bg="#f0f0f0", font=("Arial", 10))
        file2_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.file2_entry = tk.Entry(
            file2_frame,
            textvariable=self.file2,
            width=70,
            font=("Arial", 10)
        )
        self.file2_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        btn2 = tk.Button(
            file2_frame,
            text="...",
            width=3,
            command=self.browse_file2,
            font=("Arial", 10)
        )
        btn2.pack(side=tk.LEFT)
        
        # Buttons row
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=(15, 15))
        
        ok_btn = tk.Button(
            button_frame,
            text="OK",
            width=12,
            command=self.on_ok,
            font=("Arial", 10),
            bg="#0078d4",
            fg="white"
        )
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            width=12,
            command=self.on_cancel,
            font=("Arial", 10)
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        options_btn = tk.Button(
            button_frame,
            text="Options",
            width=12,
            command=self.on_options,
            font=("Arial", 10)
        )
        options_btn.pack(side=tk.LEFT, padx=5)
    
    def browse_file1(self):
        """Browse for file 1."""
        filename = filedialog.askopenfilename(
            title="Select First File",
            parent=self
        )
        if filename:
            self.file1.set(filename)
    
    def browse_file2(self):
        """Browse for file 2."""
        filename = filedialog.askopenfilename(
            title="Select Second File",
            parent=self
        )
        if filename:
            self.file2.set(filename)
    
    def on_ok(self):
        """Handle OK button."""
        f1 = self.file1.get().strip()
        f2 = self.file2.get().strip()
        
        if not f1 or not f2:
            messagebox.showwarning("Missing Files", "Please select both files.", parent=self)
            return
        
        if not Path(f1).exists():
            messagebox.showerror("File Not Found", f"File 1 does not exist:\n{f1}", parent=self)
            return
        
        if not Path(f2).exists():
            messagebox.showerror("File Not Found", f"File 2 does not exist:\n{f2}", parent=self)
            return
        
        self.result = (f1, f2)
        self.destroy()
    
    def on_cancel(self):
        """Handle Cancel button."""
        self.result = None
        self.destroy()
    
    def on_options(self):
        """Handle Options button."""
        messagebox.showinfo("Options", "Options dialog will be implemented here.", parent=self)
    
    def show(self):
        """Show dialog and wait for result."""
        self.wait_window()
        return self.result
