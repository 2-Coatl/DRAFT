from typing import Any
from tkinter import Widget
from .theme_definition import ThemeDefinition
from .colors import Colors


class StyleBuilderTK:
    """Constructor de estilos para widgets tk heredados.

    Esta clase maneja la actualización de estilos para widgets tk tradicionales,
    asegurando que coincidan con el tema actual.
    """

    def __init__(self, style: Any):
        """
        Parameters:
            style: Referencia al objeto Style
        """
        self.style = style

    @property
    def theme(self) -> ThemeDefinition:
        """Referencia al ThemeDefinition del tema actual."""
        return self.style.theme

    @property
    def colors(self) -> Colors:
        """Referencia a los colores del tema actual."""
        return self.theme.colors

    def update_window_style(self, widget: Widget) -> None:
        """Actualiza el estilo de una ventana.

        Parameters:
            widget: El widget de ventana a actualizar
        """
        widget.configure(
            background=self.colors.bg,
        )

    def update_button_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un botón tk.

        Parameters:
            widget: El botón a actualizar
        """
        widget.configure(
            background=self.colors.primary,
            foreground=self.colors.selectfg,
            activebackground=self.colors.active,
            activeforeground=self.colors.selectfg,
            highlightbackground=self.colors.border
        )

    def update_frame_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un frame tk.

        Parameters:
            widget: El frame a actualizar
        """
        widget.configure(
            background=self.colors.bg,
            highlightbackground=self.colors.border
        )

    def update_label_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un label tk.

        Parameters:
            widget: El label a actualizar
        """
        widget.configure(
            background=self.colors.bg,
            foreground=self.colors.fg
        )

    def update_entry_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un entry tk.

        Parameters:
            widget: El entry a actualizar
        """
        widget.configure(
            background=self.colors.inputbg,
            foreground=self.colors.inputfg,
            insertbackground=self.colors.inputfg,
            selectbackground=self.colors.selectbg,
            selectforeground=self.colors.selectfg
        )