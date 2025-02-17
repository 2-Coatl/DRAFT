import re
from typing import Optional, Any
from tkinter import ttk

from ui.styles.notifications.channel import Channel
from ui.styles.notifications.publisher import Publisher
from ui.styles.utils.keywords import Keywords
from ui.styles.core.style import Style
from ui.styles.style_engines.style_engine_ttk import StyleEngineTTK

class Bootstyle:
    """Clase utilitaria que proporciona métodos para manipular y gestionar estilos TTK.

    Esta clase contiene métodos estáticos para:
    - Parsear nombres de estilos TTK
    - Extraer información de widgets
    - Construir nombres de estilos
    - Actualizar estilos de widgets
    """

    @staticmethod
    def ttkstyle_widget_class(widget: Optional[ttk.Widget] = None, string: str = "") -> str:
        """Encuentra y retorna la clase del widget.

        Busca la clase del widget ya sea a partir de un patrón en una cadena o
        directamente desde el widget.

        Args:
            widget: El objeto widget a analizar.
            string: Una cadena de texto para parsear.

        Returns:
            La clase del widget o cadena vacía si no se encuentra.
        """
        # find widget class from string pattern
        match = re.search(Keywords.CLASS_PATTERN, string.lower())
        if match is not None:
            widget_class = match.group(0)
            return widget_class

        # find widget class from tkinter/tcl method
        if widget is None:
            return ""
        _class = widget.winfo_class()
        match = re.search(Keywords.CLASS_PATTERN, _class.lower())
        if match is not None:
            widget_class = match.group(0)
            return widget_class
        else:
            return ""

    @staticmethod
    def ttkstyle_widget_type(string: str) -> str:
        """Encuentra y retorna el tipo de widget.

        Busca en la cadena proporcionada un patrón que coincida con
        alguno de los tipos de widget definidos.

        Args:
            string: La cadena de texto a parsear.

        Returns:
            El tipo de widget encontrado o cadena vacía si no hay coincidencia.
        """
        match = re.search(Keywords.TYPE_PATTERN, string.lower())
        if match is None:
            return ""
        else:
            widget_type = match.group(0)
            return widget_type

    @staticmethod
    def ttkstyle_widget_orient(widget: Optional[ttk.Widget] = None, string: str = "", **kwargs: Any) -> str:
        """Encuentra y retorna la orientación del widget.

        Busca la orientación usando tres estrategias en orden de prioridad:
        1. Desde el patrón en la cadena proporcionada
        2. Desde los kwargs proporcionados
        3. Desde la configuración del widget

        Args:
            widget: El objeto widget a analizar.
            string: La cadena de texto a parsear.
            **kwargs: Argumentos adicionales que podrían contener la orientación.

        Returns:
            La orientación del widget o cadena vacía si no se encuentra.
        """
        # string method (priority)
        match = re.search(Keywords.ORIENT_PATTERN, string)
        widget_orient = ""

        if match is not None:
            widget_orient = match.group(0)
            return widget_orient

        # orient from kwargs
        if "orient" in kwargs:
            _orient = kwargs.pop("orient")
            if _orient == "h":
                widget_orient = "horizontal"
            elif _orient == "v":
                widget_orient = "vertical"
            else:
                widget_orient = _orient
            return widget_orient

        # orient from settings
        if widget is None:
            return widget_orient
        try:
            widget_orient = str(widget.cget("orient"))
        except:
            pass

        return widget_orient

    @staticmethod
    def ttkstyle_widget_color(string: str) -> str:
        """Encuentra y retorna el color del widget.

        Busca en la cadena proporcionada un patrón que coincida con
        alguno de los colores definidos en el sistema.

        Args:
            string: La cadena de texto a parsear.

        Returns:
            El color encontrado o cadena vacía si no hay coincidencia.
        """
        _color = re.search(Keywords.COLOR_PATTERN, string.lower())
        if _color is None:
            return ""
        else:
            widget_color = _color.group(0)
            return widget_color

    @staticmethod
    def ttkstyle_name(widget: Optional[ttk.Widget] = None, string: str = "", **kwargs: Any) -> str:
        """Construye y retorna un nombre de estilo TTK.

        Combina los diferentes componentes (color, tipo, orientación y clase) para
        construir un nombre de estilo TTK completo.

        Args:
            widget: El objeto widget a analizar.
            string: La cadena de texto a parsear.
            **kwargs: Argumentos adicionales para la orientación.

        Returns:
            El nombre de estilo TTK construido o cadena vacía si no hay componentes válidos.
        """
        style_string = "".join(string).lower()
        widget_color = Bootstyle.ttkstyle_widget_color(style_string)
        widget_type = Bootstyle.ttkstyle_widget_type(style_string)
        widget_orient = Bootstyle.ttkstyle_widget_orient(
            widget, style_string, **kwargs
        )
        widget_class = Bootstyle.ttkstyle_widget_class(widget, style_string)

        # Si no hay clase de widget y no hay widget, retornar cadena vacía
        if not widget_class and not widget:
            return ""

        if widget_color:
            widget_color = f"{widget_color}."

        if widget_type:
            widget_type = f"{widget_type.title()}."

        if widget_orient:
            widget_orient = f"{widget_orient.title()}."

        if widget_class:
            if widget_class.startswith("t"):
                widget_class = widget_class.title()
            else:
                widget_class = f"T{widget_class.title()}"
        else:
            return ""

        ttkstyle = f"{widget_color}{widget_type}{widget_orient}{widget_class}"
        return ttkstyle

    @staticmethod
    def ttkstyle_method_name(widget: Optional[ttk.Widget] = None, string: str = "") -> str:
        """Construye y retorna el nombre del método que crea el estilo TTK.

        Parsea una cadena para construir el nombre del método en `StyleBuilderTTK`
        que crea el estilo TTK para el widget objetivo.

        Args:
            widget: El objeto widget a analizar.
            string: La cadena de texto a parsear.

        Returns:
            El nombre del método que crea el estilo o cadena vacía si no es válido.
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
        else:
            method_name = f"create{widget_type}{widget_class}_style"
            return method_name

    @staticmethod
    def update_ttk_widget_style(
        widget: Optional[ttk.Widget] = None,
        style_string: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Actualiza el estilo TTK o lo crea si no existe.

        Actualiza el estilo del widget proporcionado o crea uno nuevo si no existe.
        Maneja casos especiales como los ComboBox.

        Args:
            widget: El widget a actualizar.
            style_string: La cadena de estilo a evaluar. Puede ser el argumento
                'style', 'ttkstyle' o 'bootstyle' dependiendo del contexto.
            **kwargs: Argumentos adicionales para la construcción del estilo.

        Returns:
            El nombre del estilo TTK o cadena vacía si no hay estilo.
        """
        style: Style = Style.get_instance() or Style()

        # get existing widget style if not provided
        if style_string is None:
            if widget is None:
                return ""
            style_string = widget.cget("style")

        # do nothing if the style has not been set
        if not style_string:
            return ""

        if style_string == '.':
            return '.'

        # build style if not existing (example: theme changed)
        ttkstyle = Bootstyle.ttkstyle_name(widget, style_string, **kwargs)
        if not style.style_exists_in_theme(ttkstyle):
            widget_color = Bootstyle.ttkstyle_widget_color(ttkstyle)
            method_name = Bootstyle.ttkstyle_method_name(widget, ttkstyle)
            builder: StyleEngineTTK = style._get_builder()
            builder_method = builder.name_to_method(method_name)
            builder_method(builder, widget_color)

        # subscribe popdown style to theme changes
        try:
            if widget and widget.winfo_class() == "TCombobox":
                builder: StyleEngineTTK = style._get_builder()
                winfo_id = hex(widget.winfo_id())
                winfo_pathname = widget.winfo_pathname(winfo_id)
                Publisher.subscribe(
                    name=winfo_pathname,
                    func=lambda w=widget: builder.update_combobox_popdown_style(w),
                    channel=Channel.STD,
                )
                builder.update_combobox_popdown_style(widget)
        except:
            pass

        return ttkstyle