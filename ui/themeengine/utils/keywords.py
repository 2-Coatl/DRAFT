import re
from typing import List, Pattern

class Keywords:
    """Clase utilitaria que define las constantes y patrones para el sistema de estilos.

    Esta clase contiene las definiciones de:
    - Colores válidos del sistema
    - Orientaciones posibles de widgets
    - Tipos de estilos disponibles
    - Clases de widgets soportadas
    - Patrones de expresiones regulares para parsing
    """

    # Colores base del sistema
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

    # Orientaciones posibles para widgets
    ORIENTS: List[str] = ["horizontal", "vertical"]

    # Tipos de estilos disponibles
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

    # Clases de widgets soportadas
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

    # Patrones de expresiones regulares precompilados
    COLOR_PATTERN: Pattern = re.compile("|".join(COLORS))
    ORIENT_PATTERN: Pattern = re.compile("|".join(ORIENTS))
    CLASS_PATTERN: Pattern = re.compile("|".join(CLASSES))
    TYPE_PATTERN: Pattern = re.compile("|".join(TYPES))