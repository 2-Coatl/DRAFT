import re
from typing import List

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