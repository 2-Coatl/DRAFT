import tkinter as tk
from tkinter import ttk
from math import ceil
from typing import Union, List, Tuple, Callable
from ui.theming.color import Colors

from ui.theming.style_engines.style_engine_tk import StyleEngineTK
from ui.theming.theme_definition import ThemeDefinition
from ui.theming.constants import LIGHT, TTK_CLAM, DEFAULT, TTK_DEFAULT, PRIMARY


class StyleEngineTTK:
    """Motor de estilos para widgets TTK.

    Responsable de:
    1. Construcción de estilos TTK bajo demanda
    2. Gestión de temas y colores para widgets TTK
    3. Actualización dinámica de estilos
    """

    def __init__(self):
        """Inicializa el motor de estilos TTK."""
        #Dependencia circular
        from ui.theming.style import Style
        self.style: Style = Style.get_instance()
        self.theme_images = {}
        self.style_engine_tk = StyleEngineTK()
        self.create_theme()

    @property
    def colors(self) -> Colors:
        """Obtiene referencia a los colores del tema actual.

        Returns:
            Colors: Objeto que contiene las definiciones de colores del tema.
        """
        return self.style.theme.colors

    @property
    def theme(self) -> ThemeDefinition:
        """Obtiene referencia a la definición del tema actual.

        Returns:
            ThemeDefinition: Objeto que contiene las definiciones del tema.
        """
        return self.style.theme

    @property
    def is_light_theme(self) -> bool:
        """Determina si el tema actual es claro.

        Returns:
            bool: True si el tema es claro, False si es oscuro.
        """
        return self.style.theme.type == LIGHT

    def scale_size(self, size: Union[int, List, Tuple]) -> Union[int, List]:
        """Escala el tamaño de imágenes y otros elementos basado en el factor de escala TTK.

        Asegura que los elementos visuales coincidan con la resolución de la pantalla
        ajustando su tamaño según el sistema operativo y la configuración.

        Args:
            size: Tamaño a escalar. Puede ser un entero único o una colección de enteros.

        Returns:
            El tamaño escalado. Si la entrada es un número, retorna un número.
            Si la entrada es una lista o tupla, retorna una lista de números escalados.
        """
        winsys = self.style.master.tk.call("tk", "windowingsystem")
        if winsys == "aqua":  # macOS
            BASELINE = 1.000492368291482
        else:  # otros sistemas
            BASELINE = 1.33398982438864281

        scaling = self.style.master.tk.call("tk", "scaling")
        factor = scaling / BASELINE

        if isinstance(size, (int, float)):
            return ceil(size * factor)
        elif isinstance(size, (tuple, list)):
            return [ceil(x * factor) for x in size]

    @staticmethod
    def name_to_method(method_name: str) -> Callable:
        """Obtiene un método por su nombre.

        Convierte un nombre de método en una referencia al método correspondiente
        dentro de la clase StyleEngineTTK.

        Args:
            method_name: Nombre del método constructor de estilo.

        Returns:
            Callable: El método referenciado por method_name.

        Example:
            >>> method = StyleEngineTTK.name_to_method("create_button_style")
            >>> method(self, "primary")
        """
        func = getattr(StyleEngineTTK, method_name)
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