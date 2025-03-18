import tkinter as tk
from tkinter import ttk
from math import ceil
from typing import Union, List, Tuple, Callable, Dict, Any
from ui.themeengine.core.color import Colors

from ui.themeengine.builders.style_builder_tk import StyleBuilderTK
from ui.themeengine.core.theme import ThemeDefinition
from ui.themeengine.utils.constants import LIGHT, TTK_CLAM, DEFAULT, TTK_DEFAULT, PRIMARY


class StyleBuilderTTK:
    """Motor de estilos para widgets TTK.

    Responsable de:
    1. Construcción de estilos TTK bajo demanda
    2. Gestión de temas y colores para widgets TTK
    3. Actualización dinámica de estilos

    Atributos:
        style (Style): Referencia singleton a la instancia de Style.
        theme_images (dict): Diccionario para almacenar imágenes del tema.
        style_builder_tk (StyleBuilderTK): Instancia para manejar widgets Tk.

    Propiedades:
        colors (Colors): Acceso a los colores del tema actual.
        theme (ThemeDefinition): Acceso a la definición del tema actual.
        is_light_theme (bool): Indica si el tema actual es claro.

    """

    def __init__(self) -> None:
        """Inicializa el motor de estilos TTK.

        Este método constructor establece las referencias y recursos necesarios para
        que el motor de estilos funcione correctamente. Resuelve la dependencia circular
        con la clase Style, inicializa estructuras de datos para recursos visuales, y
        crea el tema TTK básico que servirá como punto de partida para todos los estilos.

        La inicialización incluye los siguientes pasos:
        1. Obtención de la instancia singleton de Style
        2. Creación de un diccionario vacío para imágenes del tema
        3. Inicialización del constructor de estilos para widgets Tk tradicionales
        4. Creación del tema TTK básico

        No recibe parámetros de configuración externa, asumiendo que la configuración
        necesaria ya está presente en la instancia de Style.
        """
        # Resuelve la dependencia circular con el módulo Style
        # Esta importación se hace localmente para evitar problemas de importación cíclica
        # entre los módulos Style y StyleBuilderTTK que dependen mutuamente
        from ui.themeengine.core.style import Style

        # Obtiene la instancia única (singleton) de Style que contiene la configuración
        # del tema actual. Ejemplo: instancia con tema 'light' y colores predefinidos
        self.style: Style = Style.get_instance()

        # Inicializa un diccionario vacío para almacenar imágenes del tema
        # Este diccionario se llenará bajo demanda con imágenes como íconos de botones,
        # fondos, etc. Ejemplo: {"check_on": PhotoImage(...), "radio_off": PhotoImage(...)}
        self.theme_images: Dict[str, Any] = {}

        # Crea una instancia del constructor de estilos para widgets Tk tradicionales
        # Esta instancia auxiliar maneja widgets que no son parte del framework TTK
        # pero necesitan mantener coherencia visual con los widgets TTK
        self.style_builder_tk: StyleBuilderTK = StyleBuilderTK()

        # Inicializa el tema TTK básico llamando al método create_theme
        # Este método configura un nuevo tema TTK basado en 'clam' y lo establece como activo
        # Esto prepara el framework para la posterior creación de estilos específicos
        self.create_theme()

    @property
    def colors(self) -> Colors:
        """Obtiene referencia a los colores del tema actual.

        Esta propiedad proporciona acceso directo al objeto Colors que contiene
        todas las definiciones de colores para el tema actual, simplificando el acceso
        a los colores para la construcción de estilos TTK.

        Los colores pueden ser accedidos mediante:
        - Notación de punto: self.colors.primary
        - Método get: self.colors.get('primary')
        - Iteración: for color_label in self.colors

        Returns:
            Colors: Objeto que contiene las definiciones de colores del tema actual.
                Incluye colores básicos (primary, secondary, etc.) y colores de interfaz
                (bg, fg, etc.).
        """
        # Accede al objeto style de la instancia actual, luego a su propiedad theme,
        # y finalmente a la propiedad colors de theme. Este enfoque permite un acceso
        # directo a los colores sin necesidad de navegar por toda la jerarquía de objetos
        # cada vez que se necesite un color para un estilo.
        #
        # Por ejemplo, en lugar de escribir:
        #   bg_color = self.style.theme.colors.bg
        #   primary_color = self.style.theme.colors.primary
        #
        # Se puede escribir de forma más concisa:
        #   bg_color = self.colors.bg
        #   primary_color = self.colors.primary
        #
        # Esta propiedad no realiza ninguna validación ni manejo de errores, asumiendo que:
        # 1. El atributo self.style existe y no es None
        # 2. La propiedad style.theme existe y no es None
        # 3. La propiedad theme.colors existe y es un objeto Colors válido
        #
        # En caso de que alguna de estas condiciones no se cumpla, se producirá un AttributeError.
        # Esta propiedad es de solo lectura y retorna una referencia directa al objeto colors,
        # por lo que cualquier modificación afectará al objeto original en style.theme.colors.
        return self.style.theme.colors

    @property
    def theme(self) -> ThemeDefinition:
        """Obtiene referencia a la definición del tema actual.

        Esta propiedad proporciona acceso directo al objeto ThemeDefinition que contiene
        la definición completa del tema actual, incluyendo su nombre, tipo (claro/oscuro)
        y todos sus colores. Facilita el acceso a las propiedades del tema para la
        construcción de estilos TTK adaptados al tema actual.

        Los componentes del tema pueden ser accedidos mediante:
        - Nombre: self.theme.name (ej: "light", "dark")
        - Tipo: self.theme.type (ej: "light" o "dark")
        - Colores: self.theme.colors (objeto Colors con todos los colores)

        Returns:
            ThemeDefinition: Objeto que contiene las definiciones completas del tema actual.

        """
        # Accede al objeto style de la instancia actual y luego a su propiedad theme,
        # que contiene la definición completa del tema actual. Este enfoque simplifica
        # el acceso a las propiedades del tema para la construcción de estilos TTK.
        #
        # Por ejemplo, en lugar de escribir:
        #   theme_name = self.style.theme.name
        #   theme_type = self.style.theme.type
        #
        # Se puede escribir de forma más concisa:
        #   theme_name = self.theme.name
        #   theme_type = self.theme.type
        #
        # El objeto ThemeDefinition retornado incluye:
        # - name: Nombre del tema (ej: "light", "dark")
        # - type: Tipo de tema (LIGHT o DARK)
        # - colors: Objeto Colors con todos los colores
        #
        # Esta propiedad no realiza ninguna validación ni manejo de errores, asumiendo que:
        # 1. El atributo self.style existe y no es None
        # 2. La propiedad style.theme existe y es un objeto ThemeDefinition válido
        #
        # En caso de que alguna de estas condiciones no se cumpla, se producirá un AttributeError.
        return self.style.theme

    @property
    def is_light_theme(self) -> bool:
        """Determina si el tema actual es claro.

        Esta propiedad evalúa el tipo del tema actual para determinar si es claro (light)
        u oscuro (dark). Proporciona una forma semántica y directa de adaptar el comportamiento
        de los componentes de la interfaz según el esquema de colores actual.

        La distinción entre temas claros y oscuros es fundamental para:
        - Ajustar contrastes y visibilidad de elementos
        - Seleccionar colores complementarios apropiados
        - Adaptar íconos y recursos gráficos
        - Optimizar la legibilidad del texto

        Returns:
            bool: True si el tema actual es claro (theme.type == 'light'),
                  False si el tema es oscuro (theme.type != 'light').
        """
        # Esta propiedad evalúa si el tema actual es de tipo claro ('light')
        # comparando el valor de theme.type con la constante LIGHT.
        #
        # El flujo es:
        # 1. Acceder a self.style (instancia de Style)
        # 2. Obtener la propiedad theme (objeto ThemeDefinition)
        # 3. Leer la propiedad type (normalmente 'light' o 'dark')
        # 4. Comparar con la constante LIGHT ('light')
        #
        # Esta comparación sencilla permite adaptar rápidamente comportamientos
        # y estilos según el tipo de tema, por ejemplo:
        #
        # - Seleccionar diferentes colores de borde o contraste
        # - Ajustar la visibilidad de elementos
        # - Optimizar la legibilidad de textos
        #
        # La implementación asume que:
        # - self.style.theme existe y es válido
        # - theme.type está establecido correctamente
        # - Solo existen dos tipos principales de tema (claro y oscuro)
        #
        # Si alguna de estas condiciones falla, podría producirse un AttributeError.
        return self.style.theme.type == LIGHT

    @staticmethod
    def name_to_method(method_name: str) -> Callable:
        """Obtiene un método de la clase por su nombre.

        Convierte un nombre de método (string) en una referencia ejecutable al método
        correspondiente dentro de la clase StyleBuilderTTK. Permite la resolución dinámica
        de métodos, facilitando la invocación programática de constructores de estilo y
        otras funciones de la clase.

        Este método es útil para:
        - Implementar mapeos configurables entre widgets y sus métodos de estilo
        - Permitir la personalización de la aplicación mediante configuración externa
        - Facilitar la extensión del sistema de estilos sin modificar código base

        Args:
            method_name: Nombre del método a obtener. Debe corresponder exactamente
                         a un método existente en la clase StyleBuilderTTK.

        Returns:
            Callable: Una referencia al método solicitado que puede ser invocada
                     posteriormente.

        Raises:
            AttributeError: Si el método especificado no existe en la clase StyleBuilderTTK.

        """
        # Utiliza getattr para obtener la referencia al método a partir de su nombre
        # getattr(object, name[, default]) busca el atributo 'name' en el objeto
        # En este caso, busca un método llamado 'method_name' en la clase StyleBuilderTTK
        #
        # Ejemplos:
        # - Si method_name = "create_button_style", obtiene StyleBuilderTTK.create_button_style
        # - Si method_name = "create_combobox_style", obtiene StyleBuilderTTK.create_combobox_style
        #
        # Si el método no existe, getattr lanzará AttributeError
        func = getattr(StyleBuilderTTK, method_name)

        # Retorna la referencia al método obtenido, que puede ser invocada posteriormente
        # El método retornado normalmente será un método de instancia, por lo que requerirá
        # una instancia como primer argumento (self) cuando sea invocado
        return func

    def create_theme(self) -> None:
        """Inicializa el tema TTK con la configuración base.

        Crea un nuevo tema TTK y lo establece como el tema activo,
        aplicando la configuración inicial necesaria.
        """
        self.style.theme_create(self.theme.name, TTK_CLAM)
        ttk.Style.theme_use(self.style, self.theme.name)
        self.update_ttk_theme_settings()

    def update_ttk_theme_settings(self) -> None:
        """Actualiza la configuración del tema.

        Este método se llama internamente cada vez que el tema cambia
        para actualizar los diversos componentes del tema.
        """
        self.create_default_style()
        # Aquí se pueden agregar más actualizaciones de tema según sea necesario

    def create_default_style(self) -> None:
        """Configura el estilo predeterminado para widgets TTK.

        Establece la configuración base del estilo raíz '.' que sirve como
        base para todos los widgets TTK. Este método debe llamarse primero
        antes de aplicar cualquier otro estilo durante la creación del tema.
        """
        self.style._build_configure(
            style=".",
            background=self.colors.bg,
            darkcolor=self.colors.border,
            foreground=self.colors.fg,
            troughcolor=self.colors.bg,
            selectbg=self.colors.selectbg,
            selectfg=self.colors.selectfg,
            selectforeground=self.colors.selectfg,
            selectbackground=self.colors.selectbg,
            fieldbg="white",
            borderwidth=1,
            focuscolor="",
        )
        # Estilo general aplicado a la vista de tabla
        self.create_link_button_style()
        self.style.configure("symbol.Link.TButton", font="-size 16")

    def scale_size(self, size: Union[int, List, Tuple]) -> Union[int, List]:
        """Escala el tamaño de imágenes y otros elementos basado en el factor de escala TTK.

        Ajusta dimensiones para mantener proporciones consistentes en diferentes configuraciones
        de pantalla y sistemas operativos. Utiliza el factor de escala de Tkinter y valores de
        referencia específicos por plataforma para calcular el tamaño óptimo.

        El método:
        1. Determina el sistema de ventanas (macOS vs otros)
        2. Establece un valor base de referencia apropiado
        3. Obtiene el factor de escala actual del sistema
        4. Calcula un factor de ajuste personalizado
        5. Aplica el factor y redondea hacia arriba (ceil)

        Args:
            size: Dimensión o dimensiones a escalar. Puede ser un número individual (int/float)
                  o una colección de números (lista/tupla).

        Returns:
            Union[int, List[int]]: El tamaño escalado.
                - Si la entrada es un número, retorna un entero escalado.
                - Si la entrada es una lista/tupla, retorna una lista de enteros escalados.

        Ejemplos:
            >>> self.scale_size(10)  # Retorna 15 (en un sistema con factor ~1.5)
            >>> self.scale_size([10, 20])  # Retorna [15, 30]
            >>> self.scale_size((5, 10, 15))  # Retorna [8, 15, 23]

        Nota:
            Siempre redondea hacia arriba para evitar elementos demasiado pequeños,
            lo que podría afectar la legibilidad o usabilidad.
        """

        # Obtiene el sistema de ventanas actual: 'aqua' (macOS), 'win32' (Windows) o 'x11' (Unix/Linux)
        # Este valor determina qué factor base se utilizará para el cálculo
        winsys = self.style.master.tk.call("tk", "windowingsystem")

        # Establece el valor de referencia (BASELINE) según la plataforma
        # Estos valores representan factores de escala de referencia para normalización
        if winsys == "aqua":  # macOS
            # macOS tiene una relación diferente entre píxeles físicos y unidades Tk
            BASELINE = 1.000492368291482  # Valor muy cercano a 1.0
        else:  # Windows, Linux u otros
            # Otros sistemas tienen una relación píxel/unidad diferente
            BASELINE = 1.33398982438864281  # Aproximadamente 4/3

        # Obtiene el factor de escala actual del sistema Tkinter
        # Este valor refleja la densidad de píxeles y configuración del sistema
        # Ejemplos típicos: 1.0 (pantalla estándar), 1.5-2.0 (pantallas HiDPI)
        scaling = self.style.master.tk.call("tk", "scaling")

        # Calcula el factor de ajuste personalizado dividiendo el scaling actual
        # por el valor de referencia de la plataforma
        # Esto normaliza el factor para que sea consistente entre plataformas
        factor = scaling / BASELINE

        # Aplica el factor según el tipo de entrada
        if isinstance(size, (int, float)):
            # Para un número único, multiplica por el factor y redondea hacia arriba
            # Ejemplo: size=10, factor=1.5 → 10*1.5=15.0 → ceil(15.0)=15
            return ceil(size * factor)
        elif isinstance(size, (tuple, list)):
            # Para colecciones, procesa cada elemento individualmente
            # Crea una nueva lista con los valores escalados (siempre enteros)
            # Ejemplo: size=[10,20], factor=1.5 → [ceil(10*1.5), ceil(20*1.5)] → [15, 30]
            return [ceil(x * factor) for x in size]

    def create_button_style(self, colorname=DEFAULT) -> None:
        """Crea un estilo sólido para el widget ttk.Button.

        Crea y configura un estilo personalizado para botones ttk, incluyendo
        estados normal, deshabilitado, presionado y hover.

        Args:
            colorname (str): La etiqueta de color usada para estilizar el widget.

        Returns:
            None: Este método no retorna nada, solo crea y registra el estilo.
        """
        # Paso 1: Definición del estilo base
        # Establece el nombre base del estilo para el botón
        STYLE = "TButton"

        # Paso 2: Determinación de colores base
        # Define el nombre del estilo y los colores principales según el color proporcionado
        if any([colorname == DEFAULT, colorname == ""]):
            # Si es color por defecto, usa el estilo primario
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
        else:
            # Si es color personalizado, construye el nombre del estilo y obtiene los colores
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)

        # Paso 3: Cálculo de colores derivados
        # Calcula los colores para diferentes estados del botón
        bordercolor = background
        # Color de fondo para estado deshabilitado (10% de opacidad)
        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        # Color de texto para estado deshabilitado (30% de opacidad)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        # Color para estado presionado (80% de opacidad)
        pressed = Colors.make_transparent(0.80, background, self.colors.bg)
        # Color para estado hover (90% de opacidad)
        hover = Colors.make_transparent(0.90, background, self.colors.bg)

        # Paso 4: Configuración del estilo base
        # Establece las propiedades visuales básicas del botón
        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=bordercolor,
            darkcolor=background,
            lightcolor=background,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
        )

        # Paso 5: Mapeo de estados
        # Define cómo cambian los colores según el estado del botón
        self.style.map(
            ttkstyle,
            # Configura el color del texto en estado deshabilitado
            foreground=[("disabled", disabled_fg)],
            # Configura los colores de fondo para diferentes estados
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            # Configura el color del borde para estado deshabilitado
            bordercolor=[("disabled", disabled_bg)],
            # Configura el color oscuro para diferentes estados
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            # Configura el color claro para diferentes estados
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )

        # Paso 6: Registro del estilo
        # Registra el estilo creado en el sistema de estilos
        self.style._register_ttkstyle(ttkstyle)

    def create_link_button_style(self, colorname=DEFAULT) -> None:
        """Crea un estilo de botón tipo enlace para el widget ttk.Button.

        Configura la apariencia y comportamiento de un botón que simula ser un enlace,
        permitiendo diferentes variantes de color y estados.

        Args:
            colorname: Etiqueta de color usada para estilizar el widget.
                      Si es DEFAULT, usa los colores base del tema.
        """
        STYLE = "Link.TButton"

        # Definición de colores para estados pressed y hover
        pressed = self.colors.info
        hover = self.colors.info

        # Determina el color de primer plano y el nombre del estilo
        if any([colorname == DEFAULT, colorname == ""]):
            foreground = self.colors.fg
            ttkstyle = STYLE
        elif colorname == LIGHT:
            foreground = self.colors.fg
            ttkstyle = f"{colorname}.{STYLE}"
        else:
            foreground = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"

        # Calcula el color para el estado deshabilitado
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Configura el estilo base del botón
        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=self.colors.bg,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            anchor=tk.CENTER,
            padding=(10, 5),
        )

        # Configura el mapeo de estados del botón
        self.style.map(
            ttkstyle,
            shiftrelief=[("pressed !disabled", -1)],
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            focuscolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            background=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            bordercolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
        )

        # Registra el estilo TTK
        self.style._register_ttkstyle(ttkstyle)

    def create_combobox_style(self, colorname: str = DEFAULT) -> None:
        """Crea un estilo para el widget Combobox de TTK.

        Configura la apariencia y comportamiento del widget Combobox, incluyendo
        sus diferentes estados (normal, deshabilitado, lectura, etc.) y colores.

        Args:
            colorname: Etiqueta de color a usar como color primario del widget.
                      Si es DEFAULT, usa los colores base del tema.
        """
        STYLE = "TCombobox"

        # Determina los colores según el tipo de tema (claro/oscuro)
        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        # Configura el color de enfoque según el nombre de color
        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.get(colorname)

        # Crea los elementos base del combobox
        self.style.element_create(f"{element}.downarrow", "from", TTK_DEFAULT)
        self.style.element_create(f"{element}.padding", "from", TTK_CLAM)
        self.style.element_create(f"{element}.textarea", "from", TTK_CLAM)

        # Ajusta el color del borde si se especifica un color personalizado
        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor

        # Configura el estilo base del combobox
        self.style._build_configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            arrowcolor=self.colors.inputfg,
            foreground=self.colors.inputfg,
            fieldbackground=self.colors.inputbg,
            background=self.colors.inputbg,
            insertcolor=self.colors.inputfg,
            relief=tk.FLAT,
            padding=5,
            arrowsize=self.scale_size(12),
        )

        # Configura el mapeo de estados del combobox
        self.style.map(
            ttkstyle,
            background=[("readonly", readonly)],
            fieldbackground=[("readonly", readonly)],
            foreground=[("disabled", disabled_fg)],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
                ("readonly", readonly),
            ],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
                ("readonly", readonly),
            ],
            arrowcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", focuscolor),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
        )

        # Define el layout del combobox
        self.style.layout(
            ttkstyle,
            [
                (
                    "combo.Spinbox.field",
                    {
                        "side": tk.TOP,
                        "sticky": tk.EW,
                        "children": [
                            (
                                "Combobox.downarrow",
                                {"side": tk.RIGHT, "sticky": tk.NS},
                            ),
                            (
                                "Combobox.padding",
                                {
                                    "expand": "1",
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Combobox.textarea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            ),
                        ],
                    },
                )
            ],
        )

        # Registra el estilo TTK creado
        self.style._register_ttkstyle(ttkstyle)

    def update_combobox_popdown_style(self, widget) -> None:
        """Actualiza los elementos legacy del ttk.Combobox.

        Este método se llama cada vez que se cambia el tema para asegurar que
        los componentes tkinter heredados incrustados en este widget ttk estén
        estilizados apropiadamente según el tema actual.

        El ttk.Combobox contiene varios elementos que no están estilizados usando
        el motor de temas ttk. Esto incluye el **popdownwindow** y el **scrollbar**.
        Ambos widgets se configuran manualmente usando llamadas a tcl/tk.

        Args:
            widget (ttk.Combobox): El elemento combobox a actualizar.

        Returns:
            None: Este método no retorna nada, solo actualiza los estilos directamente.
        """

        # Paso 1: Determinación del color del borde
        # Selecciona el color adecuado según el tema actual (claro u oscuro)
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        # Paso 2: Configuración de ajustes de estilo Tk
        # Crea una lista con todas las propiedades de estilo necesarias
        tk_settings = []
        # Configura el ancho del borde
        tk_settings.extend(["-borderwidth", 2])
        # Configura el grosor del resaltado
        tk_settings.extend(["-highlightthickness", 1])
        # Establece el color del resaltado
        tk_settings.extend(["-highlightcolor", bordercolor])
        # Configura el color de fondo
        tk_settings.extend(["-background", self.colors.inputbg])
        # Configura el color del texto
        tk_settings.extend(["-foreground", self.colors.inputfg])
        # Configura el color de fondo para la selección
        tk_settings.extend(["-selectbackground", self.colors.selectbg])
        # Configura el color del texto para la selección
        tk_settings.extend(["-selectforeground", self.colors.selectfg])

        # Paso 3: Configuración del estilo de la ventana popdown
        # Obtiene la referencia a la ventana popdown del combobox
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {widget}")
        # Aplica las configuraciones de estilo al listbox del popdown
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # Paso 4: Configuración del estilo de la barra de desplazamiento
        # Define el estilo vertical para la barra de desplazamiento
        sb_style = "TCombobox.Vertical.TScrollbar"
        # Aplica el estilo a la barra de desplazamiento del popdown
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)