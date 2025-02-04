from abc import ABC, abstractmethod
from typing import Dict
from .colors import Colors


class ThemeDefinition(ABC):
    """Base abstracta para definir temas personalizados.

    Esta clase sirve como base para implementar temas específicos,
    proporcionando la estructura y métodos necesarios para crear
    nuevos temas.

    Examples:
        ```python
        class LightTheme(ThemeDefinition):
            def __init__(self):
                super().__init__("light", is_light=True)

            def _get_theme_colors(self):
                return {
                    'primary': '#007bff',
                    'secondary': '#6c757d',
                    ...
                }
        ```
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
            ValueError: Si faltan colores requeridos en la implementación
        """
        if self._colors is None:
            try:
                colors_dict = self._get_theme_colors()
                self._colors = Colors(**colors_dict)
            except TypeError as e:
                raise ValueError("Faltan colores requeridos en la definición del tema") from e
        return self._colors

    @abstractmethod
    def _get_theme_colors(self) -> Dict[str, str]:
        """Debe ser implementado por las clases hijas para definir los colores.

        Returns:
            Diccionario con los colores del tema

        Raises:
            NotImplementedError: Si la clase hija no implementa este método
        """
        pass

    def __str__(self) -> str:
        """Representación string del tema.

        Returns:
            Descripción del tema
        """
        return f"{self.name} ({'light' if self.is_light else 'dark'} theme)"