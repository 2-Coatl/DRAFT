from typing import Dict, Optional, Set, Union, AnyStr, List, Callable
from tkinter import ttk
from tkinter import TclError

from ui.themeengine.core.color import Colors
from ui.themeengine.utils.constants import DEFAULT_THEME, USER_THEMES, STANDARD_THEMES
from ui.themeengine.communication.channel import Channel
from ui.themeengine.communication.publisher import Publisher
from ui.themeengine.builders.style_builder_ttk import StyleBuilderTTK
from ui.themeengine.core.theme import ThemeDefinition
from ui.themeengine.utils.bootstyle import Bootstyle


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

        # Inicialización de colecciones
        self._theme_objects: Dict = {} # Constructores de temas
        self._theme_definitions = {}   # Definiciones de temas
        self._theme_names: Set[str] = set()  # Registro de estilos
        self._theme_styles = {}   # Estilos por tema
        self._style_registry = set()   # Nombres de temas disponibles

        # # Cargar temas ANTES de intentar usar uno
        self._load_themes()
        # print(f"Después de _load_themes")
        # print(f"_theme_objects: {self._theme_objects}")
        # print(f"_theme_definitions: {self._theme_definitions}")
        # print(f"_theme_names: {self._theme_names}")
        # print(f"_theme_styles: {self._theme_styles}")
        # print(f"_style_registry: {self._style_registry}")

        #Inicializar ttk.Style
        super().__init__()
        # Establecer instancia y tema
        Style.instance = self
        self.theme_use(theme)

        # Inicializar el sistema de localización
        # Esto configura el catálogo de mensajes y prepara la internacionalización
        from ui.themeengine import localization
        localization.initialize_localities()

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
        # print("\n--- Dentro de configure ---")
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
        # print("\n--- Dentro de style_exists_in_theme ---")
        # print(f"Iniciando: {ttkstyle}")
        theme_styles = self._theme_styles.get(self.theme.name)
        # print(f"Theme_styles: {theme_styles}")
        exists_in_theme = ttkstyle in theme_styles
        # print(f"exists_in_theme: {exists_in_theme}")
        exists_in_registry = ttkstyle in self._style_registry
        # print(f"exists_in_registry: {exists_in_registry}")
        return exists_in_theme and exists_in_registry

    def _register_ttkstyle(self, ttkstyle: str) -> None:
        """Registra un nombre de estilo ttk en el sistema.

        Este método asegura que el constructor (builder) no intentará crear un
        estilo que ya ha sido creado previamente. Mantiene un registro tanto
        global como específico por tema de los estilos ttk existentes.

        Parameters:
            ttkstyle (str):
                El nombre del estilo ttk que se va a registrar.

        Returns:
            None: Este método no retorna ningún valor.
        Raises:
            AttributeError: Si self.theme no está establecido o no tiene atributo name.
            KeyError: Si el tema actual no está inicializado en _theme_styles.
        """

        # Verificar que el parámetro sea del tipo correcto
        if not isinstance(ttkstyle, str):
            raise TypeError("ttkstyle debe ser una cadena")

        # Añadir el estilo al registro global de estilos
        self._style_registry.add(ttkstyle)
        theme = self.theme.name

        # Verificar que el tema esté inicializado en _theme_styles
        if theme not in self._theme_styles:
            # Obtener el nombre del tema actual desde el objeto theme
            self._theme_styles[theme] = set()

        # Añadir el estilo al conjunto específico del tema actual
        self._theme_styles[theme].add(ttkstyle)


    def theme_names(self) -> List[str]:
        """Obtiene la lista de temas disponibles.

        Returns:
            List[str]: Lista de nombres de temas disponibles.
        """
        return list(self._theme_definitions.keys())

    def theme_use(self, themename: Optional[str] = None) -> Union[str, None]:
        """Cambia o consulta el tema utilizado para renderizar los widgets de la aplicación.

        Si themename es None, devuelve el nombre del tema actual en uso. En caso
        contrario, establece el tema actual a themename, actualiza todos los widgets
        y emite un evento ``<<ThemeChanged>>``.

        Parameters:
            themename: El nombre del tema a aplicar para los nuevos widgets.

        Returns:
            El nombre del tema actual si `themename` es None, None en caso contrario.

        Raises:
            TclError: Si el nombre del tema proporcionado no es válido.
        """
        # print("\n--- Dentro de theme_use ---")
        # print(f"Tema solicitado: {themename}")
        # print(f"Temas existentes: {super().theme_names()}")
        # print(f"Temas registrados: {self._theme_names}")
        # print(f"Theme objects actuales: {self._theme_objects}")
        # print(f"Theme definitions: {self._theme_definitions}")

        # Si no se proporciona un nombre de tema, devolver el tema actual en uso
        # Ejemplo: style.theme_use() -> 'light'
        if not themename:
            # Se delega en la implementación de la clase base
            return super().theme_use()

        # Obtener la lista de temas ya configurados en ttk
        # Ejemplo: ['default', 'alt', 'clam', 'classic', 'vista', 'xpnative', 'light']
        existing_themes = super().theme_names()

        # CASO 1: Si el tema solicitado ya está configurado en ttk
        # Ejemplo: themename = 'light' y 'light' está en existing_themes
        if themename in existing_themes:
            # 1. Obtener la definición del tema desde nuestro registro
            # Ejemplo: self.theme = ThemeDefinition(name='light', colors={...})
            self.theme = self._theme_definitions.get(themename)

            # 2. Activar el tema en ttk (cambio efectivo del tema)
            # Internamente, esto configura ttk para usar el tema especificado
            super().theme_use(themename)

            # 3. Crear/actualizar los estilos ttk específicos para este tema
            # Esto aplica los estilos personalizados sobre el tema base
            self._create_ttk_styles_on_theme_change()

            # 4. Notificar a toda la aplicación que el tema ha cambiado
            # Esto permite que los widgets y componentes se actualicen
            Publisher.publish_message(Channel.STD)

        # CASO 2: Si el tema está registrado pero aún no configurado en ttk
        # Ejemplo: themename = 'custom_theme' que está en self._theme_names pero no en ttk
        elif themename in self._theme_names:
            # 1. Obtener la definición del tema desde nuestro registro
            self.theme = self._theme_definitions.get(themename)

            # 2. Crear un nuevo constructor de estilos para este tema
            # Esto inicializa la infraestructura necesaria para el tema
            self._theme_objects[themename] = StyleBuilderTTK()

            # 3. Crear los estilos ttk para el nuevo tema
            # Esto configura todos los widgets ttk con los estilos del tema
            self._create_ttk_styles_on_theme_change()

            # 4. Notificar el cambio de tema a toda la aplicación
            Publisher.publish_message(Channel.STD)

        # CASO 3: Si el tema solicitado no existe ni está registrado
        # Ejemplo: themename = 'tema_inexistente'
        else:
            # Lanzar una excepción con un mensaje descriptivo
            # Ejemplo: TclError('tema_inexistente', 'is not a valid theme.')
            raise TclError(themename, "is not a valid theme.")

    def register_theme(self, definition: ThemeDefinition) -> None:
        """Registra una definición de tema para ser utilizada por el objeto `Style`.

        Este método hace que la definición y el nombre del tema estén disponibles
        en tiempo de ejecución, permitiendo que los recursos visuales y estilos
        puedan ser creados cuando sean necesarios.

        Parameters:
            definition (ThemeDefinition):
                Un objeto `ThemeDefinition` que contiene la definición completa
                del tema, incluyendo su nombre, colores, y otras propiedades visuales.

        Returns:
            None: Este método no retorna ningún valor.

        Raises:
            TypeError: Si `definition` no es un objeto ThemeDefinition.
            ValueError: Si el tema no tiene un nombre válido.
        """
        if not isinstance(definition, ThemeDefinition):
            raise TypeError("La definición debe ser un objeto ThemeDefinition")

        if not definition.name or not isinstance(definition.name, str):
            raise ValueError("El tema debe tener un nombre válido")

        # Extraer el nombre del tema de la definición proporcionada
        # Por ejemplo, si definition.name es "dark", theme será "dark"
        theme = definition.name

        # Añadir el nombre del tema al conjunto de temas disponibles
        # Si el tema ya existía en el conjunto, esta operación no tiene efecto
        # Ejemplo: self._theme_names = {"light", "dark", "blue"} -> añadir "dark" no cambia nada
        self._theme_names.add(theme)

        # Almacenar la definición completa en el diccionario de definiciones
        # Si ya existía una definición con este nombre, será reemplazada
        # Ejemplo: self._theme_definitions["dark"] = <ThemeDefinition para tema oscuro>
        self._theme_definitions[theme] = definition

        # Inicializar un conjunto vacío para los estilos específicos de este tema
        # Este conjunto se llenará más adelante cuando se creen estilos para este tema
        # Ejemplo: self._theme_styles["dark"] = set() -> conjunto vacío inicialmente
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
        # print("\n--- Cargando temas ---")
        if USER_THEMES:
            STANDARD_THEMES.update(USER_THEMES)

        # print(f"Temas disponibles: {STANDARD_THEMES.keys()}")
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
            StyleBuilderTTK: El objeto constructor de estilos para el tema actual.
        """
        # print("\n--- Cargando _get_builder ---")
        style: Style = Style.get_instance()
        #print(f"style: {style}")
        theme_name = style.theme.name
        #print(f"theme_name: {theme_name}")
        return style._theme_objects[theme_name]

    @staticmethod
    def _get_builder_tk():
        """Obtiene el constructor de estilos tk para el tema actual.

        Args:


        Returns:
           StyleBuilderTK: El objeto constructor de estilos tk para el tema actual.
        """
        builder = Style._get_builder()
        return builder.style_builder_tk

    def _create_ttk_styles_on_theme_change(self) -> None:
        """Crea los estilos ttk registrados cuando cambia el tema.

        Este método se encarga de recrear todos los estilos ttk registrados
        que no existen en el tema actual. Se llama automáticamente cuando
        cambia el tema de la aplicación para asegurar que todos los widgets
        mantengan sus estilos personalizados.

        Returns:
            None: Este método no retorna ningún valor.
        """

        # Iterar sobre cada estilo registrado en el sistema
        # Ejemplo: "primary.TButton", "secondary.TLabel", etc.
        for ttkstyle in self._style_registry:
            # Verificar si el estilo ya existe en el tema actual
            # Esto evita recrear estilos que ya han sido creados para este tema
            # Ejemplo: si "primary.TButton" ya existe en el tema "dark", no recrearlo
            if not self.style_exists_in_theme(ttkstyle):
                # Extraer el color asociado con el estilo
                # Ejemplo: de "primary.TButton" extrae "primary"
                color = Bootstyle.ttkstyle_widget_color(ttkstyle)

                # Extraer el nombre del método que debe usarse para crear el estilo
                # Ejemplo: de "primary.TButton" obtiene "create_button_style"
                method_name = Bootstyle.ttkstyle_method_name(string=ttkstyle)

                # Obtener el constructor de estilos adecuado para el tema actual
                # Esto devuelve un objeto que sabe cómo crear los estilos
                builder: StyleBuilderTTK = self._get_builder()

                # Resolver dinámicamente el método que creará el estilo
                # Convierte el nombre del método en una referencia al método real
                method: Callable = builder.name_to_method(method_name)

                # Invocar el método con el constructor y el color
                # Esto creará el estilo ttk con las propiedades adecuadas
                method(builder, color)