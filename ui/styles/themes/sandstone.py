# ui/styles/themes/sandstone.py

from . import ThemeBase
from ..colors import Colors


class SandstoneTheme(ThemeBase):
    """Tema Sandstone.

    Implementa un tema con una paleta de colores cálida 
    basada en tonos arena y tierra.
    """

    @property
    def name(self) -> str:
        return "sandstone"

    @property
    def type(self) -> str:
        return "light"

    def get_colors(self) -> Colors:
        """Define los colores específicos del tema Sandstone"""
        return Colors(
            # Colores principales
            primary="#325D88",
            secondary="#8e8c84",
            success="#93c54b",
            info="#29abe0",
            warning="#f47c3c",
            danger="#d9534f",

            # Colores de interfaz
            light="#F8F5F0",
            dark="#3E3F3A",
            bg="#ffffff",
            fg="#3e3f3a",

            # Colores de selección y estados
            selectbg="#8e8c84",
            selectfg="#ffffff",
            border="#ced4da",
            inputfg="#6E6D69",
            inputbg="#fff",
            active="#e5e5e5"
        )