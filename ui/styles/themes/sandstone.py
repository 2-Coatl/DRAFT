from . import ThemeBase


class SandstoneTheme(ThemeBase):
    name = "sandstone"
    type = "light"

    colors = {
        "primary": "#325D88",
        "secondary": "#8e8c84",
        "success": "#93c54b",
        "info": "#29abe0",
        "warning": "#f47c3c",
        "danger": "#d9534f",
        "light": "#F8F5F0",
        "dark": "#3E3F3A",
        "bg": "#ffffff",
        "fg": "#3e3f3a",
        "selectbg": "#8e8c84",
        "selectfg": "#ffffff",
        "border": "#ced4da",
        "inputfg": "#6E6D69",
        "inputbg": "#fff",
        "active": "#e5e5e5",
    }

    # Personalizaciones específicas para Sandstone
    fonts = {
        **ThemeBase.fonts,  # Heredar configuración base
        "default": ("Roboto", 10),  # Sobrescribir fuente por defecto
        "heading": ("Roboto", 12, "bold"),
        "title": ("Roboto", 14, "bold"),
    }

    # Personalizar widgets específicos para Sandstone
    widgets = {
        **ThemeBase.widgets,  # Heredar configuración base
        "button": {
            "height": 32,  # Botones un poco más altos
            "padding": (12, 6),  # Más padding horizontal
            "font": ("Roboto", 10)
        }
    }