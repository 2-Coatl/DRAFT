from abc import ABC, abstractmethod
from ..colors import Colors


class ThemeBase(ABC):
    """Base abstracta para todos los temas.

    Propósito:
        Definir la interfaz común que todos los temas deben implementar
        para mantener consistencia en el sistema

    Uso:
        class MyTheme(ThemeBase):
            def get_colors(self) -> Colors:
                return Colors(primary='#ff0000', ...)
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre identificador del tema"""
        pass

    @property
    @abstractmethod
    def type(self) -> str:
        """Tipo de tema (light/dark)"""
        pass

    @abstractmethod
    def get_colors(self) -> Colors:
        """Retorna la configuración de colores del tema

        Returns:
            Colors: Objeto con la configuración de colores
        """
        pass