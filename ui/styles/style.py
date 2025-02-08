from typing import Dict, Optional, Set, Any
from tkinter import ttk, TclError
from .constants import USER_THEMES, STANDARD_THEMES
from .style_builder_tk import StyleBuilderTK
from .style_builder_ttk import StyleBuilderTTK
from .theme_definition import ThemeDefinition
from .colors import Colors
from .events import Publisher, Channel


class Style(ttk.Style):
    """Singleton para crear y gestionar temas y estilos de widgets.

    Hereda de ttk.Style y gestiona:
    1. Sistema de temas y estilos
    2. Comunicación entre componentes
    3. Sincronización de widgets TTK y heredados

    Examples:
        >>> style = Style()  # Tema por defecto
        >>> style = Style('dark')  # Tema específico
        >>> style.theme_use('custom')  # Cambiar tema
    """

    instance: Optional['Style'] = None
    DEFAULT_THEME = 'light'

    def __new__(cls, theme=None):
        """Implementación del singleton.

        Args:
            theme: Nombre opcional del tema inicial

        Returns:
            Style: Instancia única de Style
        """
        if cls.instance is None:
            return object.__new__(cls)
        return cls.instance

    def __init__(self, theme=DEFAULT_THEME):
        """Inicializa o actualiza la instancia de Style.

        Args:
            theme: Nombre del tema a usar al iniciar
        """
        if self.instance is not None:
            if theme != self.DEFAULT_THEME:
                self.instance.theme_use(theme)
            return

        # Inicialización de colecciones
        self._theme_objects: Dict = {}  # StyleBuilders por tema
        self._theme_definitions: Dict[str, ThemeDefinition] = {}
        self._style_registry: Set[str] = set()  # Estilos usados
        self._theme_styles: Dict[str, Set[str]] = {}  # Estilos por tema
        self._theme_names: Set[str] = set()
        self.theme = None  # Tema actual

        # Cargar temas base
        self._load_themes()

        # Inicializar ttk.Style base
        super().__init__()

        # Establecer instancia y tema
        Style.instance = self
        self.theme_use(theme)

    def _load_themes(self) -> None:
        """Carga los temas estándar y de usuario."""
        # Combinar temas estándar y de usuario
        if USER_THEMES:
            STANDARD_THEMES.update(USER_THEMES)

        theme_settings = {"themes": STANDARD_THEMES}

        # Registrar cada tema
        for name, definition in theme_settings["themes"].items():
            self.register_theme(
                ThemeDefinition(
                    name=name,
                    themetype=definition["type"],
                    colors=definition["colors"]
                )
            )

    def register_theme(self, definition: ThemeDefinition) -> None:
        """Registra un nuevo tema.

        Args:
            definition: Definición del tema a registrar
        """
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_styles[theme] = set()

    def theme_use(self, themename: Optional[str] = None) -> Optional[str]:
        """Cambia o consulta el tema en uso.

        Args:
            themename: Nombre del tema a usar

        Returns:
            str: Nombre del tema actual

        Raises:
            TclError: Si el tema no existe
        """
        if not themename:
            return super().theme_use()

        # Tema TTK existente
        if themename in super().theme_names():
            self.theme = self._theme_definitions.get(themename)
            super().theme_use(themename)
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
        # Nuevo tema
        elif themename in self._theme_names:
            self.theme = self._theme_definitions.get(themename)
            self._theme_objects[themename] = StyleBuilderTTK(self)
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
        else:
            raise TclError(f"{themename} is not a valid theme.")
        return themename

    def configure(self, style, query_opt: Any = None, **kw):
        """Configura o consulta opciones de estilo.

        Args:
            style: Nombre del estilo
            query_opt: Opción específica a consultar
            **kw: Opciones de configuración

        Returns:
            Any: Configuración actual si query_opt está presente
        """
        if query_opt:
            return super().configure(style, query_opt=query_opt, **kw)

        from .bootstyle import Bootstyle

        if not self.style_exists_in_theme(style):
            ttkstyle = Bootstyle.update_ttk_widget_style(None, style)
        else:
            ttkstyle = style

        if ttkstyle == style:
            return super().configure(style, query_opt=query_opt, **kw)
        else:
            result = super().configure(style, query_opt=query_opt, **kw)
            self._register_ttkstyle(style)
            return result

    def theme_names(self) -> list:
        """Obtiene la lista de temas disponibles.

        Returns:
            list: Lista de nombres de temas registrados
        """
        return list(self._theme_definitions.keys())

    @property
    def colors(self) -> Colors:
        """Obtiene los colores del tema actual.

        Returns:
            Colors: Objeto con los colores del tema actual
        """
        theme = self.theme.name if self.theme else None
        if theme in self._theme_names:
            definition = self._theme_definitions.get(theme)
            return definition.colors if definition else Colors()
        return Colors()

    def style_exists_in_theme(self, ttkstyle: str) -> bool:
        """Verifica si un estilo existe en el tema actual.

        Args:
            ttkstyle: Nombre del estilo a verificar

        Returns:
            bool: True si el estilo existe en el tema actual
        """
        theme_styles = self._theme_styles.get(self.theme.name, set())
        return ttkstyle in theme_styles and ttkstyle in self._style_registry

    def _register_ttkstyle(self, ttkstyle: str) -> None:
        """Registra un estilo TTK en el tema actual.

        Args:
            ttkstyle: Nombre del estilo TTK a registrar
        """
        self._style_registry.add(ttkstyle)
        theme = self.theme.name
        self._theme_styles[theme].add(ttkstyle)

    def _create_ttk_styles_on_theme_change(self) -> None:
        """Reconstruye los estilos TTK cuando cambia el tema."""
        for ttkstyle in self._style_registry:
            if not self.style_exists_in_theme(ttkstyle):
                self._rebuild_style(ttkstyle)

    def _rebuild_style(self, ttkstyle: str) -> None:
        """Reconstruye un estilo específico usando el builder actual.

        Args:
            ttkstyle: Identificador del estilo a reconstruir
        """
        from .bootstyle import Bootstyle
        try:
            builder = self._get_builder()
            color = Bootstyle.ttkstyle_widget_color(ttkstyle)
            method_name = Bootstyle.ttkstyle_method_name(ttkstyle)
            method = builder.name_to_method(method_name)
            method(builder, color)
        except Exception as e:
            Publisher.publish_message(
                Channel.STD,
                f"Error rebuilding style {ttkstyle}: {str(e)}"
            )

    def _get_builder(self) -> StyleBuilderTTK:
        """Obtiene el builder de estilos para el tema actual.

        Returns:
            StyleBuilderTTK: Constructor de estilos del tema actual

        Raises:
            TclError: Si no hay tema actual o builder configurado
        """
        theme_name = self.theme.name if self.theme else None
        if not theme_name:
            raise TclError("No current theme set")

        builder = self._theme_objects.get(theme_name)
        if not builder:
            raise TclError(f"No style builder found for theme {theme_name}")

        return builder

    def _get_builder_tk(self) -> 'StyleBuilderTK':
        """Obtiene el builder para widgets tk heredados.

        Returns:
            StyleBuilderTK: Constructor de estilos tk
        """
        builder = self._get_builder()
        return builder.builder_tk

    @staticmethod
    def get_instance() -> 'Style':
        """Obtiene la instancia única del gestor de estilos.

        Returns:
            Style: Instancia singleton del gestor de estilos
        """
        if Style.instance is None:
            Style()
        return Style.instance

    def __del__(self) -> None:
        """Limpieza al destruir la instancia."""
        try:
            # Limpiar recursos si es necesario
            pass
        except:
            pass