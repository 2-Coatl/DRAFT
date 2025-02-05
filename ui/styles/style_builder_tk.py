from typing import Optional
from tkinter import Widget
from .colors import Colors
from .theme_definition import ThemeDefinition


class StyleBuilderTK:
    """Constructor de estilos para widgets tk heredados.

    Esta clase maneja la actualización de widgets tk tradicionales
    para mantener consistencia con el tema actual.
    """

    def __init__(self, colors: Colors, definition: ThemeDefinition):
        """Inicializa el constructor de estilos tk.

        Args:
            colors: Objeto Colors del tema actual
            definition: Definición del tema actual
        """
        self.colors = colors
        self.definition = definition

    def update_button_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un botón tk."""
        widget.configure(
            bg=self.colors.get('primary'),
            fg=self.colors.get('selectfg'),
            activebackground=self.colors.get('active'),
            activeforeground=self.colors.get('selectfg')
        )

    def update_label_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un label tk."""
        widget.configure(
            bg=self.colors.get('bg'),
            fg=self.colors.get('fg')
        )

    def update_entry_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un entry tk."""
        widget.configure(
            bg=self.colors.get('inputbg'),
            fg=self.colors.get('inputfg'),
            insertbackground=self.colors.get('inputfg')
        )

    def update_frame_style(self, widget: Widget) -> None:
        """Actualiza el estilo de un frame tk."""
        widget.configure(
            bg=self.colors.get('bg')
        )