from typing import Dict
from .colors import Colors
from .constants import REQUIRED_COLORS


class ThemeDefinition:
    """Define la estructura base para todos los temas.

    Esta clase actúa como base para implementar temas específicos,
    proporcionando la estructura y validación necesaria.
    """

    def __init__(self, name: str, is_light: bool):
        """Inicializa un nuevo tema.

        Args:
            name: Nombre único del tema
            is_light: True si es un tema claro, False si es oscuro
        """
        self.name = name
        self.is_light = is_light
        self._colors = None

    def get_colors(self) -> Colors:
        """Obtiene los colores del tema.

        Returns:
            Objeto Colors con la definición de colores del tema

        Raises:
            NotImplementedError: Si la clase hija no implementa _get_theme_colors
        """
        if self._colors is None:
            colors_dict = self._get_theme_colors()
            # Validar que estén todos los colores requeridos
            missing = [color for color in REQUIRED_COLORS if color not in colors_dict]
            if missing:
                raise ValueError(f"Faltan colores requeridos: {', '.join(missing)}")
            self._colors = Colors(**colors_dict)
        return self._colors

    def _get_theme_colors(self) -> Dict[str, str]:
        """Debe ser implementado por las clases hijas para definir los colores.

        Returns:
            Diccionario con los colores del tema

        Raises:
            NotImplementedError: Este metodo debe ser implementado
        """
        raise NotImplementedError("Las clases hijas deben implementar _get_theme_colors")