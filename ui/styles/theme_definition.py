from typing import Dict
from .color import Colors

# Constantes para tipo de tema
LIGHT = "light"
DARK = "dark"

class ThemeDefinition:
    """Define un tema incluyendo sus colores y tipo."""

    def __init__(self, name: str, colors: Dict[str, str], themetype: str = LIGHT):
        """
        Parameters:
            name (str): Nombre del tema.
            colors (Dict[str, str]): Diccionario que define los colores del tema.
            themetype (str): Especifica si el tema es "light" o "dark".
        """
        self.name = name
        self.colors = Colors(**colors)
        self.type = themetype

    def __repr__(self) -> str:
        return " ".join([
            f"name={self.name},",
            f"type={self.type},",
            f"colors={self.colors}",
        ])