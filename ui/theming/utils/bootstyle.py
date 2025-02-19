import re
from typing import Optional, Any
from tkinter import ttk

from ui.theming.notifications.channel import Channel
from ui.theming.notifications.publisher import Publisher
from ui.theming.utils.keywords import Keywords
from ui.theming.style_engines.style_engine_ttk import StyleEngineTTK

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
        # Paso 1: Búsqueda de clase en el string proporcionado
        # Intenta encontrar un patrón de clase en el string convertido a minúsculas
        match = re.search(Keywords.CLASS_PATTERN, string.lower())
        if match is not None:
            # Si encuentra coincidencia, extrae y retorna la clase
            widget_class = match.group(0)
            return widget_class

        # Paso 2: Búsqueda de clase a través del widget
        # Verifica si existe un widget para analizar
        if widget is None:
            return ""

        # Paso 3: Extracción de clase usando métodos nativos
        # Obtiene la clase usando el método winfo_class de Tkinter/Tcl
        _class = widget.winfo_class()
        # Busca el patrón de clase en el resultado convertido a minúsculas
        match = re.search(Keywords.CLASS_PATTERN, _class.lower())

        # Paso 4: Procesamiento del resultado final
        if match is not None:
            # Si encuentra coincidencia en la clase del widget, la retorna
            widget_class = match.group(0)
            return widget_class
        else:
            # Si no encuentra ninguna coincidencia, retorna cadena vacía
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
        # Paso 1: Búsqueda en el string (máxima prioridad)
        # Intenta encontrar un patrón de orientación en la cadena proporcionada
        match = re.search(Keywords.ORIENT_PATTERN, string)
        # Inicializa la variable que almacenará la orientación
        widget_orient = ""

        # Si encuentra coincidencia en el string, la retorna inmediatamente
        if match is not None:
            widget_orient = match.group(0)
            return widget_orient

        # Paso 2: Búsqueda en kwargs (segunda prioridad)
        # Verifica si se proporcionó orientación en los argumentos
        if "orient" in kwargs:
            # Extrae y elimina el argumento 'orient'
            _orient = kwargs.pop("orient")
            # Procesa posibles abreviaciones
            if _orient == "h":
                widget_orient = "horizontal"
            elif _orient == "v":
                widget_orient = "vertical"
            else:
                # Si no es abreviación, usa el valor tal cual
                widget_orient = _orient
            return widget_orient

        # Paso 3: Búsqueda en la configuración del widget (última prioridad)
        # Verifica si existe un widget para consultar
        if widget is None:
            return widget_orient

        # Intenta obtener la orientación de la configuración del widget
        try:
            widget_orient = str(widget.cget("orient"))
        except:
            # Si hay error al obtener la configuración, mantiene el valor actual
            pass

        # Paso 4: Retorno del resultado
        # Retorna la orientación encontrada o cadena vacía si no se encontró
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
        # Paso 1: Preparación y extracción de componentes
        # Convierte el string a minúsculas para procesamiento consistente
        style_string = "".join(string).lower()

        # Extrae los componentes individuales del estilo
        widget_color = Bootstyle.ttkstyle_widget_color(style_string)  # Obtiene el color
        widget_type = Bootstyle.ttkstyle_widget_type(style_string)  # Obtiene el tipo
        widget_orient = Bootstyle.ttkstyle_widget_orient(  # Obtiene la orientación
            widget, style_string, **kwargs
        )
        widget_class = Bootstyle.ttkstyle_widget_class(widget, style_string)  # Obtiene la clase

        # Paso 2: Validación inicial de componentes
        # Verifica si hay suficiente información para construir el estilo
        if not widget_class and not widget:
            return ""

        # Paso 3: Formateo de componentes individuales
        # Añade punto al color si existe
        if widget_color:
            widget_color = f"{widget_color}."

        # Capitaliza el tipo y añade punto si existe
        if widget_type:
            widget_type = f"{widget_type.title()}."

        # Capitaliza la orientación y añade punto si existe
        if widget_orient:
            widget_orient = f"{widget_orient.title()}."

        # Paso 4: Procesamiento especial de la clase del widget
        # Aplica reglas específicas de formateo para la clase
        if widget_class:
            if widget_class.startswith("t"):
                # Si ya empieza con 't', solo capitaliza
                widget_class = widget_class.title()
            else:
                # Si no empieza con 't', añade 'T' y capitaliza
                widget_class = f"T{widget_class.title()}"
        else:
            # Sin clase de widget, no se puede construir el estilo
            return ""

        # Paso 5: Construcción del nombre de estilo final
        # Combina todos los componentes en el orden correcto:
        # color.Tipo.Orientacion.TClase
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
        # Paso 1: Inicialización del estilo
        # Previene dependencias circulares e inicializa el gestor de estilos
        from ui.theming.style import Style
        style: Style = Style.get_instance() or Style()

        # Paso 2: Obtención del estilo actual
        # Si no se proporciona un estilo, intenta obtenerlo del widget
        if style_string is None:
            if widget is None:
                return ""
            style_string = widget.cget("style")

        # Paso 3: Validaciones iniciales del estilo
        # Verifica si hay un estilo válido para procesar
        if not style_string:
            return ""

        if style_string == '.':
            return '.'

        # Paso 4: Construcción y verificación del estilo
        # Genera el nombre del estilo y lo construye si no existe
        ttkstyle = Bootstyle.ttkstyle_name(widget, style_string, **kwargs)
        if not style.style_exists_in_theme(ttkstyle):
            # 4.1: Obtención de propiedades para la construcción
            widget_color = Bootstyle.ttkstyle_widget_color(ttkstyle)
            method_name = Bootstyle.ttkstyle_method_name(widget, ttkstyle)

            # 4.2: Construcción del estilo usando el builder
            builder: StyleEngineTTK = style._get_builder()
            builder_method = builder.name_to_method(method_name)
            builder_method(builder, widget_color)

        # Paso 5: Manejo especial para widgets tipo Combobox
        # Configura suscripciones y actualizaciones específicas para combobox
        try:
            if widget and widget.winfo_class() == "TCombobox":
                builder: StyleEngineTTK = style._get_builder()
                # 5.1: Obtención de identificadores únicos
                winfo_id = hex(widget.winfo_id())
                winfo_pathname = widget.winfo_pathname(winfo_id)

                # 5.2: Suscripción a cambios de tema
                Publisher.subscribe(
                    name=winfo_pathname,
                    func=lambda w=widget: builder.update_combobox_popdown_style(w),
                    channel=Channel.STD,
                )
                # 5.3: Actualización inicial del estilo del popdown
                builder.update_combobox_popdown_style(widget)
        except:
            pass

        # Paso 6: Retorno del estilo generado
        return ttkstyle