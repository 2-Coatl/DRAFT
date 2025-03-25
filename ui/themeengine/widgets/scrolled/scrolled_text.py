import ui.themeengine as ttk
from ui.themeengine.utils.constants import *

class ScrolledText(ttk.Frame):
    """Widget de texto con barras de desplazamiento vertical y horizontal opcionales.

    Al establecer `autohide=True`, las barras de desplazamiento se ocultarán cuando
    el ratón no esté sobre el widget. La barra de desplazamiento vertical está
    activada por defecto, pero puede desactivarse. La barra de desplazamiento
    horizontal puede activarse estableciendo `hbar=True`.

    Este widget es idéntico en configuración al widget `Text` estándar, con la
    adición del marco de desplazamiento. Para todas las opciones de configuración
    del texto, consulte la documentación oficial:
    https://tcl.tk/man/tcl8.6/TkCmd/text.htm

    Parámetros:
        master (Widget): El widget padre.
        padding (int): Cantidad de espacio vacío alrededor del widget (por defecto 2).
        bootstyle (str): Estilo visual para las barras de desplazamiento.
        autohide (bool): Si es True, las barras se ocultan cuando el ratón no está
                         sobre el widget (por defecto False).
        vbar (bool): Si es True, se muestra la barra vertical (por defecto True).
        hbar (bool): Si es True, se muestra la barra horizontal (por defecto False).
        **kwargs: Argumentos adicionales pasados al widget Text.

    Atributos:
        text: El widget Text interno.
        vbar: La barra de desplazamiento vertical (None si está desactivada).
        hbar: La barra de desplazamiento horizontal (None si está desactivada).

    Ejemplos:
        ```python
        import ui.themeengine as ttk
        from ui.themeengine.utils.constants import *
        from ui.themeengine.widgets.scrolled import ScrolledText

        app = ttk.Window()

        # texto con desplazamiento y barra vertical autooculta
        st = ScrolledText(app, padding=5, height=10, autohide=True)
        st.pack(fill=BOTH, expand=YES)

        # añadir texto
        st.insert(END, 'Inserta tu texto aquí.')

        # texto con barras vertical y horizontal
        st2 = ScrolledText(app, padding=5, hbar=True, bootstyle="primary")
        st2.pack(fill=BOTH, expand=YES)

        app.mainloop()
        ```
    """

    def __init__(
        self,
        master=None,  # Widget padre, por defecto la ventana principal
        padding=2,  # Espacio alrededor del widget en píxeles
        bootstyle=DEFAULT,  # Estilo visual para las barras de desplazamiento
        autohide=False,  # True para ocultar las barras cuando no se usan
        vbar=True,  # True para mostrar barra vertical
        hbar=False,  # True para mostrar barra horizontal
        **kwargs,  # Argumentos adicionales para el widget Text
    ):
        """Inicializa un widget de texto con barras de desplazamiento opcionales.

        Este constructor crea un widget compuesto que integra un widget de texto
        con barras de desplazamiento vertical y/u horizontal configurables.

        Parámetros:
            master (Widget, opcional):
                El widget padre. Si es None, se usará la ventana principal.

            padding (int, opcional):
                La cantidad de espacio vacío alrededor del widget en píxeles.
                Por defecto es 2.

            bootstyle (str, opcional):
                Palabra clave de estilo para establecer el color y estilo de las
                barras de desplazamiento. Opciones disponibles: primary, secondary,
                success, info, warning, danger, dark, light.

            autohide (bool, opcional):
                Cuando es True, las barras de desplazamiento se ocultan cuando el
                ratón no está sobre el widget. Por defecto es False.

            vbar (bool, opcional):
                Se muestra una barra de desplazamiento vertical cuando es True.
                Por defecto es True.

            hbar (bool, opcional):
                Se muestra una barra de desplazamiento horizontal cuando es True.
                Por defecto es False. Al activar esta barra, también se establece
                wrap="none" en el widget de texto.

            **kwargs (Dict[str, Any], opcional):
                Otros argumentos pasados al widget Text.
        """
        # Inicializa el Frame contenedor con el padding especificado
        super().__init__(master, padding=padding)

        # Crea el widget Text dentro del Frame con un padding horizontal
        # La mayoría de los widgets en themeengine tienen un padding por defecto
        self._text = ttk.Text(self, padx=50, **kwargs)
        self._hbar = None  # Inicializa referencia a la barra horizontal
        self._vbar = None  # Inicializa referencia a la barra vertical

        # Delega los métodos del widget Text al Frame
        # Esto permite usar los métodos de Text directamente desde ScrolledText
        # Ejemplo: st.insert(END, "texto") en lugar de st._text.insert(END, "texto")
        for method in vars(ttk.Text).keys():
            # Excluye métodos de posicionamiento para evitar conflictos
            if any(["pack" in method, "grid" in method, "place" in method]):
                pass
            else:
                # Crea un atributo en ScrolledText que apunta al método de Text
                setattr(self, method, getattr(self._text, method))

        # Configura la barra de desplazamiento vertical si se solicita
        if vbar:
            # Crea la barra vertical con el estilo especificado
            self._vbar = ttk.Scrollbar(
                master=self,  # El Frame es el padre
                bootstyle=bootstyle,  # Usa el estilo especificado
                command=self._text.yview,  # Conecta la barra al desplazamiento vertical
                orient=VERTICAL,  # Orientación vertical
            )
            # Coloca la barra en el lado derecho del Frame
            self._vbar.place(relx=1.0, relheight=1.0, anchor=NE)
            # Conecta el desplazamiento del texto con la posición de la barra
            self._text.configure(yscrollcommand=self._vbar.set)

        # Configura la barra de desplazamiento horizontal si se solicita
        if hbar:
            # Crea la barra horizontal con el estilo especificado
            self._hbar = ttk.Scrollbar(
                master=self,  # El Frame es el padre
                bootstyle=bootstyle,  # Usa el estilo especificado
                command=self._text.xview,  # Conecta la barra al desplazamiento horizontal
                orient=HORIZONTAL,  # Orientación horizontal
            )
            # Coloca la barra en la parte inferior del Frame
            self._hbar.place(rely=1.0, relwidth=1.0, anchor=SW)
            # Conecta el desplazamiento del texto con la posición de la barra
            # y desactiva el ajuste automático del texto
            self._text.configure(xscrollcommand=self._hbar.set, wrap="none")

        # Posiciona el widget Text dentro del Frame
        # Ocupa todo el espacio disponible y se expande
        self._text.pack(side=LEFT, fill=BOTH, expand=YES)

        # Guarda dimensiones para ajustes posteriores si hay barra horizontal
        if self._hbar:
            # Actualiza las tareas pendientes para obtener dimensiones correctas
            self.update_idletasks()
            # Guarda el ancho requerido del widget
            self._text_width = self.winfo_reqwidth()
            self._scroll_width = self.winfo_reqwidth()

        # Asocia el evento de cambio de tamaño con el método de ajuste
        self.bind("<Configure>", self._on_configure)

        # Configura el autoocultar de las barras si se solicita
        if autohide:
            # Establece eventos para mostrar/ocultar las barras
            self.autohide_scrollbar()
            # Inicialmente oculta las barras
            self.hide_scrollbars()

    def _on_configure(self, *_):
        """Callback que se ejecuta cuando cambia el tamaño o configuración del widget.

        Este método ajusta la posición y el tamaño de la barra de desplazamiento
        horizontal cuando cambia el tamaño del widget, para asegurar que no se
        superponga con la barra vertical y mantenga una apariencia coherente.

        Parámetros:
            *_ : Los argumentos del evento que generó la llamada, que no se utilizan
                 en este método pero son requeridos por el sistema de eventos.

        Notas:
            - Solo realiza acciones si existe una barra horizontal (self._hbar).
            - Asume que si hay una barra horizontal también hay una vertical (self._vbar).
        """
        # Verifica si existe una barra de desplazamiento horizontal
        # Si no existe, el método termina sin hacer nada
        if self._hbar:
            # Actualiza las tareas pendientes para garantizar medidas precisas
            # Esto es necesario para obtener dimensiones actualizadas
            self.update_idletasks()

            # Obtiene el ancho actual del widget completo en píxeles
            # Ejemplo: Si el widget mide 400px de ancho, text_width = 400
            text_width = self.winfo_width()

            # Obtiene el ancho de la barra de desplazamiento vertical en píxeles
            # Ejemplo: Si la barra vertical mide 20px de ancho, vbar_width = 20
            vbar_width = self._vbar.winfo_width()

            # Calcula la proporción relativa para el ancho de la barra horizontal
            # Esta proporción asegura que la barra horizontal no se extienda debajo de la vertical
            # Ejemplo: Con widget de 400px y barra vertical de 20px:
            # relx = (400 - 20) / 400 = 0.95, es decir, 95% del ancho total
            relx = (text_width - vbar_width) / text_width

            # Reposiciona la barra horizontal con el nuevo ancho relativo
            # rely=1.0 mantiene la barra en la parte inferior del widget
            # relwidth=relx ajusta el ancho para evitar superposición con la barra vertical
            self._hbar.place(rely=1.0, relwidth=relx)

    @property
    def text(self):
        """Devuelve el objeto de texto interno.

        Esta propiedad proporciona acceso al widget Text subyacente,
        permitiendo operaciones directas sobre el texto cuando sea necesario.

        Returns:
            ttk.Text: El widget de texto interno.
        """
        return self._text

    @property
    def hbar(self):
        """Devuelve la barra de desplazamiento horizontal interna.

        Esta propiedad proporciona acceso a la barra de desplazamiento horizontal,
        permitiendo configuraciones adicionales o acceso directo cuando sea necesario.
        Puede devolver None si la barra horizontal no está habilitada.

        Returns:
            Union[ttk.Scrollbar, None]: La barra de desplazamiento horizontal o None si no está habilitada.

        """
        return self._hbar

    @property
    def vbar(self):
        """Devuelve la barra de desplazamiento vertical interna.

        Esta propiedad proporciona acceso a la barra de desplazamiento vertical,
        permitiendo configuraciones adicionales o acceso directo cuando sea necesario.
        Puede devolver None si la barra vertical no está habilitada.

        Returns:
            Union[ttk.Scrollbar, None]: La barra de desplazamiento vertical o None si no está habilitada.

        """
        return self._vbar

    def hide_scrollbars(self, *_):
        """Oculta las barras de desplazamiento.

        Este método coloca las barras de desplazamiento vertical y horizontal
        detrás del widget de texto, haciéndolas visualmente invisibles sin
        desactivar su funcionalidad. Si alguna de las barras no existe,
        el método maneja silenciosamente esta situación y continúa.

        Parámetros:
            *_ : Argumentos adicionales que permiten usar este método como
                 callback para eventos, aunque no se utilizan.

        Notas:
            - Este método utiliza el sistema de orden de apilamiento (stacking order)
              de Tkinter para ocultar las barras, no modifica su visibilidad real.
            - Las barras siguen siendo funcionales aunque no sean visibles.
            - Se puede usar en conjunto con show_scrollbars() para implementar
              comportamiento de autoocultar.

        Ejemplo:
            ```python
            st = ScrolledText(root)
            st.hide_scrollbars()  # Oculta las barras de desplazamiento
            ```
        """

        # Intenta ocultar la barra de desplazamiento vertical
        # Coloca la barra detrás del widget de texto en el orden de apilamiento
        try:
            # lower() modifica el orden Z, colocando _vbar detrás de _text
            # Esto hace que _vbar sea visualmente invisible pero sigue siendo funcional
            # Ejemplo: Si hay texto y una barra vertical, la barra quedará oculta detrás del texto
            self._vbar.lower(self._text)
        except:
            # Ignora silenciosamente cualquier error
            # Esto ocurre si _vbar es None (no hay barra vertical) o si lower() falla
            pass

        # Intenta ocultar la barra de desplazamiento horizontal
        # Similar al proceso anterior pero para la barra horizontal
        try:
            # Coloca la barra horizontal detrás del widget de texto
            # Ejemplo: Si hay una barra horizontal, quedará oculta detrás del texto
            self._hbar.lower(self._text)
        except:
            # Ignora silenciosamente cualquier error
            # Esto ocurre si _hbar es None (no hay barra horizontal) o si lower() falla
            pass

    def show_scrollbars(self, *_):
        """Muestra las barras de desplazamiento.

        Este método coloca las barras de desplazamiento vertical y horizontal
        por encima del widget de texto, haciéndolas visualmente visibles. Si
        alguna de las barras no existe, el método maneja silenciosamente esta
        situación y continúa.

        Parámetros:
            *_ : Argumentos adicionales que permiten usar este método como
                 callback para eventos, aunque no se utilizan.

        Notas:
            - Este método utiliza el sistema de orden de apilamiento (stacking order)
              de Tkinter para mostrar las barras, no modifica su visibilidad real.
            - Es el método complementario a hide_scrollbars() y se utiliza para
              restaurar la visibilidad de las barras después de ocultarlas.
            - Se puede usar en conjunto con hide_scrollbars() para implementar
              comportamiento de autoocultar.

        Ejemplo:
            ```python
            st = ScrolledText(root)
            st.hide_scrollbars()  # Oculta las barras
            # ... algún tiempo después ...
            st.show_scrollbars()  # Muestra las barras nuevamente
            ```
        """
        # Intenta mostrar la barra de desplazamiento vertical
        # Coloca la barra por encima del widget de texto en el orden de apilamiento
        try:
            # lift() modifica el orden Z, colocando _vbar por encima de _text
            # Esto hace que _vbar sea visualmente visible
            # Ejemplo: Si hay texto y una barra vertical, la barra quedará visible
            self._vbar.lift(self._text)
        except:
            # Ignora silenciosamente cualquier error
            # Esto ocurre si _vbar es None (no hay barra vertical) o si lift() falla
            pass

        # Intenta mostrar la barra de desplazamiento horizontal
        # Similar al proceso anterior pero para la barra horizontal
        try:
            # Coloca la barra horizontal por encima del widget de texto
            # Ejemplo: Si hay una barra horizontal, quedará visible
            self._hbar.lift(self._text)
        except:
            # Ignora silenciosamente cualquier error
            # Esto ocurre si _hbar es None (no hay barra horizontal) o si lift() falla
            pass

    def autohide_scrollbar(self, *_):
        """Configura el comportamiento de autoocultar para las barras de desplazamiento.

        Este método establece enlaces de eventos para mostrar automáticamente las
        barras de desplazamiento cuando el puntero del ratón entra en el widget
        y ocultarlas cuando sale. Esto mejora la experiencia de usuario reduciendo
        el desorden visual cuando las barras no se están utilizando activamente.

        Parámetros:
            *_ : Argumentos adicionales que permiten usar este método como
                 callback para eventos, aunque no se utilizan.

        Notas:
            - Utiliza los métodos show_scrollbars() y hide_scrollbars() como callbacks.
            - Una vez configurado, el comportamiento persiste hasta que se desactive.
            - Funciona incluso si algunas barras no están habilitadas.
            - Llamar a este método múltiples veces no causa problemas, pero
              podría acumular múltiples enlaces para los mismos eventos.

        Ejemplo:
            ```python
            st = ScrolledText(root, autohide=False)
            st.pack(fill=BOTH, expand=YES)

            # Activar el autoocultar después de la inicialización
            st.autohide_scrollbar()
            ```
        """
        # Enlaza el evento de entrada del ratón con el método show_scrollbars
        # Esto hace que las barras se muestren cuando el ratón entra en el widget
        # Es un enlace a nivel de widget, no a nivel de las barras individuales
        # Ejemplo: Cuando el usuario mueve el ratón sobre el widget, las barras aparecen
        self.bind("<Enter>", self.show_scrollbars)

        # Enlaza el evento de salida del ratón con el método hide_scrollbars
        # Esto hace que las barras se oculten cuando el ratón sale del widget
        # El evento se activa solo cuando el ratón sale completamente del widget
        # Ejemplo: Cuando el usuario mueve el ratón fuera del widget, las barras desaparecen
        self.bind("<Leave>", self.hide_scrollbars)
