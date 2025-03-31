import ui.themeengine as ttk
import ui.themeengine as tk
from ui.themeengine.utils.constants import *


class FloodGauge(ttk.Progressbar):
    """
    Widget que muestra el estado de una operación de larga duración
    con un indicador de texto opcional.

    Similar a `ttk.Progressbar`, este widget puede operar en dos modos:
    *determinate* muestra la cantidad completada en relación con el
    total de trabajo a realizar, e *indeterminate* proporciona una
    visualización animada para indicar al usuario que algo está ocurriendo.

    Las variables se generan automáticamente para este widget y pueden
    vincularse a otros widgets referenciándolas a través de los atributos
    `textvariable` y `variable`.

    Parámetros:
    ----------
    master : Widget, opcional
        Widget padre que contiene este control.

    cursor : str, opcional
        Cursor que aparecerá cuando el ratón esté sobre la barra de progreso.

    length : int, opcional
        Especifica la longitud del eje largo de la barra de progreso
        (ancho si orient=horizontal, alto si orient=vertical).

    maximum : float, opcional
        Número de punto flotante que especifica el valor máximo.
        Por defecto es 100.

    mode : ['determinate', 'indeterminate']
        Use `indeterminate` si no puede medir con precisión el progreso
        relativo del proceso subyacente. En este modo, un rectángulo
        rebota entre los extremos del widget una vez que se utiliza el
        método `FloodGauge.start()`. En caso contrario, use `determinate`
        si el progreso relativo puede calcularse por adelantado.

    orient : ['horizontal', 'vertical']
        Especifica la orientación del widget.

    bootstyle : str, opcional
        Estilo utilizado para renderizar el widget. Las opciones incluyen
        primary, secondary, success, info, warning, danger, light, dark.

    takefocus : bool, opcional
        Este widget no se incluye en la navegación de foco por defecto.
        Para añadir el widget a la navegación de foco, use `takefocus=True`.

    text : str, opcional
        Cadena de texto para mostrar en la etiqueta de FloodGauge.
        Se asigna al atributo `FloodGauge.textvariable`.

    value : float, opcional
        Valor actual de la barra de progreso. En modo `determinate`,
        representa la cantidad de trabajo completado. En modo `indeterminate`,
        se interpreta módulo `maximum`; es decir, la barra de progreso
        completa un "ciclo" cuando el `valor` aumenta en `maximum`.

    mask : str, opcional
        Cadena de formato que puede usarse para actualizar la etiqueta
        de FloodGauge cada vez que se actualiza el valor. Por ejemplo,
        la cadena "{}% Almacenamiento Usado" con un valor de widget de 45
        mostraría "45% Almacenamiento Usado" en la etiqueta de FloodGauge.
        Si se establece una máscara, se ignora la opción `text`.

    font : Union[Font, str], opcional
        Fuente a utilizar para la etiqueta de la barra de progreso.

    Métodos:
    -------
    start()
        Inicia la animación automática de la barra.

    stop()
        Detiene la animación automática.

    step(amount=1.0)
        Incrementa el valor en la cantidad especificada.

    configure(**kwargs)
        Configura las opciones del widget.

    Ejemplos:
    --------
    ```python
    import ui.themeengine as ttk
    from ui.themeengine.utils.constants import *

    app = ttk.Window(size=(500, 500))

    gauge = ttk.FloodGauge(
        bootstyle=INFO,
        font=(None, 24, 'bold'),
        mask='Memoria Usada {}%',
    )
    gauge.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # autoincremento de la barra
    gauge.start()

    # detener el autoincremento
    gauge.stop()

    # actualizar manualmente el valor de la barra
    gauge.configure(value=25)

    # incrementar el valor en 10 pasos
    gauge.step(10)

    app.mainloop()
    ```
    """
    def __init__(
        self,
        master=None,
        cursor=None,
        font=None,
        length=None,
        maximum=100,
        mode=DETERMINATE,
        orient=HORIZONTAL,
        bootstyle=PRIMARY,
        takefocus=False,
        text=None,
        value=0,
        mask=None,
        **kwargs,
    ):
        """
        Inicializa una instancia del widget FloodGauge.

        Este constructor configura una barra de progreso mejorada que puede mostrar texto.
        El widget puede operar en modo determinado (mostrando progreso específico) o
        indeterminado (mostrando actividad) y puede incluir un indicador de texto que se
        actualiza automáticamente si se especifica una máscara de formato.

        Parameters:
            master (Widget, optional):
                Parent widget. Defaults to None.
                Widget padre que contendrá este control.

            cursor (str, optional):
                The cursor that will appear when the mouse is over the
                progress bar. Defaults to None.
                Cursor que aparecerá cuando el ratón esté sobre la
                barra de progreso.

            font (Union[Font, str], optional):
                The font to use for the progress bar label.
                Fuente a utilizar para la etiqueta de la barra de progreso.
                Ejemplo: ("Arial", 12, "bold") o "Helvetica 10 italic"

            length (int, optional):
                Specifies the length of the long axis of the progress bar
                (width if orient = horizontal, height if if vertical);
                Especifica la longitud del eje largo de la barra de progreso
                (ancho si es horizontal, alto si es vertical).

            maximum (float, optional):
                A floating point number specifying the maximum `value`.
                Defaults to 100.
                Número de punto flotante que especifica el valor máximo.
                Predeterminado: 100.

            mode ('determinate', 'indeterminate'):
                Use `indeterminate` if you cannot accurately measure the
                relative progress of the underlying process. In this mode,
                a rectangle bounces back and forth between the ends of the
                widget once you use the `FloodGauge.start()` method.
                Otherwise, use `determinate` if the relative progress can be
                calculated in advance.

                Use `indeterminate` si no puede medir con precisión el progreso
                relativo del proceso subyacente. En este modo, un rectángulo
                rebota entre los extremos del widget una vez que use el método
                `FloodGauge.start()`. De lo contrario, use `determinate` si el
                progreso relativo puede calcularse por adelantado.

            orient ('horizontal', 'vertical'):
                Specifies the orientation of the widget.
                Especifica la orientación del widget.

            bootstyle (str, optional):
                The style used to render the widget. Options include
                primary, secondary, success, info, warning, danger, light,
                dark.

                Estilo utilizado para renderizar el widget. Las opciones incluyen
                primary, secondary, success, info, warning, danger, light, dark.

            takefocus (bool, optional):
                This widget is not included in focus traversal by default.
                To add the widget to focus traversal, use
                `takefocus=True`.

                Este widget no se incluye en la navegación de foco por defecto.
                Para añadir el widget a la navegación de foco, use `takefocus=True`.

            text (str, optional):
                A string of text to be displayed in the FloodGauge label.
                This is assigned to the attribute `FloodGauge.textvariable`

                Cadena de texto para mostrar en la etiqueta de FloodGauge.
                Se asigna al atributo `FloodGauge.textvariable`.
                Ejemplo: "Cargando datos..."

            value (float, optional):
                The current value of the progressbar. In `determinate`
                mode, this represents the amount of work completed. In
                `indeterminate` mode, it is interpreted modulo `maximum`;
                that is, the progress bar completes one "cycle" when the
                `value` increases by `maximum`.

                Valor actual de la barra de progreso. En modo `determinate`,
                representa la cantidad de trabajo completado. En modo `indeterminate`,
                se interpreta módulo `maximum`; es decir, la barra de progreso
                completa un "ciclo" cuando el `valor` aumenta en `maximum`.
                Predeterminado: 0

            mask (str, optional):
                A string format that can be used to update the FloodGauge
                label every time the value is updated. For example, the
                string "{}% Storage Used" with a widget value of 45 would
                show "45% Storage Used" on the FloodGauge label. If a
                mask is set, then the `text` option is ignored.

                Cadena de formato que se puede usar para actualizar la etiqueta
                de FloodGauge cada vez que se actualiza el valor. Por ejemplo,
                la cadena "{}% Almacenamiento Usado" con un valor de widget de 45
                mostraría "45% Almacenamiento Usado" en la etiqueta. Si se
                establece una máscara, se ignora la opción `text`.
                Ejemplo: "Progreso: {}%"

            **kwargs:
                Other configuration options from the option database.
                Otras opciones de configuración de la base de datos de opciones.
                Pueden incluir opciones como padding, borderwidth, etc.

        Ejemplos:
            # Barra de progreso básica con texto
            gauge = FloodGauge(
                master=frame,
                value=25,
                text="Cargando...",
                bootstyle="primary"
            )

            # Barra con actualización automática de texto
            gauge = FloodGauge(
                value=50,
                maximum=200,
                mask="Progreso: {}/200",
                font=("Arial", 12)
            )

            # Barra vertical en modo indeterminado
            gauge = FloodGauge(
                mode=INDETERMINATE,
                orient=VERTICAL,
                length=300,
                bootstyle="info"
            )
        """

        # Este bloque configura las variables internas y atributos que controlarán el comportamiento
        # y apariencia del widget FloodGauge.

        # Establece variables tkinter para el valor numérico y el texto del widget,
        # permitiendo tanto usar variables externas proporcionadas por el usuario como
        # crear nuevas variables internas. También almacena configuraciones de estilo
        # y prepara la base para el sistema de actualización automática de texto.

        # Manejamos la variable para el valor numérico:
        # - Si se proporciona externamente, la usamos
        # - Si no, creamos una nueva con el valor inicial
        if 'variable' in kwargs:
            self._variable = kwargs.pop('variable')  # Usamos y eliminamos de kwargs
        else:
            self._variable = tk.IntVar(value=value)  # Ej: value=25 -> IntVar(25)

        # Manejamos la variable para el texto:
        # - Si se proporciona externamente, la usamos
        # - Si no, creamos una nueva con el texto inicial
        if 'textvariable' in kwargs:
            self._textvariable = kwargs.pop('textvariable')  # Usamos y eliminamos de kwargs
        else:
            self._textvariable = tk.StringVar(value=text)  # Ej: text="Cargando" -> StringVar("Cargando")

        # Almacenamos el estilo visual para uso en métodos de configuración
        self._bootstyle = bootstyle  # Ej: bootstyle=PRIMARY -> self._bootstyle=PRIMARY

        # Configuramos la fuente, usando la proporcionada o la predeterminada
        self._font = font or "helvetica 10"  # Ej: font=None -> "helvetica 10", font="Arial 12" -> "Arial 12"

        # Almacenamos la máscara para formateo dinámico de texto
        self._mask = mask  # Ej: mask="{}% completado" -> self._mask="{}% completado"

        # Inicializamos el ID del rastreador como None
        # Se configurará más adelante si hay una máscara
        self._traceid = None

        # Este bloque de código inicializa la clase base ttk.Progressbar, configurando
        # todos los parámetros necesarios para el funcionamiento de la barra de progreso
        # subyacente al widget FloodGauge.

        # Delegar a la clase padre la inicialización de la funcionalidad base de la barra
        # de progreso, asegurando que todos los parámetros se configuren correctamente y
        # estableciendo la clase de estilo "FloodGauge" para permitir personalización
        # visual específica para este tipo de widget.

        # Invocamos el constructor de la clase padre (ttk.Progressbar)
        # para inicializar la funcionalidad base de la barra de progreso
        super().__init__(
            # Widget contenedor donde se ubicará este control
            master=master,  # Ej: master=root -> se coloca dentro de root

            # Identificador para el sistema de estilos ttk
            # Este valor siempre es "FloodGauge" para este widget
            class_="FloodGauge",

            # Tipo de cursor cuando el ratón está sobre el widget
            cursor=cursor,  # Ej: cursor="hand2" -> muestra cursor tipo mano

            # Longitud en píxeles del eje principal
            length=length,  # Ej: length=200 -> 200px de ancho (horizontal) o alto (vertical)

            # Valor máximo que puede alcanzar la barra
            maximum=maximum,  # Ej: maximum=100 -> valores de 0 a 100

            # Modo de operación: determinado o indeterminado
            mode=mode,  # Ej: mode=DETERMINATE -> muestra progreso específico

            # Orientación: horizontal o vertical
            orient=orient,  # Ej: orient=HORIZONTAL -> barra de izquierda a derecha

            # Estilo visual del widget
            bootstyle=bootstyle,  # Ej: bootstyle="success" -> barra verde

            # Si el widget puede recibir el foco con tabulación
            takefocus=takefocus,  # Ej: takefocus=False -> no recibe foco con Tab

            # Variable que controla el valor numérico
            # Usamos la variable interna configurada previamente
            variable=self._variable,  # Ej: self._variable contiene IntVar(25)

            # Parámetros adicionales que se pasan directamente
            # En este punto, kwargs no debe contener 'variable' ni 'textvariable'
            **kwargs,  # Ej: padding=10, borderwidth=2, etc.
        )
        # Bloque de Configuración de Texto y Eventos en FloodGauge
        #
        # Este bloque establece el texto inicial del widget y configura las vinculaciones de eventos
        # necesarias para mantener la consistencia visual del texto cuando cambia el tema o la
        # configuración del widget.
        # Inicializar el texto visible y asegurar que se mantenga correctamente visualizado
        # independientemente de los cambios en el tema o configuración del widget.
        #
        # Establece el texto inicial del widget utilizando el valor actual
        # de la variable de texto. Esto configura la apariencia visual
        # del texto en el widget.
        self._set_widget_text(self._textvariable.get())  # Ej: self._textvariable contiene "Cargando..."

        # Vincula el evento de cambio de tema al método _on_theme_change.
        # Esto asegura que cuando cambie el tema del framework, el widget
        # pueda actualizar su apariencia para mantener el texto correctamente visualizado.
        self.bind("<<ThemeChanged>>", self._on_theme_change)

        # Vincula el evento de cambio de configuración al mismo método _on_theme_change.
        # Esto garantiza que cuando el widget cambie de tamaño, posición u otras propiedades,
        # el texto se mantenga correctamente visualizado.
        self.bind("<<Configure>>", self._on_theme_change)

        # Configuración Condicional del Sistema de Máscara en FloodGauge
        #
        # Este bloque determina si se debe activar el sistema de formateo dinámico de texto
        # basado en el valor del widget. Si se ha proporcionado una máscara de formato,
        # configura un mecanismo que actualizará automáticamente el texto cuando cambie
        # el valor de la barra de progreso.
        # Activar condicionalmente el sistema de actualización automática de texto
        # basado en una plantilla de formato predefinida (máscara).

        # Verifica si se ha proporcionado una máscara de formato.
        # Una máscara es una plantilla con marcadores {} que serán
        # reemplazados por el valor actual del widget.
        if self._mask is not None:
            # Si hay una máscara, configura el sistema de trazado
            # para actualizar automáticamente el texto cuando cambie el valor.
            # Por ejemplo, si self._mask="{}%" y value=25, mostrará "25%".
            self._set_mask()
            # No es necesario hacer nada si no hay máscara,
            # el texto permanecerá estático.

    def _set_widget_text(self, *_):
        """
        Actualiza el texto mostrado en el widget FloodGauge.

        Este método configura el texto que se mostrará visualmente en el widget,
        utilizando el sistema de estilos ttk. Determina el texto a mostrar basándose
        en si hay una máscara de formato configurada o no.

        Comportamiento:
        - Si no hay máscara (_mask es None): Usa directamente el valor de _textvariable
        - Si hay máscara: Aplica la máscara al valor numérico de _variable

        El método también configura la fuente del texto utilizando el valor de _font.

        Parámetros:
        ----------
        self : FloodGauge
            La instancia del widget
        *_ : cualquier
            Parámetros adicionales que se ignoran (permite usar el método como callback)

        Retorno:
        -------
        None
            Este método no devuelve ningún valor, solo actualiza el widget visualmente.

        Ejemplos:
        --------
        # Sin máscara, mostrando "Procesando..."
        self._textvariable.set("Procesando...")
        self._set_widget_text()

        # Con máscara "{}%" y valor 75
        self._mask = "{}%"
        self._variable.set(75)
        self._set_widget_text()  # Mostrará "75%"

        # Como callback de un trazador
        self._variable.trace_add("write", self._set_widget_text)
        self._variable.set(30)  # Llamará a _set_widget_text automáticamente
        """
        # Obtiene el nombre del estilo ttk asignado al widget
        # Ej: "FloodGauge.Horizontal.TProgressbar"
        ttkstyle = self.cget("style")

        # Decide cómo obtener el texto basado en la existencia de una máscara
        if self._mask is None:
            # Sin máscara: Usa directamente el valor de la variable de texto
            # Ej: self._textvariable contiene "Cargando..." → text = "Cargando..."
            text = self._textvariable.get()
        else:
            # Con máscara: Formatea el valor numérico según la plantilla
            # Ej: self._mask = "{}%" y self._variable = 75 → text = "75%"
            value = self._variable.get()
            text = self._mask.format(value)

        # Configura el texto en el estilo ttk del widget
        # Esto usa la interfaz Tcl/Tk directamente para modificar el estilo
        # Ej: ttk::style configure FloodGauge.Horizontal.TProgressbar -text "75%"
        self.tk.call("ttk::style", "configure", ttkstyle, "-text", text)

        # Configura la fuente para el texto
        # Ej: ttk::style configure FloodGauge.Horizontal.TProgressbar -font "helvetica 10"
        self.tk.call("ttk::style", "configure", ttkstyle, "-font", self._font)

    def _set_mask(self):
        """
        Configura el sistema de observación automática para actualizar el texto cuando cambia el valor.

        Este método establece un trazador (tracer) en la variable de valor (self._variable)
        que llamará automáticamente al método _set_widget_text cuando el valor cambie.
        El resultado es que el texto mostrado en el widget se actualizará dinámicamente
        según la máscara de formato cada vez que cambie el valor de la barra de progreso.

        El método es idempotente: verifica si ya existe un trazador configurado (self._traceid)
        para evitar configuraciones duplicadas. Solo configura un nuevo trazador si no hay
        uno activo.

        Parámetros:
        ----------
        self : FloodGauge
            La instancia del widget

        Retorno:
        -------
        None
            Este método no devuelve ningún valor, solo configura el comportamiento interno.

        Efectos:
        -------
        - Configura un trazador para self._variable que actualizará el texto automáticamente
        - Almacena el identificador del trazador en self._traceid

        Ejemplos:
        --------
        # Configuración básica
        self._mask = "{}%"
        self._set_mask()

        # Después de configurar, los cambios en el valor actualizarán el texto
        self._variable.set(50)  # El texto se actualiza automáticamente a "50%"
        """
        # Verifica si ya existe un trazador configurado
        # Esto evita configurar múltiples trazadores para la misma variable
        # y hace que el método sea idempotente (puede llamarse varias veces sin efectos indeseados)
        if self._traceid is None:
            # Configura un nuevo trazador para la variable de valor
            # Este trazador detectará cuando se escribe un nuevo valor en la variable
            # y llamará automáticamente al método _set_widget_text
            self._traceid = self._variable.trace_add(
                "write",  # Tipo de evento a observar: escritura de un nuevo valor
                self._set_widget_text  # Método callback a llamar cuando cambie el valor
                # _set_widget_text debe estar diseñado para manejar los argumentos adicionales
                # que tkinter pasará automáticamente (nombre_var, índice, modo)
            )
            # El identificador retornado por trace_add se almacena en self._traceid
            # Este identificador será necesario si posteriormente se desea eliminar el trazador

    def _unset_mask(self):
        """
        Elimina el sistema de observación automática que actualiza el texto cuando cambia el valor.

        Este método desactiva el trazador (tracer) configurado en la variable de valor (self._variable)
        y restablece el estado interno para permitir una nueva configuración si es necesario.
        Una vez llamado este método, el texto del widget ya no se actualizará automáticamente
        cuando cambie el valor de la barra de progreso.

        El método es idempotente: puede llamarse múltiples veces sin efectos negativos,
        incluso si no hay trazador configurado. Siempre establece self._traceid a None,
        independientemente del estado previo.

        Parámetros:
        ----------
        self : FloodGauge
            La instancia del widget

        Retorno:
        -------
        None
            Este método no devuelve ningún valor, solo modifica el estado interno.

        Efectos:
        -------
        - Elimina el trazador configurado en self._variable si existe
        - Establece self._traceid a None para indicar que no hay trazador activo
        - Desactiva la actualización automática del texto

        Ejemplos:
        --------
        # Desactivar el sistema de actualización automática
        self._unset_mask()

        # Después de desactivar, los cambios en el valor no afectan al texto
        self._variable.set(75)  # El texto NO se actualiza automáticamente
        """
        # Verifica si existe un trazador activo
        # Esto previene errores al intentar eliminar un trazador inexistente
        if self._traceid is not None:
            # Elimina el trazador de la variable de valor
            # Esto desactiva la actualización automática del texto
            self._variable.trace_remove("write", self._traceid)

        # Restablece el identificador a None
        # Esto se hace siempre, independientemente de si había un trazador o no
        # Permite que una futura llamada a _set_mask() configure un nuevo trazador
        self._traceid = None

    def _on_theme_change(self, *_):
        """
        Maneja eventos de cambio de tema o configuración en el widget FloodGauge.

        Este método se activa cuando ocurre un evento de cambio de tema o de configuración
        del widget. Su propósito es asegurar que el texto se mantenga correctamente visualizado
        a pesar de los cambios visuales en el tema o la configuración.

        El método simplemente obtiene el valor actual del texto y llama a _set_widget_text()
        para refrescar la visualización manteniendo el contenido original.

        Parámetros:
        ----------
        self : FloodGauge
            La instancia del widget
        *_ : cualquier
            Parámetros adicionales que se ignoran (permite usar el método como callback de eventos)

        Retorno:
        -------
        None
            Este método no devuelve ningún valor, solo actualiza el widget visualmente.

        Notas:
        -----
        - Este método debe estar vinculado a eventos como "<<ThemeChanged>>" y "<<Configure>>"
        - Solo refresca la visualización, no cambia el contenido del texto
        - Utiliza directamente self._textvariable, sin considerar si hay una máscara activa

        Ejemplos:
        --------
        # Vinculación típica en el constructor
        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)

        # El método será llamado automáticamente cuando ocurran estos eventos
        """
        # Obtiene el valor actual del texto almacenado en la variable
        # Por ejemplo, si self._textvariable contiene "Cargando...",
        # text será "Cargando..."
        text = self._textvariable.get()

        # Llama al método que actualiza la visualización del texto
        # Este método se encargará de aplicar la fuente y el estilo correctos
        # manteniendo el contenido original del texto
        self._set_widget_text(text)

    def _configure_get(self, cnf):
        """
        Obtiene el valor actual de una opción de configuración específica del widget.

        Este método implementa el mecanismo interno que permite recuperar los valores
        de las opciones de configuración, tanto las personalizadas de FloodGauge como
        las estándar heredadas de ttk.Progressbar. Es parte del sistema que soporta
        los métodos públicos `cget` y `configure` para consultar opciones.

        Maneja específicamente las opciones personalizadas:
        - "value": Valor numérico actual de la barra de progreso
        - "text": Texto mostrado actualmente en el widget
        - "bootstyle": Estilo visual aplicado al widget
        - "mask": Plantilla de formato para actualización automática de texto
        - "font": Especificación de fuente para el texto

        Para opciones estándar no listadas arriba, delega a la clase base.

        Parámetros:
        ----------
        cnf : str
            Nombre de la opción de configuración a consultar

        Retorna:
        -------
        various
            El valor actual de la opción solicitada. El tipo depende de la opción:
            - Para "value": int/float
            - Para "text", "bootstyle", "mask", "font": str u otro tipo específico
            - Para otras opciones: El tipo definido por la clase base

        Ejemplos:
        --------
        # Interno: cuando se llama a widget.cget("value") o widget["value"]
        # se invoca este método con cnf="value"
        # Devuelve el valor numérico actual, por ejemplo: 45

        # Interno: cuando se llama a widget.cget("text") o widget["text"]
        # se invoca este método con cnf="text"
        # Devuelve el texto actual, por ejemplo: "Cargando datos..."
        """
        # Opciones personalizadas de FloodGauge

        # Valor numérico de la barra de progreso
        if cnf == "value":
            return self._variable.get()  # Ej: 45

        # Texto mostrado en el widget
        if cnf == "text":
            return self._textvariable.get()  # Ej: "Cargando..."

        # Estilo visual del widget
        if cnf == "bootstyle":
            return self._bootstyle  # Ej: "success"

        # Plantilla de formato para texto dinámico
        if cnf == "mask":
            return self._mask  # Ej: "{}%" o None

        # Fuente para el texto
        if cnf == "font":
            return self._font  # Ej: "helvetica 10"

        # Delegar a la clase base para opciones estándar
        else:
            return super(ttk.Progressbar, self).configure(cnf=cnf)
            # Ej: para cnf="length" podría devolver 100

    def _configure_set(self, **kwargs):
        """
        Configura las opciones del widget FloodGauge basándose en los parámetros proporcionados.

        Este método implementa el mecanismo interno que permite modificar las opciones de
        configuración, tanto las personalizadas de FloodGauge como las estándar heredadas
        de ttk.Progressbar. Es parte del sistema que soporta el método público `configure`
        para establecer opciones.

        Maneja específicamente las opciones personalizadas:
        - "value": Valor numérico de la barra de progreso
        - "text": Texto a mostrar en el widget
        - "bootstyle": Estilo visual a aplicar
        - "mask": Plantilla de formato para actualización automática de texto
        - "font": Especificación de fuente para el texto
        - "variable": Variable tkinter externa para el valor
        - "textvariable": Variable tkinter externa para el texto

        Para opciones estándar, delega a la clase base, aunque con un comportamiento
        condicional dependiendo de la presencia de "variable" y "textvariable".

        Parámetros:
        ----------
        **kwargs : dict
            Diccionario de pares clave-valor con las opciones a configurar

        Retorna:
        -------
        None
            Este método no devuelve ningún valor, solo modifica el widget

        Notas:
        -----
        - Las opciones se procesan de forma independiente y pueden combinarse
        - Para "value" y "text", los valores se establecen en las variables tkinter
        - Para "bootstyle", "mask" y "font", los valores se asignan directamente
        - Para "variable" y "textvariable", se sustituyen las variables internas

        Ejemplos:
        --------
        # Interno: cuando se llama a widget.configure(value=75, text="Cargando")
        # se invoca este método con kwargs={"value": 75, "text": "Cargando"}

        # Interno: cuando se llama a widget.configure(bootstyle="success")
        # se invoca este método con kwargs={"bootstyle": "success"}
        """
        # Valor numérico de la barra de progreso
        if "value" in kwargs:
            # Actualiza el valor en la variable interna y elimina la opción de kwargs
            self._variable.set(kwargs.pop("value"))  # Ej: value=75

        # Texto a mostrar en el widget
        if "text" in kwargs:
            # Actualiza el texto en la variable interna y elimina la opción de kwargs
            self._textvariable.set(kwargs.pop("text"))  # Ej: text="Cargando..."

        # Estilo visual del widget
        if "bootstyle" in kwargs:
            # Actualiza el estilo interno pero NO elimina la opción de kwargs
            self._bootstyle = kwargs.get("bootstyle")  # Ej: bootstyle="success"

        # Plantilla de formato para texto dinámico
        if "mask" in kwargs:
            # Actualiza la máscara interna y elimina la opción de kwargs
            self._mask = kwargs.pop("mask")  # Ej: mask="{}%"

        # Fuente para el texto
        if "font" in kwargs:
            # Actualiza la fuente interna y elimina la opción de kwargs
            self._font = kwargs.pop("font")  # Ej: font="Arial 12"

        # Variable externa para el valor
        if "variable" in kwargs:
            # Sustituye la variable interna pero NO elimina la opción de kwargs
            self._variable = kwargs.get("variable")  # Ej: variable=IntVar(75)
            # Configura la clase base con todas las opciones restantes
            ttk.Progressbar.configure(self, cnf=None, **kwargs)

        # Variable externa para el texto
        if "textvariable" in kwargs:
            # Utiliza la propiedad para sustituir la variable y elimina la opción
            self.textvariable = kwargs.pop("textvariable")  # Ej: textvariable=StringVar("Nuevo")
        else:
            # Si no se procesó "textvariable", configura la clase base
            # Nota: Esto solo se ejecuta si también "variable" no estaba presente
            ttk.Progressbar.configure(self, cnf=None, **kwargs)

    def __getitem__(self, key: str):
        """
        Permite acceder a las opciones de configuración mediante la sintaxis de diccionario.

        Este método especial se invoca automáticamente cuando se usa la sintaxis widget["opción"].
        Proporciona una forma concisa de obtener el valor actual de cualquier opción de
        configuración del widget. Internamente, delega la funcionalidad al método _configure_get.

        Parámetros:
        ----------
        key : str
            El nombre de la opción de configuración a consultar

        Retorna:
        -------
        various
            El valor actual de la opción solicitada. El tipo depende de la opción:
            - Para "value": int/float
            - Para "text", "bootstyle", "mask", "font": str u otro tipo específico
            - Para otras opciones: El tipo definido por la clase base

        Ejemplos:
        --------
        # Obtener el valor actual de la barra de progreso
        value = widget["value"]  # Por ejemplo: 45

        # Obtener el texto actual
        text = widget["text"]    # Por ejemplo: "Cargando..."

        # Obtener el estilo
        style = widget["bootstyle"]  # Por ejemplo: "primary"
        """
        # Delega la consulta al método _configure_get
        # pasando key como el parámetro cnf
        return self._configure_get(cnf=key)

    def __setitem__(self, key: str, value):
        """
        Permite modificar las opciones de configuración mediante la sintaxis de diccionario.

        Este método especial se invoca automáticamente cuando se usa la sintaxis
        widget["opción"] = valor. Proporciona una forma concisa de establecer
        el valor de cualquier opción de configuración del widget. Internamente,
        delega la funcionalidad al método _configure_set.

        Parámetros:
        ----------
        key : str
            El nombre de la opción de configuración a modificar
        value : any
            El nuevo valor para la opción especificada

        Retorna:
        -------
        None
            Este método no devuelve ningún valor, solo modifica el widget

        Ejemplos:
        --------
        # Establecer el valor de la barra de progreso
        widget["value"] = 75

        # Establecer el texto
        widget["text"] = "Procesando..."

        # Establecer el estilo
        widget["bootstyle"] = "success"
        """
        # Crea un diccionario con el par key:value
        # y lo desempaqueta como argumentos de palabras clave
        # para llamar al método _configure_set
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        """
        Consulta o configura las opciones del widget FloodGauge.

        Este método proporciona una interfaz estándar de tkinter para obtener o establecer
        las opciones de configuración del widget. Su comportamiento depende de los parámetros:

        - Cuando se llama con cnf como una cadena (ej: configure("value")), devuelve el
          valor actual de esa opción específica.
        - Cuando se llama con cnf=None y argumentos de palabras clave, establece las
          opciones especificadas con los nuevos valores.

        Las opciones que puede manejar incluyen:
        - "value": Valor numérico de la barra de progreso
        - "text": Texto mostrado en el widget
        - "bootstyle": Estilo visual aplicado
        - "mask": Plantilla de formato para texto dinámico
        - "font": Especificación de fuente para el texto
        - "variable": Variable tkinter para el valor
        - "textvariable": Variable tkinter para el texto
        - Otras opciones estándar heredadas de ttk.Progressbar

        Parámetros:
        ----------
        cnf : str o dict, opcional
            Si es una cadena, especifica el nombre de la opción a consultar.
            Si es None (predeterminado), indica que se establecerán opciones.

        **kwargs : dict
            Argumentos de palabras clave que especifican opciones a configurar y sus valores.
            Solo se utilizan cuando cnf es None.

        Retorna:
        -------
        various o None
            Si se consulta una opción (cnf no es None), devuelve su valor actual.
            Si se establecen opciones (cnf es None), no devuelve un valor explícito.

        Ejemplos:
        --------
        # Consultar una opción
        value = widget.configure("value")  # Devuelve el valor actual

        # Establecer una opción
        widget.configure(value=75)  # Establece el valor a 75

        # Establecer múltiples opciones
        widget.configure(
            value=60,
            text="Procesando",
            bootstyle="info",
            font="Arial 12"
        )
        """
        # Si cnf no es None, estamos consultando opciones
        if cnf is not None:
            # Delegar a _configure_get para obtener el valor
            return self._configure_get(cnf)
        # Si cnf es None, estamos estableciendo opciones
        else:
            # Delegar a _configure_set para establecer los valores
            self._configure_set(**kwargs)

    @property
    def textvariable(self):

        """
        Obtiene la variable tkinter que controla el texto del widget.

        Esta propiedad devuelve la variable tkinter actual (normalmente StringVar)
        que está vinculada al texto mostrado en el widget. Los cambios en esta
        variable afectarán automáticamente al texto mostrado.

        Retorna:
        -------
        tkinter.StringVar o similar
            La variable de texto actual vinculada al widget

        Ejemplos:
        --------
        # Obtener la variable actual
        var = widget.textvariable

        # Cambiar el texto a través de la variable
        widget.textvariable.set("Nuevo texto")

        # Vincular la variable a otro widget
        another_widget["textvariable"] = widget.textvariable
        """
        # Devuelve directamente la variable de texto interna
        return self._textvariable

    @textvariable.setter
    def textvariable(self, value):
        """
        Establece una nueva variable tkinter para controlar el texto del widget.

        Esta propiedad permite cambiar la variable tkinter vinculada al texto
        del widget. Después de la asignación, el texto mostrado se actualizará
        inmediatamente para reflejar el valor actual de la nueva variable, y
        cualquier cambio futuro en esta variable afectará al texto mostrado.

        Parámetros:
        ----------
        value : tkinter.StringVar o similar
            La nueva variable de texto para vincular al widget

        Notas:
        -----
        - La visualización del texto se actualiza inmediatamente al valor actual
          de la nueva variable.
        - Cualquier vínculo a la variable anterior se pierde.
        - La nueva variable debe ser compatible con el método get().

        Ejemplos:
        --------
        # Crear una nueva variable
        nueva_var = tk.StringVar(value="Procesando...")

        # Asignar la nueva variable al widget
        widget.textvariable = nueva_var

        # El widget mostrará inmediatamente "Procesando..."
        # y seguirá los cambios futuros en nueva_var
        """
        # Asigna la nueva variable al atributo interno
        self._textvariable = value

        # Actualiza inmediatamente la visualización del texto
        # usando el valor actual de la nueva variable
        self._set_widget_text(self._textvariable.get())

    @property
    def variable(self):
        """
        Obtiene la variable tkinter que controla el valor numérico del widget.

        Esta propiedad devuelve la variable tkinter actual (normalmente IntVar o DoubleVar)
        que está vinculada al valor numérico mostrado en la barra de progreso. Los cambios
        en esta variable afectarán automáticamente al valor mostrado en la barra.

        Retorna:
        -------
        tkinter.Variable
            La variable numérica actual vinculada al widget, normalmente
            una instancia de tkinter.IntVar o tkinter.DoubleVar

        Ejemplos:
        --------
        # Obtener la variable actual
        var = widget.variable

        # Cambiar el valor a través de la variable
        widget.variable.set(75)

        # Vincular la variable a otro widget
        another_widget["variable"] = widget.variable
        """
        # Devuelve directamente la variable numérica interna
        return self._variable

    @variable.setter
    def variable(self, value):
        """
        Establece una nueva variable tkinter para controlar el valor numérico del widget.

        Esta propiedad permite cambiar la variable tkinter vinculada al valor numérico
        de la barra de progreso. Después de la asignación, la barra mostrará el valor
        actual de la nueva variable, y cualquier cambio futuro en esta variable
        afectará a la visualización de la barra.

        El método realiza una verificación para evitar actualizar la configuración
        del widget si la nueva variable es la misma que ya está configurada.

        Parámetros:
        ----------
        value : tkinter.Variable
            La nueva variable numérica para vincular al widget, normalmente
            una instancia de tkinter.IntVar o tkinter.DoubleVar

        Notas:
        -----
        - Si la nueva variable es diferente a la actual, se actualiza
          la configuración del widget base.
        - Cualquier vínculo a la variable anterior se pierde.
        - La nueva variable debe ser compatible con el método get().

        Ejemplos:
        --------
        # Crear una nueva variable
        nueva_var = tk.IntVar(value=75)

        # Asignar la nueva variable al widget
        widget.variable = nueva_var

        # La barra de progreso mostrará inmediatamente 75%
        # y seguirá los cambios futuros en nueva_var
        """
        # Asigna la nueva variable al atributo interno
        self._variable = value

        # Verifica si la variable configurada en el widget es diferente a la nueva
        # Esto evita llamadas innecesarias a configure
        if self.cget('variable') != value:
            # Actualiza la configuración del widget base con la nueva variable
            self.configure(variable=self._variable)