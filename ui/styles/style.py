from typing import Dict, Optional, Set, Union, AnyStr, List
from tkinter import ttk
import tkinter as tk
from tkinter import TclError
from .notifications.channel import Channel
from .notifications.publisher import Publisher
from .theme_definition import ThemeDefinition
from .color import Colors
from .constants import STANDARD_THEMES, USER_THEMES, DEFAULT_THEME
from .style_engines.style_engine_ttk import StyleEngineTTK
from .utils.keywords import Keywords


class Style(ttk.Style):
    """Singleton para gestión básica de temas y sus colores.

    Esta clase es responsable de:
    1. Gestionar los temas de la aplicación
    2. Manejar la configuración de colores
    3. Registrar y aplicar estilos TTK
    """

    instance: Optional['Style'] = None

    def __new__(cls, theme=None):
        """Implementa el patrón singleton.

        Args:
            theme: Tema inicial a utilizar.

        Returns:
            Style: Instancia única de la clase Style.
        """
        if cls.instance is None:
            return object.__new__(cls)
        return cls.instance

    def __init__(self, theme=DEFAULT_THEME):
        """Inicializa la instancia de Style.

        Args:
            theme: Tema inicial a utilizar. Si no se especifica,
                  se usa el tema por defecto.
        """
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
        self._theme_styles = {}
        self._style_registry = set()

        # Cargar temas ANTES de intentar usar uno
        self._load_themes()

        # Establecer instancia y tema
        Style.instance = self
        self.theme_use(theme)

    def _load_themes(self) -> None:
        """Carga todos los temas definidos en ttkbootstrap.

        Crea un objeto ThemeDefinition para cada tema, que será
        utilizado para generar el tema en tkinter junto con cualquier
        recurso en tiempo de ejecución.
        """
        if USER_THEMES:
            STANDARD_THEMES.update(USER_THEMES)
        theme_settings = {"themes": STANDARD_THEMES}
        for name, definition in theme_settings["themes"].items():
            self.register_theme(
                ThemeDefinition(
                    name=name,
                    themetype=definition["type"],
                    colors=definition["colors"],
                )
            )

    def register_theme(self, definition: ThemeDefinition) -> None:
        """Registra una definición de tema para uso del objeto Style.

        Hace que la definición y el nombre estén disponibles en tiempo
        de ejecución para que los recursos y estilos puedan ser creados
        cuando sean necesarios.

        Args:
            definition: Objeto ThemeDefinition que contiene la definición
                      completa del tema a registrar.
        """
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_styles[theme] = set()

    def theme_use(self, themename=None) -> Union[str, None]:
        """Cambia el tema utilizado en la renderización de los widgets.

        Si themename es None, retorna el tema en uso. En caso contrario,
        establece el tema actual como themename, actualiza todos los widgets
        y emite un evento <<ThemeChanged>>.

        Este método solo debe usarse para cambiar el tema DURANTE la ejecución.
        Para el tema inicial, use el nombre del tema en el constructor de Style.

        Args:
            themename: Nombre del tema a aplicar para nuevos widgets.
                      Si es None, retorna el tema actual.

        Returns:
            Union[str, None]: Nombre del tema actual si themename es None,
                             None en caso contrario.

        Raises:
            TclError: Si el tema especificado no es válido.
        """
        # Si no hay nombre de tema, retorna el tema actual
        if not themename:
            return super().theme_use()

        # Obtiene la lista de temas existentes en ttk
        existing_themes = super().theme_names()

        # Cambiar a un tema existente en ttk
        if themename in existing_themes:
            self.theme = self._theme_definitions.get(themename)
            super().theme_use(themename)
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
            return None

        # Configurar un nuevo tema que está registrado pero no creado en ttk
        elif themename in self._theme_names:
            self.theme = self._theme_definitions.get(themename)
            self._theme_objects[themename] = StyleEngineTTK()
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
            return None

        # El tema no existe
        else:
            raise TclError(themename, "no es un tema válido.")

    def theme_names(self) -> List[str]:
        """Obtiene la lista de temas disponibles.

        Retorna una lista con los nombres de todos los temas registrados
        en el sistema, incluyendo tanto los temas estándar como los
        personalizados por el usuario.

        Returns:
            List[str]: Lista de nombres de temas disponibles.
        """
        return list(self._theme_definitions.keys())

    @property
    def colors(self) -> Colors:
        """Obtiene los colores del tema actual.

        Proporciona acceso a los colores definidos en el tema actual.
        Si no hay un tema establecido o el tema no existe, retorna
        un objeto Colors con valores por defecto.

        Returns:
            Colors: Objeto con las definiciones de colores del tema actual.
                   Si no hay tema válido, retorna un objeto Colors vacío.
        """
        # Obtiene el nombre del tema actual si existe
        theme = self.theme.name if self.theme else None

        # Verifica si el tema está registrado
        if theme in self._theme_names:
            definition = self._theme_definitions.get(theme)
            return definition.colors if definition else Colors()

        # Si no hay tema válido, retorna colores por defecto
        return Colors()

    @staticmethod
    def get_instance() -> 'Style':
        """Retorna una instancia de la clase Style.

        Returns:
            Style: Instancia única del gestor de estilos.
        """
        return Style.instance

    def configure(self, style: str, query_opt: AnyStr = None, **kw) -> Union[Dict, str, None]:
        """Configura o consulta las opciones de estilo para widgets TTK.

        Si query_opt está presente, consulta la configuración existente.
        En caso contrario, aplica la nueva configuración al estilo especificado.

        Se encarga de:
        1. Verificar si el estilo existe en el tema actual
        2. Actualizar el estilo si es necesario
        3. Registrar nuevos estilos en el tema

        Args:
            style: Nombre del estilo a configurar o consultar.
            query_opt: Opción específica a consultar.
            **kw: Opciones de configuración del estilo.

        Returns:
            Union[Dict, str, None]: Configuración del estilo si es consulta,
                                   None si es configuración.
        """
        # Si hay una consulta, retorna la configuración solicitada
        if query_opt:
            return super().configure(style, query_opt=query_opt, **kw)

        # Verifica si el estilo existe y actualiza si es necesario
        if not self.style_exists_in_theme(style):
            ttkstyle = style

        # Aplica la configuración según el tipo de estilo
        if ttkstyle == style:
            # Configura un tema ttkbootstrap existente
            return super().configure(style, query_opt=query_opt, **kw)
        else:
            # Subclase de un tema ttkbootstrap
            result = super().configure(style, query_opt=query_opt, **kw)
            self._register_ttkstyle(style)
            return result

    def _build_configure(self, style: str, **kw) -> None:
        """Construye la configuración base de un estilo TTK.

        Método auxiliar utilizado por las clases constructoras de estilos
        para aplicar configuraciones directamente mediante la clase padre.
        No realiza validaciones adicionales ni registros de estilo.

        Args:
            style: Nombre del estilo a configurar.
            **kw: Opciones de configuración del estilo.
        """
        super().configure(style, **kw)

    def style_exists_in_theme(self, ttkstyle: str) -> bool:
        """Verifica si un estilo existe en el tema actual.

        Comprueba la existencia del estilo tanto en el registro
        específico del tema como en el registro global.

        Args:
            ttkstyle: Nombre del estilo TTK a verificar.

        Returns:
            bool: True si el estilo existe en ambos registros,
                 False en caso contrario.
        """
        theme_styles = self._theme_styles.get(self.theme.name)
        exists_in_theme = ttkstyle in theme_styles
        exists_in_registry = ttkstyle in self._style_registry
        return exists_in_theme and exists_in_registry

    def _register_ttkstyle(self, ttkstyle: str) -> None:
        """Registra un nombre de estilo TTK.

        Asegura que un estilo no sea creado múltiples veces al mantener
        un registro tanto global como específico del tema. Este método es
        llamado internamente cuando se crean nuevos estilos.

        Args:
            ttkstyle: Nombre del estilo TTK a registrar.
        """
        # Agrega al registro global de estilos
        self._style_registry.add(ttkstyle)

        # Obtiene el tema actual y registra el estilo
        theme = self.theme.name
        self._theme_styles[theme].add(ttkstyle)

    def _create_ttk_styles_on_theme_change(self) -> None:
        """Recrea los estilos existentes cuando cambia el tema.

        Este método es responsable de:
        1. Iterar sobre los estilos registrados
        2. Verificar su existencia en el tema actual
        3. Recrear los estilos necesarios con la nueva configuración del tema

        Nota: Esta es una implementación temporal que será expandida
        cuando se implemente la clase Bootstyle.
        """
        for ttkstyle in self._style_registry:
            if not self.style_exists_in_theme(ttkstyle):
                # Obtener la clase de widget del estilo
                widget_class = Keywords.ttkstyle_widget_class(string=ttkstyle)
                if widget_class:
                    # Aplicar estilo básico basado en la clase de widget
                    self._apply_basic_style(widget_class, ttkstyle)

    def _apply_basic_style(self, widget_class: str, ttkstyle: str) -> None:
        """Aplica un estilo básico a un widget.

        Args:
            widget_class: Clase del widget (button, label, etc.)
            ttkstyle: Nombre del estilo TTK a aplicar
        """
        # Configuración básica usando los colores del tema actual
        self._build_configure(
            ttkstyle,
            background=self.colors.bg,
            foreground=self.colors.fg,
            bordercolor=self.colors.border,
            darkcolor=self.colors.border,
            lightcolor=self.colors.bg,
            relief=tk.FLAT,
        )

        # Registrar el estilo en el tema actual
        self._register_ttkstyle(ttkstyle)