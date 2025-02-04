from typing import Dict
from ..theme_definition import ThemeDefinition


class SuperheroTheme(ThemeDefinition):
    """Implementación del tema oscuro por defecto."""

    def __init__(self):
        super().__init__("dark", is_light=False)

    def _get_theme_colors(self) -> Dict[str, str]:
        return {
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