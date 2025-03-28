import ui.themeengine as ttk
from ui.themeengine import Bootstyle
from ui.themeengine.core.color import Colors
from ui.themeengine.utils.constants import *
from ui.themeengine.utils import utility

# floodgauge imports
import math

# meter imports
from PIL import Image, ImageTk, ImageDraw


# Valor para multiplicar la resolución de la imagen para suavizar el dibujo
M = 3  # Esta constante podría estar en otro lugar del framework, ajústala según sea necesario

class Meter(ttk.Frame):
    """
    Widget de medidor radial que visualiza valores como un arco circular o semicircular.

    El Meter es un widget flexible que puede mostrar el progreso de operaciones
    de larga duración o la cantidad de trabajo completado. También puede
    funcionar como un dial interactivo permitiendo al usuario ajustar valores.

    Este widget ofrece amplia personalización, desde la forma (círculo completo
    o semicírculo) hasta el estilo visual (indicador sólido o rayado), con
    múltiples opciones de etiquetado.

    Las variables se generan automáticamente para este widget y pueden
    accederse a través de los atributos `amountusedvar` y `amounttotalvar`.

    Parámetros:
    ----------
    master : Widget, opcional
        Widget padre que contendrá este medidor.

    bootstyle : str, opcional
        Estilo bootstrap para el color del indicador y texto central.
        Valores: primary, secondary, success, info, warning, danger, light, dark.
        Por defecto es DEFAULT.

    arcrange : int, opcional
        Rango del arco en grados. Si es None, se determina automáticamente según
        metertype (360° para 'full', 270° para 'semi').

    arcoffset : int, opcional
        Desplazamiento en grados del punto inicial del arco. Si es None, se determina
        automáticamente según metertype (-90° para 'full', 135° para 'semi').
        Un valor de 0 representa la posición "3 en punto".

    amounttotal : int, opcional
        Valor máximo del medidor. Por defecto es 100.

    amountused : int, opcional
        Valor actual del medidor. Por defecto es 0.

    wedgesize : int, opcional
        Tamaño en grados de la cuña indicadora alrededor del arco.
        Si es mayor que 0, esta cuña se centra en el valor actual.
        Por defecto es 0 (sin cuña).

    metersize : int, opcional
        Tamaño del medidor en píxeles (ancho y alto).
        Por defecto es 200.

    metertype : str, opcional
        Tipo de medidor: 'full' para círculo completo, 'semi' para semicírculo.
        Por defecto es FULL.

    meterthickness : int, opcional
        Grosor del indicador en píxeles. Por defecto es 10.

    showtext : bool, opcional
        Si se deben mostrar las etiquetas de texto. Por defecto es True.

    interactive : bool, opcional
        Si el usuario puede ajustar el valor con interacción del ratón.
        Por defecto es False.

    stripethickness : int, opcional
        Grosor de las rayas del indicador. Un valor de 0 muestra un indicador
        sólido, valores mayores crean rayas. Por defecto es 0.

    textleft : str, opcional
        Texto a mostrar a la izquierda del valor central.
        Útil para símbolos como '$'. Por defecto es None.

    textright : str, opcional
        Texto a mostrar a la derecha del valor central.
        Útil para símbolos como '%'. Por defecto es None.

    textfont : str, opcional
        Fuente para el texto central. Por defecto es "-size 20 -weight bold".

    subtext : str, opcional
        Texto adicional debajo del valor central. Por defecto es None.

    subtextstyle : str, opcional
        Estilo para el subtexto. Por defecto es DEFAULT.

    subtextfont : str, opcional
        Fuente para el subtexto. Por defecto es "-size 10".

    stepsize : int, opcional
        Incremento para ajuste interactivo y método step(). Por defecto es 1.

    Métodos:
    -------
    configure(cnf=None, **kwargs)
        Configura o consulta las opciones del widget.

    step(delta=1)
        Incrementa o decrementa el valor del indicador según la dirección actual.
        Implementa un comportamiento de "rebote" en los límites.

    Ejemplos:
    --------
    ```python
    import ui.themeengine as ttk
    from ui.themeengine.utils.constants import *

    app = ttk.Window()

    # Medidor básico
    meter = ttk.Meter(app)
    meter.pack(padx=10, pady=10)

    # Medidor semicircular con estilo
    meter_semi = ttk.Meter(
        app,
        metertype='semi',
        bootstyle='success',
        amountused=75,
        meterthickness=15,
        subtext='Batería',
        textright='%'
    )
    meter_semi.pack(padx=10, pady=10)

    # Medidor interactivo con rayas
    meter_interactive = ttk.Meter(
        app,
        interactive=True,
        stripethickness=3,
        bootstyle='danger',
        textleft='$',
        amounttotal=1000,
        amountused=650
    )
    meter_interactive.pack(padx=10, pady=10)

    # Actualizar el valor manualmente
    meter.configure(amountused=60)

    # Incrementar el valor usando step()
    meter_semi.step(5)

    app.mainloop()

    """

    def __init__(
        self,
        master=None,
        bootstyle=DEFAULT,
        arcrange=None,
        arcoffset=None,
        amounttotal=100,
        amountused=0,
        wedgesize=0,
        metersize=200,
        metertype=FULL,
        meterthickness=10,
        showtext=True,
        interactive=False,
        stripethickness=0,
        textleft=None,
        textright=None,
        textfont="-size 20 -weight bold",
        subtext=None,
        subtextstyle=DEFAULT,
        subtextfont="-size 10",
        stepsize=1,
        **kwargs,
    ):
        """Inicializa un nuevo widget de medidor radial.

        Este constructor crea y configura un medidor radial personalizado que puede
        mostrar progreso o valores como un arco visual. El medidor puede configurarse
        como un círculo completo o semicírculo, con diferentes opciones de visualización
        y estilo.

        Args:
            master (Widget, opcional):
                El widget padre que contendrá este medidor. Por defecto es None.

            bootstyle (str, opcional):
                El estilo de bootstrap para el color del indicador y texto central.
                Valores posibles: 'primary', 'secondary', 'success', 'info', 'warning',
                'danger', 'light', 'dark'. Por defecto es DEFAULT.

            arcrange (int, opcional):
                El rango del arco en grados desde el inicio hasta el final.
                Si es None, se determinará según el metertype (360° para 'full', 270° para 'semi').

            arcoffset (int, opcional):
                El desplazamiento en grados del punto inicial del arco.
                Si es None, se determinará según el metertype (-90° para 'full', 135° para 'semi').
                Un valor de 0 representa la posición "3 en punto".

            amounttotal (int, opcional):
                El valor máximo del medidor. Por defecto es 100.

            amountused (int, opcional):
                El valor actual del medidor. Por defecto es 0.

            wedgesize (int, opcional):
                El tamaño en grados de la cuña indicadora alrededor del arco.
                Si es mayor que 0, esta cuña se centra en el valor actual.
                Por defecto es 0 (sin cuña).

            metersize (int, opcional):
                El tamaño del medidor en píxeles (ancho y alto).
                Por defecto es 200.

            metertype (str, opcional):
                El tipo de medidor: 'full' para círculo completo, 'semi' para semicírculo.
                Por defecto es FULL.

            meterthickness (int, opcional):
                El grosor del indicador en píxeles. Por defecto es 10.

            showtext (bool, opcional):
                Si se deben mostrar las etiquetas de texto. Por defecto es True.

            interactive (bool, opcional):
                Si el usuario puede ajustar el valor con interacción del ratón.
                Por defecto es False.

            stripethickness (int, opcional):
                El grosor de las rayas del indicador. Un valor de 0 muestra un indicador
                sólido, valores mayores crean rayas. Por defecto es 0.

            textleft (str, opcional):
                Texto a mostrar a la izquierda del valor central. Por defecto es None.

            textright (str, opcional):
                Texto a mostrar a la derecha del valor central. Por defecto es None.

            textfont (str, opcional):
                Fuente para el texto central. Por defecto es "-size 20 -weight bold".

            subtext (str, opcional):
                Texto adicional debajo del valor central. Por defecto es None.

            subtextstyle (str, opcional):
                Estilo para el subtexto. Por defecto es DEFAULT.

            subtextfont (str, opcional):
                Fuente para el subtexto. Por defecto es "-size 10".

            stepsize (int, opcional):
                Incremento para ajuste interactivo. Por defecto es 1.

            **kwargs:
                Argumentos adicionales que se pasan al widget Frame base.

        Ejemplos:
            # Crear un medidor básico
            meter = Meter(root)
            meter.pack(padx=10, pady=10)

            # Crear un medidor semicircular con valor inicial 75
            meter = Meter(
                root,
                metertype='semi',
                bootstyle='success',
                amountused=75,
                meterthickness=15
            )

            # Crear un medidor interactivo con rayas
            meter = Meter(
                root,
                interactive=True,
                stripethickness=3,
                textright='%',
                bootstyle='danger'
            )
        """
        # Inicializa un nuevo widget de medidor radial con las configuraciones especificadas.
        #
        # Esta sección del constructor inicializa la clase base Frame y configura las variables
        # tkinter necesarias para almacenar el estado del medidor y permitir actualizaciones
        # reactivas de la interfaz.
        super().__init__(master=master, **kwargs)
        # Las variables tkinter creadas son:
        # - amountusedvar: Almacena el valor actual del medidor y desencadena
        #                 automáticamente actualizaciones visuales cuando cambia.
        # - amounttotalvar: Almacena el valor máximo del medidor.
        # - labelvar: Almacena el texto suplementario que puede mostrarse con el medidor.

        # Variables tkinter para almacenar y observar el estado del medidor
        self.amountusedvar = ttk.IntVar(value=amountused)  # Variable para el valor actual
        self.amountusedvar.trace_add("write", self._draw_meter)  # Configura observador para actualización automática
        self.amounttotalvar = ttk.IntVar(value=amounttotal)  # Variable para el valor máximo
        self.labelvar = ttk.StringVar(value=subtext)  # Variable para el texto suplementario

        # Configuración de atributos de apariencia y comportamiento
        self._set_arc_offset_range(metertype, arcoffset, arcrange)  # Configura el rango y offset del arco
        self._towardsmaximum = True  # Dirección inicial para el método step()
        self._metersize = utility.scale_size(self, metersize)  # Escala el tamaño según la configuración del sistema
        self._meterthickness = utility.scale_size(self, meterthickness)  # Escala el grosor según la configuración

        # Inicializa un nuevo widget de medidor radial con las configuraciones especificadas.
        #
        # En esta sección se configuran todos los atributos internos que determinan la apariencia
        # y el comportamiento del medidor. Algunos valores como el tamaño y grosor son escalados
        # según la configuración del sistema para garantizar una apariencia consistente en
        # diferentes entornos.
        #
        # Los atributos configurados incluyen:
        # - Propiedades del arco (offset y rango) según el tipo de medidor.
        # - Tamaño y grosor del medidor, escalados según la configuración del sistema.
        # - Propiedades visuales como grosor de rayas, visibilidad de texto, fuentes, etc.
        # - Configuraciones de interactividad para el ajuste mediante ratón.
        #
        # Estos atributos se utilizan posteriormente para construir y renderizar los componentes
        # visuales del medidor.
        #
        # Almacenamiento de propiedades de apariencia
        self._stripethickness = stripethickness  # Grosor de las rayas (0 para indicador sólido)
        self._showtext = showtext  # Mostrar etiquetas de texto
        self._wedgesize = wedgesize  # Tamaño de la cuña indicadora (en grados)
        self._stepsize = stepsize  # Incremento para el ajuste interactivo
        self._textleft = textleft  # Texto a la izquierda del valor central
        self._textright = textright  # Texto a la derecha del valor central
        self._textfont = textfont  # Fuente para el texto central
        self._subtext = subtext  # Texto suplementario
        self._subtextfont = subtextfont  # Fuente para el subtexto
        self._subtextstyle = subtextstyle  # Estilo para el subtexto
        self._bootstyle = bootstyle  # Estilo de color general

        # Configuración de interactividad
        self._interactive = interactive  # Habilitar interacción con el ratón
        self._bindids = {}  # Diccionario para almacenar IDs de eventos vinculados

        # Configurar estructura visual del widget
        self._setup_widget()

    def _setup_widget(self):
        """
        Configura la estructura visual del widget Meter.

        Este método crea y configura todos los componentes visuales necesarios para el medidor:
        - El frame principal que contendrá todos los elementos.
        - El label para mostrar la imagen del indicador del medidor.
        - El frame y labels para los elementos de texto (izquierdo, central y derecho).
        - El label para el texto suplementario.

        También establece los enlaces a eventos necesarios para responder a cambios de tema,
        configuración e interacción del usuario. Finalmente, inicia el proceso de dibujo
        del medidor y establece la geometría y visibilidad de los componentes.

        Este método se llama automáticamente durante la inicialización del widget y no
        debería ser llamado directamente por el usuario.
        """
        # Crear el frame principal que contendrá todos los elementos
        self.meterframe = ttk.Frame(
            master=self, width=self._metersize, height=self._metersize
        )

        # Crear el label para la imagen del indicador
        self.indicator = ttk.Label(self.meterframe)

        # Crear el frame para los elementos de texto
        self.textframe = ttk.Frame(self.meterframe)

        # Crear y configurar el label para el texto izquierdo
        self.textleft = ttk.Label(
            master=self.textframe,
            text=self._textleft,  # Texto a la izquierda (ej: "$")
            font=self._subtextfont,  # Fuente para texto secundario
            bootstyle=(self._subtextstyle, "metersubtxt"),  # Estilo visual
            anchor=S,  # Alineación en la parte inferior
            padding=(0, 5),  # Relleno superior de 5 píxeles
        )

        # Crear y configurar el label para el valor central
        self.textcenter = ttk.Label(
            master=self.textframe,
            textvariable=self.amountusedvar,  # Vinculado al valor actual
            bootstyle=(self._bootstyle, "meter"),  # Estilo principal
            font=self._textfont,  # Fuente para texto principal
        )

        # Crear y configurar el label para el texto derecho
        self.textright = ttk.Label(
            master=self.textframe,
            text=self._textright,  # Texto a la derecha (ej: "%")
            font=self._subtextfont,  # Fuente para texto secundario
            bootstyle=(self._subtextstyle, "metersubtxt"),  # Estilo visual
            anchor=S,  # Alineación en la parte inferior
            padding=(0, 5),  # Relleno superior de 5 píxeles
        )

        # Crear y configurar el label para el texto suplementario
        self.subtext = ttk.Label(
            master=self.meterframe,
            text=self._subtext,  # Texto suplementario
            bootstyle=(self._subtextstyle, "metersubtxt"),  # Estilo visual
            font=self._subtextfont,  # Fuente para texto secundario
        )

        # Vincular eventos para responder a cambios de tema y configuración
        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)

        # Configurar eventos para interactividad (si está habilitada)
        self._set_interactive_bind()

        # Dibujar el medidor
        self._draw_base_image()  # Crear imagen base
        self._draw_meter()  # Dibujar indicador según valor actual

        # Establecer geometría y visibilidad
        self.indicator.place(x=0, y=0)  # Posicionar indicador
        self.meterframe.pack()  # Empaquetar frame principal
        self._set_show_text()  # Configurar visibilidad de textos

    def _set_widget_colors(self):
        """
        Configura los colores del medidor basados en el estilo bootstrap seleccionado.

        Este método determina y asigna los colores apropiados para el primer plano,
        fondo y canal del medidor según el tema y estilo activos. Consulta el
        sistema de estilos TTK para obtener los colores definidos para el estilo
        actual y los asigna a atributos internos que serán utilizados posteriormente
        en los métodos de dibujo.

        Atributos establecidos:
            _meterforeground: Color para el indicador del medidor.
            _meterbackground: Color para el fondo del medidor (ligeramente oscurecido).
            _metertrough: Color para el canal del medidor.

        Notas:
            El color de fondo (_meterbackground) se ajusta reduciendo su valor (brillo)
            en un 10% para crear un mejor contraste visual.
        """
        # Crear la tupla de componentes del estilo (color, tipo, clase)
        bootstyle = (self._bootstyle, "meter", "label")  # Ej: ("success", "meter", "label")

        # Generar el nombre de estilo TTK a partir de los componentes
        ttkstyle = Bootstyle.ttkstyle_name(string="-".join(bootstyle))  # Ej: "success.Meter.TLabel"

        # Consultar los colores definidos para el estilo TTK
        textcolor = self._lookup_style_option(ttkstyle, "foreground")  # Color del texto/indicador
        background = self._lookup_style_option(ttkstyle, "background")  # Color del fondo
        troughcolor = self._lookup_style_option(ttkstyle, "space")  # Color del canal

        # Asignar colores a atributos internos para uso posterior
        self._meterforeground = textcolor  # Color para el indicador (sin modificar)
        self._meterbackground = Colors.update_hsv(background, vd=-0.1)  # Fondo ligeramente oscurecido
        self._metertrough = troughcolor  # Color para el canal (sin modificar)

    def _set_meter_text(self):
        """
        Configura y organiza las etiquetas de texto del widget Meter.

        Este método coordina la configuración y posicionamiento de todas las etiquetas
        de texto del medidor, incluyendo las etiquetas principales (izquierda, centro,
        derecha) y el subtexto. Delega las tareas específicas a métodos más
        especializados para mantener el código modular y mantenible.

        La configuración de texto se basa en los siguientes atributos:
        - _showtext: Determina si se muestran las etiquetas de texto principales.
        - _textleft: Texto a mostrar a la izquierda del valor central (ej: "$").
        - _textright: Texto a mostrar a la derecha del valor central (ej: "%").
        - _subtext: Texto adicional a mostrar debajo de las etiquetas principales.
        - _subtextfont: Fuente para el subtexto, también determina su visibilidad.

        El método no acepta parámetros adicionales ni devuelve valores.

        Ejemplo de resultado visual:
        - Con _textleft="$", amountusedvar=75, _textright="%", _subtext="Progreso":
          Se mostraría: "$ 75 %" y debajo "Progreso"
        """
        # Configurar visibilidad y posicionamiento de etiquetas principales
        self._set_show_text()

        # Configurar visibilidad y posicionamiento del subtexto
        self._set_subtext()

    def _set_subtext(self):
        """
        Configura la posición y visibilidad del subtexto en el medidor.

        Este método determina si se debe mostrar el subtexto basándose en la existencia
        de una fuente definida para el mismo (_subtextfont). Si se debe mostrar, posiciona
        el subtexto en la ubicación adecuada dependiendo de si las etiquetas principales
        están visibles (_showtext).

        Si las etiquetas principales están visibles, el subtexto se posiciona debajo de
        ellas al 60% de la altura relativa del medidor. Si no están visibles, el subtexto
        se posiciona en el centro del medidor (50% de la altura relativa).

        El método no tiene efecto si no hay una fuente definida para el subtexto.

        Nota:
            Este método no verifica si _subtext tiene contenido, solo si _subtextfont
            está definido. Esto podría llevar a mostrar un subtexto vacío si _subtextfont
            está definido pero _subtext está vacío.

        Dependencias:
            - _subtextfont: Determina si se debe mostrar el subtexto.
            - _showtext: Determina la posición vertical del subtexto.
            - subtext: Widget que muestra el subtexto.
        """
        # Verificar si existe una fuente para el subtexto
        if self._subtextfont:
            # Determinar la posición según si las etiquetas principales están visibles
            if self._showtext:
                # Posicionar debajo de las etiquetas principales
                self.subtext.place(relx=0.5, rely=0.6, anchor=CENTER)
            else:
                # Posicionar en el centro del medidor
                self.subtext.place(relx=0.5, rely=0.5, anchor=CENTER)

    def _set_show_text(self):
        """
        Configura la visibilidad y posicionamiento de los elementos de texto del medidor.

        Este método gestiona la visibilidad y posicionamiento de todas las etiquetas de
        texto del medidor. Primero limpia cualquier configuración previa de empaquetado
        para evitar conflictos. Luego, si las etiquetas de texto deben mostrarse
        (_showtext=True), posiciona el marco de texto en el lugar adecuado según si hay
        subtexto definido o no. Finalmente, llama a métodos específicos para configurar
        cada una de las etiquetas individuales (izquierda, centro, derecha) y el subtexto.

        El posicionamiento del marco de texto se ajusta verticalmente:
        - Si hay subtexto, se posiciona ligeramente por encima del centro (45% de altura)
          para dejar espacio al subtexto.
        - Si no hay subtexto, se posiciona exactamente en el centro (50% de altura).

        En ambos casos, el marco se centra horizontalmente (50% de anchura) y se ancla
        desde su centro (anchor=CENTER).

        Si _showtext es False, el marco de texto no se posiciona y permanece oculto,
        aunque los métodos para configurar las etiquetas individuales son llamados
        igualmente (estos métodos deben verificar _showtext para determinar
        si muestran sus respectivas etiquetas).

        Dependencias:
            - _showtext: Determina si se muestran las etiquetas de texto.
            - _subtext: Influye en la posición vertical del marco de texto.
            - Métodos: _set_text_left(), _set_text_center(), _set_text_right(), _set_subtext()
        """
        # Limpiar cualquier configuración previa de empaquetado
        self.textframe.pack_forget()  # Marco principal de texto
        self.textcenter.pack_forget()  # Etiqueta para el valor central
        self.textleft.pack_forget()  # Etiqueta para texto a la izquierda
        self.textright.pack_forget()  # Etiqueta para texto a la derecha
        self.subtext.pack_forget()  # Etiqueta para el subtexto

        # Verificar si se deben mostrar las etiquetas de texto
        if self._showtext:
            # Posicionar el marco de texto según si hay subtexto o no
            if self._subtext:
                # Posicionar ligeramente por encima del centro si hay subtexto
                self.textframe.place(relx=0.5, rely=0.45, anchor=CENTER)
            else:
                # Posicionar en el centro exacto si no hay subtexto
                self.textframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Configurar cada etiqueta individual
        self._set_text_left()  # Configura la etiqueta izquierda (ej: "$")
        self._set_text_center()  # Configura la etiqueta central (el valor)
        self._set_text_right()  # Configura la etiqueta derecha (ej: "%")
        self._set_subtext()  # Configura el subtexto

    def _set_text_left(self):
        """
        Configura y muestra (cuando corresponde) la etiqueta de texto izquierda del medidor.

        Este método determina si se debe mostrar la etiqueta de texto izquierda basándose
        en dos condiciones: si las etiquetas de texto en general deben mostrarse (_showtext)
        y si hay texto definido para la etiqueta izquierda (_textleft).

        Si ambas condiciones son verdaderas, empaqueta la etiqueta en el lado izquierdo
        del contenedor (textframe) con relleno vertical. Si alguna de las condiciones
        es falsa, el método termina sin hacer nada y la etiqueta no se muestra.

        Este método es llamado por _set_show_text() como parte de la configuración
        general de las etiquetas de texto del medidor.

        Dependencias:
            - _showtext: Determina si se muestran las etiquetas de texto en general.
            - _textleft: Contiene el texto para la etiqueta izquierda.
            - textleft: Widget de etiqueta que muestra el texto izquierdo.

        Ejemplo:
            Si _showtext=True y _textleft="$", la etiqueta mostrará "$" a la
            izquierda del valor central del medidor.
        """
        # Verificar si se debe mostrar la etiqueta izquierda
        if self._showtext and self._textleft:
            # Empaquetar la etiqueta en el lado izquierdo con relleno vertical
            self.textleft.pack(side=LEFT, fill=Y)

    def _set_text_center(self):
        """
        Configura y muestra (cuando corresponde) la etiqueta de texto central del medidor.

        Este método determina si se debe mostrar la etiqueta de texto central basándose
        en si las etiquetas de texto en general deben mostrarse (_showtext). A diferencia
        de otras etiquetas, no verifica si hay contenido para mostrar, asumiendo que
        la etiqueta central (que muestra el valor actual del medidor) siempre debe
        mostrarse si las etiquetas están habilitadas.

        Si _showtext es verdadero, empaqueta la etiqueta en el lado izquierdo
        del contenedor (textframe) con relleno vertical. Si _showtext es falso,
        el método termina sin hacer nada y la etiqueta no se muestra.

        La etiqueta central está vinculada a la variable tkinter amountusedvar,
        que muestra el valor actual del medidor.

        Este método es llamado por _set_show_text() como parte de la configuración
        general de las etiquetas de texto del medidor.

        Dependencias:
            - _showtext: Determina si se muestran las etiquetas de texto en general.
            - textcenter: Widget de etiqueta que muestra el valor central.
            - amountusedvar: Variable tkinter que contiene el valor actual del medidor.

        Ejemplo:
            Si _showtext=True y amountusedvar=75, la etiqueta mostrará "75"
            en el centro del medidor.
        """
        # Verificar si se deben mostrar las etiquetas de texto
        if self._showtext:
            # Empaquetar la etiqueta central con relleno vertical
            self.textcenter.pack(side=LEFT, fill=Y)

    def _set_text_right(self):
        """
        Configura y muestra (cuando corresponde) la etiqueta de texto derecha del medidor.

        Este método actualiza incondicionalmente el texto de la etiqueta derecha con
        el valor actual de _textright. Luego determina si se debe mostrar la etiqueta
        basándose en dos condiciones: si las etiquetas de texto en general deben mostrarse
        (_showtext) y si hay texto definido para la etiqueta derecha (_textright).

        Si ambas condiciones son verdaderas, empaqueta la etiqueta en el lado derecho
        del contenedor (textframe) con relleno vertical. Si alguna de las condiciones
        es falsa, el método termina sin empaquetar la etiqueta y esta no se muestra.

        A diferencia de las etiquetas izquierda y central que usan side=LEFT, esta etiqueta
        usa side=RIGHT, lo que asegura que aparezca en el lado derecho del contenedor
        independientemente del orden de empaquetado.

        Este método es llamado por _set_show_text() como parte de la configuración
        general de las etiquetas de texto del medidor.

        Dependencias:
            - _showtext: Determina si se muestran las etiquetas de texto en general.
            - _textright: Contiene el texto para la etiqueta derecha.
            - textright: Widget de etiqueta que muestra el texto derecho.

        Ejemplo:
            Si _showtext=True y _textright="%", la etiqueta mostrará "%" a la
            derecha del valor central del medidor.
        """
        # Actualizar el texto de la etiqueta incondicionalmente
        self.textright.configure(text=self._textright)

        # Verificar si se debe mostrar la etiqueta derecha
        if self._showtext and self._textright:
            # Empaquetar la etiqueta en el lado derecho con relleno vertical
            self.textright.pack(side=RIGHT, fill=Y)

    def _set_interactive_bind(self):
        """
        Configura o elimina los enlaces de eventos para la interactividad del medidor.

        Este método gestiona el ciclo de vida completo de los enlaces de eventos para
        la interactividad del medidor. Dependiendo del valor de _interactive, enlaza
        o elimina eventos de ratón que permiten al usuario ajustar el valor del medidor
        mediante interacción directa.

        Los eventos que se enlazan son:
        - <B1-Motion>: Se dispara cuando el usuario mueve el ratón mientras mantiene
                        presionado el botón izquierdo.
        - <Button-1>: Se dispara cuando el usuario presiona el botón izquierdo del ratón.

        Ambos eventos se manejan con el método _on_dial_interact, que actualiza el valor
        del medidor según la posición del ratón.

        El método almacena los identificadores de los enlaces en _bindids para poder
        eliminarlos posteriormente cuando la interactividad se desactiva.

        Precondiciones:
            - El widget indicator debe estar inicializado.
            - El atributo _interactive debe estar establecido.
            - El atributo _bindids debe estar inicializado como un diccionario.
            - El método _on_dial_interact debe estar implementado.

        Comportamiento:
            - Si _interactive es True, se enlazan los eventos y se almacenan sus identificadores.
            - Si _interactive es False y hay enlaces previos, se eliminan y se limpia _bindids.
        """
        # Definir las secuencias de eventos que se enlazarán
        seq1 = "<B1-Motion>"  # Movimiento del ratón con botón izquierdo presionado
        seq2 = "<Button-1>"  # Clic con botón izquierdo

        # Si el medidor debe ser interactivo, enlazar eventos
        if self._interactive:
            # Enlazar el evento de movimiento con botón presionado
            self._bindids[seq1] = self.indicator.bind(
                seq1, self._on_dial_interact
            )
            # Enlazar el evento de clic
            self._bindids[seq2] = self.indicator.bind(
                seq2, self._on_dial_interact
            )
            # Terminar para evitar ejecutar el código de eliminación
            return

        # Si existen enlaces previos, eliminarlos
        if seq1 in self._bindids:
            # Eliminar el enlace de movimiento
            self.indicator.unbind(seq1, self._bindids.get(seq1))
            # Eliminar el enlace de clic
            self.indicator.unbind(seq2, self._bindids.get(seq2))
            # Limpiar el diccionario de identificadores
            self._bindids.clear()

    def _set_arc_offset_range(self, metertype, arcoffset, arcrange):
        """
        Configura los parámetros geométricos del arco del medidor según su tipo.

        Este método establece el desplazamiento inicial y el rango del arco que forman
        el medidor, adaptándolos según el tipo de medidor (semicircular o círculo completo).
        Permite personalizar estos valores o usar valores predeterminados cuidadosamente
        seleccionados para crear visualizaciones estéticamente agradables.

        Parámetros:
            metertype: Tipo de medidor, puede ser SEMI (semicírculo) u otro valor
                       (típicamente FULL para círculo completo).
            arcoffset: Desplazamiento inicial del arco en grados (0° está en la posición
                       "3 en punto"). Si es None, se usará un valor predeterminado
                       según el tipo de medidor.
            arcrange:  Rango total del arco en grados. Si es None, se usará un valor
                       predeterminado según el tipo de medidor.

        Valores predeterminados:
            Para un medidor semicircular (SEMI):
                - arcoffset: 135° (posiciona el inicio del arco en la parte inferior izquierda)
                - arcrange: 270° (crea un arco que abarca tres cuartos de círculo)

            Para un medidor de círculo completo (FULL):
                - arcoffset: -90° (posiciona el inicio del arco en la parte superior)
                - arcrange: 360° (crea un arco que forma un círculo completo)

        Atributos modificados:
            _arcoffset: El desplazamiento inicial del arco en grados.
            _arcrange: El rango total del arco en grados.
            _metertype: El tipo de medidor proporcionado.

        Ejemplos:
            Medidor semicircular con valores predeterminados:
                _set_arc_offset_range(SEMI, None, None)
                # Resultado: _arcoffset=135, _arcrange=270

            Medidor de círculo completo con rango personalizado:
                _set_arc_offset_range(FULL, None, 180)
                # Resultado: _arcoffset=-90, _arcrange=180
        """
        # Configurar valores para un medidor semicircular
        if metertype == SEMI:
            # Establecer desplazamiento: 135° por defecto o valor proporcionado
            self._arcoffset = 135 if arcoffset is None else arcoffset
            # Establecer rango: 270° por defecto o valor proporcionado
            self._arcrange = 270 if arcrange is None else arcrange
        # Configurar valores para un medidor de círculo completo
        else:
            # Establecer desplazamiento: -90° por defecto o valor proporcionado
            self._arcoffset = -90 if arcoffset is None else arcoffset
            # Establecer rango: 360° por defecto o valor proporcionado
            self._arcrange = 360 if arcrange is None else arcrange

        # Almacenar el tipo de medidor para referencia futura
        self._metertype = metertype

    def _draw_meter(self, *_):
        """
        Dibuja o actualiza la representación visual del medidor radial.

        Este método genera una imagen que representa el estado actual del medidor,
        determinando si debe dibujarse un medidor con rayas o sólido según la
        configuración. Luego, aplica la imagen generada al widget indicador para
        su visualización.

        El método acepta argumentos variables (*_) pero no los utiliza, lo que permite
        que sea llamado como un callback para eventos como cambios en las variables tkinter.

        Proceso:
        1. Crea una copia de la imagen base para preservar el original.
        2. Determina si se debe dibujar un medidor rayado o sólido.
        3. Delega el dibujo específico al método apropiado.
        4. Redimensiona la imagen al tamaño correcto.
        5. Convierte la imagen a un formato compatible con tkinter.
        6. Muestra la imagen en el widget indicador.

        Precondiciones:
        - El método _draw_base_image() debe haber sido llamado previamente.
        - Los atributos _stripethickness y _metersize deben estar establecidos.
        - El widget indicator debe estar inicializado.

        Dependencias:
        - Métodos _draw_striped_meter() y _draw_solid_meter() para el dibujo específico.
        - Bibliotecas PIL/Pillow para manipulación de imágenes.

        Parámetros:
            *_: Argumentos variables no utilizados, permite que el método sea
                utilizado como callback para eventos.
        """
        # Crear una copia de la imagen base para preservar el original
        img = self._base_image.copy()

        # Crear un objeto de dibujo para modificar la imagen
        draw = ImageDraw.Draw(img)

        # Determinar si se debe dibujar un medidor rayado o sólido
        if self._stripethickness > 0:
            # Dibujar un medidor rayado si el grosor de las rayas es mayor que 0
            self._draw_striped_meter(draw)
        else:
            # Dibujar un medidor sólido si el grosor de las rayas es 0
            self._draw_solid_meter(draw)

        # Redimensionar la imagen, convertirla a formato tkinter y almacenar la referencia
        self._meterimage = ImageTk.PhotoImage(
            img.resize((self._metersize, self._metersize), Image.BICUBIC)
        )

        # Configurar el widget indicador para mostrar la nueva imagen
        self.indicator.configure(image=self._meterimage)

    def _draw_base_image(self):
        """
        Dibuja la imagen base del medidor para ser usada en actualizaciones posteriores.

        Este método crea una nueva imagen que servirá como base para representaciones
        posteriores del medidor. Configura los colores del widget, crea un lienzo de alta
        resolución y dibuja el canal (trough) del medidor según la configuración actual.

        El canal puede ser sólido o rayado dependiendo del valor de _stripethickness:
        - Si _stripethickness > 0, el canal se dibuja como una serie de arcos pequeños (rayado).
        - Si _stripethickness = 0, el canal se dibuja como un único arco continuo (sólido).

        La imagen se crea con una resolución aumentada (multiplicada por el factor M) para
        obtener mejor calidad en las formas curvas, y posteriormente se redimensionará
        al tamaño real en el método _draw_meter().

        Precondiciones:
        - Los atributos _metersize, _meterthickness, _stripethickness, _arcoffset,
          _arcrange y _metertrough deben estar establecidos.
        - El método _set_widget_colors() debe estar implementado.
        - La constante M debe estar definida.

        Atributos modificados:
        - _base_image: La imagen base generada con el canal del medidor.
        """
        # Configurar los colores del widget
        self._set_widget_colors()

        # Crear una nueva imagen con alta resolución (tamaño * M)
        self._base_image = Image.new(
            mode="RGBA",  # RGB con canal alfa para transparencia
            size=(self._metersize * M, self._metersize * M)  # Tamaño ampliado por factor M
        )

        # Crear objeto de dibujo para la imagen
        draw = ImageDraw.Draw(self._base_image)

        # Calcular dimensiones para el arco (con margen interior de 20 píxeles)
        x1 = y1 = self._metersize * M - 20  # Coordenadas finales del rectángulo de arco
        width = self._meterthickness * M  # Grosor del arco, ampliado por factor M

        # Decidir tipo de arco según el grosor de rayas
        if self._stripethickness > 0:
            # Medidor rayado: dibujar serie de arcos pequeños
            _from = self._arcoffset  # Ángulo inicial del arco
            _to = self._arcrange + self._arcoffset  # Ángulo final del arco

            # Ajustar paso entre rayas (mínimo 2 para grosor 1)
            _step = 2 if self._stripethickness == 1 else self._stripethickness

            # Dibujar cada raya como un arco pequeño
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),  # Rectángulo para el arco
                    start=x,  # Ángulo inicial de la raya
                    end=x + self._stripethickness - 1,  # Ángulo final de la raya
                    fill=self._metertrough,  # Color del canal
                    width=width,  # Grosor del arco
                )
        else:
            # Medidor sólido: dibujar un único arco continuo
            draw.arc(
                xy=(0, 0, x1, y1),  # Rectángulo para el arco
                start=self._arcoffset,  # Ángulo inicial del arco
                end=self._arcrange + self._arcoffset,  # Ángulo final del arco
                fill=self._metertrough,  # Color del canal
                width=width,  # Grosor del arco
            )

    def _draw_solid_meter(self, draw: ImageDraw.Draw):
        """
        Dibuja el indicador del medidor en modo sólido sobre la imagen base.

        Este método representa visualmente el valor actual del medidor mediante un arco
        sólido (no rayado). Permite dos modos de visualización diferentes:

        1. Modo cuña (_wedgesize > 0): Dibuja un pequeño arco centrado en el valor actual,
           creando un efecto de "aguja" o "cuña" indicadora. La cuña se extiende _wedgesize
           grados a cada lado del valor actual.

        2. Modo arco (_wedgesize = 0): Dibuja un arco continuo desde el punto inicial
           (_arcoffset) hasta el valor actual, creando un efecto de "medidor de progreso"
           que se llena a medida que aumenta el valor.

        El indicador se dibuja con el color _meterforeground para distinguirlo del canal
        base del medidor.

        Parámetros:
            draw (ImageDraw.Draw): Objeto de dibujo de PIL/Pillow para realizar
                                  operaciones de dibujo sobre la imagen.

        Precondiciones:
            - El método _meter_value() debe estar implementado para calcular el valor angular.
            - Los atributos _metersize, _meterthickness, _wedgesize, _arcoffset y
              _meterforeground deben estar establecidos.

        Ejemplos:
            Para un medidor tipo "dial" con una cuña indicadora de 5 grados a cada lado:
                _wedgesize = 5

            Para un medidor de progreso tradicional:
                _wedgesize = 0
        """
        # Calcular dimensiones para el arco
        x1 = y1 = self._metersize * M - 20  # Coordenadas finales del rectángulo de arco
        width = self._meterthickness * M  # Grosor del arco, ampliado por factor M

        # Determinar el tipo de indicador a dibujar
        if self._wedgesize > 0:
            # Modo cuña: dibujar un pequeño arco centrado en el valor actual
            meter_value = self._meter_value()  # Calcular posición angular del valor actual

            # Dibujar arco centrado en el valor actual con extensión _wedgesize a cada lado
            draw.arc(
                xy=(0, 0, x1, y1),  # Rectángulo para el arco
                start=meter_value - self._wedgesize,  # Inicio de la cuña
                end=meter_value + self._wedgesize,  # Fin de la cuña
                fill=self._meterforeground,  # Color del indicador
                width=width,  # Grosor del arco
            )
        else:
            # Modo arco: dibujar un arco desde el inicio hasta el valor actual
            draw.arc(
                xy=(0, 0, x1, y1),  # Rectángulo para el arco
                start=self._arcoffset,  # Ángulo inicial del medidor
                end=self._meter_value(),  # Ángulo correspondiente al valor actual
                fill=self._meterforeground,  # Color del indicador
                width=width,  # Grosor del arco
            )

    def _draw_striped_meter(self, draw: ImageDraw.Draw):
        """
        Dibuja el indicador del medidor en modo rayado sobre la imagen base.

        Este método representa visualmente el valor actual del medidor mediante una
        serie de arcos pequeños (rayas) o un indicador tipo "cuña". Permite dos modos
        de visualización diferentes:

        1. Modo cuña (_wedgesize > 0): Dibuja un arco sólido centrado en el valor actual,
           creando un efecto de "aguja" o "cuña" indicadora. La cuña se extiende _wedgesize
           grados a cada lado del valor actual. En este modo, el indicador es sólido,
           no rayado, para mantener consistencia visual con el modo cuña de _draw_solid_meter.

        2. Modo rayado (_wedgesize = 0): Dibuja una serie de arcos pequeños (rayas) desde
           el punto inicial (_arcoffset) hasta justo antes del valor actual, con espaciado
           determinado por _stripethickness. Cada raya tiene exactamente _stripethickness
           grados de ancho.

        El indicador se dibuja con el color _meterforeground para distinguirlo del canal
        base del medidor.

        Parámetros:
            draw (ImageDraw.Draw): Objeto de dibujo de PIL/Pillow para realizar
                                  operaciones de dibujo sobre la imagen.

        Precondiciones:
            - El método _meter_value() debe estar implementado para calcular el valor angular.
            - Los atributos _metersize, _meterthickness, _wedgesize, _arcoffset,
              _stripethickness y _meterforeground deben estar establecidos.
            - El valor de _stripethickness debe ser mayor que 0 para un dibujo efectivo
              en modo rayado.

        Ejemplos:
            Para un medidor tipo "dial" con una cuña indicadora de 5 grados a cada lado:
                _wedgesize = 5

            Para un medidor de progreso rayado con rayas de 5 grados:
                _wedgesize = 0
                _stripethickness = 5
        """
        # Calcular el valor angular actual del medidor
        meter_value = self._meter_value()

        # Calcular dimensiones para el arco
        x1 = y1 = self._metersize * M - 20  # Coordenadas finales del rectángulo de arco
        width = self._meterthickness * M  # Grosor del arco, ampliado por factor M

        # Determinar el tipo de indicador a dibujar
        if self._wedgesize > 0:
            # Modo cuña: dibujar un arco sólido centrado en el valor actual
            # (Nota: en modo cuña, el indicador es siempre sólido, no rayado)
            draw.arc(
                xy=(0, 0, x1, y1),  # Rectángulo para el arco
                start=meter_value - self._wedgesize,  # Inicio de la cuña
                end=meter_value + self._wedgesize,  # Fin de la cuña
                fill=self._meterforeground,  # Color del indicador
                width=width,  # Grosor del arco
            )
        else:
            # Modo rayado: dibujar una serie de arcos pequeños hasta el valor actual
            _from = self._arcoffset  # Ángulo inicial del medidor
            _to = meter_value - 1  # Ángulo final (justo antes del valor actual)
            _step = self._stripethickness  # Tamaño y paso de cada raya

            # Dibujar cada raya como un arco pequeño
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),  # Rectángulo para el arco
                    start=x,  # Ángulo inicial de la raya
                    end=x + self._stripethickness - 1,  # Ángulo final de la raya
                    fill=self._meterforeground,  # Color del indicador
                    width=width,  # Grosor del arco
                )

    def _meter_value(self) -> int:
        """
        Calcula el valor angular para dibujar el indicador del medidor.

        Este método convierte el valor actual del medidor (amountused) y su valor
        máximo (amounttotal) en un ángulo en grados, que determina la posición
        del arco o indicador en la representación gráfica del medidor.

        El cálculo se realiza en tres pasos:
        1. Calcular la proporción: amountused / amounttotal (completitud del medidor)
        2. Escalar esta proporción al rango del arco: proporción * _arcrange
        3. Ajustar según el desplazamiento inicial: resultado + _arcoffset

        El valor devuelto varía desde _arcoffset (cuando amountused es 0) hasta
        _arcoffset + _arcrange (cuando amountused es igual a amounttotal).

        Returns:
            int: El valor angular en grados para dibujar el indicador del medidor.

        Ejemplos:
            Con amountused=0, amounttotal=100, _arcrange=360, _arcoffset=-90:
                El resultado sería -90 (posición inicial del arco)

            Con amountused=50, amounttotal=100, _arcrange=360, _arcoffset=-90:
                El resultado sería 90 (posición a la mitad del arco)

            Con amountused=100, amounttotal=100, _arcrange=360, _arcoffset=-90:
                El resultado sería 270 (posición final del arco)
        """
        # Calcular el valor angular a partir de la proporción del valor actual
        value = int(
            (self["amountused"] / self["amounttotal"]) * self._arcrange  # Escalar al rango del arco
            + self._arcoffset  # Ajustar según el desplazamiento inicial
        )

        return value

    def _on_theme_change(self, *_):
        """
        Actualiza la apariencia visual del medidor cuando cambia el tema de la aplicación.

        Este método responde a los eventos de cambio de tema (<<ThemeChanged>>) y
        configuración (<<Configure>>), reconstruyendo la imagen base y redibujando
        el indicador del medidor con los nuevos colores y estilos del tema actual.

        La actualización se realiza en dos pasos:
        1. Reconstrucción de la imagen base con _draw_base_image()
        2. Redibujado del indicador con _draw_meter()

        Esta secuencia asegura que tanto el canal como el indicador del medidor
        reflejen correctamente los colores del tema actual, manteniendo la coherencia
        visual con el resto de la aplicación.

        Parámetros:
            *_: Argumentos variables que capturan cualquier parámetro adicional
                proporcionado por el sistema de eventos (no utilizados).

        Este método no devuelve ningún valor, pero actualiza visualmente el medidor.
        """
        # Reconstruir la imagen base con los nuevos colores del tema
        self._draw_base_image()

        # Redibujar el indicador sobre la imagen base actualizada
        self._draw_meter()

    def _on_dial_interact(self, e):
        """
        Procesa los eventos de interacción del ratón para ajustar el valor del medidor.

        Este método convierte la posición del ratón en un nuevo valor para el medidor cuando
        el usuario arrastra el puntero sobre el widget. Calcula el ángulo formado por la
        posición del ratón respecto al centro, lo ajusta según la configuración del arco,
        y luego lo transforma en un valor proporcional dentro del rango del medidor.

        El valor resultante se discretiza según el tamaño de paso configurado (_stepsize)
        y se limita al rango válido (0 a amounttotal). Si el valor calculado es igual al
        valor actual, no se realiza ninguna actualización para evitar redibujos innecesarios.

        Parámetros:
            e: Objeto de evento del ratón que contiene las coordenadas x, y de la posición actual.

        El método no devuelve ningún valor, pero actualiza la variable amountusedvar cuando
        corresponde, lo que desencadena el redibujado del medidor debido al enlace de traza.

        Ejemplos de comportamiento:
            - Si el ratón se posiciona a la derecha del centro: Ángulo 0°
            - Si el ratón se posiciona encima del centro: Ángulo -90°
            - Si el ratón se posiciona a la izquierda del centro: Ángulo ±180°
            - Si el ratón se posiciona debajo del centro: Ángulo 90°
        """
        # Calcular la posición relativa al centro del medidor
        dx = e.x - self._metersize // 2  # Desplazamiento horizontal desde el centro
        dy = e.y - self._metersize // 2  # Desplazamiento vertical desde el centro

        # Convertir coordenadas cartesianas a polares (ángulo)
        rads = math.atan2(dy, dx)  # Ángulo en radianes
        degs = math.degrees(rads)  # Ángulo en grados (-180 a 180)

        # Ajustar el ángulo respecto al punto de inicio del arco
        if degs > self._arcoffset:
            # Ángulo directo desde el desplazamiento
            factor = degs - self._arcoffset
        else:
            # Ajuste para manejar el cruce entre 359° y 0°
            factor = 360 + degs - self._arcoffset

        # Obtener los valores actuales y convertir el ángulo a valor del medidor
        amounttotal = self.amounttotalvar.get()  # Valor máximo
        lastused = self.amountusedvar.get()  # Valor actual
        amountused = (amounttotal / self._arcrange * factor)  # Valor proporcional al ángulo

        # Discretizar el valor según el tamaño de paso
        if amountused > self._stepsize // 2:
            # Redondear hacia arriba al siguiente múltiplo del tamaño de paso
            amountused = amountused // self._stepsize * self._stepsize + self._stepsize
        else:
            # Valores muy pequeños se establecen a cero
            amountused = 0

        # Evitar actualizaciones redundantes
        if lastused == amountused:
            return  # No ha cambiado el valor, terminar sin hacer nada

        # Limitar y establecer el nuevo valor
        if amountused < 0:
            # Limitar a valor mínimo
            self.amountusedvar.set(0)
        elif amountused > amounttotal:
            # Limitar a valor máximo
            self.amountusedvar.set(amounttotal)
        else:
            # Establecer el valor calculado
            self.amountusedvar.set(amountused)

    def _lookup_style_option(self, style: str, option: str):
        """
        Consulta el valor de una opción de estilo específica en el sistema de temas TTK.

        Este método es un envoltorio (wrapper) alrededor del comando Tcl 'ttk::style lookup',
        que permite consultar valores de opciones de estilo específicas (como colores,
        fuentes, etc.) para un estilo TTK dado. Proporciona una interfaz Python
        conveniente para acceder a las propiedades visuales definidas en el sistema de temas.

        Parámetros:
            style (str): El nombre del estilo TTK a consultar (ej: "TButton",
                        "success.TLabel").
            option (str): La opción de estilo a buscar, sin el prefijo "-"
                         (ej: "foreground", "background", "font").

        Returns:
            El valor de la opción de estilo si está definida, o None si no lo está.
            El tipo de retorno varía según la opción:
            - Para colores: string hexadecimal (ej: "#FF0000")
            - Para fuentes: string con descripción de fuente (ej: "Helvetica 10")
            - Para otras opciones: diversos tipos según lo que devuelva Tcl/Tk

        Ejemplos:
            Para obtener el color de fondo de un botón:
                color = _lookup_style_option("TButton", "background")

            Para obtener el color de texto de una etiqueta con estilo "success":
                color = _lookup_style_option("success.TLabel", "foreground")

        Nota:
            Este método no maneja explícitamente errores. Si el comando falla (por ejemplo,
            si el estilo no existe), probablemente lanzará una excepción.
        """
        # Construir y ejecutar el comando Tcl/Tk para consultar la opción de estilo
        value = self.tk.call(
            "ttk::style", "lookup", style, "-%s" % option, None, None
        )

        # Devolver el valor obtenido (None si la opción no está definida)
        return value

    def _configure_get(self, cnf):
        """
        Obtiene el valor actual de una opción de configuración específica del widget Meter.

        Este método sobreescribe el comportamiento estándar de obtención de configuración
        para manejar las opciones personalizadas del widget Meter. Proporciona acceso a
        los atributos internos y variables tkinter del widget a través de la interfaz
        de configuración estándar.

        Si la opción solicitada es una de las específicas del Meter, devuelve el valor
        correspondiente desde el atributo interno o variable tkinter. Si no es una opción
        específica, delega la consulta al método `configure` de la clase base.

        Las opciones específicas del Meter incluyen:
        - arcrange: Rango del arco en grados.
        - arcoffset: Desplazamiento del arco en grados.
        - amounttotal: Valor máximo del medidor.
        - amountused: Valor actual del medidor.
        - interactive: Si el medidor responde a eventos de ratón.
        - subtextfont: Fuente para el subtexto.
        - subtextstyle: Estilo para el subtexto.
        - subtext: Texto adicional a mostrar.
        - metersize: Tamaño del medidor en píxeles.
        - bootstyle: Estilo visual del medidor.
        - metertype: Tipo de medidor (completo o semicircular).
        - meterthickness: Grosor del medidor.
        - showtext: Si se muestra el texto.
        - stripethickness: Grosor de las rayas (0 para sólido).
        - textleft: Texto a la izquierda del valor.
        - textright: Texto a la derecha del valor.
        - textfont: Fuente para el texto principal.
        - wedgesize: Tamaño de la cuña indicadora.
        - stepsize: Tamaño del paso para interacción.

        Parámetros:
            cnf (str): Nombre de la opción de configuración a consultar.

        Returns:
            El valor actual de la opción de configuración solicitada. El tipo
            varía según la opción.

        Ejemplos:
            Para obtener el valor actual del medidor:
                value = meter._configure_get("amountused")

            Para obtener el tamaño del medidor:
                size = meter._configure_get("metersize")
        """
        # Verificar si es una opción específica del Meter
        if cnf == "arcrange":
            # Devuelve el rango del arco en grados (típicamente entre 0 y 360)
            return self._arcrange
        elif cnf == "arcoffset":
            # Devuelve el desplazamiento del arco en grados
            # (punto de inicio del arco, típicamente entre 0 y 360)
            return self._arcoffset
        elif cnf == "amounttotal":
            # Devuelve el valor máximo del medidor
            # Se accede a través de la variable tkinter para garantizar consistencia
            return self.amounttotalvar.get()
        elif cnf == "amountused":
            # Devuelve el valor actual del medidor
            # Se accede a través de la variable tkinter para garantizar consistencia
            return self.amountusedvar.get()
        elif cnf == "interactive":
            # Devuelve True si el medidor es interactivo (responde a eventos de ratón)
            # False en caso contrario
            return self._interactive
        elif cnf == "subtextfont":
            # Devuelve la fuente utilizada para el subtexto
            # Puede ser una cadena como "TkDefaultFont" o una tupla como ("Helvetica", 10)
            return self._subtextfont
        elif cnf == "subtextstyle":
            # Devuelve el estilo bootstrap aplicado al subtexto
            # Ejemplos: "primary", "secondary", "success", "danger", etc.
            return self._subtextstyle
        elif cnf == "subtext":
            # Devuelve el texto adicional mostrado debajo del valor principal
            return self._subtext
        elif cnf == "metersize":
            # Devuelve el tamaño del medidor en píxeles
            # Este valor puede haber sido escalado según la resolución de la pantalla
            return self._metersize
        elif cnf == "bootstyle":
            # Devuelve el estilo bootstrap aplicado al medidor
            # Define el esquema de color del medidor
            return self._bootstyle
        elif cnf == "metertype":
            # Devuelve el tipo de medidor: "full" para círculo completo, "semi" para semicírculo
            return self._metertype
        elif cnf == "meterthickness":
            # Devuelve el grosor del arco del medidor en píxeles
            # Este valor puede haber sido escalado según la resolución de la pantalla
            return self._meterthickness
        elif cnf == "showtext":
            # Devuelve True si se muestra el texto del medidor, False en caso contrario
            return self._showtext
        elif cnf == "stripethickness":
            # Devuelve el grosor de las rayas en un medidor de tipo rayado
            # Un valor de 0 indica un medidor sólido (sin rayas)
            return self._stripethickness
        elif cnf == "textleft":
            # Devuelve el texto mostrado a la izquierda del valor principal
            return self._textleft
        elif cnf == "textright":
            # Devuelve el texto mostrado a la derecha del valor principal
            return self._textright
        elif cnf == "textfont":
            # Devuelve la fuente utilizada para el texto principal
            # Puede ser una cadena como "TkTextFont" o una tupla como ("Helvetica", 12, "bold")
            return self._textfont
        elif cnf == "wedgesize":
            # Devuelve el tamaño de la cuña indicadora en píxeles
            return self._wedgesize
        elif cnf == "stepsize":
            # Devuelve el tamaño del paso para incremento/decremento
            # Utilizado por el método step()
            return self._stepsize
        else:
            # Si la opción no es específica del Meter, delegamos a la clase base
            # Esto maneja opciones estándar de ttk.Frame como background, padding, etc.
            return super(ttk.Frame, self).configure(cnf)

    def _configure_set(self, **kwargs):
        """Configura las propiedades del widget Meter.

        Este método actualiza los atributos internos del widget basándose en los parámetros
        proporcionados y refleja estos cambios en la interfaz visual. Procesa todos los
        parámetros específicos del Meter y delega los demás a la clase padre.

        Parámetros
        ----------
        **kwargs : dict
            Parámetros de configuración como pares clave-valor. Acepta:
            - arcrange : int o float
                El rango en grados del arco del medidor.
            - arcoffset : int o float
                El desplazamiento inicial del arco en grados.
            - amounttotal : int o float
                El valor total/máximo del medidor.
            - amountused : int o float
                El valor actual/usado del medidor.
            - interactive : bool
                Indica si el medidor debe ser interactivo (funcionar como dial).
            - subtextfont : str o tupla
                Fuente para el subtexto y textos laterales.
            - subtextstyle : str
                Estilo bootstrap para el subtexto.
            - metersize : int
                Tamaño del medidor en píxeles.
            - bootstyle : str
                Estilo bootstrap para el medidor.
            - metertype : str
                Tipo de medidor ('full' para círculo completo, 'semi' para semicírculo).
            - meterthickness : int
                Grosor del arco del medidor.
            - stripethickness : int
                Grosor de las rayas en un medidor rayado.
            - subtext : str
                Texto a mostrar debajo del valor del medidor.
            - textleft : str
                Texto a mostrar en la esquina inferior izquierda.
            - textright : str
                Texto a mostrar en la esquina inferior derecha.
            - showtext : bool
                Indica si se debe mostrar el texto del medidor.
            - textfont : str o tupla
                Fuente para el valor principal del medidor.
            - wedgesize : int
                Tamaño del sector si se usa un indicador de sector.
            - stepsize : int o float
                Incremento usado en el método step().

        Retorna
        -------
        None
            Este método no retorna un valor explícitamente.

        """
        # Rastrea si alguna propiedad relacionada con el texto ha cambiado
        meter_text_changed = False

        # Procesa el rango del arco (en grados)
        if "arcrange" in kwargs:
            self._arcrange = kwargs.pop("arcrange")

        # Procesa el desplazamiento del arco (en grados)
        if "arcoffset" in kwargs:
            self._arcoffset = kwargs.pop("arcoffset")

        # Procesa el valor total del medidor
        if "amounttotal" in kwargs:
            amounttotal = kwargs.pop("amounttotal")
            self.amounttotalvar.set(amounttotal)

        # Procesa el valor usado/actual del medidor
        if "amountused" in kwargs:
            amountused = kwargs.pop("amountused")
            self.amountusedvar.set(amountused)

        # Procesa el modo interactivo (comportamiento de dial)
        if "interactive" in kwargs:
            self._interactive = kwargs.pop("interactive")
            self._set_interactive_bind()

        # Procesa la fuente del subtexto y textos laterales
        if "subtextfont" in kwargs:
            self._subtextfont = kwargs.pop("subtextfont")
            self.subtext.configure(font=self._subtextfont)
            self.textleft.configure(font=self._subtextfont)
            self.textright.configure(font=self._subtextfont)

        # Procesa el estilo bootstrap del subtexto
        if "subtextstyle" in kwargs:
            self._subtextstyle = kwargs.pop("subtextstyle")
            self.subtext.configure(bootstyle=[self._subtextstyle, "meter"])

        # Procesa el tamaño del medidor
        if "metersize" in kwargs:
            self._metersize = utility.scale_size(kwargs.pop("metersize"))
            self.meterframe.configure(
                height=self._metersize, width=self._metersize
            )

        # Procesa el estilo bootstrap del medidor
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self.textcenter.configure(bootstyle=[self._bootstyle, "meter"])

        # Procesa el tipo de medidor (completo o semicírculo)
        if "metertype" in kwargs:
            self._metertype = kwargs.pop("metertype")

        # Procesa el grosor del arco del medidor
        if "meterthickness" in kwargs:
            self._meterthickness = self.scale_size(
                kwargs.pop("meterthickness")
            )

        # Procesa el grosor de las rayas en un medidor rayado
        if "stripethickness" in kwargs:
            self._stripethickness = kwargs.pop("stripethickness")

        # Procesa el subtexto
        if "subtext" in kwargs:
            self._subtext = kwargs.pop("subtext")
            self.subtext.configure(text=self._subtext)
            meter_text_changed = True

        # Procesa el texto izquierdo
        if "textleft" in kwargs:
            self._textleft = kwargs.pop("textleft")
            self.textleft.configure(text=self._textleft)
            meter_text_changed = True

        # Procesa el texto derecho
        if "textright" in kwargs:
            self._textright = kwargs.pop("textright")
            # Nota: Falta configurar el texto del widget textright
            meter_text_changed = True

        # Procesa la visibilidad del texto
        if "showtext" in kwargs:
            self._showtext = kwargs.pop("showtext")
            meter_text_changed = True

        # Procesa la fuente del texto central
        if "textfont" in kwargs:
            self._textfont = kwargs.pop("textfont")
            self.textcenter.configure(font=self._textfont)

        # Procesa el tamaño del sector
        if "wedgesize" in kwargs:
            self._wedgesize = kwargs.pop("wedgesize")

        # Procesa el tamaño del paso para incremento/decremento
        if "stepsize" in kwargs:
            self._stepsize = kwargs.pop("stepsize")

        # Si algún texto cambió, actualiza todos los componentes de texto
        if meter_text_changed:
            self._set_meter_text()

        try:
            # Si el tipo de medidor está definido, configura el arco
            if self._metertype:
                self._set_arc_offset_range(
                    metertype=self._metertype,
                    arcoffset=self._arcoffset,
                    arcrange=self._arcrange,
                )
        except AttributeError:
            # Si _metertype no está definido aún, termina el método
            return

        # Redibuja los componentes visuales del medidor
        self._draw_base_image()
        self._draw_meter()

        # Pasa configuraciones restantes a `ttk.Frame.configure`
        super(ttk.Frame, self).configure(**kwargs)

    def __getitem__(self, key: str):
        """
        Permite acceder a las opciones de configuración del widget usando la sintaxis de corchetes.

        Este método implementa el protocolo de mapping de Python para la obtención de valores,
        permitiendo usar la sintaxis `widget["opcion"]` como alternativa a `widget.configure("opcion")`.
        Delega la obtención real del valor al método `_configure_get`.

        Parámetros
        ----------
        key : str
            Nombre de la opción de configuración a consultar.

        Returns
        -------
        any
            El valor actual de la opción de configuración solicitada.
            El tipo del valor retornado depende de la opción consultada.


        See Also
        --------
        _configure_get : Método que realiza la obtención real del valor
        __setitem__ : Método complementario para establecer valores
        """
        # Delegar la obtención del valor a _configure_get
        return self._configure_get(key)

    def __setitem__(self, key: str, value) -> None:
        """
        Permite modificar las opciones de configuración del widget usando la sintaxis de corchetes.

        Este método implementa el protocolo de mapping de Python para la asignación de valores,
        permitiendo usar la sintaxis `widget["opcion"] = valor` como alternativa a
        `widget.configure(opcion=valor)`. Delega la configuración real al método `_configure_set`.

        Parámetros
        ----------
        key : str
            Nombre de la opción de configuración a modificar.
        value : any
            Nuevo valor para la opción especificada.
            El tipo aceptado depende de la opción a configurar.

        Returns
        -------
        None
            Este método no retorna un valor explícitamente.

        See Also
        --------
        _configure_set : Método que realiza la configuración real
        __getitem__ : Método complementario para obtener valores
        """
        # Crear un diccionario con un único par clave-valor
        # y pasarlo a _configure_set usando la sintaxis de desempaquetado
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        """
        Configurar o consultar las opciones para este widget.

        Este método proporciona una interfaz unificada para consultar y modificar las opciones
        de configuración del widget Meter, siguiendo el patrón estándar de tkinter.

        Puede usarse en dos modos:
        - Modo de consulta: Cuando se proporciona el nombre de una opción en el parámetro `cnf`.
          En este caso, devuelve el valor actual de la opción especificada.
        - Modo de configuración: Cuando `cnf` es None y se proporcionan opciones como argumentos
          de palabras clave. En este caso, establece las opciones especificadas a los valores dados.

        Parámetros
        ----------
        cnf : str o None, opcional
            Si es una cadena, representa el nombre de la opción cuyo valor se desea consultar.
            Si es None, se asume modo de configuración. Por defecto es None.
        **kwargs : dict
            Argumentos de palabras clave que especifican las opciones a configurar y sus valores.
            Solo se utilizan en modo de configuración (cuando cnf es None).

        Returns
        -------
        any o None
            En modo de consulta, devuelve el valor actual de la opción especificada.
            El tipo del valor retornado depende de la opción consultada.
            En modo de configuración, no retorna un valor explícitamente (implícitamente None).

        See Also
        --------
        _configure_get : Método que realiza la obtención real del valor
        _configure_set : Método que realiza la configuración real
        """
        # Verificar si estamos en modo de consulta o configuración
        if cnf is not None:
            # Modo de consulta: delegar a _configure_get
            return self._configure_get(cnf)
        else:
            # Modo de configuración: delegar a _configure_set
            self._configure_set(**kwargs)
            # No hay retorno explícito, retorna implícitamente None

    def step(self, delta=1):
        """
        Incrementa o decrementa el valor del indicador según la dirección actual.

        Este método actualiza el valor actual del medidor en `delta` unidades, siguiendo
        un comportamiento de "rebote" en los límites. Cuando el valor alcanza o supera
        el valor máximo, la dirección se invierte y el medidor comienza a decrementar.
        Cuando el valor alcanza o cae por debajo de cero, la dirección se invierte
        nuevamente y el medidor comienza a incrementar.

        El cambio de dirección ocurre automáticamente al alcanzar los límites, lo que
        resulta en un comportamiento cíclico donde el valor oscila entre 0 y el valor máximo.

        Parámetros
        ----------
        delta : int, opcional
            La cantidad a incrementar o decrementar el valor del medidor.
            Valores positivos incrementarán o decrementarán según la dirección actual.
            Valores negativos pueden causar un comportamiento opuesto al esperado.
            Por defecto es 1.


        """
        # Obtener el valor actual del medidor
        amountused = self.amountusedvar.get()

        # Obtener el valor máximo del medidor
        amounttotal = self.amounttotalvar.get()

        # Si se ha alcanzado o superado el valor máximo
        if amountused >= amounttotal:
            # Cambiar la dirección a "hacia abajo"
            self._towardsmaximum = True
            # Decrementar el valor en delta unidades
            self.amountusedvar.set(amountused - delta)

        # Si se ha alcanzado o caído por debajo de cero
        elif amountused <= 0:
            # Cambiar la dirección a "hacia arriba"
            self._towardsmaximum = False
            # Incrementar el valor en delta unidades
            self.amountusedvar.set(amountused + delta)

        # Si no se ha alcanzado ningún límite y la dirección actual es "hacia abajo"
        elif self._towardsmaximum:
            # Continuar decrementando el valor
            self.amountusedvar.set(amountused - delta)

        # Si no se ha alcanzado ningún límite y la dirección actual es "hacia arriba"
        else:
            # Continuar incrementando el valor
            self.amountusedvar.set(amountused + delta)