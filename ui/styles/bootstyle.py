from typing import Optional, Any, Callable
from tkinter import ttk
from .constants import Keywords
from .events import Publisher, Channel


class Bootstyle:
    """Utilidades para el manejo de estilos y temas en widgets.

    Esta clase proporciona métodos estáticos para:
    - Analizar y construir nombres de estilos
    - Actualizar estilos de widgets
    - Decorar constructores de widgets
    """

    @staticmethod
    def ttkstyle_widget_class(widget: Optional[ttk.Widget] = None, string: str = "") -> str:
        """Encuentra y retorna la clase del widget.

        Args:
            widget: El objeto widget (opcional)
            string: String a analizar

        Returns:
            Keyword de la clase del widget
        """
        try:
            # Buscar clase desde el patrón string
            match = Keywords.CLASS_PATTERN.search(string.lower())
            if match is not None:
                return match.group(0)

            # Buscar clase desde el método tkinter/tcl
            if widget is not None:
                try:
                    _class = widget.winfo_class()
                    match = Keywords.CLASS_PATTERN.search(_class.lower())
                    return match.group(0) if match is not None else ""
                except Exception:
                    return ""
        except Exception:
            return ""
        return ""

    @staticmethod
    def ttkstyle_widget_type(string: str) -> str:
        """Encuentra y retorna el tipo de widget.

        Args:
            string: String a analizar

        Returns:
            Keyword del tipo de widget
        """
        match = Keywords.TYPE_PATTERN.search(string.lower())
        return match.group(0) if match is not None else ""

    @staticmethod
    def ttkstyle_widget_color(string: str) -> str:
        """Encuentra y retorna el color del widget.

        Args:
            string: String a analizar

        Returns:
            Keyword del color
        """
        match = Keywords.COLOR_PATTERN.search(string.lower())
        return match.group(0) if match is not None else ""

    @staticmethod
    def ttkstyle_widget_orient(widget: Optional[ttk.Widget] = None,
                               string: str = "",
                               **kwargs) -> str:
        """Encuentra y retorna la orientación del widget.

        Args:
            widget: El objeto widget (opcional)
            string: String a analizar
            **kwargs: Argumentos adicionales del constructor

        Returns:
            Keyword de orientación
        """
        try:
            # Método string (prioridad)
            if string:
                match = Keywords.ORIENT_PATTERN.search(string.lower())
                if match is not None:
                    return match.group(0)

            # Orientación desde kwargs
            if "orient" in kwargs:
                _orient = kwargs["orient"]
                if _orient == "h":
                    return "horizontal"
                elif _orient == "v":
                    return "vertical"
                return _orient.lower()

            # Orientación desde configuración
            if widget is not None:
                try:
                    orient = str(widget.cget("orient")).lower()
                    if orient in Keywords.ORIENTS:
                        return orient
                except Exception:
                    pass

        except Exception:
            pass
        return ""

    @staticmethod
    def ttkstyle_name(widget: Optional[ttk.Widget] = None, string: str = "", **kwargs) -> str:
        """Construye y retorna un nombre de estilo ttk.

        Args:
            widget: El objeto widget (opcional)
            string: String a analizar
            **kwargs: Argumentos adicionales

        Returns:
            Nombre del estilo ttk construido

        Example:
            >>> Bootstyle.ttkstyle_name(string="primary.outline.horizontal.TButton")
            'primary.Outline.Horizontal.TButton'
        """
        style_string = "".join(string).lower()
        widget_color = Bootstyle.ttkstyle_widget_color(style_string)
        widget_type = Bootstyle.ttkstyle_widget_type(style_string)
        widget_orient = Bootstyle.ttkstyle_widget_orient(widget, style_string, **kwargs)
        widget_class = Bootstyle.ttkstyle_widget_class(widget, style_string)

        if widget_color:
            widget_color = f"{widget_color}."

        if widget_type:
            widget_type = f"{widget_type.title()}."

        if widget_orient:
            widget_orient = f"{widget_orient.title()}."

        if widget_class.startswith("t"):
            widget_class = widget_class.title()
        else:
            widget_class = f"T{widget_class.title()}"

        return f"{widget_color}{widget_type}{widget_orient}{widget_class}"

    @staticmethod
    def ttkstyle_method_name(widget: Optional[ttk.Widget] = None, string: str = "") -> str:
        """Construye y retorna el nombre del método que crea el estilo ttk.

        Args:
            widget: El objeto widget a analizar
            string: String a analizar

        Returns:
            Nombre del método que crea el estilo

        Example:
            >>> Bootstyle.ttkstyle_method_name(string="primary.outline.TButton")
            'create_outline_button_style'
        """
        style_string = "".join(string).lower()
        widget_type = Bootstyle.ttkstyle_widget_type(style_string)
        widget_class = Bootstyle.ttkstyle_widget_class(widget, style_string)

        if widget_type:
            widget_type = f"_{widget_type}"

        if widget_class:
            widget_class = f"_{widget_class}"

        if not widget_type and not widget_class:
            return ""

        return f"create{widget_type}{widget_class}_style"

    @staticmethod
    def tkupdate_method_name(widget: ttk.Widget) -> str:
        """Obtiene el nombre del método de actualización desde la clase del widget.

        Args:
            widget: El objeto widget a analizar

        Returns:
            Nombre del método de actualización

        Example:
            >>> Bootstyle.tkupdate_method_name(button_widget)
            'update_button_style'
        """
        widget_class = Bootstyle.ttkstyle_widget_class(widget)

        if widget_class:
            widget_class = f"_{widget_class}"

        return f"update{widget_class}_style"


    @staticmethod
    def override_ttk_widget_constructor(func: Callable) -> Callable:
        """Sobreescribe el constructor de widgets ttk con opciones de bootstyle.

        Args:
            func: El método __init__ de la clase widget

        Returns:
            Constructor modificado
        """
        from .style import Style

        def __init__(self, *args, **kwargs):
            # Capturar argumentos de estilo
            bootstyle = kwargs.pop("bootstyle", "")
            style = kwargs.pop("style", "") or ""

            # Instanciar el widget
            func(self, *args, **kwargs)

            # Aplicar estilo
            if style:
                if Style.get_instance().style_exists_in_theme(style):
                    self.configure(style=style)
                else:
                    ttkstyle = Bootstyle.update_ttk_widget_style(
                        self, style, **kwargs
                    )
                    self.configure(style=ttkstyle)
            elif bootstyle:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                self.configure(style=ttkstyle)
            else:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, "default", **kwargs
                )
                self.configure(style=ttkstyle)

        return __init__

    @staticmethod
    def override_ttk_widget_configure(func: Callable) -> Callable:
        """Sobreescribe el método configure de widgets ttk.

        Args:
            func: El método configure del widget

        Returns:
            Método configure modificado
        """

        def configure(self, cnf=None, **kwargs):
            # Obtener configuración
            if cnf in ("bootstyle", "style"):
                return self.cget("style")

            if cnf is not None:
                return func(self, cnf)

            # Establecer configuración
            bootstyle = kwargs.pop("bootstyle", "")

            if "style" in kwargs:
                style = kwargs["style"]
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, style, **kwargs
                )
            elif bootstyle:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                kwargs.update(style=ttkstyle)

            # Actualizar configuración del widget
            func(self, cnf, **kwargs)

        return configure

    @staticmethod
    def update_ttk_widget_style(
            widget: Optional[ttk.Widget] = None,
            style_string: Optional[str] = None,
            **kwargs
    ) -> str:
        from .style import Style
        """Actualiza o crea un estilo ttk.

        Args:
            widget: Widget a actualizar
            style_string: String de estilo
            **kwargs: Argumentos adicionales

        Returns:
            Nombre del estilo ttk o string vacío
        """
        try:
            style = Style.get_instance() or Style()

            # Obtener estilo existente si no se proporciona
            if style_string is None and widget is not None:
                style_string = widget.cget("style")

            # No hacer nada si no hay estilo
            if not style_string:
                return ""

            if style_string == '.':
                return '.'

            # Construir estilo si no existe
            ttkstyle = Bootstyle.ttkstyle_name(widget, style_string, **kwargs)
            if not style.style_exists_in_theme(ttkstyle):
                widget_color = Bootstyle.ttkstyle_widget_color(ttkstyle)
                method_name = Bootstyle.ttkstyle_method_name(widget, ttkstyle)
                builder = style._get_builder()
                builder_method = builder.name_to_method(method_name)
                builder_method(builder, widget_color)

            # Manejar popdown de Combobox
            if widget is not None and widget.winfo_class() == "TCombobox":
                builder = style._get_builder()
                winfo_id = hex(widget.winfo_id())
                winfo_pathname = widget.winfo_pathname(winfo_id)
                Publisher.subscribe(
                    name=winfo_pathname,
                    func=lambda w=widget: builder.update_combobox_popdown_style(w),
                    channel=Channel.STD
                )
                builder.update_combobox_popdown_style(widget)

            return ttkstyle
        except Exception:
            return ""

