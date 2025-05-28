import tkinter as tk
from tkinter import ttk

class ThemeManager:
    # Color scheme
    COLORS = {
        'bg_dark': '#1e1e2e',
        'bg_darker': '#181825',
        'bg_lighter': '#313244',
        'fg_light': '#cdd6f4',
        'accent': '#89b4fa',
        'accent_darker': '#74c7ec',
        'success': '#a6e3a1',
        'warning': '#fab387',
        'error': '#f38ba8',
        'border': '#45475a'
    }

    @classmethod
    def apply_theme(cls):
        style = ttk.Style()
        style.theme_use('clam')  # Use clam as base theme

        # Configure common elements
        style.configure('.',
            background=cls.COLORS['bg_dark'],
            foreground=cls.COLORS['fg_light'],
            fieldbackground=cls.COLORS['bg_lighter'],
            troughcolor=cls.COLORS['bg_darker'],
            selectbackground=cls.COLORS['accent'],
            selectforeground=cls.COLORS['bg_darker'],
            borderwidth=1,
            relief='flat'
        )

        # Frame styling
        style.configure('TFrame',
            background=cls.COLORS['bg_dark']
        )
        
        # Label styling
        style.configure('TLabel',
            background=cls.COLORS['bg_dark'],
            foreground=cls.COLORS['fg_light']
        )
        
        # Title label
        style.configure('Title.TLabel',
            font=('Helvetica', 16, 'bold'),
            foreground=cls.COLORS['accent']
        )
        
        # Subtitle label
        style.configure('Subtitle.TLabel',
            font=('Helvetica', 12, 'bold'),
            foreground=cls.COLORS['accent_darker']
        )

        # Entry styling
        style.configure('TEntry',
            fieldbackground=cls.COLORS['bg_lighter'],
            foreground=cls.COLORS['fg_light'],
            insertcolor=cls.COLORS['fg_light'],
            borderwidth=1,
            relief='solid',
            padding=5
        )
        style.map('TEntry',
            fieldbackground=[('disabled', cls.COLORS['bg_darker'])]
        )

        # Button styling
        style.configure('TButton',
            background=cls.COLORS['accent'],
            foreground=cls.COLORS['bg_darker'],
            padding=(10, 5),
            font=('Helvetica', 10, 'bold')
        )
        style.map('TButton',
            background=[('active', cls.COLORS['accent_darker'])],
            foreground=[('active', cls.COLORS['bg_darker'])]
        )
        
        # Success button
        style.configure('Success.TButton',
            background=cls.COLORS['success']
        )
        style.map('Success.TButton',
            background=[('active', cls.COLORS['success'])]
        )
        
        # Warning button
        style.configure('Warning.TButton',
            background=cls.COLORS['warning']
        )
        style.map('Warning.TButton',
            background=[('active', cls.COLORS['warning'])]
        )

        # Combobox styling
        style.configure('TCombobox',
            background=cls.COLORS['bg_lighter'],
            foreground=cls.COLORS['fg_light'],
            fieldbackground=cls.COLORS['bg_lighter'],
            arrowcolor=cls.COLORS['fg_light'],
            padding=5
        )
        style.map('TCombobox',
            fieldbackground=[('readonly', cls.COLORS['bg_lighter'])],
            selectbackground=[('readonly', cls.COLORS['accent'])]
        )

        # Notebook styling
        style.configure('TNotebook',
            background=cls.COLORS['bg_darker'],
            borderwidth=0
        )
        style.configure('TNotebook.Tab',
            background=cls.COLORS['bg_darker'],
            foreground=cls.COLORS['fg_light'],
            padding=(10, 5),
            borderwidth=0
        )
        style.map('TNotebook.Tab',
            background=[('selected', cls.COLORS['bg_dark'])],
            foreground=[('selected', cls.COLORS['accent'])]
        )

        # Treeview styling
        style.configure('Treeview',
            background=cls.COLORS['bg_lighter'],
            foreground=cls.COLORS['fg_light'],
            fieldbackground=cls.COLORS['bg_lighter'],
            borderwidth=0,
            rowheight=25
        )
        style.configure('Treeview.Heading',
            background=cls.COLORS['bg_darker'],
            foreground=cls.COLORS['accent'],
            padding=5,
            font=('Helvetica', 10, 'bold')
        )
        style.map('Treeview',
            background=[('selected', cls.COLORS['accent'])],
            foreground=[('selected', cls.COLORS['bg_darker'])]
        )

        # Radiobutton styling
        style.configure('TRadiobutton',
            background=cls.COLORS['bg_dark'],
            foreground=cls.COLORS['fg_light']
        )
        
        # LabelFrame styling
        style.configure('TLabelframe',
            background=cls.COLORS['bg_dark'],
            foreground=cls.COLORS['fg_light']
        )
        style.configure('TLabelframe.Label',
            background=cls.COLORS['bg_dark'],
            foreground=cls.COLORS['accent']
        )

    @classmethod
    def configure_window(cls, window):
        window.configure(bg=cls.COLORS['bg_dark'])
        
        # Configure text widgets background and foreground
        for widget in window.winfo_children():
            if isinstance(widget, tk.Text):
                widget.configure(
                    bg=cls.COLORS['bg_lighter'],
                    fg=cls.COLORS['fg_light'],
                    insertbackground=cls.COLORS['fg_light'],
                    selectbackground=cls.COLORS['accent'],
                    selectforeground=cls.COLORS['bg_darker'],
                    relief='flat',
                    padx=5,
                    pady=5
                ) 