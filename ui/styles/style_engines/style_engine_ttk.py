import tkinter as tk
from tkinter import ttk
from math import ceil
from typing import Union, List, Tuple, Callable
from ui.styles.color import Colors
from ui.styles.style import Style
from ui.styles.style_engines.style_engine_tk import StyleEngineTK
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.constants import LIGHT, TTK_CLAM, DEFAULT, TTK_DEFAULT


class StyleEngineTTK:
    """Motor de estilos para widgets TTK.

    Responsable de:
    1. Construcción de estilos TTK bajo demanda
    2. Gestión de temas y colores para widgets TTK
    3. Actualización dinámica de estilos
    """

    def __init__(self):
        """Inicializa el motor de estilos TTK."""
        self.style: Style = Style.get_instance()
        self.theme_images = {}
        self.style_engine_tk = StyleEngineTK()
        self.initialize_theme()

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

    def initialize_theme(self) -> None:
        """Inicializa el tema TTK con la configuración base.

        Crea un nuevo tema TTK y lo establece como el tema activo,
        aplicando la configuración inicial necesaria.
        """
        self.style.theme_create(self.theme.name, TTK_CLAM)
        ttk.Style.theme_use(self.style, self.theme.name)
        self.update_theme_settings()

    def update_theme_settings(self) -> None:
        """Actualiza la configuración del tema.

        Este método se llama internamente cada vez que el tema cambia
        para actualizar los diversos componentes del tema.
        """
        self.configure_default_style()
        # Aquí se pueden agregar más actualizaciones de tema según sea necesario

    def configure_default_style(self) -> None:
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