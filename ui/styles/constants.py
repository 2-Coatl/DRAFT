import re
from typing import List, Dict

class Keywords:
    """Define las palabras clave y patrones para el sistema de estilos."""

    COLORS: List[str] = [
        "primary",
        "secondary",
        "success",
        "info",
        "warning",
        "danger",
        "light",
        "dark",
    ]

    ORIENTS: List[str] = [
        "horizontal",
        "vertical"
    ]

    TYPES: List[str] = [
        "outline",
        "link",
        "inverse",
        "round",
        "square",
        "striped",
        "focus",
        "input",
        "date",
        "metersubtxt",
        "meter",
        "table"
    ]

    CLASSES: List[str] = [
        "button",
        "progressbar",
        "checkbutton",
        "combobox",
        "entry",
        "labelframe",
        "label",
        "frame",
        "floodgauge",
        "sizegrip",
        "optionmenu",
        "menubutton",
        "menu",
        "notebook",
        "panedwindow",
        "radiobutton",
        "separator",
        "scrollbar",
        "spinbox",
        "scale",
        "text",
        "toolbutton",
        "treeview",
        "toggle",
        "tk",
        "calendar",
        "listbox",
        "canvas",
        "toplevel",
    ]

    # Compilar los patrones de expresiones regulares una sola vez
    COLOR_PATTERN = re.compile("|".join(COLORS))
    ORIENT_PATTERN = re.compile("|".join(ORIENTS))
    CLASS_PATTERN = re.compile("|".join(CLASSES))
    TYPE_PATTERN = re.compile("|".join(TYPES))

STANDARD_THEMES = {
    'light': {
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
    'dark': {
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