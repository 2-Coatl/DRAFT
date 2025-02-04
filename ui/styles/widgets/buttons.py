from tkinter import ttk
from ..events import Channel, Publisher
from ..theme_manager import ThemeManager


class StyledButton(ttk.Button):
    """Botón que se actualiza automáticamente con cambios de tema"""

    def __init__(self, master, **kwargs):
        """
        Args:
            master: Widget padre
            **kwargs: Argumentos adicionales para ttk.Button
        """
        super().__init__(master, **kwargs)
        self.theme_manager = ThemeManager()

        # Registrar para actualizaciones de tema
        self.widget_id = str(self.winfo_id())
        Publisher.subscribe(
            self.widget_id,
            self._update_style,
            Channel.TTK
        )

        # Aplicar estilo inicial
        self._update_style()

    def _update_style(self, *args):
        """Actualiza el estilo del botón según el tema actual"""
        style = ttk.Style()
        custom_style = f'Styled.TButton.{self.widget_id}'

        style.configure(
            custom_style,
            background=self.theme_manager.get_color('primary'),
            foreground=self.theme_manager.get_color('fg'),
            padding=self.theme_manager.get_widget_config('button')['padding']
        )

        self.configure(style=custom_style)

    def destroy(self):
        """Limpia suscripciones al destruir el widget"""
        Publisher.unsubscribe(self.widget_id)
        super().destroy()