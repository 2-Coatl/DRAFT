from tkinter.constants import *
import tkinter as tk
from tkinter import ttk
from typing import Dict


TTK_CLAM = 'clam'
TTK_DEFAULT = 'default'
DEFAULT = 'default'
DEFAULT_THEME = 'cosmo'

# bootstyle colors
PRIMARY = 'primary'
INFO = 'info'
LIGHT = 'light'
DARK = 'dark'

# state constants
READONLY = 'readonly'

STANDARD_THEMES = {
    'cosmo': {
        'type': 'light',
        'colors': {
            'primary': '#007bff',
            'secondary': '#6c757d',
            'success': '#28a745',
            'info': '#17a2b8',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'bg': '#ffffff',
            'fg': '#212529',
            'selectbg': '#0063ce',
            'selectfg': '#ffffff',
            'border': '#dee2e6',
            'inputfg': '#495057',
            'inputbg': '#ffffff',
            'active': '#0056b3'
        }
    },
    'flatly': {
        'type': 'dark',
        'colors': {
            'primary': '#375a7f',
            'secondary': '#444444',
            'success': '#00bc8c',
            'info': '#3498db',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#adb5bd',
            'dark': '#303030',
            'bg': '#222222',
            'fg': '#ffffff',
            'selectbg': '#2b4764',
            'selectfg': '#ffffff',
            'border': '#444444',
            'inputfg': '#ffffff',
            'inputbg': '#303030',
            'active': '#2b4764'
        }
    }
}

# Temas de usuario
USER_THEMES: Dict = {}




TTK_WIDGETS = (
    ttk.Button,
    ttk.Checkbutton,
    ttk.Combobox,
    ttk.Entry,
    ttk.Frame,
    ttk.Labelframe,
    ttk.Label,
    ttk.Menubutton,
    ttk.Notebook,
    ttk.Panedwindow,
    ttk.Progressbar,
    ttk.Radiobutton,
    ttk.Scale,
    ttk.Scrollbar,
    ttk.Separator,
    ttk.Sizegrip,
    ttk.Spinbox,
    ttk.Treeview,
    ttk.OptionMenu,
)

TK_WIDGETS = (
    tk.Tk,
    tk.Toplevel,
    tk.Button,
    tk.Label,
    tk.Text,
    tk.Frame,
    tk.Checkbutton,
    tk.Radiobutton,
    tk.Entry,
    tk.Scale,
    tk.Listbox,
    tk.Menu,
    tk.Menubutton,
    tk.LabelFrame,
    tk.Canvas,
    tk.OptionMenu,
    tk.Spinbox,
)
