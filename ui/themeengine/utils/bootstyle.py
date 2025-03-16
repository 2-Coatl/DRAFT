import re
from typing import Optional, Any, Callable, Union, Dict
from tkinter import ttk

from ui.themeengine.communication.channel import Channel
from ui.themeengine.communication.publisher import Publisher
from ui.themeengine.builders.style_builder_tk import StyleBuilderTK
from ui.themeengine.utils.keywords import Keywords
from ui.themeengine.builders.style_builder_ttk import StyleBuilderTTK

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
        # print("\n--- Dentro de update_ttk_widget_style ---")
        # Paso 1: Inicialización del estilo
        # Previene dependencias circulares e inicializa el gestor de estilos
        from ui.themeengine.core.style import Style
        style: Style = Style.get_instance() or Style()

        # Paso 2: Obtención del estilo actual
        # Si no se proporciona un estilo, intenta obtenerlo del widget
        if style_string is None:
            if widget is None:
                return ""
            style_string = widget.cget("style")
        # print(f"style_string {style_string}")
        # Paso 3: Validaciones iniciales del estilo
        # Verifica si hay un estilo válido para procesar
        if not style_string:
            return ""

        if style_string == '.':
            return '.'

        # Paso 4: Construcción y verificación del estilo
        # Genera el nombre del estilo y lo construye si no existe
        ttkstyle = Bootstyle.ttkstyle_name(widget, style_string, **kwargs)
        # print(f"4 Generando el nombre del estilo {ttkstyle}")
        if not style.style_exists_in_theme(ttkstyle):
            # 4.1: Obtención de propiedades para la construcción
            widget_color = Bootstyle.ttkstyle_widget_color(ttkstyle)
            method_name = Bootstyle.ttkstyle_method_name(widget, ttkstyle)

            # 4.2: Construcción del estilo usando el builder
            builder: StyleBuilderTTK = style._get_builder()
            # print(f"4.2 Construcción del estilo usando el builder (StyleBuilderTTK) {builder}")
            builder_method = builder.name_to_method(method_name)
            builder_method(builder, widget_color)

        # Paso 5: Manejo especial para widgets tipo Combobox
        # Configura suscripciones y actualizaciones específicas para combobox
        try:
            if widget and widget.winfo_class() == "TCombobox":
                builder: StyleBuilderTTK = style._get_builder()
                # 5.1: Obtención de identificadores únicos
                winfo_id = hex(widget.winfo_id())
                winfo_pathname = widget.winfo_pathname(winfo_id)

                # 5.2: Suscripción a cambios de tema
                Publisher.subscribe(
                    name=winfo_pathname,
                    callback=lambda w=widget: builder.update_combobox_popdown_style(w),
                    channel=Channel.STD,
                )
                # 5.3: Actualización inicial del estilo del popdown
                builder.update_combobox_popdown_style(widget)
        except:
            pass

        # Paso 6: Retorno del estilo generado
        return ttkstyle


    @staticmethod
    def tkupdate_method_name(widget) -> str:
        """Busca el método de actualización de estilo tkinter desde la clase del widget.

        Parámetros:
            widget (Widget):
                El objeto widget del cual se obtendrá el método de actualización.

        Retorna:
            str:
                El nombre del método utilizado para actualizar el objeto widget.
                Ejemplos:
                - Para un Button: "update_Button_style"
                - Para un Label: "update_Label_style"
                - Si no hay widget_class: "update_style"
        """
        # Paso 1: Obtiene la clase del widget usando el método estático ttkstyle_widget_class
        # Esto extrae el nombre de la clase (ej: "Button", "Label", "Entry")
        widget_class = Bootstyle.ttkstyle_widget_class(widget)

        # Paso 2: Si widget_class tiene un valor, le agrega un guion bajo como prefijo
        # Ejemplo: "Button" → "_Button" | "Label" → "_Label"
        if widget_class:
            widget_class = f"_{widget_class}"

        # Paso 3: Construye el nombre final del método usando el patrón:
        # "update" + widget_class (ej: "_Button") + "_style"
        method_name = f"update{widget_class}_style"

        return method_name

    @staticmethod
    def override_ttk_widget_constructor(func: Callable[..., None]) -> Callable[..., None]:
        """Sobrescribe el constructor de widgets TTK para incorporar gestión de estilos.

        Este decorador modifica el constructor original de widgets TTK para permitir:
        1. Aplicación de estilos TTK existentes
        2. Creación y aplicación de nuevos estilos personalizados
        3. Manejo especial para widgets específicos (ej: ComboBox)
        4. Aseguramiento de estilo por defecto

        Args:
            func (Callable): Constructor original del widget TTK (__init__)

        Returns:
            Callable: Constructor modificado con gestión de estilos

        Notes:
            - La configuración de estilo se realiza post-instanciación
            - Prioriza 'style' sobre 'bootstyle'
            - Requiere las clases Style y Bootstyle para gestión de estilos
        """

        def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
            # 1. Extracción de parámetros de estilo
            # Extrae y elimina los parámetros de estilo para no interferir
            # con el constructor original
            bootstyle: str = kwargs.pop("bootstyle") if "bootstyle" in kwargs else ""
            style: str = kwargs.pop("style") or "" if "style" in kwargs else ""

            # 2. Instanciación del widget base
            # Llama al constructor original con los argumentos limpios
            func(self, *args, **kwargs)

            # 3. Aplicación de estilos
            # IMPORTANTE: La configuración de estilo debe ser post-instanciación para
            # poder utilizar winfo_class en `get_ttkstyle_name`
            from ui.themeengine.core.style import Style
            if style:
                # 3.1 Verifica si el estilo existe en el tema actual
                if Style.get_instance().style_exists_in_theme(style):
                    # Aplica el estilo existente directamente
                    self.configure(style=style)
                else:
                    # Crea y aplica un nuevo estilo basado en el existente
                    ttkstyle = Bootstyle.update_ttk_widget_style(
                        self, style, **kwargs
                    )
                    self.configure(style=ttkstyle)
            elif bootstyle:
                # 3.2 Crea y aplica un nuevo estilo personalizado
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                self.configure(style=ttkstyle)
            else:
                # 3.3 Aplica el estilo por defecto si no se especifica ninguno
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, "default", **kwargs
                )
                self.configure(style=ttkstyle)

        return __init__

    @staticmethod
    def override_ttk_widget_configure(func: Callable) -> Callable:
        """Sobrescribe el método configure de un widget ttk para soportar bootstyle.

        Este decorador modifica el comportamiento del método configure original de los
        widgets ttk, permitiendo el uso de estilos personalizados 'bootstyle' mientras
        mantiene la compatibilidad con la API original de ttk.

        Args:
            func (Callable): Método configure original del widget ttk que será modificado.
                Debe seguir la firma: configure(self, cnf=None, **kwargs)

        Returns:
            Callable: Nueva función configure que integra el soporte para bootstyle.

        Notes
        -----
        El decorador maneja tres casos principales:
        1. Consulta de estilo: widget.configure("bootstyle")
        2. Consulta general: widget.configure(cnf)
        3. Configuración: widget.configure(bootstyle="primary", **kwargs)

        La transformación de estilos se delega a Bootstyle.update_ttk_widget_style()

        """

        def configure(
                self,
                cnf: Optional[Union[str, Dict[str, Any]]] = None,
                **kwargs: Any
        ) -> Optional[Any]:
            """Método configure modificado que soporta bootstyle.

            Args:
                self: Instancia del widget ttk.
                cnf (Optional[Union[str, Dict[str, Any]]], optional):
                    String para consultas o diccionario para configuración.
                **kwargs: Argumentos adicionales de configuración.

            Returns:
                Optional[Any]:
                    - String del estilo si es consulta de estilo
                    - Resultado del configure original si es otra consulta
                    - None si es configuración
            """
            # 1. Manejo de consultas de configuración
            if cnf in ("bootstyle", "style"):
                # Retorna el estilo TTK actual del widget
                return self.cget("style")

            if cnf is not None:
                # Delega otras consultas al método original
                return func(self, cnf)

            # 2. Procesamiento del estilo bootstyle
            bootstyle = kwargs.pop("bootstyle") if "bootstyle" in kwargs else ""

            # 3. Actualización del estilo TTK
            if "style" in kwargs:
                # Si se proporciona style, actualiza usando ese valor
                style = kwargs.get("style")
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, style, **kwargs
                )
            elif bootstyle:
                # Si se proporciona bootstyle, genera y aplica el estilo TTK
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                # Actualiza kwargs con el nuevo estilo TTK
                kwargs.update(style=ttkstyle)

            # 4. Aplica la configuración final usando el método original
            func(self, cnf, **kwargs)

        return configure


    @staticmethod
    def update_tk_widget_style(widget) -> None:
        """Actualiza el estilo de un widget Tkinter nativo aplicando el método de actualización correspondiente.

        Este método es parte del sistema de gestión de estilos y se encarga de mantener la consistencia visual
        entre widgets Tkinter nativos y ttk. Funciona mediante la búsqueda dinámica y ejecución del método
        de actualización específico para cada tipo de widget en el StyleBuilderTK.

        Flujo de ejecución:
        1. Obtiene la instancia singleton de Style
        2. Determina el nombre del método de actualización basado en la clase del widget
        3. Obtiene el motor de estilos TK (StyleBuilderTK)
        4. Localiza y ejecuta el método específico para el tipo de widget

        Parameters
        ----------
        widget
            El widget nativo de Tkinter a actualizar. Debe ser una instancia válida
            que soporte el método winfo_name().

        Returns
        -------
        None
            El método modifica el widget in-place sin retornar valores.

        Notes
        -----
        - El método maneja silenciosamente las excepciones para permitir la inicialización
          diferida durante el arranque de la aplicación.
        - Si no se encuentra un método específico para el tipo de widget, se usa un
          método genérico de actualización.
        - El método es seguro de usar en cualquier momento del ciclo de vida de la aplicación.

        See Also
        --------
        StyleBuilderTK : Motor de estilos para widgets Tkinter nativos
        Bootstyle.tkupdate_method_name : Generación de nombres de métodos de actualización
        """
        from ui.themeengine.core.style import Style
        try:
            # Obtener la instancia singleton del gestor de estilos
            # Esta instancia mantiene el estado global de los estilos
            style = Style.get_instance()

            # Generar el nombre del método de actualización específico
            # Ejemplos: "update_Button_style", "update_Label_style"
            method_name = Bootstyle.tkupdate_method_name(widget)

            # Obtener el motor de estilos a través de la cadena:
            # Style -> Builder -> style_engine_tk
            builder = style._get_builder_tk()

            # Buscar dinámicamente el método específico en StyleBuilderTK
            # Si no existe, lanzará AttributeError que será capturado
            builder_method = getattr(StyleBuilderTK, method_name)

            # Ejecutar el método de actualización con el motor y widget
            # La actualización ocurre in-place sobre el widget
            builder_method(builder, widget)

        except:
            # Manejo silencioso de excepciones para permitir:
            # 1. Inicialización diferida de Tk
            # 2. Widgets no soportados
            # 3. Errores durante la actualización
            # Este comportamiento es necesario para la flexibilidad del sistema
            pass

    @staticmethod
    def override_tk_widget_constructor(func: Callable[..., None]) -> Callable[..., None]:
        """Decorador que modifica constructores de widgets Tkinter integrándolos en el sistema Bootstyle.

        Este decorador envuelve el constructor original (__init__) de widgets Tkinter para
        gestionar automáticamente los estilos a través del sistema Publisher/Subscriber,
        permitiendo control mediante el parámetro 'autostyle'.

        Args:
            func (Callable[..., None]): Constructor original del widget (__init__).
                Debe ser un método de inicialización de un widget Tkinter.

        Returns:
            Callable[..., None]: Constructor modificado que integra el widget en el
            sistema de estilos Bootstyle.

        Proceso:
            1. Extrae parámetro autostyle de kwargs (default: True)
            2. Ejecuta constructor original sin modificar su comportamiento
            3. Si autostyle es True:
               - Registra en Publisher con ID único str(self)
               - Configura callback para Bootstyle.update_tk_widget_style
               - Aplica estilo inicial mediante StyleBuilderTK y Style

        Notas:
            - Usa str(self) como identificador único para Publisher
            - Utiliza canal STD para notificaciones
            - Maneja errores silenciosamente
            - Aplica estilo inicial usando StyleBuilderTK a través del builder de Style
        """
        def __init__wrapper(self, *args: Any, **kwargs: Any) -> None:
            # 1. Extracción y gestión del parámetro autostyle
            autostyle: bool = kwargs.pop("autostyle", True)

            # 2. Construcción del widget base mediante constructor original
            # Entrada: self, args, kwargs modificado
            # Salida: widget inicializado sin estilos
            func(self, *args, **kwargs)

            # 3. Aplicación condicional del sistema de estilos
            if autostyle:
                # 3.1  Registro del widget en sistema Publisher/Subscriber
                # Entrada: widget (self)
                # Salida: widget registrado para actualizaciones
                Publisher.subscribe(
                    name=str(self),   # 3.1.1. ID único
                    callback=lambda w=self: Bootstyle.update_tk_widget_style(w),   # 3.1.2. Callback
                    channel=Channel.STD,  # 3.1.3. Canal
                )

                # 3.2. Estilo inicial
                # Entrada: widget registrado
                # Salida: widget con estilo aplicado
                Bootstyle.update_tk_widget_style(self)

        # 4. Retorno del constructor modificado
        return __init__wrapper

    @staticmethod
    def setup_ttktheming_api() -> None:
        """Configura el sistema de temas para su uso con tkinter y ttk.

        Este método modifica las clases de widgets originales para implementar
        la API del sistema de temas.

        Returns:
            None: Este método no devuelve ningún valor, pero tiene efectos globales.

        Modifies:
            TTK_WIDGETS: Modifica las clases para soportar tematización completa.
            TK_WIDGETS: Modifica las clases para soportar tematización básica.
        """

        # Importar las listas de widgets a modificar
        from ui.themeengine.utils.constants import TTK_WIDGETS  # Widgets de ttk (Button, Entry, etc.) 19
        from ui.themeengine.utils.constants import TK_WIDGETS  # Widgets de tk estándar (Label, Frame, etc.) 17

        # === MODIFICACIÓN DE WIDGETS TTK ===
        for widget in TTK_WIDGETS:
            try:
                # Paso 1: Sobreescribir el constructor del widget
                # Esto permite que new_args como 'bootstyle' se procesen al crear el widget
                # Ejemplo: ttk.Button(root, text="Botón", bootstyle="primary")
                _init = Bootstyle.override_ttk_widget_constructor(
                    widget.__init__
                )
                widget.__init__ = _init

                # Paso 2: Sobreescribir el método configure/config
                # Esto permite modificar el estilo después de la creación
                # Ejemplo: button.configure(bootstyle="secondary")
                _configure = Bootstyle.override_ttk_widget_configure(
                    widget.configure
                )
                widget.configure = _configure
                widget.config = widget.configure  # Mantener el alias común

                # Paso 3: Guardar los métodos originales de acceso por índice
                _orig_getitem = widget.__getitem__
                _orig_setitem = widget.__setitem__

                # Paso 4: Definir nuevas implementaciones para acceso por índice
                def __setitem(self, key, val):
                    # Caso especial: si la clave es 'bootstyle' o 'style', usar configure
                    if key in ("bootstyle", "style"):
                        # Ejemplo: button["bootstyle"] = "primary"
                        return _configure(self, **{key: val})
                    # Para otras claves, comportamiento normal
                    return _orig_setitem(key, val)

                def __getitem(self, key):
                    # Caso especial: si la clave es 'bootstyle' o 'style', obtener del configure
                    if key in ("bootstyle", "style"):
                        # Ejemplo: style_value = button["bootstyle"]
                        return _configure(self, cnf=key)
                    # Para otras claves, comportamiento normal
                    return _orig_getitem(key)

                # Paso 5: Aplicar las nuevas implementaciones, excepto para OptionMenu
                # OptionMenu tiene su propia implementación específica en otra parte
                if widget.__name__ != "OptionMenu":
                    widget.__setitem__ = __setitem
                    widget.__getitem__ = __getitem

            except Exception as e:
                # Manejo de errores: algunos widgets pueden no existir en versiones
                # antiguas de Python o tener implementaciones incompatibles
                # En caso de error, simplemente continuar con el siguiente widget
                continue

        # === MODIFICACIÓN DE WIDGETS TK ESTÁNDAR ===
        for widget in TK_WIDGETS:
            # Para widgets tk estándar, solo se modifica el constructor
            # Los widgets tk tienen una estructura diferente a los ttk
            # Ejemplo: tk.Label(root, text="Etiqueta", bootstyle="primary")
            _init = Bootstyle.override_tk_widget_constructor(widget.__init__)
            widget.__init__ = _init