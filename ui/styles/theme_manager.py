from typing import Dict, Type, Optional
from .themes import ThemeBase
from .themes.sandstone import SandstoneTheme
from .themes.superhero import SuperheroTheme
from .events import Channel, Publisher


class ThemeManager:
    """Gestor centralizado de temas.

    Maneja el registro y cambio de temas, notificando a través del
    sistema Publisher existente.
    """
    _instance = None
    _current_theme: Optional[ThemeBase] = None
    _available_themes: Dict[str, Type[ThemeBase]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._register_default_themes()
        return cls._instance

    def _register_default_themes(self):
        """Registra los temas disponibles por defecto"""
        self.register_theme(SandstoneTheme)
        self.register_theme(SuperheroTheme)

    def register_theme(self, theme_class: Type[ThemeBase]):
        """Registra un nuevo tema"""
        theme = theme_class()
        self._available_themes[theme.name] = theme_class

    def set_theme(self, name: str) -> bool:
        """Cambia el tema actual y notifica a los suscriptores

        Args:
            name: Nombre del tema a establecer

        Returns:
            bool: True si el cambio fue exitoso
        """
        theme_class = self._available_themes.get(name)
        if theme_class:
            self._current_theme = theme_class()
            # Notificar a través del Publisher existente
            Publisher.publish_message(Channel.STD, self._current_theme)
            return True
        return False

    @property
    def current_theme(self) -> Optional[ThemeBase]:
        """Tema actual"""
        return self._current_theme

    @property
    def available_themes(self) -> list:
        """Lista de nombres de temas disponibles"""
        return list(self._available_themes.keys())