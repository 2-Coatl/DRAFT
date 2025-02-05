from tkinter import ttk
from typing import Optional, Dict, Set, Any, Callable

from .constants import USER_THEMES, STANDARD_THEMES
from .style_builder_ttk import StyleBuilderTTK
from .theme_definition import ThemeDefinition
from .colors import Colors
from .events import Publisher, Channel
from .bootstyle import Bootstyle
from tkinter import TclError


class Style(ttk.Style):
    """Singleton para crear y gestionar temas y estilos de widgets.

    Esta clase es un reemplazo directo de ttk.Style y hereda todos sus
    métodos y propiedades. Se implementa como singleton para mantener
    consistencia en toda la aplicación.

    Examples:
        ```python
        # Instanciar con tema por defecto
        style = Style()

        # Instanciar con tema específico
        style = Style(theme='superhero')

        # Ver temas disponibles
        for theme in style.theme_names():
            print(theme)
        ```
    """

    instance: Optional['Style'] = None
    DEFAULT_THEME = 'light'

    def __new__(cls, theme=None):
        """Implementación del singleton."""
        if Style.instance is None:
            return object.__new__(cls)
        return Style.instance

    def __init__(self, theme=DEFAULT_THEME):
        """
        Parameters:
            theme (str): Nombre del tema a usar al iniciar
        """
        if Style.instance is not None:
            if theme != self.DEFAULT_THEME:
                Style.instance.theme_use(theme)
            return

        # Inicializar colecciones
        self._theme_objects: Dict = {}
        self._theme_definitions: Dict[str, ThemeDefinition] = {}
        self._style_registry: Set[str] = set()  # Estilos usados
        self._theme_styles: Dict[str, Set[str]] = {}  # Estilos por tema
        self._theme_names: Set[str] = set()
        self.theme = None  # Tema actual

        # Cargar temas y configurar
        self._load_themes()

        super().__init__()
        Style.instance = self
        self.theme_use(theme)

    @property
    def colors(self) -> Colors:
        """Obtiene los colores del tema actual.

        Returns:
            Objeto Colors del tema actual
        """
        theme = self.theme.name
        if theme in self._theme_names:
            definition = self._theme_definitions.get(theme)
            return definition.colors if definition else Colors()
        return Colors()

    def configure(self, style, query_opt: Any = None, **kw):
        """Configura o consulta opciones de estilo.

        Args:
            style: Nombre del estilo
            query_opt: Opción a consultar
            **kw: Opciones de configuración

        Returns:
            Configuración actual si query_opt está presente
        """
        if query_opt:
            return super().configure(style, query_opt=query_opt, **kw)

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
            Lista de nombres de temas
        """
        return list(self._theme_definitions.keys())

    def register_theme(self, definition: ThemeDefinition) -> None:
        """Registra un nuevo tema.

        Args:
            definition: Definición del tema a registrar
        """
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_styles[theme] = set()

    def _load_themes(self) -> None:
        """Carga todos los temas definidos."""
        # Combinar temas estándar con temas de usuario
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

    def load_user_themes(self, file: str) -> None:
        """Carga temas personalizados desde un archivo JSON.

        Parameters:
            file: Ruta al archivo JSON con definiciones de temas
        """
        import json
        try:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
                themes = data['themes']
            for theme in themes:
                for name, definition in theme.items():
                    self.register_theme(
                        ThemeDefinition(
                            name=name,
                            themetype=definition["type"],
                            colors=definition["colors"]
                        )
                    )
        except Exception as e:
            raise ValueError(f"Error loading user themes: {str(e)}")

    def theme_use(self, themename: Optional[str] = None):
        """Cambia o consulta el tema en uso.

        Si themename es None, retorna el tema actual. De lo contrario,
        establece el tema especificado y emite un evento de cambio.

        Parameters:
            themename: Nombre del tema a usar

        Returns:
            str: Nombre del tema actual si themename es None

        Raises:
            TclError: Si el tema no existe
        """
        if not themename:
            return super().theme_use()

        # Cambiar a tema existente
        if themename in super().theme_names():
            self.theme = self._theme_definitions.get(themename)
            super().theme_use(themename)
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
        # Configurar nuevo tema
        elif themename in self._theme_names:
            self.theme = self._theme_definitions.get(themename)
            self._theme_objects[themename] = StyleBuilderTTK(self)
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
        else:
            raise TclError(themename, "is not a valid theme.")
        return themename

    def style_exists_in_theme(self, ttkstyle: str) -> bool:
        """Verifica si un estilo existe en el tema actual.

        Args:
            ttkstyle: Nombre del estilo a verificar

        Returns:
            True si el estilo existe
        """
        theme_styles = self._theme_styles.get(self.theme.name, set())
        return ttkstyle in theme_styles and ttkstyle in self._style_registry

    @staticmethod
    def get_instance() -> 'Style':
        """Obtiene la instancia única del gestor de estilos."""
        return Style.instance


    def _get_builder(self):
        """Obtiene el objeto que construye los estilos de widget para el tema actual.

        Returns:
            ThemeBuilderTTK: El objeto constructor de estilos para el tema actual
        """
        theme_name = self.theme.name
        return self._theme_objects[theme_name]

    def _get_builder_tk(self):
        """Obtiene el objeto que construye los estilos para widgets tk heredados.

        Returns:
            ThemeBuilderTK: El objeto constructor de estilos tk
        """
        builder = self._get_builder()
        return builder.builder_tk

    def _register_ttkstyle(self, ttkstyle: str) -> None:
        """Registra un nombre de estilo ttk.

        Args:
            ttkstyle: Nombre del estilo ttk a registrar
        """
        self._style_registry.add(ttkstyle)
        theme = self.theme.name
        self._theme_styles[theme].add(ttkstyle)

    def _create_ttk_styles_on_theme_change(self):
        """Crea los estilos existentes cuando cambia el tema."""
        for ttkstyle in self._style_registry:
            if not self.style_exists_in_theme(ttkstyle):
                color = Bootstyle.ttkstyle_widget_color(ttkstyle)
                method_name = Bootstyle.ttkstyle_method_name(string=ttkstyle)
                builder = self._get_builder()
                method = builder.name_to_method(method_name)
                method(builder, color)