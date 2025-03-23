import tkinter as tk
from tkinter import ttk
from tkinter import font
from math import ceil
from typing import Union, List, Tuple, Callable, Dict, Any
from PIL import ImageTk, ImageDraw, Image

from ui.themeengine.core.color import Colors
from ui.themeengine.builders.style_builder_tk import StyleBuilderTK
from ui.themeengine.core.theme import ThemeDefinition
from ui.themeengine.utils.constants import LIGHT, DARK, TTK_CLAM, TTK_ALT, TTK_DEFAULT, DEFAULT, PRIMARY
from ui.themeengine.utils import utility as util

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
        """Inicializa un tema TTK personalizado con la configuración base.

        Este método crea un nuevo tema TTK basado en 'clam', lo establece como el
        tema activo en el sistema, y aplica la configuración inicial necesaria para
        todos los widgets. Es una parte fundamental del proceso de inicialización
        del sistema de temas.

        El proceso incluye tres pasos principales:
        1. Creación del tema personalizado basado en 'clam'
        2. Activación del tema en el sistema TTK
        3. Configuración detallada de todos los componentes del tema

        Este método no recibe parámetros y se basa en el estado actual de la instancia,
        específicamente en las propiedades 'style' y 'theme'. Utiliza la infraestructura
        de temas de tkinter.ttk para crear y aplicar el tema personalizado.

        Returns:
            None: Este método no devuelve ningún valor, pero como efecto secundario
                crea y activa un nuevo tema TTK en el sistema.

        Dependencias:
            - tkinter y tkinter.ttk: Módulos estándar para interfaz gráfica.
            - self.style: Instancia de la clase Style personalizada.
            - self.theme: Objeto que contiene la definición del tema actual.
            - TTK_CLAM: Constante con valor 'clam' (tema base de TTK).
        """
        # Paso 1: Crear un nuevo tema TTK personalizado
        # Utiliza el nombre del tema actual y lo basa en el tema 'clam' de TTK
        # 'clam' proporciona un conjunto visual coherente como punto de partida
        # que funciona de manera consistente en diferentes plataformas (Windows, Mac, Linux)
        # Ejemplo: Si self.theme.name es "dark", crea un tema llamado "dark"
        self.style.theme_create(self.theme.name, TTK_CLAM)

        # Paso 2: Establecer el tema creado como tema activo en el sistema TTK
        # Utiliza el método estático theme_use de ttk.Style (no el método de instancia)
        # Esto activa el tema para todos los widgets TTK de la aplicación
        # y actualiza la apariencia de los widgets existentes inmediatamente
        # A partir de aquí, todos los widgets nuevos usarán este tema por defecto
        ttk.Style.theme_use(self.style, self.theme.name)

        # Paso 3: Aplicar la configuración específica del tema
        # Esto desencadena una serie de actualizaciones que configuran:
        # - El estilo predeterminado (raíz '.') que afecta a todos los widgets
        # - Estilos específicos para diferentes tipos de widgets
        # - Otras personalizaciones necesarias para el tema actual
        # La cadena de llamadas incluye create_default_style(), create_link_button_style(), etc.
        self.update_ttk_theme_settings()

    def update_ttk_theme_settings(self) -> None:
        """Coordina la actualización de la configuración visual del tema TTK actual.

        Este método sirve como punto central para iniciar la cadena de actualizaciones
        necesarias cuando el tema cambia. Es responsable de asegurar que todos los
        componentes visuales se configuren correctamente según el tema actual.

        El método es llamado en dos escenarios principales:
        1. Durante la creación de un nuevo tema (`create_theme()`)
        2. Cuando se cambia dinámicamente de un tema a otro

        La implementación actual configura el estilo raíz a través de `create_default_style()`
        y proporciona un punto de extensión para agregar más actualizaciones específicas
        según sea necesario.

        Flujo de ejecución típico:
        - Configuración del estilo raíz '.' que afecta a todos los widgets
        - Creación de estilos específicos (como botones tipo enlace)
        - [Punto de extensión] Otras actualizaciones específicas del tema

        Returns:
            None: Este método no devuelve ningún valor, pero como efecto secundario
                configura todos los componentes visuales del tema TTK actual.

        See Also:
            create_theme: Método que crea un nuevo tema TTK y llama a este método.
            create_default_style: Método llamado para configurar el estilo raíz.
        """
        # Paso 1: Configurar el estilo raíz y estilos básicos
        # Esta llamada inicia la configuración del estilo base '.' que afecta a todos los widgets
        # y también configura algunos estilos básicos como el de botón tipo enlace
        # Es el primer paso esencial en la cadena de actualización del tema
        self.create_default_style()

    def create_default_style(self) -> None:
        """Configura el estilo predeterminado para widgets TTK y estilos básicos adicionales.

        Este método establece la configuración base del estilo raíz '.' que sirve como
        fundamento visual para todos los widgets TTK. Define las propiedades visuales
        fundamentales como colores de fondo, texto, selección y bordes que serán
        heredadas por todos los widgets TTK a menos que se sobrescriban específicamente.

        Además de configurar el estilo raíz, este método también inicializa algunos
        estilos básicos adicionales como el estilo de botón tipo enlace y su variante
        para símbolos.

        Este método debe llamarse primero antes de aplicar cualquier otro estilo durante
        la creación o actualización del tema, ya que establece la base visual sobre la
        que se construirán los demás estilos.

        Propiedades configuradas en el estilo raíz:
        - background: Color de fondo principal
        - foreground: Color de texto principal
        - darkcolor: Color para bordes y efectos 3D
        - troughcolor: Color para canaletas en scrollbars y progressbars
        - selectbg/selectbackground: Color de fondo para elementos seleccionados
        - selectfg/selectforeground: Color de texto para elementos seleccionados
        - fieldbg: Color de fondo para campos de entrada (siempre blanco)
        - borderwidth: Ancho del borde (1 píxel)
        - focuscolor: Color del indicador de foco

        Returns:
            None: Este método no devuelve ningún valor, pero como efecto secundario
                configura el estilo raíz y otros estilos básicos en el sistema TTK.

        See Also:
            update_ttk_theme_settings: Método que llama a este como primer paso de configuración.
            create_link_button_style: Método llamado por este para configurar el estilo de enlaces.
        """
        self.style._build_configure(
            style=".",  # Identificador del estilo raíz
            background=self.colors.bg,  # Color de fondo principal (ej: "#f0f0f0" en tema claro)
            darkcolor=self.colors.border,  # Color para bordes y efectos 3D (ej: "#c0c0c0")
            foreground=self.colors.fg,  # Color de texto principal (ej: "#333333" en tema claro)
            troughcolor=self.colors.bg,  # Color de canaletas en scrollbars/progressbars (mismo que el fondo)
            selectbg=self.colors.selectbg,  # Color de fondo para elementos seleccionados (ej: "#0078d7")
            selectfg=self.colors.selectfg,  # Color de texto para elementos seleccionados (ej: "#ffffff")
            selectforeground=self.colors.selectfg,  # Alias de selectfg para compatibilidad
            selectbackground=self.colors.selectbg,  # Alias de selectbg para compatibilidad
            fieldbg="white",  # Color de fondo para campos de entrada (siempre blanco para legibilidad)
            borderwidth=1,  # Ancho del borde en píxeles (valor estándar)
            focuscolor="",  # Color del indicador de foco (vacío = usar predeterminado)
        )

        # Paso 2: Crear el estilo de botón tipo enlace (botones que parecen enlaces web)
        # Este estilo se considera básico y se crea temprano en el proceso de configuración
        # Permite tener botones que visualmente se comportan como enlaces de hipertexto
        self.create_link_button_style()

        # Paso 3: Configurar variante del estilo de enlace para símbolos/iconos
        # Esta variante usa un tamaño de fuente mayor (16) para mostrar símbolos o iconos basados en texto
        # Es útil para botones que muestran iconos simples mediante caracteres tipográficos
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

    def create_button_style(self, colorname: str = DEFAULT) -> None:
        """Crea un estilo visual personalizado para widgets ttk.Button.

        Este método genera y registra un estilo TTK completo para botones, definiendo
        su apariencia visual en todos sus estados posibles (normal, deshabilitado,
        presionado, hover). El estilo creado se adapta automáticamente al tema actual
        y puede ser personalizado mediante la especificación de un color base.

        La generación del estilo incluye:
        - Determinación de colores base según el parámetro y tema actual
        - Cálculo de colores derivados para diferentes estados interactivos
        - Configuración de propiedades visuales básicas (relieve, padding, etc.)
        - Definición del comportamiento visual en diferentes estados
        - Registro del estilo en el sistema para su posterior utilización

        Args:
            colorname (str, opcional): Etiqueta de color para estilizar el botón.
                Valores comunes: 'primary', 'success', 'info', 'warning', 'danger'.
                Si es DEFAULT o vacío, se utiliza el color primario del tema.
                Defaults a DEFAULT ('default').

        Returns:
            None: Este método no devuelve ningún valor, pero como efecto secundario
                crea y registra un estilo TTK que puede ser utilizado por widgets
                ttk.Button mediante la propiedad 'style'.

        """
        # Definición del estilo base para botones TTK
        # Este nombre se usa como identificador en el sistema de estilos TTK
        STYLE = "TButton"

        # Determinación del nombre del estilo y colores base según el parámetro recibido
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso 1: Color por defecto - usar color primario del tema
            # ttkstyle: Nombre simple sin prefijo (ej: "TButton")
            # foreground: Color de texto con contraste adecuado para color primario
            # background: Color primario del tema actual (ej: azul "#007bff")
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
        else:
            # Caso 2: Color personalizado - construir nombre y obtener colores correspondientes
            # ttkstyle: Nombre compuesto con prefijo de color (ej: "success.TButton")
            # foreground: Color de texto apropiado para el color especificado
            # background: Color correspondiente al nombre (ej: verde "#28a745" para 'success')
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)

        # Cálculo de colores derivados para diferentes estados del botón
        # Utilizamos el mismo color para el borde que para el fondo (botón sólido)
        bordercolor = background

        # Color de fondo para estado deshabilitado - 10% de opacidad del texto sobre fondo
        # Genera un color grisáceo atenuado para indicar que el botón está deshabilitado
        # Ejemplo: Si fg="#000000" y bg="#ffffff" → aproximadamente "#e6e6e6" (gris claro)
        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)

        # Color de texto para estado deshabilitado - 30% de opacidad del texto sobre fondo
        # Genera un texto atenuado para mostrar que el botón está deshabilitado
        # Ejemplo: Mismos colores → aproximadamente "#b3b3b3" (gris medio)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Color para estado presionado - 80% de opacidad del color base sobre fondo
        # Crea un efecto visual de botón presionado (ligeramente oscurecido)
        # Ejemplo: Si background="#007bff" y bg="#ffffff" → aproximadamente "#3395ff"
        pressed = Colors.make_transparent(0.80, background, self.colors.bg)

        # Color para estado hover - 90% de opacidad del color base sobre fondo
        # Crea un efecto visual sutil cuando el cursor está sobre el botón
        # Ejemplo: Con mismos colores → aproximadamente "#1a87ff"
        hover = Colors.make_transparent(0.90, background, self.colors.bg)

        # Configuración del estilo base con propiedades visuales fundamentales
        self.style._build_configure(
            ttkstyle,  # Nombre del estilo a configurar
            foreground=foreground,  # Color del texto del botón
            background=background,  # Color de fondo principal
            bordercolor=bordercolor,  # Color del borde (igual al fondo para aspecto sólido)
            darkcolor=background,  # Color oscuro para efectos 3D (igual al fondo)
            lightcolor=background,  # Color claro para efectos 3D (igual al fondo)
            relief=tk.RAISED,  # Relieve sutil para efecto 3D ligero
            focusthickness=0,  # Sin borde visible cuando el botón tiene el foco
            focuscolor=foreground,  # Color de enfoque (igual al texto)
            padding=(10, 5),  # Espaciado interno: 10px horizontal, 5px vertical
            anchor=tk.CENTER,  # Alineación del contenido centrada
        )

        # Mapeo de estados para definir cambios visuales según la interacción del usuario
        self.style.map(
            ttkstyle,  # Nombre del estilo a mapear

            # Color del texto - solo cambia en estado deshabilitado
            foreground=[
                ("disabled", disabled_fg),  # Texto atenuado cuando está deshabilitado
            ],

            # Color de fondo - cambia según el estado del botón
            # El orden importa: la última coincidencia tiene prioridad
            background=[
                ("disabled", disabled_bg),  # Grisáceo cuando está deshabilitado
                ("pressed !disabled", pressed),  # Color oscurecido cuando está presionado
                ("hover !disabled", hover),  # Color sutilmente alterado al pasar el cursor
            ],

            # Color del borde - cambia solo en estado deshabilitado
            bordercolor=[
                ("disabled", disabled_bg),  # Borde grisáceo cuando está deshabilitado
            ],

            # Color oscuro para efectos 3D - cambia según el estado
            darkcolor=[
                ("disabled", disabled_bg),  # Grisáceo cuando está deshabilitado
                ("pressed !disabled", pressed),  # Oscurecido cuando está presionado
                ("hover !disabled", hover),  # Sutilmente alterado al pasar el cursor
            ],

            # Color claro para efectos 3D - cambia según el estado (mismo patrón)
            lightcolor=[
                ("disabled", disabled_bg),  # Grisáceo cuando está deshabilitado
                ("pressed !disabled", pressed),  # Oscurecido cuando está presionado
                ("hover !disabled", hover),  # Sutilmente alterado al pasar el cursor
            ],
        )

        # Registro del estilo creado en el sistema de estilos TTK
        # Esto permite que el estilo sea localizado y reutilizado cuando sea necesario
        # También evita recrear el mismo estilo múltiples veces
        self.style._register_ttkstyle(ttkstyle)

    def create_link_button_style(self, colorname: str = DEFAULT) -> None:
        """Crea un estilo de botón que simula un enlace web para widgets ttk.Button.

        Este método genera y registra un estilo TTK que hace que un botón se comporte y
        se vea como un enlace de texto, sin el aspecto visual tradicional de un botón
        (sin fondo visible ni bordes). El enlace cambia de color al interactuar con él,
        simulando el comportamiento estándar de los enlaces web.

        Características principales:
        - Apariencia de texto simple sin bordes ni fondo visible
        - Cambio de color al pasar el cursor (hover) o al hacer clic (pressed)
        - Efecto visual sutil de "presionado" al hacer clic
        - Adaptación automática al tema actual de la aplicación
        - Posibilidad de personalizar el color base del enlace

        Args:
            colorname (str, opcional): Etiqueta de color para el texto del enlace.
                Si es DEFAULT o vacío, usa el color de texto estándar del tema.
                Si es LIGHT, usa el color de texto estándar pero con nombre específico.
                Si es otro valor, usa ese color específico de la paleta.
                Valores comunes: 'primary', 'info', 'success', etc.
                Defaults a DEFAULT ('default').

        Returns:
            None: Este método no devuelve ningún valor, pero como efecto secundario
                crea y registra un estilo TTK que puede ser utilizado por widgets
                ttk.Button mediante la propiedad 'style'.

        """
        # Nombre base del estilo para botones tipo enlace
        # Este sufijo distingue este estilo especial de los botones normales
        STYLE = "Link.TButton"

        # Definición de colores para estados interactivos
        # A diferencia de los botones normales, usamos un color fijo (info) para ambos estados
        # Normalmente este es un azul informativo que se asocia con enlaces
        # Ejemplo: Si self.colors.info es "#17a2b8", ambos estados usarán este color
        pressed = self.colors.info  # Color cuando el enlace se presiona
        hover = self.colors.info  # Color cuando el cursor está sobre el enlace

        # Determinación del color del texto y nombre del estilo según el parámetro
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso 1: Color por defecto - usar el color de texto estándar del tema
            # Ejemplo: Si self.colors.fg es "#333333", el enlace tendrá este color
            foreground = self.colors.fg
            ttkstyle = STYLE  # Nombre sin prefijo: "Link.TButton"
        elif colorname == LIGHT:
            # Caso 2: Color LIGHT - comportamiento especial para temas claros
            # Usa el mismo color de texto estándar pero con nombre distintivo
            foreground = self.colors.fg
            ttkstyle = f"{colorname}.{STYLE}"  # Nombre: "light.Link.TButton"
        else:
            # Caso 3: Color personalizado - usar el color específico de la paleta
            # Ejemplo: Si colorname es "primary", usa el color primario del tema
            foreground = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"  # Nombre: "primary.Link.TButton"

        # Cálculo del color para el estado deshabilitado
        # Usamos 30% de opacidad del color de texto sobre el fondo para un efecto atenuado
        # Ejemplo: Si fg="#000000" y bg="#ffffff" → aproximadamente "#b3b3b3" (gris)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Configuración del estilo base para simular un enlace
        # La clave es usar el color de fondo como color de todos los elementos
        # esto hace que el botón parezca "invisible" excepto por su texto
        self.style._build_configure(
            ttkstyle,  # Nombre del estilo a configurar
            foreground=foreground,  # Color del texto (según parámetro)
            background=self.colors.bg,  # Fondo igual al de la aplicación ("invisible")
            bordercolor=self.colors.bg,  # Borde invisible (igual al fondo)
            darkcolor=self.colors.bg,  # Color oscuro invisible (igual al fondo)
            lightcolor=self.colors.bg,  # Color claro invisible (igual al fondo)
            relief=tk.RAISED,  # Relieve técnicamente presente pero no visible
            focusthickness=0,  # Sin borde visible cuando tiene el foco
            focuscolor=foreground,  # Color de enfoque igual al texto
            anchor=tk.CENTER,  # Alineación del texto centrada
            padding=(10, 5),  # Espaciado interno: 10px horizontal, 5px vertical
        )

        # Mapeo de estados para definir cambios visuales según la interacción
        self.style.map(
            ttkstyle,
            # Efecto visual sutil al presionar: cambia ligeramente el relieve (-1)
            # Esto crea una sensación de "hundimiento" al hacer clic
            shiftrelief=[("pressed !disabled", -1)],

            # Configuración del color del texto según el estado
            # Solo el texto cambia de color, manteniendo la apariencia de enlace
            foreground=[
                ("disabled", disabled_fg),  # Atenuado cuando está deshabilitado
                ("pressed !disabled", pressed),  # Color info cuando está presionado
                ("hover !disabled", hover),  # Color info cuando el cursor está encima
            ],

            # Configuración del color de enfoque según el estado
            focuscolor=[
                ("pressed !disabled", pressed),  # Color info cuando está presionado
                ("hover !disabled", pressed),  # Color info cuando el cursor está encima
            ],

            # Las siguientes propiedades mantienen el color de fondo en todos los estados
            # Esto asegura que el botón parezca un enlace de texto simple
            # sin importar el estado de interacción
            background=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],

            # Color del borde igual al fondo en todos los estados (invisible)
            bordercolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],

            # Color oscuro igual al fondo en todos los estados (invisible)
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],

            # Color claro igual al fondo en todos los estados (invisible)
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
        )

        # Registro del estilo creado en el sistema de estilos TTK
        # Esto permite su utilización posterior y evita recreación innecesaria
        self.style._register_ttkstyle(ttkstyle)

    def create_outline_button_style(self, colorname=DEFAULT):
        """Crea un estilo tipo "outline" (contorno) para widgets ttk.Button.

        Este método define un estilo de botón donde el color principal se usa como
        contorno y texto sobre un fondo neutro. Al interactuar con el botón (hover
        o presionado), los colores se invierten: el color principal pasa a ser el
        fondo y el texto adquiere un color contrastante.

        El efecto visual es el de un botón que se "llena" con su color principal
        al interactuar con él, similar a los botones outline de frameworks como
        Bootstrap.

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el widget. Puede ser:
                - DEFAULT o "": Utiliza el color PRIMARY del tema
                - Cualquier etiqueta de color definida: Aplica ese color específico

        Returns:
            None: El método no retorna valores, pero registra un estilo TTK
                  que puede ser utilizado por widgets Button.

        """
        # Identificador base para estilo de botón tipo outline/contorno
        STYLE = "Outline.TButton"

        # Calcula color semitransparente para estado deshabilitado
        # Aplica 30% de transparencia al color de texto sobre fondo
        # Ej: si fg="#000000" y bg="#FFFFFF", disabled_fg="#B3B3B3" (gris)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Determina nombre de estilo y color a utilizar
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso DEFAULT: usa estilo base sin prefijo
            ttkstyle = STYLE  # Resultado: "Outline.TButton"
            # Usa el color primario del tema
            colorname = PRIMARY  # Ej: PRIMARY="primary"
        else:
            # Caso específico: crea nombre con prefijo
            # Ej: si colorname=SUCCESS, resultado="Success.Outline.TButton"
            ttkstyle = f"{colorname}.{STYLE}"

        # Calcula los colores para los diferentes estados del botón

        # Color principal para texto y borde en estado normal
        # Ej: para PRIMARY podría ser "#1976D2" (azul)
        foreground = self.colors.get(colorname)

        # Color contrastante para texto en estados interactivos
        # Utiliza get_foreground que elige entre blanco/negro según contraste
        # Ej: para azul oscuro podría ser "#FFFFFF" (blanco)
        background = self.colors.get_foreground(colorname)

        # Color de texto para estados pressed/hover (invertido del normal)
        foreground_pressed = background  # Ej: "#FFFFFF"

        # Color para el borde (igual al color principal)
        bordercolor = foreground  # Ej: "#1976D2"

        # Color de fondo para estados pressed/hover (igual al principal)
        pressed = foreground  # Ej: "#1976D2"
        hover = foreground  # Ej: "#1976D2"

        # Configura el estilo base (estado normal del botón)
        self.style._build_configure(
            ttkstyle,
            foreground=foreground,  # Color principal para el texto
            background=self.colors.bg,  # Fondo neutral del tema
            bordercolor=bordercolor,  # Borde del color principal
            darkcolor=self.colors.bg,  # Evita sombreado 3D en bordes
            lightcolor=self.colors.bg,  # Evita sombreado 3D en bordes
            relief=tk.RAISED,  # Ligero efecto 3D elevado
            focusthickness=0,  # Sin borde adicional de foco
            focuscolor=foreground,  # Indicador de foco del color principal
            padding=(10, 5),  # Espaciado interior estándar
            anchor=tk.CENTER,  # Texto centrado en el botón
        )

        # Define cambios visuales para diferentes estados del botón
        self.style.map(
            ttkstyle,
            # Cambios en el color de texto
            foreground=[
                # Texto semitransparente cuando está deshabilitado
                ("disabled", disabled_fg),
                # Texto invertido (ej: blanco) cuando está presionado
                ("pressed !disabled", foreground_pressed),
                # Mismo efecto al hacer hover
                ("hover !disabled", foreground_pressed),
            ],
            # Cambios en el color de fondo
            background=[
                # Color principal como fondo al presionar
                # Crea efecto de "llenado" del botón
                ("pressed !disabled", pressed),
                # Mismo efecto al hacer hover
                ("hover !disabled", hover),
            ],
            # Cambios en el color del borde
            bordercolor=[
                # Borde semitransparente cuando deshabilitado
                ("disabled", disabled_fg),
                # Borde del mismo color que el fondo al presionar
                ("pressed !disabled", pressed),
                # Mismo efecto al hacer hover
                ("hover !disabled", hover),
            ],
            # Cambios en el color de foco (coherente con texto)
            focuscolor=[
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            # Cambios en colores de sombreado (coherentes con fondo)
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )

        # Registra el estilo para hacerlo disponible en la aplicación
        self.style._register_ttkstyle(ttkstyle)

    def create_combobox_style(self, colorname: str = DEFAULT) -> None:
        """Crea un estilo personalizado para widgets Combobox de TTK.

        Este método configura la apariencia visual y el comportamiento interactivo
        de los widgets Combobox de TTK, definiendo cómo se ven y responden en
        diferentes estados (normal, deshabilitado, solo lectura, etc.).

        La implementación considera el tipo de tema actual (claro u oscuro) y
        permite personalizar el color primario del widget a través del parámetro
        colorname, afectando principalmente el color de enfoque y bordes.

        El método genera todos los componentes necesarios para el Combobox:
        - Flecha desplegable
        - Área de texto
        - Padding y estructura de layout
        - Configuración de colores para todos los estados

        Args:
            colorname (str, opcional): Etiqueta de color a usar como color primario.
                Si es DEFAULT o cadena vacía, usa los colores base del tema.
                Ejemplos: "primary", "info", "danger", etc.
                Default: DEFAULT.

        Returns:
            None: Este método no retorna ningún valor, pero registra el estilo
            creado en el sistema TTK.

        """
        # Constante que define el nombre base del estilo TTK para Combobox
        STYLE = "TCombobox"

        # Ajustar colores según el tipo de tema (claro/oscuro)
        # Estos colores se usan para estados especiales como deshabilitado o solo lectura
        if self.is_light_theme:
            # En temas claros: usar colores más suaves para mejor visibilidad
            disabled_fg = self.colors.border  # Color para texto deshabilitado
            bordercolor = self.colors.border  # Color base para bordes
            readonly = self.colors.light  # Fondo para estado solo-lectura
        else:
            # En temas oscuros: usar colores con más contraste
            disabled_fg = self.colors.selectbg  # Color para texto deshabilitado
            bordercolor = self.colors.selectbg  # Color base para bordes
            readonly = bordercolor  # Fondo para estado solo-lectura

        # Determinar nombre de estilo y color de enfoque según el parámetro colorname
        if any([colorname == DEFAULT, colorname == ""]):
            # Para color predeterminado: usar el estilo base "TCombobox"
            ttkstyle = STYLE  # Ejemplo: "TCombobox"
            element = f"{ttkstyle.replace('TC', 'C')}"  # Ejemplo: "Combobox"
            focuscolor = self.colors.primary  # Usar color primario del tema
        else:
            # Para color personalizado: crear un estilo derivado con prefijo
            ttkstyle = f"{colorname}.{STYLE}"  # Ejemplo: "info.TCombobox"
            element = f"{ttkstyle.replace('TC', 'C')}"  # Ejemplo: "info.Combobox"
            focuscolor = self.colors.get(colorname)  # Obtener color específico

        # Crear los elementos básicos del combobox a partir de temas predefinidos
        # Estos elementos son los componentes visuales fundamentales del widget
        self.style.element_create(f"{element}.downarrow", "from", TTK_DEFAULT)  # Flecha desplegable
        self.style.element_create(f"{element}.padding", "from", TTK_CLAM)  # Espaciado interno
        self.style.element_create(f"{element}.textarea", "from", TTK_CLAM)  # Área de texto

        # Solo aplicar configuración completa para colores personalizados
        # Esto evita sobrescribir innecesariamente el estilo predeterminado
        if all([colorname, colorname != DEFAULT]):
            # Para estilos personalizados, usar el color de enfoque como color de borde
            bordercolor = focuscolor

            # Configurar estilo base del combobox con todos sus atributos visuales
            self.style._build_configure(
                ttkstyle,
                bordercolor=bordercolor,  # Color del borde
                darkcolor=self.colors.inputbg,  # Color para sombras
                lightcolor=self.colors.inputbg,  # Color para iluminaciones
                arrowcolor=self.colors.inputfg,  # Color de la flecha desplegable
                foreground=self.colors.inputfg,  # Color del texto
                fieldbackground=self.colors.inputbg,  # Color de fondo del campo
                background=self.colors.inputbg,  # Color de fondo general
                insertcolor=self.colors.inputfg,  # Color del cursor de inserción
                relief=tk.FLAT,  # Estilo de borde (plano)
                padding=5,  # Espaciado interno en píxeles
                arrowsize=self.scale_size(12),  # Tamaño de flecha adaptado a resolución
            )

            # Definir comportamiento visual según el estado del widget
            # Mapea diferentes estados a cambios visuales específicos
            self.style.map(
                ttkstyle,
                # Cambios de fondo para estado solo-lectura
                background=[("readonly", readonly)],
                fieldbackground=[("readonly", readonly)],

                # Cambio de color de texto para estado deshabilitado
                foreground=[("disabled", disabled_fg)],

                # Cambios en color del borde según estado
                bordercolor=[
                    ("invalid", self.colors.danger),  # Rojo para validación fallida
                    ("focus !disabled", focuscolor),  # Color primario cuando tiene foco
                    ("hover !disabled", focuscolor),  # Color primario al pasar el mouse
                ],

                # Cambios en color claro según estado
                lightcolor=[
                    ("focus invalid", self.colors.danger),  # Rojo para validación fallida con foco
                    ("focus !disabled", focuscolor),  # Color primario cuando tiene foco
                    ("pressed !disabled", focuscolor),  # Color primario cuando está presionado
                    ("readonly", readonly),  # Color especial para solo-lectura
                ],

                # Cambios en color oscuro según estado
                darkcolor=[
                    ("focus invalid", self.colors.danger),  # Rojo para validación fallida con foco
                    ("focus !disabled", focuscolor),  # Color primario cuando tiene foco
                    ("pressed !disabled", focuscolor),  # Color primario cuando está presionado
                    ("readonly", readonly),  # Color especial para solo-lectura
                ],

                # Cambios en color de flecha según estado
                arrowcolor=[
                    ("disabled", disabled_fg),  # Color atenuado cuando deshabilitado
                    ("pressed !disabled", focuscolor),  # Color primario cuando presionado
                    ("focus !disabled", focuscolor),  # Color primario cuando tiene foco
                    ("hover !disabled", focuscolor),  # Color primario al pasar el mouse
                ],
            )

            # Definir estructura jerárquica del widget (layout)
            # Establece cómo se organizan y anidan los elementos visuales
            self.style.layout(
                ttkstyle,
                [
                    (
                        "combo.Spinbox.field",  # Contenedor principal basado en Spinbox
                        {
                            "side": tk.TOP,  # Posicionado en la parte superior
                            "sticky": tk.EW,  # Expandirse horizontalmente
                            "children": [
                                (
                                    "Combobox.downarrow",  # Flecha desplegable
                                    {"side": tk.RIGHT, "sticky": tk.NS},  # A la derecha, altura completa
                                ),
                                (
                                    "Combobox.padding",  # Área de padding
                                    {
                                        "expand": "1",  # Expandirse para llenar espacio
                                        "sticky": tk.NSEW,  # Expandirse en todas direcciones
                                        "children": [
                                            (
                                                "Combobox.textarea",  # Área de texto
                                                {"sticky": tk.NSEW},  # Expandirse en todas direcciones
                                            )
                                        ],
                                    },
                                ),
                            ],
                        },
                    )
                ],
            )

            # Registrar el estilo TTK creado para evitar recreación innecesaria
            self.style._register_ttkstyle(ttkstyle)

    def update_combobox_popdown_style(self, widget) -> None:
        """Actualiza los elementos legacy (heredados) del ttk.Combobox.

        Este método estiliza manualmente los componentes internos del Combobox
        que no son controlados por el sistema de temas TTK estándar, utilizando
        llamadas directas a la interfaz Tcl/Tk subyacente.

        El ttk.Combobox contiene dos elementos principales que requieren estilización
        manual:
        1. popdownwindow: La ventana desplegable que muestra las opciones
        2. scrollbar: La barra de desplazamiento vertical para navegar las opciones

        La configuración aplicada incluye:
        - Colores de fondo y texto
        - Colores de selección
        - Grosores y colores de bordes
        - Estilo de la barra de desplazamiento

        Los colores se adaptan automáticamente según el tema actual (claro u oscuro)
        para mantener coherencia visual con el resto de la aplicación.

        Args:
            widget (ttk.Combobox): El widget Combobox cuyos elementos internos
                                 serán estilizados.

        Returns:
            None: Este método no retorna ningún valor, pero modifica directamente
                  la apariencia del widget proporcionado.

        Nota:
            Este método debe llamarse después de crear el widget Combobox y
            cada vez que se cambia el tema de la aplicación.
        """

        # Paso 1: DETERMINACIÓN DEL COLOR DEL BORDE
        # Selecciona el color adecuado según el tema actual (claro u oscuro)
        if self.is_light_theme:
            # En temas claros: usar el color de borde estándar (normalmente gris claro)
            # Ejemplo: "#d9d9d9"
            bordercolor = self.colors.border
        else:
            # En temas oscuros: usar el color de fondo de selección (normalmente más oscuro)
            # Ejemplo: "#4e5969"
            bordercolor = self.colors.selectbg

        # Paso 2: PREPARACIÓN DE CONFIGURACIONES DE ESTILO
        # Crea una lista con todas las propiedades de estilo en formato Tcl/Tk
        # Las propiedades se agregan como pares [opción, valor]
        tk_settings = []

        # Configuración de bordes y resaltado
        tk_settings.extend(["-borderwidth", 2])  # Ancho del borde: 2px
        tk_settings.extend(["-highlightthickness", 1])  # Grosor del resaltado: 1px
        tk_settings.extend(["-highlightcolor", bordercolor])  # Color del resaltado

        # Configuración de colores principales
        tk_settings.extend(["-background", self.colors.inputbg])  # Color de fondo
        tk_settings.extend(["-foreground", self.colors.inputfg])  # Color del texto

        # Configuración de colores para elementos seleccionados
        tk_settings.extend(["-selectbackground", self.colors.selectbg])  # Fondo selección
        tk_settings.extend(["-selectforeground", self.colors.selectfg])  # Texto selección

        # Paso 3: OBTENCIÓN Y CONFIGURACIÓN DE LA VENTANA POPDOWN
        # Obtiene la referencia Tcl a la ventana popdown mediante comandos Tcl/Tk
        # Ejemplo de valor retornado: ".140257291655416.140257288977872"
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {widget}")

        # Aplica las configuraciones al listbox (.f.l) dentro del popdown
        # .f es el frame, .l es el listbox
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # Paso 4: CONFIGURACIÓN DE LA BARRA DE DESPLAZAMIENTO
        # Define el nombre del estilo TTK para la barra de desplazamiento vertical
        sb_style = "TCombobox.Vertical.TScrollbar"

        # Aplica el estilo a la barra de desplazamiento (.f.sb) del popdown
        # .f es el frame, .sb es la barra de desplazamiento
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)

    def create_separator_style(self, colorname=DEFAULT):
        """Crea estilos personalizados para los widgets ttk.Separator.

        Este método genera y registra dos estilos TTK: uno para separadores horizontales y
        otro para separadores verticales. Los estilos creados utilizan imágenes de color sólido
        para representar visualmente los separadores, adaptándose automáticamente según el tema
        actual sea claro u oscuro.

        Parameters:
            colorname (str):
                Nombre del color a utilizar para los separadores. Debe corresponder a un color
                definido en self.colors (como 'primary', 'secondary', etc.).
                Si es 'default' o una cadena vacía, se utilizará automáticamente el color de
                borde para temas claros o el color de selección para temas oscuros.
                Valor predeterminado: 'default'

        Returns:
            None: Este método no retorna ningún valor, pero tiene los siguientes efectos:

            1. Crea dos estilos TTK:
               - Si colorname es 'default': "Horizontal.TSeparator" y "Vertical.TSeparator"
               - Si se especifica colorname: "{colorname}.Horizontal.TSeparator" y
                 "{colorname}.Vertical.TSeparator"

            2. Genera imágenes personalizadas para representar los separadores

            3. Registra los estilos creados en el sistema de estilos TTK

        """
        # Definir constantes para los nombres base de estilos y tamaños
        HSTYLE = "Horizontal.TSeparator"  # Estilo base para separador horizontal
        VSTYLE = "Vertical.TSeparator"  # Estilo base para separador vertical

        # Dimensiones en píxeles para las imágenes de los separadores
        hsize = [40, 1]  # Horizontal: 40px de ancho, 1px de alto
        vsize = [1, 40]  # Vertical: 1px de ancho, 40px de alto

        # Determinar el color predeterminado según el tema actual
        if self.is_light_theme:
            # En temas claros, el separador destacará mejor con el color de borde
            default_color = self.colors.border  # Ej: "#cccccc"
        else:
            # En temas oscuros, usar el color de selección para mejor visibilidad
            default_color = self.colors.selectbg  # Ej: "#4a6984"

        # Determinar el color a utilizar y construir los nombres de estilo
        if any([colorname == DEFAULT, colorname == ""]):
            # Usar configuración predeterminada si no se especifica un color válido
            background = default_color
            h_ttkstyle = HSTYLE  # "Horizontal.TSeparator"
            v_ttkstyle = VSTYLE  # "Vertical.TSeparator"
        else:
            # Usar el color especificado por el parámetro colorname
            background = self.colors.get(colorname)  # Ej: self.colors.primary
            # Construir nombres con prefijo del color
            h_ttkstyle = f"{colorname}.{HSTYLE}"  # Ej: "primary.Horizontal.TSeparator"
            v_ttkstyle = f"{colorname}.{VSTYLE}"  # Ej: "primary.Vertical.TSeparator"

        # CREACIÓN DEL SEPARADOR HORIZONTAL
        # Convertir el nombre de estilo a nombre de elemento (quitar el prefijo 'T')
        h_element = h_ttkstyle.replace(".TS", ".S")  # Ej: "Horizontal.Separator"

        # Crear una imagen RGB del tamaño y color especificados
        h_img = ImageTk.PhotoImage(Image.new("RGB", hsize, background))

        # Generar un nombre único para la imagen y guardarla para evitar que el GC la elimine
        h_name = util.get_image_name(h_img)  # Ej: "pyimage42"
        self.theme_images[h_name] = h_img

        # Crear un elemento visual usando la imagen generada
        self.style.element_create(f"{h_element}.separator", "image", h_name)

        # Definir el layout del estilo con expansión horizontal (East-West)
        self.style.layout(h_ttkstyle, [(f"{h_element}.separator", {"sticky": tk.EW})])

        # CREACIÓN DEL SEPARADOR VERTICAL (proceso análogo al horizontal)
        v_element = v_ttkstyle.replace(".TS", ".S")
        v_img = ImageTk.PhotoImage(Image.new("RGB", vsize, background))
        v_name = util.get_image_name(v_img)
        self.theme_images[v_name] = v_img
        self.style.element_create(f"{v_element}.separator", "image", v_name)

        # Layout con expansión vertical (North-South)
        self.style.layout(v_ttkstyle, [(f"{v_element}.separator", {"sticky": tk.NS})]) # El parámetro "sticky" con valor tk.EW (East-West) hace que el separador se expanda horizontalmente

        # Registrar los estilos creados en el sistema para su posterior gestión
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_striped_progressbar_assets(self, thickness, colorname=DEFAULT):
        """Crea imágenes para barras de progreso con patrón rayado diagonal.

        Este método genera dos imágenes:
        1. Una horizontal con patrón rayado diagonal
        2. Una vertical (rotación de 90° de la horizontal)

        Las imágenes se crean combinando dos tonalidades del color especificado:
        - Color base: El color principal para las rayas
        - Color claro: Una versión más clara del color base para el fondo

        El contraste entre ambos colores se ajusta automáticamente según el brillo
        del color base para garantizar visibilidad en colores tanto oscuros como claros.

        Parameters:
            thickness (int):
                Grosor en píxeles de la barra de progreso. Define el tamaño final
                de las imágenes generadas (thickness × thickness píxeles).

            colorname (str, opcional):
                Nombre del color a utilizar para la barra de progreso. Debe corresponder
                a un color definido en self.colors (como 'primary', 'secondary', etc.).
                Si es 'default' o una cadena vacía, se utilizará el color primario del tema.
                Valor predeterminado: 'default'

        Returns:
            Tuple[str, str]:
                Una tupla con dos elementos:
                - Primer elemento: Identificador (nombre) de la imagen horizontal
                - Segundo elemento: Identificador (nombre) de la imagen vertical

                Estos identificadores pueden usarse posteriormente para acceder a las imágenes
                almacenadas en self.theme_images.
        """
        # Determinar el color base para la barra de progreso
        if any([colorname == DEFAULT, colorname == ""]):
            # Si no se especifica un color, usar el color primario del tema
            barcolor = self.colors.primary  # Ej: "#007bff"
        else:
            # Obtener el color correspondiente al nombre especificado
            barcolor = self.colors.get(colorname)  # Ej: self.colors.success -> "#28a745"

        # Calcular la variante más clara del color base
        # 1. Obtener el componente de brillo (Value) del color base
        brightness = Colors.rgb_to_hsv(*Colors.hex_to_rgb(barcolor))[2]

        # 2. Determinar el incremento de brillo según el brillo del color base
        if brightness < 0.4:
            # Para colores oscuros, aumentar significativamente el brillo
            value_delta = 0.3  # Ej: para un color muy oscuro como "#212529"
        elif brightness > 0.8:
            # Para colores muy brillantes, no aumentar el brillo
            value_delta = 0  # Ej: para un color muy brillante como "#f8f9fa"
        else:
            # Para colores de brillo medio, aumentar ligeramente el brillo
            value_delta = 0.1  # Ej: para un color medio como "#007bff"

        # 3. Crear la variante más clara: reducir saturación y ajustar brillo
        barcolor_light = Colors.update_hsv(barcolor, sd=-0.2, vd=value_delta)
        # Ej: "#007bff" -> "#3399ff"

        # Crear la imagen base con el patrón rayado (100×100 píxeles)
        # 4. Crear una imagen con fondo del color claro
        img = Image.new("RGBA", (100, 100), barcolor_light)

        # 5. Preparar objeto para dibujar en la imagen
        draw = ImageDraw.Draw(img)

        # 6. Dibujar polígono grande diagonal (rayas principales)
        draw.polygon(
            xy=[(0, 0), (48, 0), (100, 52), (100, 100)],
            fill=barcolor,  # Usar el color base
        )

        # 7. Dibujar polígono pequeño en esquina inferior izquierda (completar patrón)
        draw.polygon(xy=[(0, 52), (48, 100), (0, 100)], fill=barcolor)

        # Redimensionar la imagen al tamaño final requerido
        _resized = img.resize((thickness, thickness), Image.LANCZOS)
        # Ej: Si thickness=20, redimensiona de 100×100 a 20×20 píxeles

        # Crear y almacenar la imagen horizontal
        h_img = ImageTk.PhotoImage(_resized)
        h_name = h_img._PhotoImage__photo.name  # Ej: "pyimage123"

        # Crear y almacenar la imagen vertical (rotación de 90° de la horizontal)
        v_img = ImageTk.PhotoImage(_resized.rotate(90))
        v_name = v_img._PhotoImage__photo.name  # Ej: "pyimage124"

        # Guardar las imágenes en el diccionario de imágenes del tema
        # Esto previene que sean eliminadas por el recolector de basura
        self.theme_images[h_name] = h_img
        self.theme_images[v_name] = v_img

        # Devolver los identificadores para su uso posterior
        return h_name, v_name

    def create_striped_progressbar_style(self, colorname=DEFAULT):
        """Crea un estilo con patrón rayado para widgets ttk.Progressbar.

        Este método genera estilos TTK para barras de progreso con un patrón rayado
        diagonal. Crea tanto la versión horizontal como vertical, y se adapta
        automáticamente al tema actual (claro/oscuro).

        El método utiliza imágenes rayadas generadas por el método
        create_striped_progressbar_assets y configura todas las propiedades visuales
        necesarias, incluyendo colores, bordes y disposición de los elementos.

        Parameters:
            colorname (str, opcional):
                Nombre del color a utilizar para la barra de progreso. Debe corresponder
                a un color definido en self.colors (como 'primary', 'secondary', etc.).

                Si es 'default' o una cadena vacía, se utilizarán los estilos base sin prefijo.

                El valor 'light' tiene un tratamiento especial para los colores de canal y borde
                en temas claros.

                Valor predeterminado: 'default'

        Returns:
            None: Este método no retorna ningún valor, pero tiene los siguientes efectos:

            1. Crea dos estilos TTK:
               - Si colorname es 'default': "Striped.Horizontal.TProgressbar" y
                 "Striped.Vertical.TProgressbar"
               - Si se especifica colorname: "{colorname}.Striped.Horizontal.TProgressbar" y
                 "{colorname}.Striped.Vertical.TProgressbar"

            2. Configura el layout y las propiedades visuales de ambos estilos

            3. Registra los estilos en el sistema de estilos TTK

        """
        # Definir constantes para los nombres base de los estilos
        HSTYLE = "Striped.Horizontal.TProgressbar"  # Estilo base para barra horizontal rayada
        VSTYLE = "Striped.Vertical.TProgressbar"  # Estilo base para barra vertical rayada

        # Calcular el grosor de la barra adaptado a la densidad de la pantalla
        thickness = self.scale_size(12)  # Escala el valor base de 12 píxeles

        # Determinar los nombres completos de los estilos
        if any([colorname == DEFAULT, colorname == ""]):
            # Si no se especifica un color válido, usar nombres base
            h_ttkstyle = HSTYLE  # Ej: "Striped.Horizontal.TProgressbar"
            v_ttkstyle = VSTYLE  # Ej: "Striped.Vertical.TProgressbar"
        else:
            # Si se especifica un color, usar como prefijo
            h_ttkstyle = f"{colorname}.{HSTYLE}"  # Ej: "primary.Striped.Horizontal.TProgressbar"
            v_ttkstyle = f"{colorname}.{VSTYLE}"  # Ej: "primary.Striped.Vertical.TProgressbar"

        # Configurar colores según el tema actual y el color especificado
        if self.is_light_theme:
            # Configuración para temas claros
            if colorname == LIGHT:
                # Caso especial para el color 'light'
                troughcolor = self.colors.bg  # Color de fondo para el canal
                bordercolor = self.colors.light  # Color claro para el borde
            else:
                # Para otros colores en tema claro
                troughcolor = self.colors.light  # Color claro para el canal
                bordercolor = troughcolor  # Mismo color para el borde
        else:
            # Configuración para temas oscuros
            # Crear una versión más oscura del color de selección para el canal
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)
            bordercolor = troughcolor  # Mismo color para el borde

        # Obtener las imágenes rayadas para las barras de progreso
        # Devuelve una tupla (imagen_horizontal, imagen_vertical)
        images = self.create_striped_progressbar_assets(thickness, colorname)

        # ---- CREACIÓN DEL ESTILO HORIZONTAL ----
        # Convertir el nombre de estilo a nombre de elemento (quitar el prefijo 'T')
        h_element = h_ttkstyle.replace(".TP", ".P")  # Ej: "Striped.Horizontal.Progressbar"

        # Crear un elemento visual personalizado para la barra de progreso horizontal
        self.style.element_create(
            f"{h_element}.pbar",  # Nombre del elemento
            "image",  # Tipo de elemento (basado en imagen)
            images[0],  # Imagen horizontal obtenida anteriormente
            width=thickness,  # Ancho igual al grosor calculado
            sticky=tk.EW,  # Expansión horizontal
        )

        # Definir el layout del estilo horizontal
        self.style.layout(
            h_ttkstyle,  # Nombre del estilo
            [
                (
                    f"{h_element}.trough",  # Elemento canal (contenedor)
                    {
                        "sticky": tk.NSEW,  # Expandir en todas direcciones
                        "children": [
                            (
                                f"{h_element}.pbar",  # Elemento barra de progreso
                                {"side": tk.LEFT, "sticky": tk.NS},  # Alineado a la izquierda, expandido verticalmente
                            )
                        ],
                    },
                )
            ],
        )

        # Configurar propiedades visuales del estilo horizontal
        self.style._build_configure(
            h_ttkstyle,  # Nombre del estilo
            troughcolor=troughcolor,  # Color del canal
            thickness=thickness,  # Grosor de la barra
            bordercolor=bordercolor,  # Color del borde
            borderwidth=1,  # Ancho del borde (1 píxel)
        )

        # ---- CREACIÓN DEL ESTILO VERTICAL ----
        # Convertir el nombre de estilo a nombre de elemento (quitar el prefijo 'T')
        v_element = v_ttkstyle.replace(".TP", ".P")  # Ej: "Striped.Vertical.Progressbar"

        # Crear un elemento visual personalizado para la barra de progreso vertical
        self.style.element_create(
            f"{v_element}.pbar",  # Nombre del elemento
            "image",  # Tipo de elemento (basado en imagen)
            images[1],  # Imagen vertical (rotada 90°)
            width=thickness,  # Ancho igual al grosor calculado
            sticky=tk.NS,  # Expansión vertical
        )

        # Definir el layout del estilo vertical
        self.style.layout(
            v_ttkstyle,  # Nombre del estilo
            [
                (
                    f"{v_element}.trough",  # Elemento canal (contenedor)
                    {
                        "sticky": tk.NSEW,  # Expandir en todas direcciones
                        "children": [
                            (
                                f"{v_element}.pbar",  # Elemento barra de progreso
                                {"side": tk.BOTTOM, "sticky": tk.EW},  # Alineado abajo, expandido horizontalmente
                            )
                        ],
                    },
                )
            ],
        )

        # Configurar propiedades visuales del estilo vertical
        self.style._build_configure(
            v_ttkstyle,  # Nombre del estilo
            troughcolor=troughcolor,  # Color del canal
            bordercolor=bordercolor,  # Color del borde
            thickness=thickness,  # Grosor de la barra
            borderwidth=1,  # Ancho del borde (1 píxel)
        )

        # Registrar los estilos creados en el sistema
        self.style._register_ttkstyle(h_ttkstyle)  # Registrar estilo horizontal
        self.style._register_ttkstyle(v_ttkstyle)  # Registrar estilo vertical

    def create_progressbar_style(self, colorname=DEFAULT):
        """Crea un estilo sólido para widgets ttk.Progressbar.

        Este método genera estilos TTK para barras de progreso con un color sólido
        (sin patrones). Crea tanto la versión horizontal como vertical, y se adapta
        automáticamente al tema actual (claro/oscuro).

        El método configura todas las propiedades visuales necesarias, incluyendo
        colores, bordes, y disposición de los elementos. Utiliza elementos de los
        temas TTK predefinidos ('clam' y 'default') como base.

        Parameters:
            colorname (str, opcional):
                Nombre del color a utilizar para la barra de progreso. Debe corresponder
                a un color definido en self.colors (como 'primary', 'secondary', etc.).

                Si es 'default' o una cadena vacía, se utilizará el color primario del tema
                y los estilos base sin prefijo.

                El valor 'light' tiene un tratamiento especial para los colores de canal y borde
                en temas claros.

                Valor predeterminado: 'default'

        Returns:
            None: Este método no retorna ningún valor, pero tiene los siguientes efectos:

            1. Crea dos estilos TTK:
               - Si colorname es 'default': "Horizontal.TProgressbar" y "Vertical.TProgressbar"
               - Si se especifica colorname: "{colorname}.Horizontal.TProgressbar" y
                 "{colorname}.Vertical.TProgressbar"

            2. Configura el layout y las propiedades visuales de ambos estilos

            3. Registra los estilos en el sistema de estilos TTK
        """
        # Definir constantes para los nombres base de los estilos
        H_STYLE = "Horizontal.TProgressbar"  # Estilo base para barra horizontal
        V_STYLE = "Vertical.TProgressbar"  # Estilo base para barra vertical

        # Calcular el grosor de la barra adaptado a la densidad de la pantalla
        thickness = self.scale_size(10)  # Escala el valor base de 10 píxeles

        # Configurar colores de canal y borde según el tema actual
        if self.is_light_theme:
            # Configuración para temas claros
            if colorname == LIGHT:
                # Caso especial para el color 'light'
                troughcolor = self.colors.bg  # Color de fondo para el canal
                bordercolor = self.colors.light  # Color claro para el borde
            else:
                # Para otros colores en tema claro
                troughcolor = self.colors.light  # Color claro para el canal
                bordercolor = troughcolor  # Mismo color para el borde
        else:
            # Configuración para temas oscuros
            # Crear una versión más oscura del color de selección para el canal
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)
            bordercolor = troughcolor  # Mismo color para el borde

        # Determinar color de fondo y nombres de estilo según el parámetro colorname
        if any([colorname == DEFAULT, colorname == ""]):
            # Si no se especifica un color válido, usar color primario y nombres base
            background = self.colors.primary  # Ej: "#007bff"
            h_ttkstyle = H_STYLE  # "Horizontal.TProgressbar"
            v_ttkstyle = V_STYLE  # "Vertical.TProgressbar"
        else:
            # Si se especifica un color, usarlo y prefijar los nombres de estilo
            background = self.colors.get(colorname)  # Ej: self.colors.success -> "#28a745"
            h_ttkstyle = f"{colorname}.{H_STYLE}"  # Ej: "success.Horizontal.TProgressbar"
            v_ttkstyle = f"{colorname}.{V_STYLE}"  # Ej: "success.Vertical.TProgressbar"

        # Configurar propiedades iniciales para el estilo horizontal
        self.style._build_configure(
            h_ttkstyle,
            thickness=thickness,  # Grosor calculado
            borderwidth=1,  # Ancho del borde en píxeles
            bordercolor=bordercolor,  # Color del borde determinado anteriormente
            lightcolor=self.colors.border,  # Color claro (generalmente para efectos)
            pbarrelief=tk.FLAT,  # Relieve plano para la barra
            troughcolor=troughcolor,  # Color del canal determinado anteriormente
        )

        # Obtener lista de elementos existentes para evitar recrearlos
        existing_elements = self.style.element_names()

        # Configurar propiedades iniciales para el estilo vertical (similar al horizontal)
        self.style._build_configure(
            v_ttkstyle,
            thickness=thickness,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=self.colors.border,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
        )

        # Esta línea parece redundante, ya se obtuvo la lista de elementos
        existing_elements = self.style.element_names()

        # CREACIÓN DEL ESTILO HORIZONTAL
        # Generar nombres para los elementos
        h_element = h_ttkstyle.replace(".TP", ".P")  # Ej: "Horizontal.Progressbar"
        trough_element = f"{h_element}.trough"  # Ej: "Horizontal.Progressbar.trough"
        pbar_element = f"{h_element}.pbar"  # Ej: "Horizontal.Progressbar.pbar"

        # Crear elementos si no existen, evitando errores de duplicación
        if trough_element not in existing_elements:
            # Crear elemento de canal basado en el tema 'clam'
            self.style.element_create(trough_element, "from", TTK_CLAM)
            # Crear elemento de barra basado en el tema 'default'
            self.style.element_create(pbar_element, "from", TTK_DEFAULT)

        # Definir el layout del estilo horizontal
        self.style.layout(
            h_ttkstyle,  # Nombre del estilo
            [
                (
                    trough_element,  # Elemento canal (contenedor)
                    {
                        "sticky": "nswe",  # Expandir en todas direcciones
                        "children": [
                            (
                                pbar_element,  # Elemento barra de progreso
                                {"side": "left", "sticky": "ns"},  # Alineado a la izquierda, expandido verticalmente
                            )
                        ],
                    },
                )
            ],
        )

        # Configurar el color de fondo para el estilo horizontal
        self.style._build_configure(h_ttkstyle, background=background)

        # CREACIÓN DEL ESTILO VERTICAL
        # Generar nombres para los elementos
        v_element = v_ttkstyle.replace(".TP", ".P")  # Ej: "Vertical.Progressbar"
        trough_element = f"{v_element}.trough"  # Ej: "Vertical.Progressbar.trough"
        pbar_element = f"{v_element}.pbar"  # Ej: "Vertical.Progressbar.pbar"

        # Crear elementos si no existen, evitando errores de duplicación
        if trough_element not in existing_elements:
            # Crear elemento de canal basado en el tema 'clam'
            self.style.element_create(trough_element, "from", TTK_CLAM)
            # Crear elemento de barra basado en el tema 'default'
            self.style.element_create(pbar_element, "from", TTK_DEFAULT)
            # Configurar el color de fondo para el estilo vertical
            # NOTA: Esta configuración solo se aplica si los elementos no existían
            # lo que parece ser un error, ya que debería aplicarse siempre
            self.style._build_configure(v_ttkstyle, background=background)

        # Definir el layout del estilo vertical
        self.style.layout(
            v_ttkstyle,  # Nombre del estilo
            [
                (
                    trough_element,  # Elemento canal (contenedor)
                    {
                        "sticky": "nswe",  # Expandir en todas direcciones
                        "children": [
                            (
                                pbar_element,  # Elemento barra de progreso
                                {"side": "bottom", "sticky": "we"},  # Alineado abajo, expandido horizontalmente
                            )
                        ],
                    },
                )
            ],
        )

        # Registrar los estilos creados en el sistema
        self.style._register_ttkstyle(h_ttkstyle)  # Registrar estilo horizontal
        self.style._register_ttkstyle(v_ttkstyle)  # Registrar estilo vertical

    def create_scale_assets(self, colorname=DEFAULT, size=14):
        """Crea los activos visuales (imágenes) para el widget ttk.Scale.

        Este método genera las imágenes necesarias para personalizar completamente
        un widget de escala deslizante, incluyendo:

        1. El controlador (handle) del deslizador en cuatro estados:
           - Normal: estado predeterminado
           - Presionado: cuando se está arrastrando
           - Hover: cuando el cursor está encima
           - Deshabilitado: cuando el widget está inactivo

        2. Las pistas (tracks) por las que se desliza el controlador:
           - Horizontal: para escalas con orientación horizontal
           - Vertical: para escalas con orientación vertical

        El tamaño del controlador se ajusta automáticamente según la resolución de
        la pantalla para garantizar una buena experiencia de usuario en diferentes
        dispositivos.

        Parameters:
            colorname (str, opcional):
                Nombre del color a utilizar para el controlador. Debe corresponder
                a un color definido en self.colors (como 'primary', 'secondary', etc.).
                Si es 'default' o una cadena vacía, se utilizará el color primario.
                El valor 'light' tiene un tratamiento especial para el color de la pista
                en temas claros.
                Valor predeterminado: 'default'

            size (int, opcional):
                Diámetro base del círculo del controlador en píxeles. Este valor será
                escalado automáticamente según la resolución de la pantalla.
                Valor predeterminado: 14

        Returns:
            Tuple[str, str, str, str, str, str]:
                Una tupla con seis identificadores de imágenes en el siguiente orden:
                1. Controlador en estado normal
                2. Controlador en estado presionado
                3. Controlador en estado hover
                4. Controlador en estado deshabilitado
                5. Pista horizontal
                6. Pista vertical

                Estos identificadores pueden usarse posteriormente para acceder a las imágenes
                almacenadas en self.theme_images.
        """
        # Escalar el tamaño según la densidad de la pantalla
        size = self.scale_size(size)  # Ej: 14 -> 21 en pantallas de alta densidad

        # Determinar colores para componentes según el tema actual
        if self.is_light_theme:
            # En temas claros
            disabled_color = self.colors.border  # Color para estado deshabilitado (ej: "#ced4da")
            if colorname == LIGHT:
                # Caso especial para el color 'light'
                track_color = self.colors.bg  # Color de fondo para la pista (ej: "#f8f9fa")
            else:
                # Para otros colores en tema claro
                track_color = self.colors.light  # Color claro para la pista (ej: "#e9ecef")
        else:
            # En temas oscuros
            disabled_color = self.colors.selectbg  # Color de selección para deshabilitado (ej: "#375a7f")
            # Versión más oscura del color de selección para la pista
            track_color = Colors.update_hsv(self.colors.selectbg, vd=-0.2)  # Ej: "#2d4869"

        # Determinar el color base para el controlador
        if any([colorname == DEFAULT, colorname == ""]):
            # Si no se especifica un color válido, usar color primario
            normal_color = self.colors.primary  # Ej: "#007bff"
        else:
            # Si se especifica un color, usarlo
            normal_color = self.colors.get(colorname)  # Ej: self.colors.success -> "#28a745"

        # Calcular colores derivados para estados especiales
        # Color para estado presionado: ligeramente más oscuro
        pressed_color = Colors.update_hsv(normal_color, vd=-0.1)  # Ej: "#0062cc"
        # Color para estado hover: ligeramente más claro
        hover_color = Colors.update_hsv(normal_color, vd=0.1)  # Ej: "#3395ff"

        # ----- CREACIÓN DE IMÁGENES PARA EL CONTROLADOR EN DIFERENTES ESTADOS -----

        # Estado normal
        _normal = Image.new("RGBA", (100, 100))  # Imagen base transparente
        draw = ImageDraw.Draw(_normal)  # Objeto para dibujar en la imagen
        draw.ellipse((0, 0, 95, 95), fill=normal_color)  # Dibujar círculo
        # Redimensionar al tamaño final y convertir a formato Tkinter
        normal_img = ImageTk.PhotoImage(
            _normal.resize((size, size), Image.LANCZOS)  # LANCZOS para mejor calidad
        )
        # Generar nombre único y almacenar para evitar que el GC la elimine
        normal_name = util.get_image_name(normal_img)  # Ej: "pyimage1"
        self.theme_images[normal_name] = normal_img

        # Estado presionado (cuando se hace clic)
        _pressed = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_pressed)
        draw.ellipse((0, 0, 95, 95), fill=pressed_color)  # Color más oscuro
        pressed_img = ImageTk.PhotoImage(
            _pressed.resize((size, size), Image.LANCZOS)
        )
        pressed_name = util.get_image_name(pressed_img)  # Ej: "pyimage2"
        self.theme_images[pressed_name] = pressed_img

        # Estado hover (cuando el cursor está encima)
        _hover = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_hover)
        draw.ellipse((0, 0, 95, 95), fill=hover_color)  # Color más claro
        hover_img = ImageTk.PhotoImage(
            _hover.resize((size, size), Image.LANCZOS)
        )
        hover_name = util.get_image_name(hover_img)  # Ej: "pyimage3"
        self.theme_images[hover_name] = hover_img

        # Estado deshabilitado (cuando el widget está inactivo)
        _disabled = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_disabled)
        draw.ellipse((0, 0, 95, 95), fill=disabled_color)  # Color gris o apagado
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize((size, size), Image.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)  # Ej: "pyimage4"
        self.theme_images[disabled_name] = disabled_img

        # ----- CREACIÓN DE IMÁGENES PARA LAS PISTAS -----

        # Pista horizontal (rectángulo ancho pero bajo)
        h_track_img = ImageTk.PhotoImage(
            Image.new("RGB", self.scale_size((40, 5)), track_color)
        )
        h_track_name = util.get_image_name(h_track_img)  # Ej: "pyimage5"
        self.theme_images[h_track_name] = h_track_img

        # Pista vertical (rectángulo alto pero estrecho)
        v_track_img = ImageTk.PhotoImage(
            Image.new("RGB", self.scale_size((5, 40)), track_color)
        )
        v_track_name = util.get_image_name(v_track_img)  # Ej: "pyimage6"
        self.theme_images[v_track_name] = v_track_img

        # Devolver todos los identificadores de imágenes en orden específico
        return (
            normal_name,  # Identificador para imagen de estado normal
            pressed_name,  # Identificador para imagen de estado presionado
            hover_name,  # Identificador para imagen de estado hover
            disabled_name,  # Identificador para imagen de estado deshabilitado
            h_track_name,  # Identificador para imagen de pista horizontal
            v_track_name,  # Identificador para imagen de pista vertical
        )

    def create_scale_style(self, colorname=DEFAULT):
        """Crea un estilo personalizado para widgets ttk.Scale.

        Este método genera estilos TTK para controles deslizantes (escalas)
        con apariencia personalizada tanto en orientación horizontal como vertical.
        Utiliza los activos visuales (imágenes) generados por el método
        create_scale_assets para crear controles deslizantes visualmente atractivos
        que responden a diferentes estados (normal, hover, presionado, deshabilitado).

        Parameters:
            colorname (str, opcional):
                Nombre del color a utilizar para el control deslizante. Debe corresponder
                a un color definido en self.colors (como 'primary', 'secondary', etc.).

                Si es 'default' o una cadena vacía, se utilizarán los estilos base con
                prefijo de orientación.

                Valor predeterminado: 'default'

        Returns:
            None: Este método no retorna ningún valor, pero tiene los siguientes efectos:

            1. Crea dos estilos TTK:
               - Si colorname es 'default': "Horizontal.TScale" y "Vertical.TScale"
               - Si se especifica colorname: "{colorname}.Horizontal.TScale" y
                 "{colorname}.Vertical.TScale"

            2. Configura elementos y layouts para proporcionar una experiencia visual
               personalizada y responsiva

            3. Registra los estilos en el sistema de estilos TTK

        """
        # Definir constante para el nombre base del estilo
        STYLE = "TScale"  # Nombre estándar de TTK para controles deslizantes

        # Determinar los nombres completos de los estilos
        if any([colorname == DEFAULT, colorname == ""]):
            # Si no se especifica un color válido, usar prefijos de orientación
            h_ttkstyle = f"Horizontal.{STYLE}"  # Ej: "Horizontal.TScale"
            v_ttkstyle = f"Vertical.{STYLE}"  # Ej: "Vertical.TScale"
        else:
            # Si se especifica un color, usarlo como prefijo
            h_ttkstyle = f"{colorname}.Horizontal.{STYLE}"  # Ej: "primary.Horizontal.TScale"
            v_ttkstyle = f"{colorname}.Vertical.{STYLE}"  # Ej: "primary.Vertical.TScale"

        # Obtener las imágenes necesarias para los controles deslizantes
        # La tupla contiene: (normal, pressed, hover, disabled, pista_horizontal, pista_vertical)
        images = self.create_scale_assets(colorname)

        # ---- CREACIÓN DEL ESTILO HORIZONTAL ----
        # Convertir el nombre de estilo a nombre de elemento (quitar el prefijo 'T')
        h_element = h_ttkstyle.replace(".TS", ".S")  # Ej: "Horizontal.Scale"

        # Crear elemento para el deslizador horizontal con imágenes para diferentes estados
        self.style.element_create(
            f"{h_element}.slider",  # Nombre del elemento
            "image",  # Tipo de elemento (basado en imagen)
            images[0],  # Imagen para estado normal
            ("disabled", images[3]),  # Imagen para estado deshabilitado
            ("pressed", images[1]),  # Imagen para estado presionado
            ("hover", images[2]),  # Imagen para estado hover
        )

        # Crear elemento para la pista horizontal
        self.style.element_create(
            f"{h_element}.track",  # Nombre del elemento
            "image",  # Tipo de elemento (basado en imagen)
            images[4],  # Imagen de pista horizontal
        )

        # Definir el layout del estilo horizontal
        self.style.layout(
            h_ttkstyle,  # Nombre del estilo
            [
                (
                    f"{h_element}.focus",  # Elemento contenedor (foco)
                    {
                        "expand": "1",  # Expandir para ocupar todo el espacio
                        "sticky": tk.NSEW,  # Adherir en todas direcciones
                        "children": [
                            # Pista horizontal expandida horizontalmente
                            (f"{h_element}.track", {"sticky": tk.EW}),
                            # Deslizador colocado en el lado izquierdo
                            (
                                f"{h_element}.slider",
                                {"side": tk.LEFT, "sticky": ""},
                            ),
                        ],
                    },
                )
            ],
        )

        # ---- CREACIÓN DEL ESTILO VERTICAL ----
        # Convertir el nombre de estilo a nombre de elemento (quitar el prefijo 'T')
        v_element = v_ttkstyle.replace(".TS", ".S")  # Ej: "Vertical.Scale"

        # Crear elemento para el deslizador vertical con imágenes para diferentes estados
        # Usa las mismas imágenes de estado que el deslizador horizontal
        self.style.element_create(
            f"{v_element}.slider",
            "image",
            images[0],  # Normal
            ("disabled", images[3]),  # Deshabilitado
            ("pressed", images[1]),  # Presionado
            ("hover", images[2]),  # Hover
        )

        # Crear elemento para la pista vertical
        self.style.element_create(
            f"{v_element}.track",
            "image",
            images[5],  # Imagen de pista vertical
        )

        # Definir el layout del estilo vertical
        self.style.layout(
            v_ttkstyle,  # Nombre del estilo
            [
                (
                    f"{v_element}.focus",  # Elemento contenedor (foco)
                    {
                        "expand": "1",  # Expandir para ocupar todo el espacio
                        "sticky": tk.NSEW,  # Adherir en todas direcciones
                        "children": [
                            # Pista vertical expandida verticalmente
                            (f"{v_element}.track", {"sticky": tk.NS}),
                            # Deslizador colocado en la parte superior
                            (
                                f"{v_element}.slider",
                                {"side": tk.TOP, "sticky": ""},
                            ),
                        ],
                    },
                )
            ],
        )

        # Registrar los estilos creados en el sistema
        self.style._register_ttkstyle(h_ttkstyle)  # Registrar estilo horizontal
        self.style._register_ttkstyle(v_ttkstyle)  # Registrar estilo vertical

    def create_floodgauge_style(self, colorname=DEFAULT):
        """Crea un estilo TTK para el widget Floodgauge.

        Este método genera estilos para un widget personalizado llamado Floodgauge,
        que combina elementos de barra de progreso (progressbar) y etiqueta (label).
        El resultado es una barra de progreso con texto superpuesto que puede mostrar
        información mientras se llena.

        El estilo creado incluye configuraciones tanto para orientación horizontal
        como vertical, con un grosor fijo de 50 píxeles y texto centrado con tamaño
        de fuente 14.

        Parameters:
            colorname (str, opcional):
                Nombre del color a utilizar para el widget. Debe corresponder
                a un color definido en self.colors (como 'primary', 'secondary', etc.).

                Si es 'default' o una cadena vacía, se utilizará el color primario del tema.

                El valor 'light' tiene un tratamiento especial, utilizando el color de fondo
                del tema para el canal y el color de texto estándar para el texto.

                Valor predeterminado: 'default'

        Returns:
            None: Este método no retorna ningún valor, pero tiene los siguientes efectos:

            1. Crea dos estilos TTK:
               - Si colorname es 'default': "Horizontal.TFloodgauge" y "Vertical.TFloodgauge"
               - Si se especifica colorname: "{colorname}.Horizontal.TFloodgauge" y
                 "{colorname}.Vertical.TFloodgauge"

            2. Configura elementos, layouts y propiedades visuales para ambos estilos

            3. Registra los estilos en el sistema de estilos TTK

        """
        # Definir constantes para nombres de estilo y fuente
        HSTYLE = "Horizontal.TFloodgauge"  # Estilo base para Floodgauge horizontal
        VSTYLE = "Vertical.TFloodgauge"  # Estilo base para Floodgauge vertical
        FLOOD_FONT = "-size 14"  # Especificación de fuente tamaño 14

        # Determinar nombres de estilo y color de fondo según el parámetro colorname
        if any([colorname == DEFAULT, colorname == ""]):
            # Si no se especifica un color válido, usar nombres base y color primario
            h_ttkstyle = HSTYLE  # Ej: "Horizontal.TFloodgauge"
            v_ttkstyle = VSTYLE  # Ej: "Vertical.TFloodgauge"
            background = self.colors.primary  # Ej: "#007bff"
        else:
            # Si se especifica un color, usarlo como prefijo y como color de fondo
            h_ttkstyle = f"{colorname}.{HSTYLE}"  # Ej: "danger.Horizontal.TFloodgauge"
            v_ttkstyle = f"{colorname}.{VSTYLE}"  # Ej: "danger.Vertical.TFloodgauge"
            background = self.colors.get(colorname)  # Ej: self.colors.danger -> "#dc3545"

        # Determinar colores de primer plano y canal según el color seleccionado
        if colorname == LIGHT:
            # Caso especial para el color 'light'
            foreground = self.colors.fg  # Color de texto estándar (Ej: "#212529")
            troughcolor = self.colors.bg  # Color de fondo estándar (Ej: "#f8f9fa")
        else:
            # Para otros colores, calcular colores derivados
            # Canal: versión más clara y menos saturada del color de fondo
            troughcolor = Colors.update_hsv(background, sd=-0.3, vd=0.8)  # Ej: "#d1e6ff"
            # Texto: color de texto para selección (generalmente blanco)
            foreground = self.colors.selectfg  # Ej: "#ffffff"

        # ---- CREACIÓN DEL ESTILO HORIZONTAL ----
        # Convertir el nombre de estilo a nombre de elemento (quitar el prefijo 'T')
        h_element = h_ttkstyle.replace(".TF", ".F")  # Ej: "Horizontal.Floodgauge"

        # Crear elementos reutilizando componentes de temas existentes
        # Elemento canal basado en tema Clam
        self.style.element_create(f"{h_element}.trough", "from", TTK_CLAM)
        # Elemento barra de progreso basado en tema Default
        self.style.element_create(f"{h_element}.pbar", "from", TTK_DEFAULT)

        # Definir el layout del estilo horizontal
        self.style.layout(
            h_ttkstyle,  # Nombre del estilo
            [
                (
                    f"{h_element}.trough",  # Elemento canal (contenedor)
                    {
                        "children": [
                            # Barra de progreso expandida verticalmente
                            (f"{h_element}.pbar", {"sticky": tk.NS}),
                            # Etiqueta para mostrar texto sobre la barra
                            ("Floodgauge.label", {"sticky": ""}),
                        ],
                        "sticky": tk.NSEW,  # Canal expandido en todas direcciones
                    },
                )
            ],
        )

        # Configurar propiedades visuales del estilo horizontal
        self.style._build_configure(
            h_ttkstyle,
            thickness=50,  # Grosor fijo de 50 píxeles
            borderwidth=1,  # Ancho del borde de 1 píxel
            bordercolor=background,  # Color del borde igual al color de fondo
            lightcolor=background,  # Color claro igual al color de fondo
            pbarrelief=tk.FLAT,  # Relieve plano para la barra de progreso
            troughcolor=troughcolor,  # Color del canal calculado previamente
            background=background,  # Color de fondo calculado previamente
            foreground=foreground,  # Color de texto calculado previamente
            justify=tk.CENTER,  # Texto centrado horizontalmente
            anchor=tk.CENTER,  # Texto anclado al centro
            font=FLOOD_FONT,  # Fuente de tamaño 14
        )

        # ---- CREACIÓN DEL ESTILO VERTICAL ----
        # Convertir el nombre de estilo a nombre de elemento (quitar el prefijo 'T')
        v_element = v_ttkstyle.replace(".TF", ".F")  # Ej: "Vertical.Floodgauge"

        # Crear elementos reutilizando componentes de temas existentes
        # Elemento canal basado en tema Clam
        self.style.element_create(f"{v_element}.trough", "from", TTK_CLAM)
        # Elemento barra de progreso basado en tema Default
        self.style.element_create(f"{v_element}.pbar", "from", TTK_DEFAULT)

        # Definir el layout del estilo vertical
        self.style.layout(
            v_ttkstyle,  # Nombre del estilo
            [
                (
                    f"{v_element}.trough",  # Elemento canal (contenedor)
                    {
                        "children": [
                            # Barra de progreso expandida horizontalmente (diferencia con horizontal)
                            (f"{v_element}.pbar", {"sticky": tk.EW}),
                            # Etiqueta para mostrar texto sobre la barra
                            ("Floodgauge.label", {"sticky": ""}),
                        ],
                        "sticky": tk.NSEW,  # Canal expandido en todas direcciones
                    },
                )
            ],
        )

        # Configurar propiedades visuales del estilo vertical (idénticas al horizontal)
        self.style._build_configure(
            v_ttkstyle,
            thickness=50,
            borderwidth=1,
            bordercolor=background,
            lightcolor=background,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
            background=background,
            foreground=foreground,
            justify=tk.CENTER,
            anchor=tk.CENTER,
            font=FLOOD_FONT,
        )

        # Registrar los estilos creados en el sistema
        self.style._register_ttkstyle(h_ttkstyle)  # Registrar estilo horizontal
        self.style._register_ttkstyle(v_ttkstyle)  # Registrar estilo vertical

    def create_arrow_assets(self, arrowcolor, pressed, active):
        """Crea activos de flechas utilizados para varios botones de widgets.

        Este método genera imágenes de flechas en cuatro direcciones (arriba, abajo,
        izquierda, derecha) con tres estados diferentes (normal, presionado, activo).
        Las imágenes generadas se almacenan en el diccionario `theme_images` para su
        uso posterior en la aplicación.

        !!! Nota:
            Este método actualmente no está siendo utilizado.

        Args:
            arrowcolor (str):
                El valor de color a utilizar como color de relleno para la flecha
                en estado normal.

            pressed (str):
                El valor de color a utilizar cuando la flecha está presionada.

            active (str):
                El valor de color a utilizar cuando la flecha está activa o
                con el cursor encima.

        Returns:
            tuple: Una tupla con tres elementos, cada uno conteniendo los nombres de
                   las imágenes para cada estado (normal, presionado, activo). Cada
                   elemento es una tupla de 4 strings con el formato:
                   (flecha_arriba, flecha_abajo, flecha_izquierda, flecha_derecha)

        Ejemplo:
            ```python
            # Crear assets de flechas con colores específicos
            normal_color = "#333333"
            pressed_color = "#555555"
            active_color = "#777777"

            arrow_assets = style_builder.create_arrow_assets(
                normal_color, pressed_color, active_color
            )

            # Los nombres de las imágenes están disponibles en arrow_assets
            normal_arrows, pressed_arrows, active_arrows = arrow_assets
            up_arrow_name, down_arrow_name, left_arrow_name, right_arrow_name = normal_arrows
            ```
        """

        # Función interna para generar un conjunto de flechas en las cuatro direcciones
        def draw_arrow(color: str) -> tuple[str, str, str, str]:
            """Dibuja y almacena un conjunto de flechas en cuatro direcciones.

            Args:
                color: Color para dibujar las flechas.

            Returns:
                Tupla con los nombres de las imágenes (arriba, abajo, izquierda, derecha).
            """
            # Crear imagen base transparente de 11x11 píxeles
            img = Image.new("RGBA", (11, 11))
            # Obtener objeto de dibujo para manipular la imagen
            draw = ImageDraw.Draw(img)
            # Escalar el tamaño según la configuración DPI del sistema
            # Ejemplo: en pantalla de alta densidad podría ser [22, 22]
            size = self.scale_size([11, 11])

            # Dibujar líneas que forman una flecha hacia arriba
            # Cada draw.line([x1, y1, x2, y2], fill=color) dibuja una línea con el color especificado
            draw.line([2, 6, 2, 9], fill=color)  # Vertical izquierda
            draw.line([3, 5, 3, 8], fill=color)  # Vertical izquierda-centro
            draw.line([4, 4, 4, 7], fill=color)  # Vertical centro-izquierda
            draw.line([5, 3, 5, 6], fill=color)  # Vertical centro
            draw.line([6, 4, 6, 7], fill=color)  # Vertical centro-derecha
            draw.line([7, 5, 7, 8], fill=color)  # Vertical derecha-centro
            draw.line([8, 6, 8, 9], fill=color)  # Vertical derecha

            # Redimensionar la imagen al tamaño escalado usando interpolación bicúbica
            img = img.resize(size, Image.BICUBIC)

            # --- Crear y almacenar las cuatro direcciones de flechas ---

            # 1. Flecha hacia arriba (imagen original)
            up_img = ImageTk.PhotoImage(img)
            up_name = util.get_image_name(up_img)  # Genera un nombre único (ej: "arrow_up_ff5733")
            self.theme_images[up_name] = up_img  # Almacena en caché para evitar garbage collection

            # 2. Flecha hacia abajo (rotar 180°)
            down_img = ImageTk.PhotoImage(img.rotate(180))
            down_name = util.get_image_name(down_img)
            self.theme_images[down_name] = down_img

            # 3. Flecha hacia la izquierda (rotar 90°)
            left_img = ImageTk.PhotoImage(img.rotate(90))
            left_name = util.get_image_name(left_img)
            self.theme_images[left_name] = left_img

            # 4. Flecha hacia la derecha (rotar -90°)
            right_img = ImageTk.PhotoImage(img.rotate(-90))
            right_name = util.get_image_name(right_img)
            self.theme_images[right_name] = right_img

            # Retornar los nombres/referencias de las cuatro imágenes
            return up_name, down_name, left_name, right_name

        # Generar flechas para cada estado usando el color correspondiente
        normal_names = draw_arrow(arrowcolor)  # Estado normal
        pressed_names = draw_arrow(pressed)  # Estado presionado
        active_names = draw_arrow(active)  # Estado activo/hover

        # Retornar tupla con las tres tuplas de nombres de imágenes
        # Ejemplo: (("arrow_up_normal", "arrow_down_normal", ...), ("arrow_up_pressed", ...), ...)
        return normal_names, pressed_names, active_names

    def create_round_scrollbar_assets(self, thumbcolor, pressed, active):
        """Crea activos de imagen para barras de desplazamiento redondeadas.

        Este método genera imágenes para los thumbs (controles deslizantes) de las barras de
        desplazamiento con esquinas redondeadas, tanto en orientación horizontal como vertical,
        y en tres estados diferentes: normal, presionado y activo/hover. Las imágenes generadas
        se almacenan en el diccionario `theme_images` para su uso posterior.

        La generación de imágenes utiliza una técnica de sobremuestreo (10x) y posterior
        redimensionado para asegurar bordes suaves y una alta calidad visual en las esquinas
        redondeadas.

        Args:
            thumbcolor (str):
                El valor de color para el thumb en estado normal.

            pressed (str):
                El valor de color a utilizar cuando el thumb está presionado.

            active (str):
                El valor de color a utilizar cuando el thumb está activo o
                con el cursor encima (hover).

        Returns:
            tuple[str, str, str, str, str, str]: Una tupla con seis elementos, que son los
            identificadores únicos de las imágenes generadas en el siguiente orden:
            1. Thumb horizontal en estado normal
            2. Thumb horizontal en estado presionado
            3. Thumb horizontal en estado activo
            4. Thumb vertical en estado normal
            5. Thumb vertical en estado presionado
            6. Thumb vertical en estado activo

        """
        # Definir tamaños escalados para thumbs verticales y horizontales
        # ajustados según la configuración DPI del sistema
        vsize = self.scale_size([9, 28])  # Tamaño para orientación vertical (ancho x alto)
        hsize = self.scale_size([28, 9])  # Tamaño para orientación horizontal (ancho x alto)

        def rounded_rect(size: list[int], fill: str) -> str:
            """Crea un rectángulo redondeado y devuelve su identificador.

            Args:
                size: Dimensiones finales [ancho, alto] de la imagen.
                fill: Color de relleno del rectángulo.

            Returns:
                Identificador único de la imagen creada.
            """
            # Ampliar tamaño por factor de 10 para mejor calidad
            # Ejemplo: [28, 9] -> [280, 90]
            x = size[0] * 10
            y = size[1] * 10

            # Crear imagen base transparente con tamaño ampliado
            img = Image.new("RGBA", (x, y))
            draw = ImageDraw.Draw(img)

            # Calcular radio para las esquinas redondeadas (mitad de la dimensión menor)
            # Ejemplo: para [280, 90], radio = 45
            radius = min([x, y]) // 2

            # Dibujar rectángulo redondeado con el color especificado
            # Las coordenadas [0, 0, x-1, y-1] abarcan toda la imagen menos el borde extremo
            draw.rounded_rectangle([0, 0, x - 1, y - 1], radius, fill)

            # Redimensionar a tamaño final y convertir a formato Tkinter
            # Usar interpolación bicúbica para mantener bordes suaves
            image = ImageTk.PhotoImage(img.resize(size, Image.BICUBIC))

            # Generar nombre único para la imagen y almacenarla en el diccionario
            name = util.get_image_name(image)
            self.theme_images[name] = image  # Mantiene referencia para evitar garbage collection

            return name  # Devolver el identificador único

        # --- Generar imágenes para thumbs horizontales en tres estados ---

        # Thumb horizontal en estado normal
        h_normal_img = rounded_rect(hsize, thumbcolor)
        # Thumb horizontal en estado presionado
        h_pressed_img = rounded_rect(hsize, pressed)
        # Thumb horizontal en estado activo/hover
        h_active_img = rounded_rect(hsize, active)

        # --- Generar imágenes para thumbs verticales en tres estados ---

        # Thumb vertical en estado normal
        v_normal_img = rounded_rect(vsize, thumbcolor)
        # Thumb vertical en estado presionado
        v_pressed_img = rounded_rect(vsize, pressed)
        # Thumb vertical en estado activo/hover
        v_active_img = rounded_rect(vsize, active)

        # Retornar tupla con los seis identificadores de imágenes
        # Orden: horizontal (normal, presionado, activo), vertical (normal, presionado, activo)
        return (
            h_normal_img,  # Horizontal normal
            h_pressed_img,  # Horizontal presionado
            h_active_img,  # Horizontal activo
            v_normal_img,  # Vertical normal
            v_pressed_img,  # Vertical presionado
            v_active_img,  # Vertical activo
        )

    def create_round_scrollbar_style(self, colorname=DEFAULT):
        """Crea un estilo redondeado para el widget ttk.Scrollbar.

        Este método configura estilos personalizados tanto para barras de desplazamiento
        horizontales como verticales con una apariencia redondeada. Genera todos los
        recursos visuales necesarios y define la estructura y comportamiento de los widgets.

        El estilo creado adapta automáticamente los colores según el tema actual (claro u
        oscuro) y la etiqueta de color proporcionada, generando diferentes versiones para
        los estados normal, presionado y activo (hover).

        Args:
            colorname (str, optional):
                La etiqueta de color utilizada para estilizar el widget. Si es DEFAULT o
                cadena vacía, se utiliza un estilo base sin prefijo de color.
                Los valores posibles incluyen: 'primary', 'secondary', 'success', 'info',
                'warning', 'danger', 'light', 'dark', etc.
                Valor predeterminado: DEFAULT.

        Returns:
            None: Este método no retorna ningún valor, pero modifica el estado interno
                  creando y registrando dos estilos TTK nuevos (horizontal y vertical).

        """
        # Constante que define el sufijo base para estilos de scrollbar
        STYLE = "TScrollbar"

        # --- Determinación de nombres de estilo y color base ---

        # Caso 1: Sin color específico (estilo base)
        if any([colorname == DEFAULT, colorname == ""]):
            # Nombres de estilo sin prefijo de color
            h_ttkstyle = f"Round.Horizontal.{STYLE}"  # Ej: "Round.Horizontal.TScrollbar"
            v_ttkstyle = f"Round.Vertical.{STYLE}"  # Ej: "Round.Vertical.TScrollbar"

            # Color de fondo adaptado al tipo de tema
            if self.is_light_theme:
                background = self.colors.border  # Color de borde en tema claro
            else:
                background = self.colors.selectbg  # Color de selección en tema oscuro

        # Caso 2: Color específico proporcionado
        else:
            # Nombres de estilo con prefijo de color
            h_ttkstyle = f"{colorname}.Round.Horizontal.{STYLE}"  # Ej: "primary.Round.Horizontal.TScrollbar"
            v_ttkstyle = f"{colorname}.Round.Vertical.{STYLE}"  # Ej: "primary.Round.Vertical.TScrollbar"

            # Obtener color dinámicamente según la etiqueta proporcionada
            background = self.colors.get(colorname)  # Ej: self.colors.primary, self.colors.success, etc.

        # --- Cálculo de colores específicos para diferentes partes y estados ---

        # Color del canal (troughcolor) adaptado al tipo de tema
        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg  # Fondo normal para tema "light" en tema claro
            else:
                troughcolor = self.colors.light  # Color claro para otros temas en tema claro
        else:
            # Para tema oscuro, versión más oscura del color de selección
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)  # Reduce brillo en 20%

        # Colores para estados específicos
        pressed = Colors.update_hsv(background, vd=-0.05)  # Versión más oscura para estado presionado
        active = Colors.update_hsv(background, vd=0.05)  # Versión más clara para estado activo/hover

        # --- Generación de imágenes para los thumbs ---

        # Obtener imágenes para todos los estados y orientaciones
        scroll_images = self.create_round_scrollbar_assets(
            background, pressed, active
        )
        # scroll_images contiene 6 identificadores:
        # 0: thumb horizontal normal, 1: h-presionado, 2: h-activo,
        # 3: thumb vertical normal, 4: v-presionado, 5: v-activo

        # === CONFIGURACIÓN DE BARRA DE DESPLAZAMIENTO HORIZONTAL ===

        # 1. Configuración básica de apariencia
        self.style._build_configure(
            h_ttkstyle,
            troughcolor=troughcolor,  # Color del canal
            darkcolor=troughcolor,  # Color oscuro (sombra)
            bordercolor=troughcolor,  # Color del borde
            lightcolor=troughcolor,  # Color claro (iluminación)
            arrowcolor=background,  # Color de las flechas
            arrowsize=self.scale_size(11),  # Tamaño de flecha escalado según DPI
            background=troughcolor,  # Color de fondo
            relief=tk.FLAT,  # Sin relieve
            borderwidth=0,  # Sin borde
        )

        # 2. Creación del elemento thumb personalizado
        self.style.element_create(
            f"{h_ttkstyle}.thumb",  # Nombre único del elemento
            "image",  # Tipo de elemento (basado en imagen)
            scroll_images[0],  # Imagen para estado normal
            ("pressed", scroll_images[1]),  # Imagen para estado presionado
            ("active", scroll_images[2]),  # Imagen para estado activo/hover
            border=self.scale_size(9),  # Tamaño de borde escalado
            padding=0,  # Sin relleno
            sticky=tk.EW,  # Adherencia este-oeste
        )

        # 3. Definición del layout (estructura jerárquica)
        self.style.layout(
            h_ttkstyle,
            [
                (
                    "Horizontal.Scrollbar.trough",  # Canal principal
                    {
                        "sticky": "we",  # Adherencia oeste-este
                        "children": [
                            (
                                "Horizontal.Scrollbar.leftarrow",  # Flecha izquierda
                                {"side": "left", "sticky": ""},
                            ),
                            (
                                "Horizontal.Scrollbar.rightarrow",  # Flecha derecha
                                {"side": "right", "sticky": ""},
                            ),
                            (
                                f"{h_ttkstyle}.thumb",  # Thumb personalizado
                                {"expand": "1", "sticky": "nswe"},  # Expandible, adherencia completa
                            ),
                        ],
                    },
                )
            ],
        )

        # 4. Configuración de colores de flecha
        self.style._build_configure(h_ttkstyle, arrowcolor=background)  # Color base
        self.style.map(
            h_ttkstyle,
            arrowcolor=[("pressed", pressed), ("active", active)]  # Mapeo de estados
        )

        # === CONFIGURACIÓN DE BARRA DE DESPLAZAMIENTO VERTICAL ===

        # 1. Configuración básica de apariencia (similar a horizontal)
        self.style._build_configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
        )

        # 2. Creación del elemento thumb personalizado
        self.style.element_create(
            f"{v_ttkstyle}.thumb",
            "image",
            scroll_images[3],  # Imagen vertical normal (#3 en la tupla)
            ("pressed", scroll_images[4]),  # Vertical presionado (#4)
            ("active", scroll_images[5]),  # Vertical activo (#5)
            border=self.scale_size(9),
            padding=0,
            sticky=tk.NS,  # Adherencia norte-sur
        )

        # 3. Definición del layout
        self.style.layout(
            v_ttkstyle,
            [
                (
                    "Vertical.Scrollbar.trough",  # Canal vertical
                    {
                        "sticky": "ns",  # Adherencia norte-sur
                        "children": [
                            (
                                "Vertical.Scrollbar.uparrow",  # Flecha arriba
                                {"side": "top", "sticky": ""},
                            ),
                            (
                                "Vertical.Scrollbar.downarrow",  # Flecha abajo
                                {"side": "bottom", "sticky": ""},
                            ),
                            (
                                f"{v_ttkstyle}.thumb",  # Thumb personalizado
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        )

        # 4. Configuración de colores de flecha
        self.style._build_configure(v_ttkstyle, arrowcolor=background)
        self.style.map(
            v_ttkstyle,
            arrowcolor=[("pressed", pressed), ("active", active)]
        )

        # --- Registro de estilos creados ---

        # Registrar los estilos TTK para evitar recreación y seguimiento
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_scrollbar_assets(self, thumbcolor, pressed, active):
        """Crea los activos de imagen utilizados para construir el estilo estándar de barra de desplazamiento.

        Este método genera imágenes rectangulares para los thumbs (controles deslizantes) de las barras
        de desplazamiento estándar, tanto en orientación horizontal como vertical, y en tres estados
        diferentes: normal, presionado y activo/hover. Las imágenes generadas se almacenan en el
        diccionario `theme_images` para su uso posterior.

        La generación de imágenes utiliza una técnica de sobremuestreo (10x) y posterior redimensionado
        para asegurar una alta calidad visual en los bordes.

        Args:
            thumbcolor (str):
                El color primario utilizado para colorear el thumb en estado normal.

            pressed (str):
                El color a utilizar cuando el thumb está presionado.

            active (str):
                El color a utilizar cuando el thumb está activo o con el cursor encima (hover).

        Returns:
            tuple[str, str, str, str, str, str]: Una tupla con seis elementos, que son los
            identificadores únicos de las imágenes generadas en el siguiente orden:
            1. Thumb horizontal en estado normal
            2. Thumb horizontal en estado presionado
            3. Thumb horizontal en estado activo
            4. Thumb vertical en estado normal
            5. Thumb vertical en estado presionado
            6. Thumb vertical en estado activo

        """
        # Definir tamaños escalados para thumbs verticales y horizontales
        # ajustados según la configuración DPI del sistema
        vsize = self.scale_size([9, 28])  # Tamaño para orientación vertical (ancho x alto)
        hsize = self.scale_size([28, 9])  # Tamaño para orientación horizontal (ancho x alto)

        def draw_rect(size: list[int], fill: str) -> str:
            """Crea un rectángulo sólido y devuelve su identificador.

            Args:
                size: Dimensiones finales [ancho, alto] de la imagen.
                fill: Color de relleno del rectángulo.

            Returns:
                Identificador único de la imagen creada.
            """
            # Ampliar tamaño por factor de 10 para mejor calidad
            # Ejemplo: [28, 9] -> [280, 90]
            x = size[0] * 10
            y = size[1] * 10

            # Crear imagen directamente con el color de relleno especificado
            # A diferencia del método para scrollbars redondeados, aquí no necesitamos
            # dibujar formas adicionales
            img = Image.new("RGBA", (x, y), fill)

            # Redimensionar a tamaño final y convertir a formato Tkinter
            # Usar interpolación bicúbica para mantener bordes suaves
            # NOTA: Hay un error sintáctico en el código original, el parámetro Image.BICUBIC
            # debería ser parte del método resize, no un argumento separado
            image = ImageTk.PhotoImage(img.resize(size, Image.BICUBIC))

            # Generar nombre único para la imagen y almacenarla en el diccionario
            name = util.get_image_name(image)
            self.theme_images[name] = image  # Mantiene referencia para evitar garbage collection

            return name  # Devolver el identificador único

        # --- Generar imágenes para thumbs horizontales en tres estados ---

        # Thumb horizontal en estado normal
        h_normal_img = draw_rect(hsize, thumbcolor)
        # Thumb horizontal en estado presionado
        h_pressed_img = draw_rect(hsize, pressed)
        # Thumb horizontal en estado activo/hover
        h_active_img = draw_rect(hsize, active)

        # --- Generar imágenes para thumbs verticales en tres estados ---

        # Thumb vertical en estado normal
        v_normal_img = draw_rect(vsize, thumbcolor)
        # Thumb vertical en estado presionado
        v_pressed_img = draw_rect(vsize, pressed)
        # Thumb vertical en estado activo/hover
        v_active_img = draw_rect(vsize, active)

        # Retornar tupla con los seis identificadores de imágenes
        # Orden: horizontal (normal, presionado, activo), vertical (normal, presionado, activo)
        return (
            h_normal_img,  # Horizontal normal
            h_pressed_img,  # Horizontal presionado
            h_active_img,  # Horizontal activo
            v_normal_img,  # Vertical normal
            v_pressed_img,  # Vertical presionado
            v_active_img,  # Vertical activo
        )

    def create_scrollbar_style(self, colorname=DEFAULT):
        """Crea un estilo estándar (rectangular) para el widget ttk.Scrollbar.

        Este método configura estilos personalizados tanto para barras de desplazamiento
        horizontales como verticales con una apariencia rectangular estándar. Genera todos los
        recursos visuales necesarios y define la estructura y comportamiento de los widgets.

        El estilo creado adapta automáticamente los colores según el tema actual (claro u
        oscuro) y la etiqueta de color proporcionada, generando diferentes versiones para
        los estados normal, presionado y activo (hover).

        Args:
            colorname (str, optional):
                La etiqueta de color utilizada para estilizar el widget. Si es DEFAULT o
                cadena vacía, se utiliza un estilo base sin prefijo de color.
                Los valores posibles incluyen: 'primary', 'secondary', 'success', 'info',
                'warning', 'danger', 'light', 'dark', etc.
                Valor predeterminado: DEFAULT.

        Returns:
            None: Este método no retorna ningún valor, pero modifica el estado interno
                  creando y registrando dos estilos TTK nuevos (horizontal y vertical).

        Notas:
            Para barras de desplazamiento con esquinas redondeadas, utilice
            `create_round_scrollbar_style()` en su lugar.
        """
        # Constante que define el sufijo base para estilos de scrollbar
        STYLE = "TScrollbar"

        # --- Determinación de nombres de estilo y color base ---

        # Caso 1: Sin color específico (estilo base)
        if any([colorname == DEFAULT, colorname == ""]):
            # Nombres de estilo sin prefijo de color
            h_ttkstyle = f"Horizontal.{STYLE}"  # Ej: "Horizontal.TScrollbar"
            v_ttkstyle = f"Vertical.{STYLE}"  # Ej: "Vertical.TScrollbar"

            # Color de fondo adaptado al tipo de tema
            if self.is_light_theme:
                background = self.colors.border  # Color de borde en tema claro
            else:
                background = self.colors.selectbg  # Color de selección en tema oscuro

        # Caso 2: Color específico proporcionado
        else:
            # Nombres de estilo con prefijo de color
            h_ttkstyle = f"{colorname}.Horizontal.{STYLE}"  # Ej: "primary.Horizontal.TScrollbar"
            v_ttkstyle = f"{colorname}.Vertical.{STYLE}"  # Ej: "primary.Vertical.TScrollbar"

            # Obtener color dinámicamente según la etiqueta proporcionada
            background = self.colors.get(colorname)  # Ej: self.colors.primary, self.colors.success, etc.

        # --- Cálculo de colores específicos para diferentes partes y estados ---

        # Color del canal (troughcolor) adaptado al tipo de tema
        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg  # Fondo normal para tema "light" en tema claro
            else:
                troughcolor = self.colors.light  # Color claro para otros temas en tema claro
        else:
            # Para tema oscuro, versión más oscura del color de selección
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)  # Reduce brillo en 20%

        # Colores para estados específicos
        pressed = Colors.update_hsv(background, vd=-0.05)  # Versión más oscura para estado presionado
        active = Colors.update_hsv(background, vd=0.05)  # Versión más clara para estado activo/hover

        # --- Generación de imágenes para los thumbs ---

        # Obtener imágenes para todos los estados y orientaciones
        scroll_images = self.create_scrollbar_assets(
            background, pressed, active
        )
        # scroll_images contiene 6 identificadores:
        # 0: thumb horizontal normal, 1: h-presionado, 2: h-activo,
        # 3: thumb vertical normal, 4: v-presionado, 5: v-activo

        # === CONFIGURACIÓN DE BARRA DE DESPLAZAMIENTO HORIZONTAL ===

        # 1. Configuración básica de apariencia
        self.style._build_configure(
            h_ttkstyle,
            troughcolor=troughcolor,  # Color del canal
            darkcolor=troughcolor,  # Color oscuro (sombra)
            bordercolor=troughcolor,  # Color del borde
            lightcolor=troughcolor,  # Color claro (iluminación)
            arrowcolor=background,  # Color de las flechas
            arrowsize=self.scale_size(11),  # Tamaño de flecha escalado según DPI
            background=troughcolor,  # Color de fondo
            relief=tk.FLAT,  # Sin relieve
            borderwidth=0,  # Sin borde
        )

        # 2. Creación del elemento thumb personalizado
        self.style.element_create(
            f"{h_ttkstyle}.thumb",  # Nombre único del elemento
            "image",  # Tipo de elemento (basado en imagen)
            scroll_images[0],  # Imagen para estado normal
            ("pressed", scroll_images[1]),  # Imagen para estado presionado
            ("active", scroll_images[2]),  # Imagen para estado activo/hover
            border=(3, 0),  # Borde horizontal (3px) pero no vertical
            sticky=tk.NSEW,  # Adherencia completa (norte-sur-este-oeste)
        )

        # 3. Definición del layout (estructura jerárquica)
        self.style.layout(
            h_ttkstyle,
            [
                (
                    "Horizontal.Scrollbar.trough",  # Canal principal
                    {
                        "sticky": "we",  # Adherencia oeste-este
                        "children": [
                            (
                                "Horizontal.Scrollbar.leftarrow",  # Flecha izquierda
                                {"side": "left", "sticky": ""},
                            ),
                            (
                                "Horizontal.Scrollbar.rightarrow",  # Flecha derecha
                                {"side": "right", "sticky": ""},
                            ),
                            (
                                f"{h_ttkstyle}.thumb",  # Thumb personalizado
                                {"expand": "1", "sticky": "nswe"},  # Expandible, adherencia completa
                            ),
                        ],
                    },
                )
            ],
        )

        # 4. Configuración de colores de flecha
        self.style._build_configure(h_ttkstyle, arrowcolor=background)  # Color base
        self.style.map(
            h_ttkstyle,
            arrowcolor=[("pressed", pressed), ("active", active)]  # Mapeo de estados
        )

        # === CONFIGURACIÓN DE BARRA DE DESPLAZAMIENTO VERTICAL ===

        # 1. Configuración básica de apariencia (similar a horizontal)
        self.style._build_configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
            borderwidth=0,
        )

        # 2. Creación del elemento thumb personalizado
        self.style.element_create(
            f"{v_ttkstyle}.thumb",
            "image",
            scroll_images[3],  # Imagen vertical normal (#3 en la tupla)
            ("pressed", scroll_images[4]),  # Vertical presionado (#4)
            ("active", scroll_images[5]),  # Vertical activo (#5)
            border=(0, 3),  # Borde vertical (3px) pero no horizontal
            sticky=tk.NSEW,  # Adherencia completa
        )

        # 3. Definición del layout
        self.style.layout(
            v_ttkstyle,
            [
                (
                    "Vertical.Scrollbar.trough",  # Canal vertical
                    {
                        "sticky": "ns",  # Adherencia norte-sur
                        "children": [
                            (
                                "Vertical.Scrollbar.uparrow",  # Flecha arriba
                                {"side": "top", "sticky": ""},
                            ),
                            (
                                "Vertical.Scrollbar.downarrow",  # Flecha abajo
                                {"side": "bottom", "sticky": ""},
                            ),
                            (
                                f"{v_ttkstyle}.thumb",  # Thumb personalizado
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        )

        # 4. Configuración de colores de flecha
        self.style._build_configure(v_ttkstyle, arrowcolor=background)
        self.style.map(
            v_ttkstyle,
            arrowcolor=[("pressed", pressed), ("active", active)]
        )

        # --- Registro de estilos creados ---

        # Registrar los estilos TTK para evitar recreación y seguimiento
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_spinbox_style(self, colorname=DEFAULT):
        """Crea un estilo personalizado para el widget ttk.Spinbox.

        Este método configura la apariencia y comportamiento del widget Spinbox según el
        tema actual (claro u oscuro) y el color especificado. Maneja varios estados del
        widget, incluyendo: normal, enfocado, hover, presionado, deshabilitado, inválido
        y solo lectura, adaptando la apariencia para cada situación.

        El método crea elementos personalizados para las flechas arriba/abajo y define
        un layout completo para el widget, controlando la ubicación y comportamiento
        de cada componente.

        Args:
            colorname (str, optional):
                La etiqueta de color utilizada para estilizar el widget. Si es DEFAULT o
                cadena vacía, se utiliza un estilo base sin prefijo de color.
                Los valores posibles incluyen: 'primary', 'secondary', 'success', 'info',
                'warning', 'danger', 'light', 'dark', etc.
                Valor predeterminado: DEFAULT.

        Returns:
            None: Este método no retorna ningún valor, pero modifica el estado interno
                  creando y registrando un estilo TTK nuevo para el widget Spinbox.

        """
        STYLE = "TSpinbox"  # Constante que define el nombre base del estilo

        # --- Definir colores base según el tema actual ---
        if self.is_light_theme:
            # En tema claro, usar colores más suaves
            disabled_fg = self.colors.border  # Ej: "#E0E0E0" - color gris claro
            bordercolor = self.colors.border  # Mismo color para bordes
            readonly = self.colors.light  # Ej: "#F5F5F5" - color gris muy claro
        else:
            # En tema oscuro, usar colores más oscuros
            disabled_fg = self.colors.selectbg  # Ej: "#555555" - color gris oscuro
            bordercolor = self.colors.selectbg  # Mismo color para bordes
            readonly = bordercolor  # Mismo color para modo readonly

        # --- Determinar nombre de estilo y color de enfoque según el parámetro ---
        if any([colorname == DEFAULT, colorname == ""]):
            # Sin color específico - usar estilo base
            ttkstyle = STYLE  # Resultado: "TSpinbox"
            focuscolor = self.colors.primary  # Ej: "#007BFF" - azul primario
        else:
            # Con color específico - crear estilo con prefijo
            ttkstyle = f"{colorname}.{STYLE}"  # Resultado: "primary.TSpinbox"
            focuscolor = self.colors.get(colorname)  # Ej: self.colors.success = "#28A745"

        # Ajustar color de borde cuando se especifica un color personalizado
        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor  # Usar el mismo color para el borde

        # --- Determinar color de flecha en estados interactivos ---
        if colorname == "light":
            # Caso especial: tema "light" necesita mejor contraste para las flechas
            arrowfocus = self.colors.fg  # Usar color de texto normal (más oscuro)
        else:
            # Otros temas: usar el color de enfoque para las flechas
            arrowfocus = focuscolor

        # --- Crear elementos personalizados para las flechas ---
        # Transformar nombre de estilo para elementos (ej: "primary.TSpinbox" -> "primary.Spinbox")
        element = ttkstyle.replace(".TS", ".S")

        # Crear elementos de flecha basados en el estilo predeterminado de TTK
        self.style.element_create(f"{element}.uparrow", "from", TTK_DEFAULT)  # Flecha arriba
        self.style.element_create(f"{element}.downarrow", "from", TTK_DEFAULT)  # Flecha abajo

        # --- Definir layout (estructura jerárquica del widget) ---
        self.style.layout(
            ttkstyle,
            [
                (
                    f"{element}.field",  # Campo principal contenedor
                    {
                        "side": tk.TOP,
                        "sticky": tk.EW,  # Adherir a este-oeste (expandir horizontalmente)
                        "children": [
                            (
                                "null",  # Contenedor para las flechas (sin nombre específico)
                                {
                                    "side": tk.RIGHT,  # Ubicar a la derecha
                                    "sticky": "",  # Sin adherencia específica
                                    "children": [
                                        # Flecha arriba en la parte superior del contenedor
                                        (
                                            f"{element}.uparrow",
                                            {"side": tk.TOP, "sticky": tk.E},  # Adherir al este
                                        ),
                                        # Flecha abajo en la parte inferior del contenedor
                                        (
                                            f"{element}.downarrow",
                                            {"side": tk.BOTTOM, "sticky": tk.E},  # Adherir al este
                                        ),
                                    ],
                                },
                            ),
                            (
                                f"{element}.padding",  # Área con padding para el contenido
                                {
                                    "sticky": tk.NSEW,  # Adherir a todos los lados
                                    "children": [
                                        # Área de texto (donde se muestra el valor)
                                        (
                                            f"{element}.textarea",
                                            {"sticky": tk.NSEW},  # Expandir en todas direcciones
                                        )
                                    ],
                                },
                            ),
                        ],
                    },
                )
            ],
        )

        # --- Configurar propiedades básicas del estilo ---
        self.style._build_configure(
            ttkstyle,
            # Colores del widget
            bordercolor=bordercolor,  # Color del borde
            darkcolor=self.colors.inputbg,  # Color para sombras/oscurecimiento
            lightcolor=self.colors.inputbg,  # Color para iluminación/resaltado
            fieldbackground=self.colors.inputbg,  # Color de fondo del campo de entrada
            foreground=self.colors.inputfg,  # Color del texto
            borderwidth=0,  # Sin borde visible (0 píxeles)
            background=self.colors.inputbg,  # Color de fondo general
            relief=tk.FLAT,  # Sin relieve (plano)
            arrowcolor=self.colors.inputfg,  # Color de las flechas
            insertcolor=self.colors.inputfg,  # Color del cursor de inserción
            arrowsize=self.scale_size(12),  # Tamaño de flecha (12px, escalado según DPI)
            padding=(10, 5),  # Padding horizontal y vertical
        )

        # --- Configurar mapeos de estado (cómo cambia la apariencia según el estado) ---
        self.style.map(
            ttkstyle,
            # Color del texto: cambia cuando está deshabilitado
            foreground=[
                ("disabled", disabled_fg)  # Ej: texto gris claro cuando deshabilitado
            ],

            # Color de fondo: cambia en modo solo lectura
            fieldbackground=[
                ("readonly", readonly)  # Ej: fondo gris claro en modo solo lectura
            ],
            background=[
                ("readonly", readonly)  # Consistente con fieldbackground
            ],

            # Colores de iluminación: cambian según el estado
            lightcolor=[
                # Color rojo cuando tiene foco y es inválido (ej: valor fuera de rango)
                ("focus invalid", self.colors.danger),
                # Color de énfasis cuando tiene foco (ej: azul primario)
                ("focus !disabled", focuscolor),
                # Color específico en modo solo lectura
                ("readonly", readonly),
            ],

            # Colores de sombreado: cambian según el estado (consistente con lightcolor)
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],

            # Color del borde: cambia según estado de validez e interacción
            bordercolor=[
                ("invalid", self.colors.danger),  # Rojo para valores inválidos
                ("focus !disabled", focuscolor),  # Color de énfasis cuando tiene foco
                ("hover !disabled", focuscolor),  # Mismo color al pasar el cursor
            ],

            # Color de las flechas: cambia según la interacción
            arrowcolor=[
                ("disabled !disabled", disabled_fg),  # Gris para estado deshabilitado
                ("pressed !disabled", arrowfocus),  # Color de énfasis cuando se presiona
                ("hover !disabled", arrowfocus),  # Mismo color al pasar el cursor
            ],
        )

        # --- Registrar el estilo creado ---
        # Esto evita recreación innecesaria y mantiene seguimiento de estilos disponibles
        self.style._register_ttkstyle(ttkstyle)

    def create_table_treeview_style(self, colorname=DEFAULT):
        """Crea un estilo personalizado para widgets Treeview (tablas).

        Este método configura la apariencia visual completa de widgets Treeview,
        adaptándose automáticamente al tipo de tema actual (claro u oscuro) y
        aplicando el esquema de colores especificado por 'colorname'. Define
        estilos tanto para el encabezado como para el cuerpo de la tabla,
        incluyendo efectos visuales para estados como hover, selección y
        deshabilitado.

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el widget. Pueden ser:
                - DEFAULT o "": Utiliza los colores de entrada predeterminados
                - LIGHT: En temas claros, aplica un estilo con fondo claro
                - Cualquier etiqueta de color definida: Aplica ese color como base

        Returns:
            None: El método no retorna valores, pero registra estilos TTK
                  que pueden ser utilizados por widgets Treeview.
        """
        # Identificador base para los estilos de Treeview
        STYLE = "Table.Treeview"

        # Obtiene la fuente predeterminada para calcular dimensiones
        f = font.nametofont("TkDefaultFont")
        # Calcula la altura de fila basada en el espacio de línea de la fuente
        # Ejemplo: si linespace=20, rowheight=20 píxeles
        rowheight = f.metrics()["linespace"]

        # Configura colores base según el tipo de tema (claro u oscuro)
        if self.is_light_theme:
            # Para tema claro: colores más suaves
            # Ejemplo: si inputbg="#FFFFFF", disabled_fg podría ser "#CCCCCC"
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
            # Ejemplo: si light="#F5F5F5", hover podría ser "#DADADA"
            hover = Colors.update_hsv(self.colors.light, vd=-0.1)
        else:
            # Para tema oscuro: colores con mayor contraste
            # Ejemplo: si inputbg="#303030", disabled_fg podría ser "#202020"
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg
            # Ejemplo: si dark="#202020", hover podría ser "#303030"
            hover = Colors.update_hsv(self.colors.dark, vd=0.1)

        # Determina esquema de colores y nombres de estilo según 'colorname'
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso 1: Usa valores predeterminados
            # Ejemplo: background="#FFFFFF", foreground="#000000"
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            # Nombres de estilo sin prefijo: "Table.Treeview", "Table.Treeview.Heading"
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
        elif colorname == LIGHT and self.is_light_theme:
            # Caso 2: Esquema claro en tema claro
            # Ejemplo: background="#F5F5F5", foreground="#333333"
            background = self.colors.get(colorname)
            foreground = self.colors.fg
            # Nombres con prefijo: "Light.Table.Treeview"
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            # Recalcula hover para este esquema
            hover = Colors.update_hsv(background, vd=-0.1)
        else:
            # Caso 3: Cualquier otro esquema o LIGHT en tema oscuro
            # Ejemplo si colorname=PRIMARY: background="#1E88E5", foreground="#FFFFFF"
            background = self.colors.get(colorname)
            foreground = self.colors.selectfg
            # Nombres con prefijo del color: "Primary.Table.Treeview"
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            # Aclara ligeramente para hover en colores más oscuros
            hover = Colors.update_hsv(background, vd=0.1)

        # Configura el estilo para el encabezado de la tabla
        self.style._build_configure(
            header_style,
            background=background,  # Color de fondo base
            foreground=foreground,  # Color de texto base
            relief=tk.RAISED,  # Relieve 3D tipo "elevado"
            borderwidth=1,  # Ancho del borde: 1 píxel
            darkcolor=background,  # Color para sombra en relieve
            bordercolor=bordercolor,  # Color específico para los bordes
            lightcolor=background,  # Color para iluminación en relieve
            padding=5,  # Espaciado interior: 5 píxeles
        )
        # Define cambios de estilo para estados específicos del encabezado
        self.style.map(
            header_style,
            # Texto gris cuando está deshabilitado
            foreground=[("disabled", disabled_fg)],
            # Cambia el fondo al hacer hover (si está habilitado)
            background=[
                ("active !disabled", hover),
            ],
            # Actualiza colores de sombreado al hacer hover
            darkcolor=[
                ("active !disabled", hover),
            ],
            lightcolor=[
                ("active !disabled", hover),
            ],
        )

        # Configura el estilo para el cuerpo de la tabla
        self.style._build_configure(
            body_style,
            background=self.colors.inputbg,  # Color de fondo general
            fieldbackground=self.colors.inputbg,  # Color de fondo de celdas
            foreground=self.colors.inputfg,  # Color de texto
            bordercolor=bordercolor,  # Color de bordes
            lightcolor=self.colors.inputbg,  # Color para iluminación
            darkcolor=self.colors.inputbg,  # Color para sombra
            borderwidth=2,  # Ancho del borde: 2 píxeles
            padding=0,  # Sin espaciado interior
            rowheight=rowheight,  # Altura calculada de las filas
            relief=tk.RAISED,  # Relieve 3D tipo "elevado"
        )
        # Define cambios de estilo para estados específicos del cuerpo
        self.style.map(
            body_style,
            # Cambia el fondo cuando una fila está seleccionada
            # Ejemplo: si normal es "#FFFFFF", seleccionado es "#1E88E5"
            background=[("selected", self.colors.selectbg)],
            foreground=[
                # Texto gris cuando está deshabilitado
                ("disabled", disabled_fg),
                # Color de texto contrastante para filas seleccionadas
                # Ejemplo: si normal es "#000000", seleccionado es "#FFFFFF"
                ("selected", self.colors.selectfg),
            ],
        )

        # Define la estructura visual (layout) para el widget
        self.style.layout(
            body_style,
            [
                (
                    # Contenedor exterior: borde tipo botón
                    "Button.border",
                    {
                        "sticky": tk.NSEW,  # Expandir en todas direcciones
                        "border": "1",  # Ancho del borde
                        "children": [
                            (
                                # Contenedor medio: área de padding
                                "Treeview.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            # Contenedor interior: área de contenido
                                            "Treeview.treearea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )
        # Registra el estilo en el sistema para hacerlo disponible
        # Esto permite usar "colorname.Table.Treeview" en widgets
        self.style._register_ttkstyle(body_style)

    def create_treeview_style(self, colorname=DEFAULT):
        """Crea un estilo personalizado para widgets ttk.Treeview estándar.

        Este método configura la apariencia visual completa de widgets Treeview,
        adaptándose al tema actual (claro u oscuro) y aplicando el esquema de
        colores especificado por 'colorname'. Define estilos tanto para el
        encabezado como para el cuerpo del Treeview, incluyendo comportamiento
        visual para distintos estados (selección, hover, foco, deshabilitado).

        También intenta mejorar los indicadores de expansión/colapso del árbol
        utilizando elementos visuales de un tema alternativo.

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el widget. Puede ser:
                - DEFAULT o "": Utiliza los colores de entrada predeterminados
                  con color primario para elementos de foco
                - LIGHT: En temas claros, aplica un estilo con fondo claro y
                  bordes sutiles
                - Cualquier etiqueta de color definida: Aplica ese color como base
                  para el estilo y elementos interactivos

        Returns:
            None: El método no retorna valores, pero registra estilos TTK
                  que pueden ser utilizados por widgets Treeview.

        """
        # Identificador base para los estilos de Treeview
        STYLE = "Treeview"

        # Obtiene la fuente predeterminada para calcular dimensiones apropiadas
        f = font.nametofont("TkDefaultFont")
        # Calcula la altura de fila basada en el espacio de línea de la fuente
        # Ejemplo: si linespace=20, rowheight=20 píxeles
        rowheight = f.metrics()["linespace"]

        # Configura colores base según el tipo de tema (claro u oscuro)
        if self.is_light_theme:
            # Para tema claro: colores más suaves
            # Ejemplo: si inputbg="#FFFFFF", disabled_fg podría ser "#CCCCCC"
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border  # Ej: "#E0E0E0" (gris claro)
        else:
            # Para tema oscuro: colores con mayor contraste
            # Ejemplo: si inputbg="#303030", disabled_fg podría ser "#202020"
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg  # Ej: "#1E88E5" (azul)

        # Determina esquema de colores y nombres de estilo según 'colorname'
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso DEFAULT: Usa valores predeterminados del tema
            background = self.colors.inputbg  # Ej: "#FFFFFF" (blanco)
            foreground = self.colors.inputfg  # Ej: "#000000" (negro)
            # Nombres sin prefijo: "Treeview", "Treeview.Heading"
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
            # Color primario para elementos con foco, Ej: "#1976D2" (azul)
            focuscolor = self.colors.primary
        elif colorname == LIGHT and self.is_light_theme:
            # Caso LIGHT en tema claro: Esquema muy claro
            # Ej: background="#F5F5F5" (blanco hueso)
            background = self.colors.get(colorname)
            foreground = self.colors.fg  # Ej: "#212121" (casi negro)
            # Nombres con prefijo "Light.": "Light.Treeview"
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            # Usa color de fondo también para foco y bordes (coherencia visual)
            focuscolor = background
            bordercolor = focuscolor
        else:
            # Otros casos: Usa el color específico como base
            # Ej. para PRIMARY: background="#1976D2" (azul)
            background = self.colors.get(colorname)
            # Asegura contraste, Ej: "#FFFFFF" (blanco)
            foreground = self.colors.selectfg
            # Nombres con prefijo según color: "Primary.Treeview"
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            # Usa color base para foco y bordes (refuerza identidad visual)
            focuscolor = background
            bordercolor = focuscolor

        # Configura el estilo para el encabezado del Treeview
        self.style._build_configure(
            header_style,
            background=background,  # Color de fondo base
            foreground=foreground,  # Color de texto base
            relief=tk.FLAT,  # Sin efecto 3D (plano)
            padding=5,  # Espaciado interno de 5 píxeles
        )
        # Define cambios de estilo para estados específicos del encabezado
        self.style.map(
            header_style,
            # Texto gris cuando está deshabilitado
            foreground=[("disabled", disabled_fg)],
            # Borde del mismo color que el fondo cuando tiene foco
            # Esto crea efecto de "fusión" visual
            bordercolor=[("focus !disabled", background)],
        )

        # Configura el estilo para el cuerpo del Treeview
        self.style._build_configure(
            body_style,
            background=self.colors.inputbg,  # Color de fondo general
            fieldbackground=self.colors.inputbg,  # Color de fondo de celdas
            foreground=self.colors.inputfg,  # Color de texto
            bordercolor=bordercolor,  # Color de bordes
            lightcolor=self.colors.inputbg,  # Color para iluminación
            darkcolor=self.colors.inputbg,  # Color para sombra
            borderwidth=2,  # Ancho del borde: 2 píxeles
            padding=0,  # Sin espaciado interior
            rowheight=rowheight,  # Altura calculada de filas
            relief=tk.RAISED,  # Efecto 3D elevado
        )
        # Define cambios de estilo para estados específicos del cuerpo
        self.style.map(
            body_style,
            # Cambia fondo cuando una fila está seleccionada
            # Ej: si normal "#FFFFFF", seleccionado "#1E88E5"
            background=[("selected", self.colors.selectbg)],
            foreground=[
                # Texto gris cuando está deshabilitado
                ("disabled", disabled_fg),
                # Color contrastante para texto en filas seleccionadas
                # Ej: si normal "#000000", seleccionado "#FFFFFF"
                ("selected", self.colors.selectfg),
            ],
            # Define colores de borde para diferentes estados interactivos
            bordercolor=[
                ("disabled", bordercolor),  # Estado deshabilitado
                ("focus", focuscolor),  # Tiene foco
                ("pressed", focuscolor),  # Está presionado
                ("hover", focuscolor),  # Mouse encima
            ],
            # Ajusta sombreado 3D cuando tiene foco
            lightcolor=[("focus", focuscolor)],
            darkcolor=[("focus", focuscolor)],
        )

        # Define la estructura visual (layout) para el widget
        self.style.layout(
            body_style,
            [
                (
                    # Contenedor exterior: borde tipo botón
                    "Button.border",
                    {
                        "sticky": tk.NSEW,  # Expandir en todas direcciones
                        "border": "1",  # Ancho del borde
                        "children": [
                            (
                                # Contenedor medio: área de padding
                                "Treeview.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            # Contenedor interior: área de contenido
                                            "Treeview.treearea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )

        # Intenta mejorar los indicadores de expansión/colapso del árbol
        # utilizando elementos visuales de un tema alternativo
        try:
            # Crea elemento personalizado tomado del tema alternativo
            # Esto suele proporcionar triángulos de expansión más atractivos
            self.style.element_create("Treeitem.indicator", "from", TTK_ALT)
        except:
            # Si falla (ej: tema alternativo no disponible), continúa sin error
            # Usará los indicadores predeterminados del tema actual
            pass

        # Registra el estilo en el sistema para hacerlo disponible
        # Esto permite usar identificadores como "Primary.Treeview" en widgets
        self.style._register_ttkstyle(body_style)

    def create_frame_style(self, colorname=DEFAULT):
        """Crea un estilo personalizado para widgets ttk.Frame.

        Este método define la apariencia básica de los widgets Frame, configurando
        principalmente el color de fondo según el esquema de color especificado.

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el widget. Puede ser:
                - DEFAULT o "": Utiliza el color de fondo predeterminado del tema
                - Cualquier etiqueta de color definida: Aplica ese color como fondo

        Returns:
            None: El método no retorna valores, pero registra un estilo TTK
                  que puede ser utilizado por widgets Frame.
        """
        # Identificador base para los estilos de Frame en TTK
        STYLE = "TFrame"

        # Determinar el nombre del estilo y color de fondo según colorname
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso DEFAULT: Usa el estilo base sin prefijo
            ttkstyle = STYLE  # Resultado: "TFrame"
            # Utiliza el color de fondo general del tema
            # Ejemplo: en tema claro podría ser "#FFFFFF" (blanco)
            background = self.colors.bg
        else:
            # Caso específico: Crea un nombre compuesto con prefijo
            # Ejemplo: si colorname=PRIMARY, resultado="Primary.TFrame"
            ttkstyle = f"{colorname}.{STYLE}"
            # Obtiene el color correspondiente a la etiqueta
            # Ejemplo: si colorname=PRIMARY, podría ser "#1976D2" (azul)
            background = self.colors.get(colorname)

        # Configura el estilo estableciendo solo el color de fondo
        # No configura otras propiedades como bordes, relieves, etc.
        self.style._build_configure(ttkstyle, background=background)

        # Registra el estilo en el sistema para que esté disponible
        self.style._register_ttkstyle(ttkstyle)

    def create_square_toggle_assets(self, colorname=DEFAULT):
        """Crea las imágenes (assets) necesarias para construir un estilo de
        interruptor (toggle) cuadrado.

        Este método genera cuatro imágenes distintas que representan los diferentes
        estados visuales de un interruptor tipo toggle:
        1. OFF: Interruptor apagado - indicador a la izquierda
        2. ON: Interruptor encendido - indicador a la derecha, colores activos
        3. Disabled: Interruptor deshabilitado (apagado) - apariencia inactiva
        4. ON Disabled: Interruptor encendido pero deshabilitado

        Las imágenes creadas se almacenan en self.theme_images y pueden ser
        utilizadas posteriormente para construir un estilo de interruptor visual.

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el widget. Puede ser:
                - DEFAULT o "": Utiliza el color PRIMARY del tema
                - LIGHT: Usa colores claros con ajustes específicos para contraste
                - DARK: Usa colores oscuros con ajustes específicos para contraste
                - Cualquier otra etiqueta de color definida en el tema

        Returns:
            Tuple[str, str, str, str]:
                Una tupla con los nombres de las cuatro imágenes creadas, en el
                siguiente orden: (off_name, on_name, disabled_name, on_disabled_name).
                Estos nombres son los identificadores para acceder a las imágenes
                almacenadas en self.theme_images.
        """
        # Cálculo del tamaño apropiado según la escala del sistema
        # Convierte dimensiones base [24, 15] al tamaño adecuado
        # Ej: en escala 2x podría ser [48, 30]
        size = self.scale_size([24, 15])

        # Si no se especifica color o es DEFAULT, usa PRIMARY
        # Ej: si PRIMARY="primary", usará ese color
        if any([colorname == DEFAULT, colorname == ""]):
            colorname = PRIMARY

        # Definición de colores base para los diferentes componentes

        # Color principal según la etiqueta especificada
        # Ej: para PRIMARY podría ser "#1976D2" (azul)
        prime_color = self.colors.get(colorname)

        # Color para el borde en estado activo (ON)
        on_border = prime_color

        # Color para el indicador (cuadrado interior) en estado ON
        # Normalmente color contrastante, ej: "#FFFFFF" (blanco)
        on_indicator = self.colors.selectfg

        # Color de fondo para estado ON (igual al color principal)
        on_fill = prime_color

        # Color de fondo para estado OFF (fondo del tema)
        # Ej: en tema claro, "#FFFFFF" (blanco)
        off_fill = self.colors.bg

        # Color semitransparente para elementos deshabilitados
        # 30% de transparencia del color de texto sobre fondo
        # Ej: si fg="#000000" y bg="#FFFFFF", resultaría "#B3B3B3" (gris)
        disabled_fg = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)

        # Color semitransparente para borde en estado OFF
        # 40% de transparencia, ej: "#999999" (gris más oscuro)
        off_border = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)

        # Color semitransparente para indicador en estado OFF
        off_indicator = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)

        # Ajustes específicos para colores especiales LIGHT y DARK
        if colorname == LIGHT:
            # Para color LIGHT (claro), usar color oscuro del tema
            # para asegurar contraste con fondo claro
            on_border = self.colors.dark  # Ej: "#212121" (casi negro)
            on_indicator = on_border  # Mismo color para el indicador
        elif colorname == DARK:
            # Para color DARK (oscuro), usar color claro del tema
            # para asegurar contraste con fondo oscuro
            on_border = self.colors.light  # Ej: "#F5F5F5" (casi blanco)
            on_indicator = on_border  # Mismo color para el indicador

        # IMAGEN 1: Estado OFF (apagado)
        # Creación de imagen base con canal alfa, tamaño grande para calidad
        _off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_off)
        # Rectángulo principal: borde semitransparente, fondo del tema
        draw.rectangle(
            xy=[1, 1, 225, 129], outline=off_border, width=6, fill=off_fill
        )
        # Indicador (cuadrado) en posición izquierda
        draw.rectangle([18, 18, 110, 110], fill=off_indicator)

        # Redimensionar al tamaño calculado con algoritmo de alta calidad
        off_img = ImageTk.PhotoImage(_off.resize(size, Image.LANCZOS))
        # Generar nombre único para la imagen
        off_name = util.get_image_name(off_img)
        # Almacenar la imagen en el diccionario
        self.theme_images[off_name] = off_img

        # IMAGEN 2: Estado ON (encendido)
        toggle_on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        # Rectángulo principal: borde y fondo del color principal
        draw.rectangle(
            xy=[1, 1, 225, 129], outline=on_border, width=6, fill=on_fill
        )
        # Indicador inicialmente en misma posición que OFF
        draw.rectangle([18, 18, 110, 110], fill=on_indicator)
        # Rotación 180° para mover indicador a la derecha
        _on = toggle_on.transpose(Image.ROTATE_180)
        # Procesamiento y almacenamiento similar al anterior
        on_img = ImageTk.PhotoImage(_on.resize(size, Image.LANCZOS))
        on_name = util.get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # IMAGEN 3: Estado Disabled (deshabilitado)
        _disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_disabled)
        # Rectángulo hueco (sin fill) con borde semitransparente
        draw.rectangle([1, 1, 225, 129], outline=disabled_fg, width=6)
        # Indicador en posición izquierda, color semitransparente
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)
        # Procesamiento y almacenamiento
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize(size, Image.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        # IMAGEN 4: Estado ON Disabled (encendido pero deshabilitado)
        toggle_on_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on_disabled)
        # Rectángulo con borde semitransparente y fondo neutro
        draw.rectangle(
            xy=[1, 1, 225, 129], outline=disabled_fg, width=6, fill=off_fill
        )
        # Indicador inicialmente en posición izquierda
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)
        # Rotación 180° para mover indicador a la derecha
        _on_disabled = toggle_on_disabled.transpose(Image.ROTATE_180)
        # Procesamiento y almacenamiento
        on_dis_img = ImageTk.PhotoImage(_on_disabled.resize(size, Image.LANCZOS))
        on_disabled_name = util.get_image_name(on_dis_img)
        self.theme_images[on_disabled_name] = on_dis_img

        # Retornar los nombres de las cuatro imágenes creadas
        # Estos nombres serán usados para acceder a las imágenes
        # almacenadas en self.theme_images
        return off_name, on_name, disabled_name, on_disabled_name

    def create_round_toggle_assets(self, colorname=DEFAULT):
        """Crea las imágenes (assets) necesarias para construir un estilo de
        interruptor (toggle) redondo.

        Este método genera cuatro imágenes distintas que representan los diferentes
        estados visuales de un interruptor tipo toggle con apariencia redondeada,
        similar a los controles de iOS o Android:
        1. OFF: Interruptor apagado - indicador circular a la izquierda
        2. ON: Interruptor encendido - indicador circular a la derecha, colores activos
        3. Disabled: Interruptor deshabilitado (apagado) - apariencia inactiva
        4. ON Disabled: Interruptor encendido pero deshabilitado

        Las imágenes creadas se almacenan en self.theme_images y pueden ser
        utilizadas posteriormente para construir un estilo de interruptor visual
        con apariencia redondeada y moderna.

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el widget. Puede ser:
                - DEFAULT o "": Utiliza el color PRIMARY del tema
                - LIGHT: Usa colores claros con ajustes específicos para contraste
                - DARK: Usa colores oscuros con ajustes específicos para contraste
                - Cualquier otra etiqueta de color definida en el tema

        Returns:
            Tuple[str, str, str, str]:
                Una tupla con los nombres de las cuatro imágenes creadas, en el
                siguiente orden: (off_name, on_name, disabled_name, on_disabled_name).
                Estos nombres son los identificadores para acceder a las imágenes
                almacenadas en self.theme_images.
        """
        # Cálculo del tamaño apropiado según la escala del sistema
        # Convierte dimensiones base [24, 15] al tamaño adecuado
        # Ej: en escala 2x podría ser [48, 30]
        size = self.scale_size([24, 15])

        # Si no se especifica color o es DEFAULT, usa PRIMARY
        # Ej: si PRIMARY="primary", usará ese color
        if any([colorname == DEFAULT, colorname == ""]):
            colorname = PRIMARY

        # Definición de colores base para los diferentes componentes

        # Color principal según la etiqueta especificada
        # Ej: para PRIMARY podría ser "#1976D2" (azul)
        prime_color = self.colors.get(colorname)

        # Color para el borde en estado activo (ON)
        on_border = prime_color

        # Color para el indicador (círculo interior) en estado ON
        # Normalmente color contrastante, ej: "#FFFFFF" (blanco)
        on_indicator = self.colors.selectfg

        # Color de fondo para estado ON (igual al color principal)
        on_fill = prime_color

        # Color de fondo para estado OFF (fondo del tema)
        # Ej: en tema claro, "#FFFFFF" (blanco)
        off_fill = self.colors.bg

        # Color semitransparente para elementos deshabilitados
        # 30% de transparencia del color de texto sobre fondo
        # Ej: si fg="#000000" y bg="#FFFFFF", resultaría "#B3B3B3" (gris)
        disabled_fg = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)

        # Color semitransparente para borde en estado OFF
        # 40% de transparencia, ej: "#999999" (gris más oscuro)
        off_border = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)

        # Color semitransparente para indicador en estado OFF
        off_indicator = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)

        # Ajustes específicos para colores especiales LIGHT y DARK
        if colorname == LIGHT:
            # Para color LIGHT (claro), usar color oscuro del tema
            # para asegurar contraste con fondo claro
            on_border = self.colors.dark  # Ej: "#212121" (casi negro)
            on_indicator = on_border  # Mismo color para el indicador
        elif colorname == DARK:
            # Para color DARK (oscuro), usar color claro del tema
            # para asegurar contraste con fondo oscuro
            on_border = self.colors.light  # Ej: "#F5F5F5" (casi blanco)
            on_indicator = on_border  # Mismo color para el indicador

        # IMAGEN 1: Estado OFF (apagado)
        # Creación de imagen base con canal alfa, tamaño grande para calidad
        _off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_off)
        # Rectángulo redondeado para el cuerpo principal
        # Radio grande (64px) crea forma casi ovalada
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=off_border,
            width=6,
            fill=off_fill,
        )
        # Indicador circular en posición izquierda
        draw.ellipse([20, 18, 112, 110], fill=off_indicator)

        # Redimensionar al tamaño calculado con algoritmo de alta calidad
        off_img = ImageTk.PhotoImage(_off.resize(size, Image.LANCZOS))
        # Generar nombre único para la imagen
        off_name = util.get_image_name(off_img)
        # Almacenar la imagen en el diccionario
        self.theme_images[off_name] = off_img

        # IMAGEN 2: Estado ON (encendido)
        _on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_on)
        # Rectángulo redondeado: borde y fondo del color principal
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=on_border,
            width=6,
            fill=on_fill,
        )
        # Indicador circular inicialmente en misma posición que OFF
        draw.ellipse([20, 18, 112, 110], fill=on_indicator)
        # Rotación 180° para mover indicador a la derecha
        _on = _on.transpose(Image.ROTATE_180)
        # Procesamiento y almacenamiento similar al anterior
        on_img = ImageTk.PhotoImage(_on.resize(size, Image.LANCZOS))
        on_name = util.get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # IMAGEN 3: Estado ON Disabled (encendido pero deshabilitado)
        _on_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_on_disabled)
        # Rectángulo redondeado con borde semitransparente y fondo neutro
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=disabled_fg,
            width=6,
            fill=off_fill,
        )
        # Indicador circular inicialmente en posición izquierda
        draw.ellipse([20, 18, 112, 110], fill=disabled_fg)
        # Rotación 180° para mover indicador a la derecha
        _on_disabled = _on_disabled.transpose(Image.ROTATE_180)
        # Procesamiento y almacenamiento
        on_dis_img = ImageTk.PhotoImage(_on_disabled.resize(size, Image.LANCZOS))
        on_disabled_name = util.get_image_name(on_dis_img)
        self.theme_images[on_disabled_name] = on_dis_img

        # IMAGEN 4: Estado Disabled (deshabilitado)
        _disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_disabled)
        # Rectángulo redondeado hueco (sin fill) con borde semitransparente
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129], radius=(128 / 2), outline=disabled_fg, width=6
        )
        # Indicador circular en posición izquierda, color semitransparente
        draw.ellipse([20, 18, 112, 110], fill=disabled_fg)
        # Procesamiento y almacenamiento
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize(size, Image.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        # Retornar los nombres de las cuatro imágenes creadas
        # Estos nombres serán usados para acceder a las imágenes
        # almacenadas en self.theme_images
        return off_name, on_name, disabled_name, on_disabled_name

    def create_round_toggle_style(self, colorname=DEFAULT):
        """Crea un estilo de interruptor redondo para widgets ttk.Checkbutton.

        Este método transforma la apariencia de un widget Checkbutton estándar
        en un interruptor con apariencia moderna y redondeada, similar a los
        controles de iOS o Android. Utiliza imágenes personalizadas generadas
        por create_round_toggle_assets() para representar los diferentes estados
        visuales (on/off/disabled).

        El estilo resultante mantiene la funcionalidad del Checkbutton pero con
        una representación visual completamente diferente: en lugar del tradicional
        cuadro de verificación, muestra un interruptor circular que se desliza
        entre posiciones izquierda (off) y derecha (on).

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el interruptor. Puede ser:
                - DEFAULT o "": Utiliza el color PRIMARY del tema
                - Cualquier etiqueta de color definida en el tema (ej: SUCCESS, WARNING)

        Returns:
            None: El método no retorna valores, pero registra un estilo TTK
                  que puede ser utilizado por widgets Checkbutton.

        """
        # Identificador base para este estilo
        STYLE = "Round.Toggle"

        # Color semitransparente para texto en estado deshabilitado
        # 30% de transparencia del color de texto sobre fondo
        # Ej: si fg="#000000" y bg="#FFFFFF", resultaría "#B3B3B3" (gris)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Determinar nombre del estilo y color a utilizar
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso DEFAULT: usar nombre base sin prefijo
            ttkstyle = STYLE  # Resultado: "Round.Toggle"
            # Usar color primario para las imágenes
            colorname = PRIMARY
        else:
            # Caso específico: crear nombre con prefijo del color
            # Ej: si colorname=SUCCESS, resultado="Success.Round.Toggle"
            ttkstyle = f"{colorname}.{STYLE}"

        # Obtener las imágenes para los diferentes estados del interruptor
        # Retorna tupla con 4 nombres: (off, on, disabled, on_disabled)
        images = self.create_round_toggle_assets(colorname)

        # Intentar crear un elemento personalizado para el indicador
        try:
            # Calcular dimensiones según escala del sistema
            # Ej: en escala 2x, width=56 y borderpad=8
            width = self.scale_size(28)  # Ancho del indicador
            borderpad = self.scale_size(4)  # Padding del borde

            # Crear elemento de imagen personalizado para el indicador
            self.style.element_create(
                f"{ttkstyle}.indicator",  # Nombre único del elemento
                "image",  # Tipo: basado en imágenes
                # Imagen predeterminada (estado ON)
                images[1],
                # Mapeo de imágenes según estados:
                ("disabled selected", images[3]),  # Deshabilitado + Seleccionado
                ("disabled", images[2]),  # Solo deshabilitado
                ("!selected", images[0]),  # No seleccionado (OFF)
                # Parámetros de configuración:
                width=width,  # Ancho del elemento
                border=borderpad,  # Padding alrededor del elemento
                sticky=tk.W,  # Alineación a la izquierda
            )
        except:
            # Capturar posibles errores si el elemento ya existe
            # Esto permite reutilizar el método sin fallos
            """This method is used as the default Toggle style, so it
            is neccessary to catch Tcl Errors when it tries to create
            and element that was already created by the Toggle or
            Round Toggle style"""
            pass

        # Configurar propiedades base del estilo
        self.style._build_configure(
            ttkstyle,
            relief=tk.FLAT,  # Sin efecto de relieve (plano)
            borderwidth=0,  # Sin borde visible
            padding=0,  # Sin espaciado interno
            foreground=self.colors.fg,  # Color de texto del tema
            background=self.colors.bg,  # Color de fondo del tema
        )

        # Definir cambios visuales para estados específicos
        self.style.map(
            ttkstyle,
            # Texto gris cuando está deshabilitado
            foreground=[("disabled", disabled_fg)],
            # Mantener color de fondo cuando está seleccionado
            background=[("selected", self.colors.bg)],
        )

        # Definir la estructura visual (layout) del widget
        self.style.layout(
            ttkstyle,
            [
                (
                    # Contenedor exterior: borde de Toolbutton
                    "Toolbutton.border",
                    {
                        "sticky": tk.NSEW,  # Expandir en todas direcciones
                        "children": [
                            (
                                # Contenedor medio: área de padding
                                "Toolbutton.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            # Indicador personalizado (interruptor)
                                            f"{ttkstyle}.indicator",
                                            {"side": tk.LEFT},  # Posición izquierda
                                        ),
                                        (
                                            # Etiqueta de texto
                                            "Toolbutton.label",
                                            {"side": tk.LEFT},  # A la derecha del indicador
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )

        # Registrar el estilo para hacerlo disponible
        # Ejemplo de uso: ttk.Checkbutton(parent, style="Primary.Round.Toggle")
        self.style._register_ttkstyle(ttkstyle)

    def create_square_toggle_style(self, colorname=DEFAULT):
        """Crea un estilo de interruptor cuadrado para widgets ttk.Checkbutton.

        Este método transforma la apariencia de un widget Checkbutton estándar
        en un interruptor con apariencia cuadrada moderna. Utiliza imágenes
        personalizadas generadas por create_square_toggle_assets() para representar
        los diferentes estados visuales (on/off/disabled).

        El estilo resultante mantiene la funcionalidad del Checkbutton pero con
        una representación visual completamente diferente: en lugar del tradicional
        cuadro de verificación, muestra un interruptor cuadrado que se desliza
        entre posiciones izquierda (off) y derecha (on).

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el interruptor. Puede ser:
                - DEFAULT o "": Utiliza el estilo base sin prefijo
                - Cualquier etiqueta de color definida en el tema (ej: PRIMARY, SUCCESS)

        Returns:
            None: El método no retorna valores, pero registra un estilo TTK
                  que puede ser utilizado por widgets Checkbutton.
        """
        # Identificador base para este estilo
        STYLE = "Square.Toggle"

        # Color semitransparente para texto en estado deshabilitado
        # 30% de transparencia del color de texto sobre fondo
        # Ej: si fg="#000000" y bg="#FFFFFF", resultaría "#B3B3B3" (gris)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Determinar nombre del estilo según colorname
        if any([colorname == DEFAULT, colorname == ""]):
            # Caso DEFAULT: usar nombre base sin prefijo
            ttkstyle = STYLE  # Resultado: "Square.Toggle"
        else:
            # Caso específico: crear nombre con prefijo del color
            # Ej: si colorname=PRIMARY, resultado="Primary.Square.Toggle"
            ttkstyle = f"{colorname}.{STYLE}"

        # Obtener las imágenes para los diferentes estados del interruptor
        # Retorna tupla con 4 nombres: (off, on, disabled, on_disabled)
        # Nota: A pesar del comentario que indica 3 imágenes, son 4
        images = self.create_square_toggle_assets(colorname)

        # Calcular dimensiones según escala del sistema
        # Ej: en escala 2x, width=56 y borderpad=8
        width = self.scale_size(28)  # Ancho del indicador
        borderpad = self.scale_size(4)  # Padding del borde

        # Crear elemento de imagen personalizado para el indicador
        self.style.element_create(
            f"{ttkstyle}.indicator",  # Nombre único del elemento
            "image",  # Tipo: basado en imágenes
            # Imagen predeterminada (estado ON)
            images[1],
            # Mapeo de imágenes según estados:
            ("disabled selected", images[3]),  # Deshabilitado + Seleccionado
            ("disabled", images[2]),  # Solo deshabilitado
            ("!selected", images[0]),  # No seleccionado (OFF)
            # Parámetros de configuración:
            width=width,  # Ancho del elemento
            border=borderpad,  # Padding alrededor del elemento
            sticky=tk.W,  # Alineación a la izquierda
        )

        # Definir la estructura visual (layout) del widget
        self.style.layout(
            ttkstyle,
            [
                (
                    # Contenedor exterior: borde de Toolbutton
                    "Toolbutton.border",
                    {
                        "sticky": tk.NSEW,  # Expandir en todas direcciones
                        "children": [
                            (
                                # Contenedor medio: área de padding
                                "Toolbutton.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            # Indicador personalizado (interruptor)
                                            f"{ttkstyle}.indicator",
                                            {"side": tk.LEFT},  # Posición izquierda
                                        ),
                                        (
                                            # Etiqueta de texto
                                            "Toolbutton.label",
                                            {"side": tk.LEFT},  # A la derecha del indicador
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )

        # Configurar propiedades base del estilo
        self.style._build_configure(
            ttkstyle,
            relief=tk.FLAT,  # Sin efecto de relieve (plano)
            borderwidth=0,  # Sin borde visible
            foreground=self.colors.fg,  # Color de texto del tema
        )

        # Definir cambios visuales para estados específicos
        self.style.map(
            ttkstyle,
            # Texto gris cuando está deshabilitado
            foreground=[("disabled", disabled_fg)],
            # Mismo color de fondo para ambos estados (podría anular comportamientos predeterminados)
            background=[
                ("selected", self.colors.bg),
                ("!selected", self.colors.bg),
            ],
        )

        # Registrar el estilo para hacerlo disponible
        # Ejemplo de uso: ttk.Checkbutton(parent, style="Primary.Square.Toggle")
        self.style._register_ttkstyle(ttkstyle)

    def create_toggle_style(self, colorname=DEFAULT):
        """Crea un estilo de interruptor redondo para widgets ttk.Checkbutton.

        Este método es un alias para create_round_toggle_style() y está incluido
        para proporcionar una interfaz más simple y genérica. Internamente,
        delega toda la funcionalidad a create_round_toggle_style().

        Parameters:
            colorname (str):
                Etiqueta de color utilizada para estilizar el interruptor. Puede ser:
                - DEFAULT o "": Utiliza el color PRIMARY del tema
                - Cualquier etiqueta de color definida en el tema (ej: SUCCESS, WARNING)

        Returns:
            None: El método no retorna valores, pero indirectamente registra
                  un estilo TTK para widgets Checkbutton.

        """
        # Este método simplemente delega toda la funcionalidad a create_round_toggle_style
        # Actúa como un alias o interfaz simplificada para crear un estilo de interruptor redondo
        # Pasa directamente el parámetro colorname sin realizar ninguna transformación
        self.create_round_toggle_style(colorname)

    def create_toolbutton_style(self, colorname=DEFAULT):
        """Crea un estilo sólido para botones de herramientas (toolbutton) para los widgets ttk.Checkbutton
        y ttk.Radiobutton.

        Este método define la apariencia visual completa de los botones de herramientas, incluyendo
        colores, bordes, y comportamiento visual para diferentes estados (hover, presionado,
        seleccionado, deshabilitado). El estilo creado seguirá el esquema de colores del tema actual.

        Parameters:
            colorname (str, optional):
                Etiqueta de color utilizada para estilizar el widget. Si es DEFAULT o vacío,
                se utilizará el estilo base "Toolbutton" con el color primario del tema.
                Si se especifica (ej: "primary", "success"), el estilo se nombrará como
                "{colorname}.Toolbutton" y utilizará el color correspondiente.
                Default: DEFAULT

        Returns:
            None: El método no retorna ningún valor, pero registra el estilo TTK en el sistema
            para que esté disponible para los widgets.
        """
        # Nombre base del estilo TTK a crear
        STYLE = "Toolbutton"

        # Determina el nombre del estilo y el color activo según el parámetro colorname
        if any([colorname == DEFAULT, colorname == ""]):
            # Para el caso predeterminado, usa el estilo base y el color primario
            # Ejemplo: ttkstyle = "Toolbutton", toggle_on = "#0078D7"
            ttkstyle = STYLE
            toggle_on = self.colors.primary
        else:
            # Para colores específicos, crea un nombre compuesto y obtiene el color correspondiente
            # Ejemplo: colorname="success" → ttkstyle = "success.Toolbutton", toggle_on = "#28A745"
            ttkstyle = f"{colorname}.{STYLE}"
            toggle_on = self.colors.get(colorname)

        # Obtiene el color de texto apropiado para contrastar con el color de fondo
        # Ejemplo: con fondo oscuro → foreground = "#FFFFFF", con fondo claro → foreground = "#000000"
        foreground = self.colors.get_foreground(colorname)

        # Determina el color para el estado "desactivado" según el tipo de tema
        if self.is_light_theme:
            # Para temas claros, usa el color de borde (ejemplo: "#E0E0E0")
            toggle_off = self.colors.border
        else:
            # Para temas oscuros, usa el color de fondo seleccionado (ejemplo: "#444444")
            toggle_off = self.colors.selectbg

        # Crea colores semi-transparentes para el estado deshabilitado
        # Mezcla el color de primer plano con el fondo en diferentes proporciones
        # Ejemplo: disabled_bg ≈ "#E6E6E6", disabled_fg ≈ "#B3B3B3" (en tema claro)
        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Configura las propiedades base del estilo
        self.style._build_configure(
            ttkstyle,
            foreground=self.colors.selectfg,  # Color del texto en estado normal
            background=toggle_off,  # Color de fondo en estado normal
            bordercolor=toggle_off,  # Color del borde en estado normal
            darkcolor=toggle_off,  # Color oscuro en estado normal (para efectos 3D)
            lightcolor=toggle_off,  # Color claro en estado normal (para efectos 3D)
            relief=tk.RAISED,  # Relieve: ligeramente elevado
            focusthickness=0,  # Sin indicador de foco visible
            focuscolor="",  # Sin color específico para el foco
            padding=(10, 5),  # Espaciado interno: 10px horizontal, 5px vertical
            anchor=tk.CENTER,  # Alineación del contenido: centrado
        )

        # Define cómo cambian las propiedades visuales según el estado del widget
        self.style.map(
            ttkstyle,
            # Configuración del color de texto según el estado
            foreground=[
                ("disabled", disabled_fg),  # Deshabilitado: color semi-transparente
                ("hover", foreground),  # Hover: color de contraste adecuado
                ("selected", foreground),  # Seleccionado: color de contraste adecuado
            ],
            # Configuración del color de fondo según el estado
            background=[
                ("disabled", disabled_bg),  # Deshabilitado: color semi-transparente
                ("pressed !disabled", toggle_on),  # Presionado (y no deshabilitado): color activo
                ("selected !disabled", toggle_on),  # Seleccionado (y no deshabilitado): color activo
                ("hover !disabled", toggle_on),  # Hover (y no deshabilitado): color activo
            ],
            # Configuraciones similares para colores de bordes y efectos 3D
            # para mantener consistencia visual en todos los aspectos
            bordercolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
        )

        # Registra el estilo TTK en el sistema para su uso por widgets
        self.style._register_ttkstyle(ttkstyle)

    def create_outline_toolbutton_style(self, colorname=DEFAULT):
        """Crea un estilo de botón con contorno (outline) para los widgets ttk.Checkbutton
        y ttk.Radiobutton.

        Este método define la apariencia visual de botones con estilo de contorno, donde el color
        principal se aplica al borde y al texto mientras que el fondo es transparente. Cuando el
        botón está presionado o en hover, los colores se invierten (el color principal pasa a ser
        el fondo). El estilo creado seguirá el esquema de colores del tema actual.

        Parameters:
            colorname (str, optional):
                Etiqueta de color utilizada para estilizar el widget. Si es DEFAULT o vacío,
                se utilizará el estilo base "Outline.Toolbutton" con el color primario del tema.
                Si se especifica (ej: "primary", "danger"), el estilo se nombrará como
                "{colorname}.Outline.Toolbutton" y utilizará el color correspondiente.
                Default: DEFAULT

        Returns:
            None: El método no retorna ningún valor, pero registra el estilo TTK en el sistema
            para que esté disponible para los widgets.

        """
        # Nombre base del estilo TTK a crear (estilo de botón con contorno)
        STYLE = "Outline.Toolbutton"

        # Crea color semi-transparente para el texto en estado deshabilitado
        # Mezcla 30% del color de primer plano con el fondo
        # Ejemplo: En tema claro, disabled_fg ≈ "#B3B3B3"
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Determina el nombre del estilo y ajusta colorname si es necesario
        if any([colorname == DEFAULT, colorname == ""]):
            # Para el caso predeterminado, usa el estilo base y establece colorname como PRIMARY
            # Ejemplo: ttkstyle = "Outline.Toolbutton", colorname = "primary"
            ttkstyle = STYLE
            colorname = PRIMARY  # Asigna PRIMARY para uso posterior en el método
        else:
            # Para colores específicos, crea un nombre compuesto
            # Ejemplo: colorname="danger" → ttkstyle = "danger.Outline.Toolbutton"
            ttkstyle = f"{colorname}.{STYLE}"

        # Obtiene y calcula los colores para diferentes elementos y estados
        foreground = self.colors.get(colorname)  # Color del texto y borde en estado normal
        background = self.colors.get_foreground(colorname)  # Color contrastante para inversión
        foreground_pressed = background  # Color del texto cuando está presionado (invertido)
        bordercolor = foreground  # Color del borde (igual al texto)
        pressed = foreground  # Color de fondo cuando está presionado
        hover = foreground  # Color de fondo cuando está en hover

        # Configura las propiedades base del estilo (estado normal)
        self.style._build_configure(
            ttkstyle,
            foreground=foreground,  # Color del texto (color principal)
            background=self.colors.bg,  # Color de fondo (transparente/tema)
            bordercolor=bordercolor,  # Color del borde (igual al texto)
            darkcolor=self.colors.bg,  # Color oscuro (fondo del tema)
            lightcolor=self.colors.bg,  # Color claro (fondo del tema)
            relief=tk.RAISED,  # Relieve: ligeramente elevado
            focusthickness=0,  # Sin indicador de foco visible
            focuscolor=foreground,  # Color de foco igual al texto
            padding=(10, 5),  # Espaciado interno: 10px horizontal, 5px vertical
            anchor=tk.CENTER,  # Alineación del contenido: centrado
            arrowcolor=foreground,  # Color de flecha para botones con menú
            arrowpadding=(0, 0, 15, 0),  # Espaciado de la flecha
            arrowsize=3,  # Tamaño de la flecha
        )

        # Define cómo cambian las propiedades visuales según el estado del widget
        self.style.map(
            ttkstyle,
            # Configuración del color de texto según el estado
            foreground=[
                ("disabled", disabled_fg),  # Deshabilitado: color semi-transparente
                ("pressed !disabled", foreground_pressed),  # Presionado: color invertido (contraste)
                ("selected !disabled", foreground_pressed),  # Seleccionado: color invertido (contraste)
                ("hover !disabled", foreground_pressed),  # Hover: color invertido (contraste)
            ],
            # Configuración del color de fondo según el estado
            background=[
                # Note que no hay estado "disabled" aquí, usa el fondo del tema
                ("pressed !disabled", pressed),  # Presionado: color principal (inversión)
                ("selected !disabled", pressed),  # Seleccionado: color principal (inversión)
                ("hover !disabled", hover),  # Hover: color principal (inversión)
            ],
            # Configuración del color de borde según el estado
            bordercolor=[
                ("disabled", disabled_fg),  # Deshabilitado: color semi-transparente
                ("pressed !disabled", pressed),  # Presionado: color principal
                ("selected !disabled", pressed),  # Seleccionado: color principal
                ("hover !disabled", hover),  # Hover: color principal
            ],
            # Configuraciones para efectos 3D (consistentes con el fondo)
            darkcolor=[
                ("disabled", self.colors.bg),  # Deshabilitado: fondo del tema
                ("pressed !disabled", pressed),  # Presionado: color principal
                ("selected !disabled", pressed),  # Seleccionado: color principal
                ("hover !disabled", hover),  # Hover: color principal
            ],
            lightcolor=[
                ("disabled", self.colors.bg),  # Deshabilitado: fondo del tema
                ("pressed !disabled", pressed),  # Presionado: color principal
                ("selected !disabled", pressed),  # Seleccionado: color principal
                ("hover !disabled", hover),  # Hover: color principal
            ],
        )

        # Registra el estilo TTK en el sistema para su uso por widgets
        self.style._register_ttkstyle(ttkstyle)

    def create_entry_style(self, colorname=DEFAULT):
        """Crea un estilo personalizado para el widget ttk.Entry (campo de entrada de texto).

        Este método define la apariencia visual completa del campo de entrada, incluyendo colores de texto,
        fondo, bordes, y comportamiento visual para diferentes estados (foco, hover, inválido, deshabilitado,
        solo lectura). El estilo creado seguirá el esquema de colores del tema actual.

        Parameters:
            colorname (str, optional):
                Etiqueta de color utilizada para estilizar el widget. Principalmente determina el color
                del borde cuando el campo tiene foco. Si es DEFAULT o vacío, se utilizará el estilo base
                "TEntry" con el color primario para el borde en foco. Si se especifica (ej: "primary",
                "success"), el estilo se nombrará como "{colorname}.TEntry" y utilizará ese color
                específico para el borde.
                Default: DEFAULT

        Returns:
            None: El método no retorna ningún valor, pero registra el estilo TTK en el sistema
            para que esté disponible para los widgets.

        """
        # Nombre base del estilo TTK para campos de entrada
        STYLE = "TEntry"

        # Establece colores predeterminados según el tipo de tema (claro u oscuro)
        if self.is_light_theme:
            # Para temas claros, usa colores más suaves
            # Ejemplo: disabled_fg = "#E0E0E0", bordercolor = "#E0E0E0", readonly = "#F5F5F5"
            disabled_fg = self.colors.border  # Color de texto deshabilitado
            bordercolor = self.colors.border  # Color de borde predeterminado
            readonly = self.colors.light  # Color de fondo para solo lectura
        else:
            # Para temas oscuros, usa colores más contrastantes
            # Ejemplo: disabled_fg = "#444444", bordercolor = "#444444", readonly = "#444444"
            disabled_fg = self.colors.selectbg  # Color de texto deshabilitado
            bordercolor = self.colors.selectbg  # Color de borde predeterminado
            readonly = bordercolor  # Color de fondo para solo lectura

        # Determina el nombre del estilo y los colores específicos según el parámetro colorname
        if any([colorname == DEFAULT, not colorname]):
            # Para el caso predeterminado o valor vacío
            # Ejemplo: ttkstyle = "TEntry", focuscolor = "#0078D7"
            ttkstyle = STYLE  # Usa nombre base sin prefijo
            focuscolor = self.colors.primary  # Usa color primario para el foco
        else:
            # Para colores específicos
            # Ejemplo: colorname="success" → ttkstyle = "success.TEntry", focuscolor = "#28A745"
            ttkstyle = f"{colorname}.{STYLE}"  # Crea nombre con prefijo de color
            focuscolor = self.colors.get(colorname)  # Obtiene el color específico
            bordercolor = focuscolor  # Usa el mismo color para el borde normal

        # Configura las propiedades base del estilo
        self.style._build_configure(
            ttkstyle,
            bordercolor=bordercolor,  # Color del borde en estado normal
            darkcolor=self.colors.inputbg,  # Color oscuro (para efectos 3D)
            lightcolor=self.colors.inputbg,  # Color claro (para efectos 3D)
            fieldbackground=self.colors.inputbg,  # Color de fondo del área de texto
            foreground=self.colors.inputfg,  # Color del texto
            insertcolor=self.colors.inputfg,  # Color del cursor de inserción
            padding=5,  # Espaciado interno en píxeles
        )

        # Define cómo cambian las propiedades visuales según el estado del widget
        self.style.map(
            ttkstyle,
            # Configuración del color de texto
            foreground=[
                ("disabled", disabled_fg),  # Texto deshabilitado: color atenuado
            ],
            # Configuración del color de fondo del campo
            fieldbackground=[
                ("readonly", readonly),  # En solo lectura: color especial
            ],
            # Configuración del color de borde
            bordercolor=[
                ("invalid", self.colors.danger),  # Entrada inválida: color de error
                ("focus !disabled", focuscolor),  # Con foco (y no deshabilitado): color de foco
                ("hover !disabled", focuscolor),  # En hover (y no deshabilitado): color de foco
            ],
            # Configuración de efectos visuales del borde (parte clara)
            lightcolor=[
                ("focus invalid", self.colors.danger),  # Foco + inválido: color de error
                ("focus !disabled", focuscolor),  # Con foco: color de foco
                ("readonly", readonly),  # Solo lectura: color especial
            ],
            # Configuración de efectos visuales del borde (parte oscura)
            darkcolor=[
                ("focus invalid", self.colors.danger),  # Foco + inválido: color de error
                ("focus !disabled", focuscolor),  # Con foco: color de foco
                ("readonly", readonly),  # Solo lectura: color especial
            ],
        )

        # Registra el estilo TTK en el sistema para su uso por widgets
        self.style._register_ttkstyle(ttkstyle)

    def create_radiobutton_assets(self, colorname=DEFAULT):
        """Crea los recursos de imagen (assets) necesarios para construir el estilo visual
        de los botones de radio (radiobuttons).

        Este método genera cuatro imágenes diferentes que representan los estados visuales
        de un botón de radio:
        1. No seleccionado (off): Círculo con borde y fondo transparente
        2. Seleccionado (on): Círculo relleno con un indicador central
        3. No seleccionado y deshabilitado (disabled): Versión atenuada del estado off
        4. Seleccionado y deshabilitado (on_disabled): Versión atenuada del estado on

        Las imágenes se crean usando PIL/Pillow, se almacenan en el diccionario self.theme_images
        y sus nombres se retornan para ser utilizados al crear los estilos.

        Parameters:
            colorname (str, optional):
                Etiqueta de color utilizada para el estilo del widget. Define el color de relleno
                cuando el botón está seleccionado. Si es DEFAULT, se utilizará el color primario
                del tema actual.
                Default: DEFAULT

        Returns:
            Tuple[str]:
                Una tupla de cuatro strings que son los nombres de las imágenes creadas, en el
                siguiente orden: (off_name, on_name, disabled_name, on_disabled_name).
                Estos nombres se utilizan para referenciar las imágenes en self.theme_images.

        Note:
            Este método tiene un caso especial para colorname=LIGHT en temas claros, donde
            el estado seleccionado usa solo un borde en lugar de un relleno completo, y
            el indicador central usa un color oscuro para mejor contraste.
        """

        # Establece los colores y tamaños base para todas las imágenes
        prime_color = self.colors.get(colorname)  # Color principal según parámetro
        on_fill = prime_color  # Color de relleno para estado seleccionado
        off_fill = self.colors.bg  # Color de fondo (transparente/tema)
        on_indicator = self.colors.selectfg  # Color del círculo central indicador
        size = self.scale_size([14, 14])  # Tamaño final escalado según la interfaz
        # Colores semi-transparentes para bordes y estados deshabilitados
        # Ejemplos: off_border ≈ "#999999", disabled ≈ "#B3B3B3" en tema claro
        off_border = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)
        disabled = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)

        # Caso especial: Si es tema claro y color LIGHT, usa indicador oscuro para contraste
        if self.is_light_theme:
            if colorname == LIGHT:
                on_indicator = self.colors.dark  # Ejemplo: "#505050"

        # ----- IMAGEN 1: RADIO NO SELECCIONADO (OFF) -----
        # Crea una imagen en blanco de 134x134 píxeles con canal alfa (transparencia)
        _off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_off)

        # Dibuja círculo con borde semi-transparente y fondo del tema
        draw.ellipse(
            xy=[1, 1, 133, 133],  # Coordenadas: casi toda la imagen
            outline=off_border,  # Color del borde: semi-transparente
            width=6,  # Ancho del borde: 6 píxeles
            fill=off_fill  # Relleno: color de fondo del tema
        )

        # Redimensiona la imagen, convierte a PhotoImage y almacena
        off_img = ImageTk.PhotoImage(_off.resize(size, Image.LANCZOS))
        off_name = util.get_image_name(off_img)  # Obtiene nombre único
        self.theme_images[off_name] = off_img  # Almacena en diccionario

        # ----- IMAGEN 2: RADIO SELECCIONADO (ON) -----
        _on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_on)

        # Dibuja el círculo exterior con caso especial para LIGHT en tema claro
        if colorname == LIGHT and self.is_light_theme:
            # Caso especial: Solo dibuja el contorno (sin relleno)
            draw.ellipse(xy=[1, 1, 133, 133], outline=off_border, width=6)
        else:
            # Caso normal: Rellena todo el círculo con el color principal
            draw.ellipse(xy=[1, 1, 133, 133], fill=on_fill)

        # Dibuja el círculo indicador central
        draw.ellipse([40, 40, 94, 94], fill=on_indicator)

        # Procesa y almacena la imagen
        on_img = ImageTk.PhotoImage(_on.resize(size, Image.LANCZOS))
        on_name = util.get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # ----- IMAGEN 3: RADIO SELECCIONADO Y DESHABILITADO (ON DISABLED) -----
        _on_dis = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_on_dis)

        # Dibuja el círculo exterior con el mismo caso especial
        if colorname == LIGHT and self.is_light_theme:
            # Caso especial: Solo dibuja el contorno
            draw.ellipse(xy=[1, 1, 133, 133], outline=off_border, width=6)
        else:
            # Caso normal: Usa color deshabilitado (semi-transparente)
            draw.ellipse(xy=[1, 1, 133, 133], fill=disabled)

        # Dibuja el círculo central con color de fondo (en lugar de color activo)
        draw.ellipse([40, 40, 94, 94], fill=off_fill)

        # Procesa y almacena la imagen
        on_dis_img = ImageTk.PhotoImage(_on_dis.resize(size, Image.LANCZOS))
        on_disabled_name = util.get_image_name(on_dis_img)
        self.theme_images[on_disabled_name] = on_dis_img

        # ----- IMAGEN 4: RADIO NO SELECCIONADO Y DESHABILITADO (DISABLED) -----
        _disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_disabled)

        # Dibuja círculo con borde semi-transparente más delgado
        draw.ellipse(
            xy=[1, 1, 133, 133],  # Coordenadas: casi toda la imagen
            outline=disabled,  # Color del borde: deshabilitado
            width=3,  # Ancho del borde: 3 píxeles (más delgado)
            fill=off_fill  # Relleno: color de fondo del tema
        )

        # Procesa y almacena la imagen
        disabled_img = ImageTk.PhotoImage(_disabled.resize(size, Image.LANCZOS))
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        # Retorna los nombres de las cuatro imágenes como tupla
        return off_name, on_name, disabled_name, on_disabled_name

    def create_radiobutton_style(self, colorname=DEFAULT):
        """Crea un estilo personalizado para el widget ttk.Radiobutton.

        Este método define la apariencia visual completa del botón de radio, usando imágenes
        personalizadas para el indicador en diferentes estados (seleccionado, no seleccionado,
        deshabilitado). También configura la disposición (layout) de los elementos dentro del
        widget y el comportamiento visual del texto en estado deshabilitado.

        Parameters:
            colorname (str, optional):
                Etiqueta de color utilizada para estilizar el widget. Define el color del
                indicador cuando el botón está seleccionado. Si es DEFAULT o vacío, se utilizará
                el estilo base "TRadiobutton" con el color primario del tema. Si se especifica
                (ej: "primary", "success"), el estilo se nombrará como "{colorname}.TRadiobutton".
                Default: DEFAULT

        Returns:
            None: El método no retorna ningún valor, pero registra el estilo TTK en el sistema
            para que esté disponible para los widgets.

        Notes:
            Este método depende de `create_radiobutton_assets` para generar las imágenes
            necesarias para los diferentes estados del botón de radio.
        """
        # Nombre base del estilo TTK para botones de radio
        STYLE = "TRadiobutton"

        # Crea color semi-transparente para texto en estado deshabilitado
        # Ejemplo: En tema claro, disabled_fg ≈ "#B3B3B3"
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        # Determina el nombre del estilo y ajusta colorname si es necesario
        if any([colorname == DEFAULT, colorname == ""]):
            # Para el caso predeterminado, usa el estilo base y PRIMARY para las imágenes
            # Ejemplo: ttkstyle = "TRadiobutton", colorname = "primary"
            ttkstyle = STYLE
            colorname = PRIMARY  # Cambia para la generación de imágenes
        else:
            # Para colores específicos, crea un nombre compuesto
            # Ejemplo: colorname="success" → ttkstyle = "success.TRadiobutton"
            ttkstyle = f"{colorname}.{STYLE}"

        # Obtiene las imágenes para los diferentes estados del botón de radio
        # Retorna una tupla (off_name, on_name, disabled_name, on_disabled_name)
        images = self.create_radiobutton_assets(colorname)

        # Calcula dimensiones escaladas según la configuración de la interfaz
        width = self.scale_size(20)  # Ancho del indicador
        borderpad = self.scale_size(4)  # Espaciado del borde

        # Crea un elemento personalizado para el indicador usando las imágenes
        self.style.element_create(
            f"{ttkstyle}.indicator",  # Nombre del elemento personalizado
            "image",  # Tipo de elemento (basado en imágenes)
            images[1],  # Imagen predeterminada (estado seleccionado)
            ("disabled selected", images[3]),  # Imagen para deshabilitado+seleccionado
            ("disabled", images[2]),  # Imagen para deshabilitado
            ("!selected", images[0]),  # Imagen para no seleccionado
            width=width,  # Ancho escalado
            border=borderpad,  # Borde escalado
            sticky=tk.W,  # Alineación a la izquierda
        )

        # Define el color de texto para estado deshabilitado
        self.style.map(ttkstyle, foreground=[("disabled", disabled_fg)])

        # Configura el estilo base (sin parámetros específicos)
        self.style._build_configure(ttkstyle)

        # Define la disposición (layout) de los elementos dentro del widget
        self.style.layout(
            ttkstyle,  # Nombre del estilo a configurar
            [
                (
                    "Radiobutton.padding",  # Elemento contenedor principal
                    {
                        "children": [  # Elementos hijos dentro del padding
                            (
                                f"{ttkstyle}.indicator",  # Indicador personalizado
                                {"side": tk.LEFT, "sticky": ""},  # A la izquierda
                            ),
                            (
                                "Radiobutton.focus",  # Elemento para el foco
                                {
                                    "children": [  # Elementos dentro del foco
                                        (
                                            "Radiobutton.label",  # Etiqueta (texto)
                                            {"sticky": tk.NSEW},  # Expande en todas direcciones
                                        )
                                    ],
                                    "side": tk.LEFT,  # A la izquierda (después del indicador)
                                    "sticky": "",
                                },
                            ),
                        ],
                        "sticky": tk.NSEW,  # El padding se expande en todas direcciones
                    },
                )
            ],
        )

        # Registra el estilo TTK en el sistema para su uso por widgets
        self.style._register_ttkstyle(ttkstyle)