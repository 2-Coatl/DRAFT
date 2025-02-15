import tkinter as tk
from ui.styles.color import Colors
from ui.styles.theme_definition import ThemeDefinition, LIGHT
from ui.styles.style import Style

class StyleEngineTK:
    """Motor de estilos para widgets Tkinter nativos.

    Esta clase se encarga de aplicar y actualizar los estilos de los widgets
    Tkinter tradicionales. Sus métodos son de uso interno y no están diseñados
    para ser llamados directamente por el usuario final.

    Los widgets de Tkinter nativos necesitan una gestión especial de estilos
    ya que no utilizan el sistema de estilos de ttk. Este motor asegura que
    mantengan una apariencia consistente con los widgets ttk.
    """

    def __init__(self):
        """Inicializa el motor de estilos TK.

        Obtiene la instancia única de Style y establece las referencias necesarias
        para la gestión de estilos.
        """
        self.style = Style.get_instance()
        self.master = self.style.master

    @property
    def theme(self) -> ThemeDefinition:
        """Obtiene la definición del tema actual.

        Returns:
            ThemeDefinition: Objeto que define el tema en uso.
        """
        return self.style.theme

    @property
    def colors(self) -> Colors:
        """Obtiene los colores del tema actual.

        Returns:
            Colors: Objeto que contiene la paleta de colores actual.
        """
        return self.style.colors

    @property
    def is_light_theme(self) -> bool:
        """Determina si el tema actual es claro.

        Returns:
            bool: True si es un tema claro, False si es oscuro.
        """
        return self.style.theme.type == LIGHT

    def update_tk_style(self, widget: tk.Tk):
        """Actualiza el estilo de la ventana principal.

        Args:
            widget: Ventana principal a actualizar.
        """
        widget.configure(background=self.colors.bg)
        widget.option_add('*Text*Font', 'TkDefaultFont')

    def update_toplevel_style(self, widget: tk.Toplevel):
        """Actualiza el estilo de una ventana secundaria.

        Args:
            widget: Ventana secundaria a actualizar.
        """
        widget.configure(background=self.colors.bg)

    def update_canvas_style(self, widget: tk.Canvas):
        """Actualiza el estilo de un canvas.

        Args:
            widget: Canvas a actualizar.
        """
        widget.configure(
            background=self.colors.bg,
            highlightthickness=0,
        )

    def update_button_style(self, widget: tk.Button):
        """Actualiza el estilo de un botón.

        Args:
            widget: Botón a actualizar.
        """
        background = self.colors.primary
        foreground = self.colors.selectfg
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.1)

        widget.configure(
            background=background,
            foreground=foreground,
            relief=tk.FLAT,
            borderwidth=0,
            activebackground=activebackground,
            highlightbackground=self.colors.selectfg,
        )