from . import ThemeBase


class SuperheroTheme(ThemeBase):
    name = "superhero"
    type = "dark"

    colors = {
        "primary": "#4c9be8",
        "secondary": "#4e5d6c",
        "success": "#5cb85c",
        "info": "#5bc0de",
        "warning": "#f0ad4e",
        "danger": "#d9534f",
        "light": "#ABB6C2",
        "dark": "#20374C",
        "bg": "#2b3e50",
        "fg": "#ffffff",
        "selectbg": "#526170",
        "selectfg": "#ffffff",
        "border": "#222222",
        "inputfg": "#ebebeb",
        "inputbg": "#32465a",
        "active": "#2B4155",
    }

    # Personalizaciones específicas para Superhero
    fonts = {
        **ThemeBase.fonts,
        "default": ("Roboto Condensed", 10),  # Fuente más condensada para tema oscuro
        "heading": ("Roboto Condensed", 12, "bold"),
        "title": ("Roboto Condensed", 14, "bold"),
        "small": ("Roboto Condensed", 9),
    }

    # Personalizar widgets específicos para tema oscuro
    widgets = {
        **ThemeBase.widgets,
        "button": {
            "height": 32,
            "padding": (12, 6),
            "font": ("Roboto Condensed", 10)
        },
        "entry": {
            "height": 28,
            "padding": 8,
            "font": ("Roboto Condensed", 10),
            "relief": "flat"  # Mejor look para tema oscuro
        },
        "treeview": {
            "row_height": 28,
            "header_height": 32,
            "font": ("Roboto Condensed", 10),
            "selected_bg": "#526170"  # Color especial para selección en tema oscuro
        }
    }