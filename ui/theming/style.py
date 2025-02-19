from typing import Dict, Optional, Set, Union, AnyStr, List, Callable
from tkinter import ttk
from tkinter import TclError

from ui.theming.color import Colors
from ui.theming.constants import DEFAULT_THEME, USER_THEMES, STANDARD_THEMES
from ui.theming.notifications.channel import Channel
from ui.theming.notifications.publisher import Publisher
from ui.theming.style_engines.style_engine_ttk import StyleEngineTTK
from ui.theming.theme_definition import ThemeDefinition
from ui.theming.utils.bootstyle import Bootstyle


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
        if Style.instance is not None:  # Verifica si ya existe una instancia creada previamente
            if theme != DEFAULT_THEME:
                Style.instance.theme_use(theme)  # Usa la instancia existente
            return

        # Inicializar ttk.Style primero
        super().__init__()

        # Inicialización de colecciones
        self._theme_objects: Dict = {} # Constructores de temas
        self._theme_definitions: Dict[str, ThemeDefinition] = {}   # Definiciones de temas
        self._theme_names: Set[str] = set()  # Registro de estilos
        self._theme_styles = {}   # Estilos por tema
        self._style_registry = set()   # Nombres de temas disponibles

        # Cargar temas ANTES de intentar usar uno
        self._load_themes()
        print(f"Después de _load_themes: {self._theme_objects}")

        # Establecer instancia y tema
        Style.instance = self
        self.theme_use(theme)

    @staticmethod
    def get_instance() -> 'Style':
        """Retorna una instancia de la clase Style.

        Returns:
            Style: Instancia única del gestor de estilos.
        """
        return Style.instance

    def configure(self, style: str, query_opt: AnyStr = None, **kw) -> Union[Dict, str, None]:
        """Configura o consulta las opciones de estilo para widgets TTK.

        Args:
            style: Nombre del estilo a configurar o consultar.
            query_opt: Opción específica a consultar.
            **kw: Opciones de configuración del estilo.

        Returns:
            Union[Dict, str, None]: Configuración del estilo si es consulta,
                                   None si es configuración.
        """
        # Paso 1: Manejo rápido de consultas directas
        # Si existe query_opt, retorna inmediatamente la configuración
        if query_opt:
            return super().configure(style, query_opt=query_opt, **kw)

        # Paso 2: Verificación y actualización del estilo
        # Comprueba si el estilo existe en el tema actual
        if not self.style_exists_in_theme(style):
            # Si no existe, actualiza el estilo del widget TTK
            ttkstyle = Bootstyle.update_ttk_widget_style(None, style)
        else:
            # Si existe, mantiene el estilo actual sin modificaciones
            ttkstyle = style

        # Paso 3: Configuración final y registro
        if ttkstyle == style:
            # Si el estilo no fue modificado, configura el tema existente
            return super().configure(style, query_opt=query_opt, **kw)
        else:
            # Si el estilo fue modificado:
            # 1. Aplica la configuración con el nuevo estilo
            # 2. Registra el estilo modificado
            # 3. Retorna el resultado
            result = super().configure(style, query_opt=query_opt, **kw)
            self._register_ttkstyle(style)
            return result

    def _build_configure(self, style: str, **kw) -> None:
        """Construye la configuración base de un estilo TTK.

        Args:
            style: Nombre del estilo a configurar.
            **kw: Opciones de configuración del estilo.
        """
        super().configure(style, **kw)

    def style_exists_in_theme(self, ttkstyle: str) -> bool:
        """Verifica si un estilo existe en el tema actual.

        Args:
            ttkstyle: Nombre del estilo TTK a verificar.

        Returns:
            bool: True si el estilo existe en ambos registros.
        """
        theme_styles = self._theme_styles.get(self.theme.name)
        exists_in_theme = ttkstyle in theme_styles
        exists_in_registry = ttkstyle in self._style_registry
        return exists_in_theme and exists_in_registry

    def _register_ttkstyle(self, ttkstyle: str) -> None:
        """Registra un nombre de estilo TTK.

        Args:
            ttkstyle: Nombre del estilo TTK a registrar.
        """
        self._style_registry.add(ttkstyle)
        theme = self.theme.name
        self._theme_styles[theme].add(ttkstyle)


    def theme_names(self) -> List[str]:
        """Obtiene la lista de temas disponibles.

        Returns:
            List[str]: Lista de nombres de temas disponibles.
        """
        return list(self._theme_definitions.keys())

    def theme_use(self, themename=None) -> Union[str, None]:
        """Cambia o consulta el tema actual.

        Args:
            themename: Nombre del tema a aplicar. Si es None, retorna el tema actual.

        Returns:
            Union[str, None]: Nombre del tema actual si themename es None,
                             None en caso contrario.

        Raises:
            TclError: Si el tema especificado no es válido.
        """
        print("\n--- Dentro de theme_use ---")
        print(f"Tema solicitado: {themename}")
        print(f"Temas existentes: {super().theme_names()}")
        print(f"Temas registrados: {self._theme_names}")
        print(f"Theme objects actuales: {self._theme_objects}")
        print(f"Theme definitions: {self._theme_definitions}")

        if not themename:
            # 1. Consultar el tema actual
            print(f"Consultando tema actual: {super().theme_use()}")
            return super().theme_use()

        # 2. Cambiar a un tema existente
        existing_themes = super().theme_names()
        if themename in existing_themes:
            print(f"Cambiando a tema existente: {themename}")
            self.theme = self._theme_definitions.get(themename)
            super().theme_use(themename)
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)

        # 3. Configurar un nuevo tema personalizado
        elif themename in self._theme_names:
            print(f"Configurando nuevo tema personalizado: {themename}")
            self.theme = self._theme_definitions.get(themename)
            self._theme_objects[themename] = StyleEngineTTK()
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)

        else:
            print(f"Tema inválido: {themename}")
            raise TclError(themename, "no es un tema válido.")

    def register_theme(self, definition: ThemeDefinition) -> None:
        """Registra una definición de tema para uso del objeto Style.

        Args:
            definition: Objeto ThemeDefinition con la definición del tema.
        """
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_styles[theme] = set()

    def _load_themes(self) -> None:
        """Carga todos los temas definidos.

        Esta función inicializa los temas base del sistema, combinando
        los temas estándar con cualquier tema personalizado definido
        por el usuario.

        Args:

        Returns:
            None
        """
        # Si existen temas de usuario, se añaden a los estándar
        print("\n--- Cargando temas ---")
        if USER_THEMES:
            STANDARD_THEMES.update(USER_THEMES)

        print(f"Temas disponibles: {STANDARD_THEMES.keys()}")
        # Crear diccionario de configuración de temas
        theme_settings = {"themes": STANDARD_THEMES}

        # Registrar cada tema en el sistema
        for name, definition in theme_settings["themes"].items():
            self.register_theme(
                ThemeDefinition(
                    name=name,
                    themetype=definition["type"],
                    colors=definition["colors"],
                )
            )

    @property
    def colors(self) -> Union[Colors, List]:
        """Obtiene los colores utilizados en el tema actual.

        Args:


        Returns:
            Union[Colors, List]: Objeto que contiene los colores del tema actual.
                                Si no hay tema válido o definición, retorna lista vacía.
        """
        # caso de tema nulo
        if not hasattr(self, 'theme') or self.theme is None:
            return []

        theme = self.theme.name
        if theme in self._theme_names:
            definition = self._theme_definitions.get(theme)
            if not definition:
                return []
            return definition.colors
        return []

    @staticmethod
    def _get_builder():
        """Obtiene el constructor de estilos para el tema actual.

        Args:


        Returns:
            StyleEngineTTK: El objeto constructor de estilos para el tema actual.
        """
        style: Style = Style.get_instance()
        theme_name = style.theme.name
        return style._theme_objects[theme_name]

    @staticmethod
    def _get_builder_tk():
        """Obtiene el constructor de estilos tk para el tema actual.

        Args:


        Returns:
            StyleBuilderTK: El objeto constructor de estilos tk para el tema actual.
        """
        builder = Style._get_builder()
        return builder.style_engine_tk

    def _create_ttk_styles_on_theme_change(self) -> None:
        """Recrea los estilos existentes cuando cambia el tema.

        Args:


        Returns:
            None
        """
        for ttkstyle in self._style_registry:
            if not self.style_exists_in_theme(ttkstyle):
                # Obtener el color del widget del estilo
                color = Bootstyle.ttkstyle_widget_color(ttkstyle)
                # Obtener el nombre del método para crear el estilo
                method_name = Bootstyle.ttkstyle_method_name(string=ttkstyle)
                # Obtener el constructor de estilos
                builder: StyleEngineTTK = self._get_builder()
                # Encontrar y ejecutar el método apropiado
                method: Callable = builder.name_to_method(method_name)
                method(builder, color)