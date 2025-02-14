from typing import Dict, Optional, Set
from tkinter import ttk
from tkinter import TclError

from .notifications.channel import Channel
from .notifications.publisher import Publisher
from .theme_definition import ThemeDefinition
from .color import Colors
from .constants import STANDARD_THEMES, USER_THEMES, DEFAULT_THEME


class Style(ttk.Style):
    """Singleton para gestión básica de temas y sus colores."""

    instance: Optional['Style'] = None

    def __new__(cls, theme=None):
        """Implementación del singleton."""
        if cls.instance is None:
            return object.__new__(cls)
        return cls.instance

    def __init__(self, theme=DEFAULT_THEME):
        """Inicializa la instancia de Style."""
        if self.instance is not None:
            if theme != DEFAULT_THEME:
                self.instance.theme_use(theme)
            return

        # Inicializar ttk.Style primero
        super().__init__()

        # Inicialización de colecciones
        self._theme_objects: Dict = {}
        self._theme_definitions: Dict[str, ThemeDefinition] = {}
        self._theme_names: Set[str] = set()
        self.theme = None

        # Cargar temas ANTES de intentar usar uno
        self._load_themes()

        # Establecer instancia y tema
        Style.instance = self
        self.theme_use(theme)

    def _load_themes(self) -> None:
        """Carga los temas estándar y de usuario."""
        themes = STANDARD_THEMES.copy()
        if USER_THEMES:
            themes.update(USER_THEMES)

        for name, definition in themes.items():
            self.register_theme(
                ThemeDefinition(
                    name=name,
                    themetype=definition["type"],
                    colors=definition["colors"]
                )
            )

    def register_theme(self, definition: ThemeDefinition) -> None:
        """Registra un nuevo tema."""
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_objects[theme] = None

    def theme_use(self, themename=None):
        """Cambia el tema utilizado en la renderización de los widgets.

        Si themename es None, retorna el tema actual. En caso contrario,
        establece el nuevo tema y notifica del cambio a los widgets.

        Este método debe usarse solo para cambiar el tema durante la
        ejecución. Para el tema inicial, use el constructor de Style.

        Args:
            themename: Nombre del tema a aplicar. Si es None, retorna
                      el tema actual.

        Returns:
            str | None: Nombre del tema actual si themename es None,
                       None en caso contrario.

        Raises:
            TclError: Si el tema especificado no es válido.
        """
        if not themename:
            return super().theme_use()

        existing_themes = super().theme_names()

        # Validar si el tema existe
        if themename not in existing_themes and themename not in self._theme_names:
            raise TclError(f"'{themename}' no es un tema válido.")

        # Actualizar el tema actual
        self.theme = self._theme_definitions.get(themename)

        # Aplicar el tema si ya existe
        if themename in existing_themes:
            super().theme_use(themename)

        # Notificar a ambos tipos de widgets sobre el cambio de tema
        Publisher.publish_message(Channel.TTK, themename)
        Publisher.publish_message(Channel.STD, themename)

    def theme_names(self) -> list:
        """Obtiene la lista de temas disponibles."""
        return list(self._theme_definitions.keys())

    @property
    def colors(self) -> Colors:
        """Obtiene los colores del tema actual."""
        theme = self.theme.name if self.theme else None
        if theme in self._theme_names:
            definition = self._theme_definitions.get(theme)
            return definition.colors if definition else Colors()
        return Colors()

    @staticmethod
    def get_instance() -> 'Style':
        """Obtiene la instancia única del gestor de estilos."""
        if Style.instance is None:
            Style()
        return Style.instance