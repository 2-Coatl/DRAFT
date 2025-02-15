import tkinter as tk
from tkinter import ttk
from math import ceil
from typing import Union, List, Tuple, Callable
from ui.styles.color import Colors
from ui.styles.style import Style
from ui.styles.style_engines.style_engine_tk import StyleEngineTK
from ui.styles.theme_definition import LIGHT, ThemeDefinition

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

    def create_link_button_style(self) -> None:
        """Crea un estilo para botones tipo enlace.

        Configura un estilo especial para botones que se comportan como enlaces,
        estableciendo características visuales distintivas. Este estilo es
        aplicado generalmente en vistas de tabla o listados.
        """
        # Configuración del estilo para el botón tipo enlace
        self.style.configure(
            "Link.TButton",
            borderwidth=0,
            foreground=self.colors.primary,
            focuscolor="",
            padding=0
        )

        # Configuración del mapeo de estados para el botón tipo enlace
        self.style.map(
            "Link.TButton",
            foreground=[
                ("pressed", self.colors.primary),
                ("active", self.colors.primary),
                ("hover", self.colors.primary)
            ]
        )

        # Configuración para símbolos en botones tipo enlace
        self.style.configure(
            "symbol.Link.TButton",
            font="-size 16"
        )