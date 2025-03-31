import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from tkinter import Pack, Place, Grid


class ScrolledFrame(ttk.Frame):
    """Un contenedor widget con barra de desplazamiento vertical.

    ScrolledFrame extiende ttk.Frame para proporcionar capacidades de desplazamiento
    vertical. Es útil cuando se necesita mostrar más contenido del que cabe en el
    espacio disponible en pantalla.

    El ScrolledFrame ocupa todo el ancho de su contenedor. La altura puede ser
    establecida explícitamente o determinada por el contenido del frame interno.

    Este widget se comporta principalmente como un frame normal, con algunas excepciones:
    1. Al añadirlo a un Notebook o Panedwindow, se debe usar .container en lugar
       del widget directamente. Por ejemplo: `notebook.add(scrolledframe.container)`.
    2. La barra de desplazamiento puede configurarse para ocultarse automáticamente
       cuando no es necesaria, usando el parámetro `autohide=True`.

    Args:
        master: Widget padre donde se colocará el ScrolledFrame.
        padding (int, opcional): Espacio alrededor del contenido. Por defecto es 2.
        bootstyle (str, opcional): Estilo visual del widget. Por defecto es DEFAULT.
        autohide (bool, opcional): Si True, la barra de desplazamiento se oculta
                                 automáticamente cuando no se necesita. Por defecto es False.
        height (int, opcional): Altura explícita del widget. Por defecto es 200.
        width (int, opcional): Ancho explícito del widget. Por defecto es 300.
        scrollheight (int, opcional): Altura específica para el área desplazable.
                                     Si es None, se determina por el contenido.
        **kwargs: Argumentos adicionales que se pasan al constructor de ttk.Frame.

    Atributos:
        container: Frame que contiene todos los elementos.
        interior: Frame donde se colocan los widgets hijos.
        vscroll: Barra de desplazamiento vertical.
        autohide: Indica si la barra de desplazamiento se oculta automáticamente.

    Examples:
        ```python
        import ui.themeengine as ttk
        from ui.themeengine.utils.constants import *
        from ui.themeengine.widgets.containers import ScrolledFrame

        app = ttk.Window()

        sf = ScrolledFrame(app, autohide=True)
        sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # add a large number of checkbuttons into the containers frame
        for x in range(20):
            ttk.Checkbutton(sf, text=f"Checkbutton {x}").pack(anchor=W)

        app.mainloop()
        ```

        Ejemplo con Notebook:
        ```python
        notebook = ttk.Notebook(app)
        sf = ScrolledFrame(notebook)
        notebook.add(sf.container, text="Pestaña con scroll")

        # Añadir contenido al ScrolledFrame
        for i in range(30):
            ttk.Label(sf, text=f"Elemento {i}").pack()
        ```
    """

    def __init__(
            self,
            master=None,
            padding=2,
            bootstyle=DEFAULT,
            autohide=False,
            height=200,
            width=300,
            scrollheight=None,
            **kwargs,
    ):
        """
        Inicializa un widget ScrolledFrame con capacidad de desplazamiento vertical.

        Este constructor crea un widget compuesto que permite mostrar contenido
        que excede el área visible, facilitando la navegación mediante una barra
        de desplazamiento vertical.

        Parámetros:
            master (Widget):
                El widget padre donde se creará el ScrolledFrame.

            padding (int):
                Cantidad de espacio vacío alrededor del widget.

            bootstyle (str):
                Palabra clave de estilo para definir el color y estilo de la
                barra de desplazamiento vertical. Opciones disponibles: primary,
                secondary, success, info, warning, danger, dark, light.

            autohide (bool):
                Si es True, las barras de desplazamiento se ocultarán cuando
                el ratón no esté dentro del área del widget.

            height (int):
                Altura del marco contenedor en unidades de pantalla.

            width (int):
                Anchura del marco contenedor en unidades de pantalla.

            scrollheight (int):
                Altura del marco de contenido en unidades de pantalla. Si es None,
                la altura se determina por el contenido del marco.

            **kwargs (Dict[str, Any]):
                Otros argumentos que se pasarán al marco de contenido.

        Nota:
            Este widget se comporta como un marco normal con algunas excepciones.
            Por ejemplo, al incluirlo en un Notebook o Panedwindow, deberá añadir
            el contenedor en lugar del marco de contenido:
            `minotebook.add(miscrolledframe.container)`
        """

        #  Crea y configura el contenedor principal del ScrolledFrame.
        #
        # Este fragmento de código genera el marco exterior que contendrá tanto el
        # contenido desplazable como la barra de desplazamiento vertical. Establece
        # un tamaño fijo para el contenedor y lo configura para que no se redimensione
        # automáticamente según su contenido, lo que permite implementar la funcionalidad
        # de desplazamiento.
        self.container = ttk.Frame(
            master=master,  # Widget padre (ventana, frame, etc.)
            relief=FLAT,  # Sin relieve visual en los bordes
            borderwidth=0,  # Sin borde visible
            width=width,  # Ancho fijo en píxeles (ej: 300)
            height=height,  # Altura fija en píxeles (ej: 200)
        )
        # Vincula actualización de vista cuando el contenedor cambia de tamaño
        self.container.bind("<Configure>", lambda _: self.yview())
        # Desactiva el redimensionamiento automático según el contenido
        self.container.propagate(0)  # Equivalente a propagate(False)

        # Inicializa y posiciona el marco de contenido del ScrolledFrame.
        # Este fragmento inicializa el marco principal heredando de ttk.Frame y luego
        # lo posiciona dentro del contenedor. Este marco servirá como el área desplazable
        # donde se colocarán los widgets hijos.
        super().__init__(
            master=self.container,  # Contenedor como widget padre
            padding=padding,  # Espacio de relleno (ej: 5 píxeles)
            bootstyle=bootstyle.replace('round', ''),  # Estilo sin 'round' (ej: "primary")
            width=width,  # Ancho en píxeles (ej: 300)
            height=height,  # Altura en píxeles (ej: 200)
            **kwargs,  # Argumentos adicionales
        )
        # Posiciona el marco dentro del contenedor
        self.place(
            rely=0.0,  # Alineado con la parte superior
            relwidth=1.0,  # Ocupa todo el ancho disponible
            height=scrollheight  # Altura específica o None
        )

        # Crea, configura la barra de desplazamiento vertical y detecta el sistema de ventanas.
        # Este fragmento establece la barra de desplazamiento que permitirá al usuario navegar
        # por el contenido que excede el área visible del widget. También detecta el sistema
        # de ventanas en uso para adaptarse a comportamientos específicos de la plataforma.
        self.vscroll = ttk.Scrollbar(
            master=self.container,  # Contenedor como widget padre
            command=self.yview,  # Método para controlar el desplazamiento
            orient=VERTICAL,  # Orientación vertical (arriba-abajo)
            bootstyle=bootstyle,  # Estilo visual (ej: "primary")
        )
        # Posiciona la barra en el lado derecho, expandiéndola verticalmente
        self.vscroll.pack(side=RIGHT, fill=Y)

        # Detecta el sistema de ventanas para adaptaciones específicas
        # (win32=Windows, x11=Linux, aqua=macOS)
        self.winsys = self.tk.call("tk", "windowingsystem")

        # Configura el comportamiento de auto-ocultamiento de las barras de desplazamiento.
        # Este fragmento determina si las barras deben ocultarse automáticamente cuando
        # el ratón no está sobre el widget. Si se activa esta función, las barras estarán
        # ocultas inicialmente y solo aparecerán cuando el usuario mueva el ratón sobre
        # el área del ScrolledFrame.
        self.autohide = autohide  # Almacena la preferencia de auto-ocultamiento
        if self.autohide:  # Si se activa el auto-ocultamiento
            self.hide_scrollbars()  # Oculta las barras inicialmente

        # Configura los vínculos de eventos necesarios para el funcionamiento del ScrolledFrame.
        # Este fragmento vincula diferentes eventos del sistema y personalizados a métodos específicos
        # que gestionan el comportamiento reactivo del widget. Los principales comportamientos
        # controlados son:
        # 1. Auto-ocultamiento de barras: Mostrar/ocultar barras cuando el ratón entra/sale
        # 2. Actualización de vista: Asegurar que la posición de visualización sea correcta cuando el widget o sus hijos se muestran
        # Cuando el ratón entra en el área del widget
        self.container.bind("<Enter>", self._on_enter, "+")  # Ratón entra -> Mostrar barras
        # Cuando el ratón sale del área del widget
        self.container.bind("<Leave>", self._on_leave, "+")  # Ratón sale -> Ocultar barras
        # Cuando el widget se hace visible en la pantalla
        self.container.bind("<Map>", self._on_map, "+")  # Widget visible -> Actualizar vista
        # Evento personalizado para cuando un hijo se mapea al contenido
        self.bind("<<MapChild>>", self._on_map_child, "+")  # Hijo mapeado -> Actualizar vista

        # Delega los métodos de gestión de geometría del marco de contenido al contenedor externo.
        # Este fragmento implementa un mecanismo avanzado de delegación que permite que los métodos
        # de posicionamiento (pack, grid, place) del ScrolledFrame afecten al contenedor completo
        # en lugar de solo al marco de contenido. Esto facilita el uso del widget, ya que el usuario
        # puede posicionar todo el conjunto (contenedor, contenido y barras) como una unidad.
        # La delegación funciona en dos pasos:
        # 1. Preservar los métodos originales del marco de contenido con el prefijo "content_"
        # 2. Sobrescribir los métodos originales para que apunten a los métodos del contenedor
        _methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()  # Obtener todos los métodos
        for method in _methods:  # Iterar sobre cada nombre de método
            if any(["pack" in method, "grid" in method, "place" in method]):  # Filtrar métodos relevantes
                # Guardar método original con prefijo "content_"
                setattr(self, f"content_{method}", getattr(self, method))
                # Sobrescribir con el método equivalente del contenedor
                setattr(self, method, getattr(self.container, method))

        # Inicializar caché para optimizaciones
        self._measures_cache = None
        self._bound_widgets = set()
        self._last_wheel_time = 0
        self._wheel_delay = 30  # ms entre eventos

        # Habilitar desplazamiento inicialmente
        self.enable_scrolling()

    def yview(self, *args):
        """
        Actualiza la posición vertical del marco de contenido dentro del contenedor.

        Este método controla el desplazamiento vertical del contenido, permitiendo
        navegar por información que excede el área visible. Funciona como un
        distribuidor que redirige a métodos específicos según los argumentos.

        Parámetros:
            *args: Argumentos que determinan el tipo de desplazamiento:
                - Sin argumentos: Actualiza la vista a la posición actual.
                - ("moveto", fracción): Desplaza a una posición específica.
                    fracción: Valor entre 0.0 (inicio) y 1.0 (final).
                - ("scroll", cantidad, tipo): Desplaza relativamente.
                    cantidad: Número entero (positivo=abajo, negativo=arriba).
                    tipo: "units" (pequeños incrementos) o "pages" (páginas completas).

        Ejemplos:
            # Actualizar la vista a la posición actual
            self.yview()

            # Desplazar a la mitad del contenido
            self.yview("moveto", 0.5)

            # Desplazar tres unidades hacia abajo
            self.yview("scroll", 3, "units")

            # Retroceder una página
            self.yview("scroll", -1, "pages")
        """
        # Evitar actualizaciones cuando el widget no está visible
        if not args and not self.container.winfo_ismapped():
            return

        # Evitar actualizaciones cuando no hay contenido que desplazar
        base, thumb = self._measures()
        if thumb >= 1.0 and not args:
            return  # No hay necesidad de desplazamiento

        # Caso 1: Sin argumentos - Actualizar a la posición actual
        if not args:
            # Obtener la posición actual del inicio de la vista (0.0 a 1.0)
            first, _ = self.vscroll.get()  # Ejemplo: (0.3, 0.6) -> first = 0.3
            # Actualizar la vista a esa misma posición
            self.yview_moveto(fraction=first)  # Refresca la vista actual

        # Caso 2: Comando "moveto" - Desplazar a posición específica
        elif args[0] == "moveto":
            # Convertir el segundo argumento a número decimal (fracción)
            # Ejemplo: "0.5" -> 0.5 (50% del contenido)
            self.yview_moveto(fraction=float(args[1]))

        # Caso 3: Comando "scroll" - Desplazar relativamente
        elif args[0] == "scroll":
            # Convertir cantidad a entero y pasar el tipo de unidad
            # Ejemplo: ("scroll", "1", "units") -> desplazar 1 unidad hacia abajo
            # Ejemplo: ("scroll", "-1", "pages") -> desplazar 1 página hacia arriba
            self.yview_scroll(number=int(args[1]), what=args[2])

        # Caso 4: Comando desconocido - No hacer nada
        else:
            return

    def yview_moveto(self, fraction: float):
        """
        Actualiza la posición vertical del marco de contenido a una ubicación específica.

        Este método desplaza el contenido a una posición relativa determinada por la
        fracción proporcionada, ajustando automáticamente valores fuera de rango
        y coordinando la posición visual del contenido con la barra de desplazamiento.

        Parámetros:
            fraction (float):
                Posición relativa a la que desplazar el contenido.
                - 0.0 representa el inicio del contenido.
                - 1.0 representa el final del contenido.
                - Valores intermedios representan posiciones proporcionales.
                - Valores fuera del rango [0.0, 1.0] serán ajustados automáticamente.

        Notas:
            - Si fraction < 0, se ajustará a 0.0 (inicio del contenido).
            - Si (fraction + tamaño_visible) > 1, se ajustará para mostrar el final
              del contenido sin exceder los límites.
            - El tamaño visible depende de la relación entre el contenido y el contenedor.

        Ejemplos:
            # Desplazar al inicio del contenido
            self.yview_moveto(0.0)

            # Desplazar a la mitad del contenido
            self.yview_moveto(0.5)

            # Desplazar al final del contenido
            self.yview_moveto(1.0)
        """
        # Obtener las medidas fundamentales para cálculos de posición
        # base: relación de tamaño entre contenido y contenedor
        # thumb: proporción del contenido visible a la vez
        base, thumb = self._measures()  # Ej: base=2.0, thumb=0.5

        # Validar y ajustar la fracción dentro de límites válidos
        if fraction < 0:
            # Si es negativa, ajustar al inicio
            first = 0.0  # Mostrar desde el principio
        elif (fraction + thumb) > 1:
            # Si excede el final, ajustar para mostrar la última parte posible
            first = 1 - thumb  # Ej: Si thumb=0.3, first=0.7 para mostrar 0.7-1.0
        else:
            # Si está dentro de límites válidos, usar directamente
            first = fraction  # Ej: Si fraction=0.4, first=0.4

        # Actualizar la posición visual de la barra de desplazamiento
        # Esto mueve el "pulgar" de la barra a la posición correspondiente
        self.vscroll.set(first, first + thumb)  # Ej: set(0.3, 0.6)

        # Actualizar la posición física del contenido mediante place
        # El signo negativo indica desplazamiento hacia arriba
        # base es el factor de escalado entre contenido y contenedor
        self.content_place(rely=-first * base)  # Ej: rely=-0.6

    def yview_scroll(self, number: int, what: str):
        """
        Desplaza el contenido verticalmente de forma relativa a la posición actual.

        Este método realiza un desplazamiento incremental basado en la posición actual.
        Cada unidad de desplazamiento representa un 1% del tamaño total del contenido
        (independientemente del valor del parámetro 'what').

        Parámetros:
            number (int):
                Cantidad de unidades a desplazar el contenido.
                - Valores positivos: Desplazamiento hacia abajo.
                - Valores negativos: Desplazamiento hacia arriba.
                - Cada unidad equivale a un 1% del contenido total.

            what (str, opcional):
                Tipo de unidades para interpretar el número.
                Actualmente este parámetro no afecta al comportamiento y todas
                las unidades se tratan igual (1% del contenido).

        Ejemplos:
            # Desplazar un 5% hacia abajo
            self.yview_scroll(5, "units")

            # Desplazar un 10% hacia arriba
            self.yview_scroll(-10, "units")

        Nota:
            El desplazamiento está limitado por los extremos del contenido.
            Si se intenta desplazar más allá de los límites, se ajustará automáticamente.
        """
        # Obtener la posición actual del contenido visible
        first, _ = self.vscroll.get()  # Ej: first = 0.3 (30% desde el inicio)

        # Calcular la nueva posición sumando el incremento relativo
        # Cada unidad representa un 1% del contenido
        fraction = (number / 100) + first  # Ej: (5/100) + 0.3 = 0.35

        # Delegar al método de posicionamiento absoluto
        # Este método se encargará de validar límites y actualizar la UI
        self.yview_moveto(fraction)

    def _add_scroll_binding(self, parent):
        """
        Añade vinculaciones de eventos de rueda del ratón a un widget y todos sus descendientes.

        Este método recorre recursivamente la jerarquía de widgets a partir del widget
        padre proporcionado, añadiendo vinculaciones para eventos de rueda del ratón
        a cada widget encontrado. Se adapta automáticamente a diferentes sistemas de
        ventanas (X11, Windows, macOS) y evita añadir vinculaciones duplicadas.

        En sistemas X11 (Linux/Unix), vincula los eventos <Button-4> y <Button-5>.
        En otros sistemas (Windows/macOS), vincula el evento <MouseWheel>.

        Parámetros:
            parent: El widget desde el que comenzar a añadir vinculaciones.
                    Tanto este widget como todos sus descendientes recibirán
                    las vinculaciones apropiadas.

        Notas:
            - Este método es recursivo y puede procesar árboles de widgets profundos.
            - Verifica vinculaciones existentes para evitar duplicados.
            - Todos los eventos de rueda se vinculan al método self._on_mousewheel.
        """
        # Almacenar widgets ya vinculados para evitar duplicados
        if not hasattr(self, '_bound_widgets'):
            self._bound_widgets = set()

        # Obtener todos los widgets hijos directos del widget padre
        children = parent.winfo_children()

        # Iterar por el padre y todos sus hijos
        for widget in [parent, *children]:
            # Verificar si ya está vinculado
            widget_id = str(widget)
            if widget_id in self._bound_widgets:
                continue

            # Marcar como vinculado
            self._bound_widgets.add(widget_id)

            # Diferente manejo según el sistema de ventanas
            if self.winsys.lower() == "x11":  # Linux/Unix
                # Añadir vinculaciones para rueda arriba (<Button-4>) y abajo (<Button-5>)
                widget.bind("<Button-4>", self._on_mousewheel, "+")  # Rueda hacia arriba
                widget.bind("<Button-5>", self._on_mousewheel, "+")  # Rueda hacia abajo
            else:  # Windows/macOS
                # Añadir vinculación genérica para evento de rueda
                widget.bind("<MouseWheel>", self._on_mousewheel, "+")

            # Vinculación para detectar cuando el widget se destruye
            widget.bind("<Destroy>",
                        lambda e, w=widget_id: self._bound_widgets.discard(w), "+")

            # Recursión: continuar con los widgets hijos (que no sean el padre original)
            # Esto evita recursión infinita mientras procesa toda la jerarquía
            if widget.winfo_children() and widget != parent:
                self._add_scroll_binding(widget)  # Llamada recursiva

    def _del_scroll_binding(self, parent):
        """Elimina recursivamente las vinculaciones de eventos de desplazamiento.

        Este método desvincula todos los eventos de rueda del ratón del widget padre
        proporcionado y de todos sus descendientes en la jerarquía de widgets. Los eventos
        específicos que se desvinculan dependen del sistema de ventanas:
        - En X11 (Linux): <Button-4> (arriba) y <Button-5> (abajo)
        - En Windows/macOS: <MouseWheel>

        Args:
            parent: Widget Tkinter del que se eliminarán las vinculaciones de desplazamiento,
                    junto con todos sus descendientes.

        Returns:
            None

        Ejemplos:
            # Eliminar vinculaciones de desplazamiento de todo el contenedor
            self._del_scroll_binding(self.container)

            # Eliminar vinculaciones solo de un widget específico y sus hijos
            self._del_scroll_binding(self.specific_widget)
        """
        # Limpiar el conjunto de widgets vinculados
        if hasattr(self, '_bound_widgets'):
            self._bound_widgets.clear()

        # Obtener todos los widgets hijos directos del widget padre
        children = parent.winfo_children()

        # Procesar el widget padre y todos sus hijos directos
        for widget in [parent, *children]:
            # Desvincular eventos según el sistema de ventanas
            if self.winsys.lower() == "x11":  # Sistema Linux (X11)
                widget.unbind("<Button-4>")  # Evento de desplazamiento hacia arriba
                widget.unbind("<Button-5>")  # Evento de desplazamiento hacia abajo
            else:  # Windows o macOS
                widget.unbind("<MouseWheel>")  # Evento estándar de rueda del ratón

            # Procesar recursivamente los descendientes si existen y no es el padre original
            if widget.winfo_children() and widget != parent:
                self._del_scroll_binding(widget)  # Llamada recursiva con el widget actual

    def enable_scrolling(self):
        """Habilita el desplazamiento con la rueda del ratón en el marco y todos sus widgets hijos.

        Este método activa la capacidad de desplazamiento vertical mediante la rueda del ratón
        en toda la jerarquía de widgets del ScrolledFrame. Vincula los eventos apropiados
        de la rueda del ratón a cada widget, permitiendo que el contenido se desplace
        verticalmente cuando el usuario utiliza la rueda del ratón mientras el cursor
        está sobre cualquier parte del marco o sus widgets hijos.

        La implementación se delega al método privado `_add_scroll_binding`, que se encarga
        de añadir las vinculaciones de eventos específicas para cada sistema operativo.

        Returns:
            None

        Ejemplos:
            # Habilitar el desplazamiento en un ScrolledFrame existente
            my_scrolled_frame = ScrolledFrame(root)
            my_scrolled_frame.disable_scrolling()  # Primero deshabilitamos
            # ... alguna lógica ...
            my_scrolled_frame.enable_scrolling()   # Luego habilitamos nuevamente
        """
        # Delegar la implementación a _add_scroll_binding, pasando self como el widget raíz
        # desde el que comenzar a agregar vinculaciones de desplazamiento
        self._add_scroll_binding(self)

    def disable_scrolling(self):
        """Deshabilita el desplazamiento con la rueda del ratón en el marco y todos sus widgets hijos.

        Este método desactiva la capacidad de desplazamiento vertical mediante la rueda del ratón
        en toda la jerarquía de widgets del ScrolledFrame. Elimina las vinculaciones de eventos
        de la rueda del ratón de cada widget, haciendo que el contenido ya no responda cuando
        el usuario utiliza la rueda del ratón mientras el cursor está sobre cualquier parte
        del marco o sus widgets hijos.

        La implementación se delega al método privado `_del_scroll_binding`, que se encarga
        de eliminar las vinculaciones de eventos específicas para cada sistema operativo.

        Returns:
            None

        Ejemplos:
            # Deshabilitar el desplazamiento en un ScrolledFrame existente
            my_scrolled_frame = ScrolledFrame(root)
            my_scrolled_frame.disable_scrolling()  # Deshabilitamos el desplazamiento

            # Deshabilitar temporalmente y luego habilitar nuevamente
            my_scrolled_frame.disable_scrolling()
            # ... alguna operación que no debería ser interrumpida por desplazamiento ...
            my_scrolled_frame.enable_scrolling()
        """
        # Delegar la implementación a _del_scroll_binding, pasando self como el widget raíz
        # desde el que comenzar a eliminar vinculaciones de desplazamiento
        self._del_scroll_binding(self)

    def hide_scrollbars(self):
        """Oculta las barras de desplazamiento del ScrolledFrame.

        Este método oculta la barra de desplazamiento vertical (vscroll) sin afectar
        la funcionalidad de desplazamiento. El contenido seguirá siendo desplazable
        mediante la rueda del ratón o técnicas programáticas, pero la barra visual
        de desplazamiento no será visible.

        El método utiliza pack_forget() para eliminar la barra de desplazamiento del
        sistema de gestión de geometría sin destruirla, lo que permite mostrarla
        nuevamente más tarde con show_scrollbars().

        Returns:
            None

        Ejemplos:
            # Ocultar las barras de desplazamiento de un ScrolledFrame existente
            my_scrolled_frame = ScrolledFrame(root)
            my_scrolled_frame.hide_scrollbars()

            # Ocultar temporalmente y luego mostrar de nuevo
            my_scrolled_frame.hide_scrollbars()
            # ... alguna operación ...
            my_scrolled_frame.show_scrollbars()
        """
        # Oculta la barra de desplazamiento vertical eliminándola del sistema de
        # gestión de geometría pack, sin destruirla
        self.vscroll.pack_forget()

    def show_scrollbars(self):
        """Muestra las barras de desplazamiento del ScrolledFrame.

        Este método muestra la barra de desplazamiento vertical (vscroll) en el lado
        derecho del marco. Esto permite al usuario interactuar directamente con la barra
        de desplazamiento además de usar la rueda del ratón para desplazarse.

        El método utiliza pack() con los parámetros side=RIGHT y fill=Y para posicionar
        la barra de desplazamiento en el lado derecho del contenedor y hacer que ocupe
        toda la altura disponible.

        Returns:
            None

        Ejemplos:
            # Mostrar las barras de desplazamiento de un ScrolledFrame existente
            my_scrolled_frame = ScrolledFrame(root)
            my_scrolled_frame.show_scrollbars()

            # Mostrar barras de desplazamiento después de haberlas ocultado
            my_scrolled_frame.hide_scrollbars()
            # ... alguna operación ...
            my_scrolled_frame.show_scrollbars()
        """
        # Muestra la barra de desplazamiento vertical en el lado derecho,
        # ocupando toda la altura disponible
        self.vscroll.pack(side=RIGHT, fill=Y)

    def autohide_scrollbar(self):
        """Alterna la funcionalidad de ocultamiento automático de las barras de desplazamiento.

        Este método actúa como un interruptor que alterna entre dos modos:

        1. Modo de ocultamiento automático activado (self.autohide = True):
           - Las barras de desplazamiento se muestran automáticamente cuando el ratón
             entra en el área del widget.
           - Las barras de desplazamiento se ocultan automáticamente cuando el ratón
             sale del área del widget.

        2. Modo de ocultamiento automático desactivado (self.autohide = False):
           - Las barras de desplazamiento mantienen su estado de visibilidad actual
             independientemente de la posición del ratón.
           - Su visibilidad solo cambia mediante llamadas explícitas a hide_scrollbars()
             o show_scrollbars().

        Cada llamada a este método invierte el estado actual.

        Returns:
            None

        Ejemplos:
            # Activar el ocultamiento automático en un ScrolledFrame
            my_scrolled_frame = ScrolledFrame(root, autohide=False)  # Inicialmente desactivado
            my_scrolled_frame.autohide_scrollbar()  # Ahora activado

            # Alternar el estado de ocultamiento automático
            my_scrolled_frame.autohide_scrollbar()  # Alterna de activado a desactivado, o viceversa
        """
        # Invierte el valor actual de autohide (True → False, False → True)
        self.autohide = not self.autohide

        # Actualizar estado visual según el nuevo valor
        if self.autohide:
            self.hide_scrollbars()
        else:
            self.show_scrollbars()

    def _measures(self):
        """Calcula las proporciones necesarias para el sistema de desplazamiento vertical.

        Este método privado calcula dos valores clave utilizados por los métodos yview:

        1. base: La relación entre el tamaño del contenido y el área visible (inner/outer).
           - Si base = 1.0, el contenido cabe exactamente en el área visible.
           - Si base > 1.0, el contenido es más grande que el área visible y requiere desplazamiento.

        2. thumb: La proporción de la barra de desplazamiento que debe ocupar el "pulgar" visual.
           - Si thumb = 1.0, el pulgar ocupa toda la barra (no se necesita desplazamiento).
           - Si thumb < 1.0, el pulgar ocupa solo una parte de la barra, calculada como (outer/inner).

        El método maneja correctamente casos especiales como cuando el contenido y el área visible
        tienen el mismo tamaño, o cuando el contenido es más pequeño que el área visible.

        Returns:
            tuple: Una tupla (base, thumb) donde:
                - base (float): Relación entre el contenido y el área visible.
                - thumb (float): Proporción de la barra de desplazamiento que debe ocupar el pulgar.

        Ejemplo:
            Si el contenido es dos veces más alto que el área visible:
            - base = 2.0 (contenido dos veces más grande)
            - thumb = 0.5 (el pulgar ocupa la mitad de la barra)
        """
        # Verificar si podemos usar valores en caché
        current_height = self.container.winfo_height()
        content_height = self.winfo_height()

        if (hasattr(self, '_measures_cache') and
                self._measures_cache and
                self._measures_cache['outer'] == current_height and
                self._measures_cache['inner'] == content_height):
            return self._measures_cache['base'], self._measures_cache['thumb']

        # Obtener la altura en píxeles del contenedor visible
        outer = current_height

        # Determinar la altura del contenido interno
        # Usamos max() para asegurar que inner nunca sea menor que outer,
        # lo que garantiza cálculos válidos
        inner = max([content_height, outer])

        # Calcular la relación entre el contenido y el área visible
        # Esta relación indica cuántas veces más grande es el contenido
        base = inner / outer  # Siempre ≥ 1.0

        # Determinar el tamaño relativo del "pulgar" de la barra de desplazamiento
        if inner == outer:
            # Si el contenido y el área visible tienen el mismo tamaño,
            # no se necesita desplazamiento y el pulgar ocupa toda la barra
            thumb = 1.0
        else:
            # El pulgar debe ocupar una proporción de la barra basada en la
            # relación entre el área visible y el contenido total
            thumb = outer / inner  # Siempre < 1.0 cuando se necesita desplazamiento

        # Guardar en caché para futuras llamadas
        self._measures_cache = {
            'outer': current_height,
            'inner': content_height,
            'base': base,
            'thumb': thumb
        }

        # Devolver ambos valores para ser utilizados por los métodos yview
        return base, thumb

    def _on_map_child(self, event):
        """Callback que se ejecuta cuando un widget hijo se mapea en el marco de contenido.

        Este método es llamado automáticamente por el sistema de eventos de Tkinter cuando
        un widget hijo se hace visible (se mapea) dentro del marco de contenido. Su propósito
        es actualizar la vista de desplazamiento para reflejar el nuevo contenido visible.

        La actualización de la vista solo se realiza si el contenedor principal también está
        mapeado (visible), para evitar operaciones innecesarias y posibles errores.

        Args:
            self: Instancia de ScrolledFrame.
            event: Objeto de evento Tkinter que contiene información sobre el evento de mapeo.
                  Incluye detalles como el widget que se mapeó y el tiempo del evento.

        Returns:
            None: Este método no devuelve ningún valor, pero puede modificar la posición
                  de desplazamiento del marco si el contenedor está mapeado.

        Note:
            Este método es privado y está destinado a ser utilizado internamente como un
            callback para eventos <Map>. No debe ser llamado directamente por el usuario.
        """
        # Verificar si el contenedor principal está mapeado (visible)
        if self.container.winfo_ismapped():
            # Actualizar la vista de desplazamiento para reflejar el nuevo contenido
            self.yview()

    def _on_enter(self, event):
        """Callback que se ejecuta cuando el puntero del ratón entra en el ScrolledFrame.

        Este método es llamado automáticamente por el sistema de eventos de Tkinter cuando
        el puntero del ratón entra en el área del widget ScrolledFrame. Tiene dos funciones
        principales:

        1. Habilitar la funcionalidad de desplazamiento con la rueda del ratón, permitiendo
           al usuario desplazar el contenido cuando el ratón está sobre el widget.

        2. Si la funcionalidad de autohide está activada, mostrar las barras de desplazamiento
           para que el usuario pueda interactuar con ellas mientras el ratón está sobre el widget.

        Este método trabaja en conjunto con _on_leave para implementar la funcionalidad de
        autohide, que muestra las barras de desplazamiento solo cuando el ratón está sobre
        el widget, proporcionando una interfaz más limpia y minimalista.

        Args:
            self: Instancia de ScrolledFrame.
            event: Objeto de evento Tkinter que contiene información sobre el evento de entrada
                  del ratón. Incluye detalles como las coordenadas donde entró el ratón.

        Returns:
            None: Este método no devuelve ningún valor, pero modifica el estado del widget.

        Note:
            Este método es privado y está destinado a ser vinculado como callback para
            el evento <Enter> del widget. No debe ser llamado directamente por el usuario.
        """
        # Habilitar el desplazamiento con la rueda del ratón para este widget y sus hijos
        self.enable_scrolling()

        # Si la funcionalidad de autohide está activada, mostrar las barras de desplazamiento
        if self.autohide:
            self.show_scrollbars()

    def _on_leave(self, event):
        """Callback que se ejecuta cuando el puntero del ratón sale del ScrolledFrame.

        Este método es llamado automáticamente por el sistema de eventos de Tkinter cuando
        el puntero del ratón sale del área del widget ScrolledFrame. Tiene dos funciones
        principales:

        1. Deshabilitar la funcionalidad de desplazamiento con la rueda del ratón, evitando
           que el usuario desplace el contenido cuando el ratón no está sobre el widget.

        2. Si la funcionalidad de autohide está activada, ocultar las barras de desplazamiento
           para proporcionar una interfaz más limpia cuando el usuario no está interactuando
           con el widget.

        Este método trabaja en conjunto con _on_enter para implementar la funcionalidad de
        autohide, que muestra las barras de desplazamiento solo cuando el ratón está sobre
        el widget, proporcionando una interfaz más limpia y minimalista.

        Args:
            self: Instancia de ScrolledFrame.
            event: Objeto de evento Tkinter que contiene información sobre el evento de salida
                  del ratón. Incluye detalles como las coordenadas donde salió el ratón.

        Returns:
            None: Este método no devuelve ningún valor, pero modifica el estado del widget.

        Note:
            Este método es privado y está destinado a ser vinculado como callback para
            el evento <Leave> del widget. No debe ser llamado directamente por el usuario.
            Es el complemento directo de _on_enter, realizando las operaciones opuestas.
        """
        # Deshabilitar el desplazamiento con la rueda del ratón para este widget y sus hijos
        self.disable_scrolling()

        # Si la funcionalidad de autohide está activada, ocultar las barras de desplazamiento
        if self.autohide:
            self.hide_scrollbars()

    def _on_configure(self, event):
        """Callback que se ejecuta cuando cambia la configuración del ScrolledFrame.

        Este método es llamado automáticamente por el sistema de eventos de Tkinter cuando
        ocurre un evento <Configure> en el widget. Estos eventos se generan típicamente
        cuando cambia el tamaño o la posición del widget, pero también pueden ocurrir por
        otros cambios de configuración.

        El propósito principal de este callback es actualizar la vista de desplazamiento
        para asegurar que el contenido visible se muestre correctamente después del cambio
        de configuración. Esto es especialmente importante cuando cambia el tamaño del widget,
        ya que puede afectar a qué parte del contenido debería ser visible.

        Args:
            self: Instancia de ScrolledFrame.
            event: Objeto de evento Tkinter que contiene información sobre el evento de
                   configuración, como el nuevo ancho y alto del widget.

        Returns:
            None: Este método no devuelve ningún valor, pero actualiza la posición
                  de desplazamiento del marco.

        Note:
            Este método es privado y está destinado a ser vinculado como callback para
            el evento <Configure> del widget. No debe ser llamado directamente por el usuario.
        """
        # Limpiar caché de medidas ya que el tamaño ha cambiado
        if hasattr(self, '_measures_cache'):
            self._measures_cache = None

        # Actualizar la vista de desplazamiento para reflejar la nueva configuración
        self.yview()

    def _on_map(self, event):
        """Callback que se ejecuta cuando el ScrolledFrame se mapea (se hace visible).

        Este método es llamado automáticamente por el sistema de eventos de Tkinter cuando
        ocurre un evento <Map> en el widget. Estos eventos se generan cuando el widget
        se hace visible en la interfaz, por ejemplo, cuando se muestra inicialmente la ventana
        o cuando se cambia de una pestaña oculta a una visible en una interfaz con pestañas.

        El propósito principal de este callback es actualizar la vista de desplazamiento
        para asegurar que el contenido visible se muestre correctamente cuando el widget
        aparece. Esto es crucial para proporcionar una experiencia de usuario coherente,
        especialmente cuando el widget ha estado previamente oculto.

        Args:
            self: Instancia de ScrolledFrame.
            event: Objeto de evento Tkinter que contiene información sobre el evento de mapeo.

        Returns:
            None: Este método no devuelve ningún valor, pero actualiza la posición
                  de desplazamiento del marco.

        Note:
            Este método es privado y está destinado a ser vinculado como callback para
            el evento <Map> del widget. No debe ser llamado directamente por el usuario.
        """
        # Actualizar la vista de desplazamiento cuando el widget se hace visible
        self.yview()

    def _on_mousewheel(self, event):
        """Callback que se ejecuta cuando se desplaza la rueda del ratón sobre el ScrolledFrame.

        Este método convierte los eventos de rueda del ratón en comandos de desplazamiento
        vertical, adaptándose a las diferencias en la implementación de estos eventos entre
        diferentes sistemas operativos (Windows, macOS, X11).

        La conversión del evento a un valor de desplazamiento (delta) varía según la plataforma:

        - En Windows (win32): Convierte event.delta (múltiplo de 120) a unidades de desplazamiento
          dividiendo por 120 e invirtiendo el signo.
        - En macOS (aqua): Simplemente invierte el signo de event.delta.
        - En X11 (Linux/Unix):
          - Para evento Button-4 (rueda hacia arriba): delta fijo de -10 unidades
          - Para evento Button-5 (rueda hacia abajo): delta fijo de 10 unidades

        En todos los casos, un delta negativo causa desplazamiento hacia arriba y un delta
        positivo causa desplazamiento hacia abajo.

        Args:
            self: Instancia de ScrolledFrame.
            event: Objeto de evento Tkinter que contiene información sobre el evento de la
                   rueda del ratón. Los atributos relevantes varían según el sistema operativo:
                   - Windows: event.delta (múltiplo de ±120)
                   - macOS: event.delta (valor específico de macOS)
                   - X11: event.num (4 para arriba, 5 para abajo)

        Returns:
            None: Este método no devuelve ningún valor, pero causa el desplazamiento
                  del contenido del widget según el movimiento de la rueda del ratón.

        Note:
            Este método es privado y está destinado a ser vinculado como callback para
            eventos de rueda del ratón. La constante UNITS debe estar definida o importada.
        """
        # Obtener tiempo actual para throttling
        current_time = self.tk.call('clock', 'milliseconds')

        # Verificar si ha pasado suficiente tiempo desde el último evento
        if current_time - getattr(self, '_last_wheel_time', 0) < getattr(self, '_wheel_delay', 30):
            return

        # Actualizar timestamp
        self._last_wheel_time = current_time

        # Determinar el valor de desplazamiento (delta) según el sistema operativo
        if self.winsys.lower() == "win32":  # Windows
            # En Windows, event.delta es un múltiplo de 120
            # Dividimos por 120 para normalizar y negamos para que la dirección sea correcta
            delta = -int(event.delta / 120)

        elif self.winsys.lower() == "aqua":  # macOS
            # En macOS, simplemente negamos event.delta
            delta = -event.delta

        elif event.num == 4:  # X11/Linux - desplazamiento hacia arriba
            # Para Button-4 (rueda hacia arriba), usamos un delta fijo de -10
            delta = -10

        elif event.num == 5:  # X11/Linux - desplazamiento hacia abajo
            # Para Button-5 (rueda hacia abajo), usamos un delta fijo de 10
            delta = 10

        else:
            # Evento desconocido, no hacer nada
            return

        # Aplicar el desplazamiento utilizando el delta calculado
        # UNITS indica que el desplazamiento es en unidades, no en páginas
        self.yview_scroll(delta, UNITS)