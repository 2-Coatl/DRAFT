from typing import Dict
from ..theme_definition import ThemeDefinition

class SandstoneTheme(ThemeDefinition):
    """Implementación del tema claro por defecto."""

    def __init__(self):
        super().__init__("light", is_light=True)

    def _get_theme_colors(self) -> Dict[str, str]:
        return {
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
