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