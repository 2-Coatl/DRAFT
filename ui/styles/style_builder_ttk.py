from typing import Any, Optional, Callable
from tkinter import ttk
from .theme_definition import ThemeDefinition
from .colors import Colors


class StyleBuilderTTK:
    """Constructor de estilos para widgets ttk.

    Esta clase genera y administra los estilos ttk bajo demanda,
    manteniendo la consistencia con el tema actual.
    """

    def __init__(self, style: Any):
        """
        Parameters:
            style: Referencia al objeto Style
        """
        self.style = style
        self.builder_tk = None  # Se inicializará bajo demanda

    @property
    def theme(self) -> ThemeDefinition:
        """Referencia al ThemeDefinition del tema actual."""
        return self.style.theme

    @property
    def colors(self) -> Colors:
        """Referencia a los colores del tema actual."""
        return self.theme.colors

    def name_to_method(self, method_name: str) -> Optional[Callable]:
        """Obtiene el método de creación de estilo por nombre.

        Parameters:
            method_name: Nombre del método a buscar

        Returns:
            Callable o None si no existe el método
        """
        if not method_name:
            return None
        return getattr(self, method_name, None)

    def create_button_style(self, color: str = "") -> None:
        """Crea el estilo para botones ttk.

        Parameters:
            color: Color base opcional para el botón
        """
        foreground = self.colors.selectfg
        if not color:
            background = self.colors.primary
        else:
            background = getattr(self.colors, color, self.colors.primary)

        # Estilo normal
        self.style.configure(
            "TButton",
            foreground=foreground,
            background=background,
            padding=(10, 5)
        )

        # Estilo hover/active
        hover_bg = self.colors.update_hsv(background, vd=0.1)
        self.style.map(
            "TButton",
            foreground=[("active", foreground)],
            background=[("active", hover_bg)]
        )

    def create_outline_button_style(self, color: str = "") -> None:
        """Crea el estilo para botones con contorno.

        Parameters:
            color: Color base opcional para el botón
        """
        if not color:
            base_color = self.colors.primary
        else:
            base_color = getattr(self.colors, color, self.colors.primary)

        style_name = f"{color}.Outline.TButton" if color else "Outline.TButton"

        # Estilo normal
        self.style.configure(
            style_name,
            foreground=base_color,
            background=self.colors.bg,
            bordercolor=base_color,
            padding=(10, 5)
        )

        # Estilo hover/active
        hover_bg = self.colors.update_hsv(base_color, vd=0.1)
        self.style.map(
            style_name,
            foreground=[("active", self.colors.selectfg)],
            background=[("active", hover_bg)]
        )

    def update_combobox_popdown_style(self, widget: ttk.Combobox) -> None:
        """Actualiza el estilo del popdown de un Combobox.

        Parameters:
            widget: Widget Combobox a actualizar
        """
        try:
            popdown = widget.winfo_children()[0]
            popdown.configure(
                background=self.colors.bg,
                foreground=self.colors.fg,
                selectbackground=self.colors.selectbg,
                selectforeground=self.colors.selectfg
            )
        except (IndexError, AttributeError):
            pass