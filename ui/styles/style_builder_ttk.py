from typing import Optional, Callable, Dict
from .colors import Colors
from .style_builder_tk import StyleBuilderTK
from .theme_definition import ThemeDefinition
from .constants import Keywords

class StyleBuilderTTK:
    """Constructor de estilos para widgets ttk.

    Esta clase genera y administra los estilos ttk bajo demanda,
    manteniendo la consistencia con el tema actual.
    """

    def __init__(self, colors: Colors, definition: ThemeDefinition):
        """Inicializa el constructor de estilos ttk.

        Args:
            colors: Objeto Colors del tema actual
            definition: Definición del tema actual
        """
        self.colors = colors
        self.definition = definition
        self.is_light = definition.is_light
        self.style_cache: Dict[str, bool] = {}
        self.builder_tk = StyleBuilderTK(colors, definition)

    def name_to_method(self, method_name: str) -> Optional[Callable]:
        """Obtiene el método correspondiente al nombre.

        Args:
            method_name: Nombre del método a obtener

        Returns:
            Método correspondiente o None si no existe
        """
        method = getattr(self, method_name, None)
        if callable(method):
            return method
        return None

    def create_button_style(self, color: str) -> None:
        """Crea el estilo para botones.

        Args:
            color: Color base para el estilo
        """
        foreground = self.colors.get('selectfg')
        if not color:
            background = self.colors.get('primary')
        else:
            background = self.colors.get(color)

        # Estilo normal
        self.style.configure(
            "TButton",
            foreground=foreground,
            background=background,
            padding=(10, 5)
        )

        # Estilo al pasar el mouse
        hover_bg = self.colors.update_hsv(background, vd=0.1)
        self.style.map(
            "TButton",
            foreground=[("active", foreground)],
            background=[("active", hover_bg)]
        )

    def create_outline_button_style(self, color: str) -> None:
        """Crea el estilo para botones con contorno.

        Args:
            color: Color base para el estilo
        """
        if not color:
            base_color = self.colors.get('primary')
        else:
            base_color = self.colors.get(color)

        # Estilo normal
        self.style.configure(
            f"{color}.Outline.TButton",
            foreground=base_color,
            background=self.colors.get('bg'),
            bordercolor=base_color,
            padding=(10, 5)
        )

        # Estilo al pasar el mouse
        hover_bg = self.colors.update_hsv(base_color, vd=0.1)
        self.style.map(
            f"{color}.Outline.TButton",
            foreground=[("active", self.colors.get('selectfg'))],
            background=[("active", hover_bg)]
        )

    def update_combobox_popdown_style(self, widget) -> None:
        """Actualiza el estilo del popdown de un Combobox.

        Args:
            widget: Widget Combobox a actualizar
        """
        try:
            popdown = widget.winfo_children()[0]
            popdown.configure(
                background=self.colors.get('bg'),
                foreground=self.colors.get('fg'),
                selectbackground=self.colors.get('selectbg'),
                selectforeground=self.colors.get('selectfg')
            )
        except Exception:
            pass

    # ... Otros métodos de creación de estilos para cada tipo de widget ...

    def _get_style_elements(self, style_name: str) -> tuple:
        """Obtiene los elementos de un nombre de estilo.

        Args:
            style_name: Nombre del estilo a analizar

        Returns:
            Tupla con (color, tipo, orientación, clase)
        """
        parts = [part.lower() for part in style_name.split('.')]

        # Color (case sensitive)
        color = ""
        if parts and parts[0] in Keywords.COLORS:
            color = parts[0]

        # Tipo (debe coincidir con Keywords.TYPES)
        widget_type = ""
        for part in parts:
            if part in Keywords.TYPES:
                widget_type = part.title()  # Convertimos a Title case para el resultado
                break

        # Orientación
        orient = ""
        for part in parts:
            if part in Keywords.ORIENTS:
                orient = part.title()  # Convertimos a Title case para el resultado
                break

        # Clase (último elemento)
        widget_class = style_name.split('.')[-1]  # Mantenemos el caso original de la clase

        return color, widget_type, orient, widget_class