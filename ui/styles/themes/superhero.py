# ui/styles/themes/superhero.py

from . import ThemeBase
from ..colors import Colors


class SuperheroTheme(ThemeBase):
    """Tema Superhero.

    Implementa un tema oscuro con acentos en tonos azules,
    proporcionando un contraste alto y buena legibilidad.
    """

    @property
    def name(self) -> str:
        return "superhero"

    @property
    def type(self) -> str:
        return "dark"

    def get_colors(self) -> Colors:
        """Define los colores específicos del tema Superhero"""
        return Colors(
            # Colores principales
            primary="#4c9be8",
            secondary="#4e5d6c",
            success="#5cb85c",
            info="#5bc0de",
            warning="#f0ad4e",
            danger="#d9534f",

            # Colores de interfaz
            light="#ABB6C2",
            dark="#20374C",
            bg="#2b3e50",
            fg="#ffffff",

            # Colores de selección y estados
            selectbg="#526170",
            selectfg="#ffffff",
            border="#222222",
            inputfg="#ebebeb",
            inputbg="#32465a",
            active="#2B4155"
        )