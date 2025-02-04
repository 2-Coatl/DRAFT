from typing import Dict, Tuple, Any


class ThemeBase:
    name: str
    type: str  # 'light' o 'dark'

    # Colores del tema
    colors: Dict[str, str] = {}

    # Configuración de tipografía
    fonts: Dict[str, Tuple[str, int, str]] = {
        "default": ("Arial", 10),
        "heading": ("Arial", 12, "bold"),
        "title": ("Arial", 14, "bold"),
        "small": ("Arial", 9),
    }

    # Espaciado y dimensiones
    spacing: Dict[str, int] = {
        "small": 5,
        "medium": 10,
        "large": 20,
        "xlarge": 30
    }

    # Bordes y radios
    geometry: Dict[str, Any] = {
        "border_width": 1,
        "border_radius": 4,
        "button_padding": (10, 5),
        "input_padding": (5, 5),
        "widget_height": 30
    }

    # Configuraciones específicas de widgets
    widgets: Dict[str, Dict[str, Any]] = {
        "button": {
            "height": 30,
            "padding": (10, 5),
            "font": ("Arial", 10)
        },
        "entry": {
            "height": 25,
            "padding": 5,
            "font": ("Arial", 10)
        },
        "treeview": {
            "row_height": 25,
            "header_height": 30,
            "font": ("Arial", 10)
        }
    }

    @classmethod
    def get_font(cls, font_type: str) -> Tuple[str, int, str]:
        return cls.fonts.get(font_type, cls.fonts["default"])

    @classmethod
    def get_spacing(cls, size: str) -> int:
        return cls.spacing.get(size, cls.spacing["medium"])

    @classmethod
    def get_widget_config(cls, widget_type: str) -> Dict[str, Any]:
        return cls.widgets.get(widget_type, {})