from tkinter import BaseWidget
import ui.themeengine as ttk

class Dialog(BaseWidget):
    """
    Una clase base para crear diálogos modales.

    Esta clase proporciona la estructura e implementación base para crear diálogos
    modales personalizados utilizando el motor de temas (themeengine). Implementa
    el patrón Template Method, definiendo el flujo de construcción y visualización
    del diálogo, pero delegando la creación del contenido específico a las subclases.

    Los diálogos creados con esta clase son modales (bloquean la interacción con
    otras ventanas de la aplicación hasta que se cierran) y pueden devolver un
    resultado que representa la elección del usuario.

    Para crear un diálogo personalizado, se debe extender esta clase e implementar
    al menos los métodos `create_body` y `create_buttonbox`.
    """

    def __init__(self, parent=None, title="", alert=False):
        """
        Inicializa un nuevo diálogo.

        Configura los atributos básicos necesarios para un diálogo, incluyendo su
        relación con el widget padre, título y comportamiento de alerta. El diálogo
        no se muestra inmediatamente después de la inicialización; para ello se
        debe llamar al método `show()`.

        Parameters:
            parent (Widget, optional):
                Makes the window the logical parent of the message box.
                The messagebox is displayed on top of its parent window.
                Por defecto: None.

            title (str, optional):
                The string displayed as the title of the message box.
                This option is ignored on Mac OS X, where platform
                guidelines forbid the use of a title on this kind of
                dialog.
                Por defecto: "" (se convertirá a un espacio en blanco).

            alert (bool, optional):
                Ring the display's bell when the dialog is shown.
                Por defecto: False.

        Returns:
            None: Este método no devuelve ningún valor explícito.

        Ejemplo:
            dialog = Dialog(parent=main_window, title="Información", alert=True)
        """
        # Inicialización del widget base utilizando el método _setup de BaseWidget
        # En lugar de usar super().__init__(), se utiliza este método específico
        BaseWidget._setup(self, parent, {})

        # Obtiene y almacena el sistema de ventanas actual (win32, x11, aqua)
        # Esto permite comportamientos específicos por plataforma
        self._winsys = self.master.tk.call("tk", "windowingsystem")  # Ejemplo: "win32" en Windows

        # Almacena la referencia al widget padre para su uso posterior
        self._parent = parent  # Ejemplo: un objeto ttk.Frame o None

        # Inicializa el atributo para la ventana de nivel superior como None
        # Esta ventana se creará posteriormente en el método build()
        self._toplevel = None

        # Asegura que el título nunca sea una cadena vacía
        # Si title es vacío, se usa un espacio en blanco
        self._title = title or " "  # Ejemplo: si title="", entonces self._title=" "

        # Inicializa el resultado del diálogo como None
        # Este atributo almacenará el valor de retorno cuando se complete el diálogo
        self._result = None

        # Almacena si se debe emitir un sonido de alerta al mostrar el diálogo
        self._alert = alert  # Ejemplo: True o False

        # Inicializa el widget que recibirá el foco inicial como None
        # Este atributo se establecerá en los métodos create_body o create_buttonbox
        self._initial_focus = None

    def _locate(self):
        """
        Posiciona la ventana de diálogo en relación al widget padre.

        Este método privado calcula las coordenadas x, y de la esquina superior
        izquierda del widget padre (o del maestro del toplevel si no hay padre)
        y establece la geometría del toplevel para que aparezca en esa posición.

        No recibe parámetros adicionales y no devuelve ningún valor.

        Precondiciones:
            - self._toplevel debe estar ya creado
            - self._parent o toplevel.master debe ser un widget válido

        Returns:
            None: Este método no devuelve un valor explícito.

        Nota:
            Este método es para uso interno y normalmente es llamado por el
            método show() cuando no se especifica una posición explícita.
        """
        # Obtiene una referencia local al toplevel para simplificar el código
        toplevel = self._toplevel  # Ejemplo: <ttk.Toplevel object .toplevel1234>

        # Determina qué widget usar como referencia para el posicionamiento
        if self._parent is None:
            # Si no hay un widget padre explícito, usa el maestro del toplevel
            master = toplevel.master  # Ejemplo: la ventana principal de la aplicación
        else:
            # Si hay un widget padre explícito, úsalo como referencia
            master = self._parent  # Ejemplo: un frame específico <ttk.Frame object .frame567>

        # Obtiene la coordenada x absoluta de la esquina superior izquierda del widget de referencia
        x = master.winfo_rootx()  # Ejemplo: 100 (píxeles desde el borde izquierdo de la pantalla)

        # Obtiene la coordenada y absoluta de la esquina superior izquierda del widget de referencia
        y = master.winfo_rooty()  # Ejemplo: 150 (píxeles desde el borde superior de la pantalla)

        # Establece la posición del toplevel para que coincida con la esquina superior izquierda
        # del widget de referencia, sin modificar su tamaño
        toplevel.geometry(f"+{x}+{y}")  # Ejemplo: toplevel.geometry("+100+150")

    def show(self, position=None):
        """
        Muestra el diálogo y bloquea la interacción hasta que se cierre.

        Este método construye el diálogo, lo posiciona en la pantalla, lo hace
        visible y modal (bloqueante), y espera hasta que el usuario lo cierre.
        Es un método bloqueante debido a wait_window(), lo que significa que
        la ejecución del programa se detiene hasta que el diálogo se cierra.

        Parameters:
            position: Tuple[int, int], optional
                The x and y coordinates used to position the dialog. By
                default the dialog will anchor at the NW corner of the
                parent window.

        Returns:
            None: Este método no retorna un valor explícito.
                El resultado del diálogo se debe obtener a través de la
                propiedad `result` después de que el diálogo se cierre.

        Ejemplo:
            dialog = MyDialog(parent=main_window)
            dialog.show()
            result = dialog.result  # Obtiene el resultado después de cerrar
        """
        # Inicializa el resultado como None para asegurar un estado limpio
        self._result = None  # Se reinicia para cada nueva invocación

        # Construye el diálogo (crea self._toplevel y todos los widgets)
        self.build()  # Este método debe estar implementado en esta clase o en subclases

        # Establece la posición del diálogo en la pantalla
        if position is None:
            # Si no se proporciona una posición, usa el posicionamiento automático
            self._locate()  # Posiciona relativo al widget padre
        else:
            try:
                # Intenta desempaquetar y usar las coordenadas proporcionadas
                x, y = position  # Ejemplo: si position=(100, 200), x=100, y=200
                # Establece la geometría (posición) del toplevel
                self._toplevel.geometry(f'+{x}+{y}')  # Ejemplo: '+100+200'
            except:
                # Si hay un error (position no es una tupla válida), usa posicionamiento automático
                self._locate()  # Fallback al método automático

        # Hace visible el diálogo (puede haber estado oculto)
        self._toplevel.deiconify()

        # Emite un sonido de alerta si está configurado para hacerlo
        if self._alert:
            self._toplevel.bell()  # Reproduce el sonido de alerta del sistema

        # Establece el foco inicial en un widget específico si está definido
        if self._initial_focus:
            self._initial_focus.focus_force()  # Fuerza el foco en el widget especificado

        # Hace que el diálogo sea modal (bloquea interacción con otras ventanas)
        self._toplevel.grab_set()  # Redirige todos los eventos a esta ventana

        # Espera hasta que el diálogo se cierre (método bloqueante)
        self._toplevel.wait_window()  # La ejecución se detiene aquí hasta que se cierre

    def create_body(self, master):
        """
        Crea el cuerpo del diálogo.

        Este método debe ser sobrescrito por las subclases y es llamado por el método
        `build`. Su propósito es crear y configurar los widgets que conformarán el
        contenido principal del diálogo.

        Las subclases deben asignar el atributo `self._initial_focus` al widget que
        debe recibir el foco inicial cuando se muestre el diálogo.

        Parameters:
            master (Widget):
                The parent widget.
                El widget padre donde se crearán los widgets del cuerpo del diálogo.

        Returns:
            None: Este método no debe retornar un valor explícito.

        Raises:
            NotImplementedError: Si este método no es sobrescrito por una subclase.

        Ejemplo de implementación en una subclase:
            def create_body(self, master):
                # Crear widgets para el cuerpo del diálogo
                frame = ttk.Frame(master)
                frame.pack(padx=10, pady=10)

                # Añadir un campo de entrada
                self.entry = ttk.Entry(frame)
                self.entry.pack()

                # Establecer el foco inicial en el campo de entrada
                self._initial_focus = self.entry
        """
        # Este método es abstracto y debe ser implementado por subclases
        # Si se llama directamente, lanzará esta excepción
        raise NotImplementedError  # Indica que las subclases deben sobrescribir este método

    def create_buttonbox(self, master):
        """
        Crea la caja de botones del diálogo.

        Este método debe ser sobrescrito por las subclases y es llamado por el método
        `build`. Su propósito es crear y configurar los botones que aparecerán
        típicamente en la parte inferior del diálogo (como "Aceptar", "Cancelar", etc.).

        Las subclases pueden asignar el atributo `self._initial_focus` a uno de los
        botones creados si se desea que este botón reciba el foco inicial cuando se
        muestre el diálogo. Esto tendrá prioridad sobre cualquier widget establecido
        como foco inicial en el método `create_body`.

        Parameters:
            master (Widget):
                The parent widget.
                El widget padre donde se crearán los botones del diálogo.

        Returns:
            None: Este método no debe retornar un valor explícito.

        Raises:
            NotImplementedError: Si este método no es sobrescrito por una subclase.

        Ejemplo de implementación en una subclase:
            def create_buttonbox(self, master):
                # Crear un frame para los botones
                button_frame = ttk.Frame(master)
                button_frame.pack(fill='x', pady=10)

                # Crear botones estándar
                ok_button = ttk.Button(
                    button_frame,
                    text="Aceptar",
                    command=lambda: self._on_button("ok")
                )
                ok_button.pack(side='right', padx=5)

                cancel_button = ttk.Button(
                    button_frame,
                    text="Cancelar",
                    command=lambda: self._on_button("cancel")
                )
                cancel_button.pack(side='right', padx=5)

                # Establecer el foco inicial en el botón Aceptar
                self._initial_focus = ok_button

            def _on_button(self, result):
                # Establecer el resultado y cerrar el diálogo
                self._result = result
                if self._toplevel:
                    self._toplevel.destroy()
        """
        # Este método es abstracto y debe ser implementado por subclases
        # Si se llama directamente, lanzará esta excepción
        raise NotImplementedError  # Indica que las subclases deben sobrescribir este método

    def build(self):
        """
        Construye el diálogo a partir de la configuración establecida.

        Este método crea la ventana de nivel superior (toplevel) con la configuración
        adecuada según la plataforma, y coordina la creación del cuerpo y botones
        del diálogo mediante los métodos template `create_body` y `create_buttonbox`.

        La implementación:
        1. Crea un widget Toplevel con configuración específica según la plataforma
        2. Establece la vinculación de la tecla Escape para cerrar el diálogo
        3. Llama a create_body() para construir el contenido principal
        4. Llama a create_buttonbox() para añadir los botones
        5. Actualiza la ventana para asegurar que todo está correctamente dimensionado

        Este método es llamado típicamente por show() antes de mostrar el diálogo.

        Returns:
            None: Este método no devuelve un valor explícito.

        Nota:
            Este método requiere que las subclases implementen los métodos
            create_body() y create_buttonbox().
        """
        # Configuración del toplevel basada en el sistema de ventanas
        if self._winsys == "win32":
            # Configuración específica para Windows
            self._toplevel = ttk.Toplevel(
                transient=self.master,  # Hace que el diálogo sea transitorio respecto a su maestro
                title=self._title,  # Establece el título configurado en __init__
                resizable=(0, 0),  # No permite redimensionar (ni horizontal ni verticalmente)
                minsize=(250, 15),  # Establece un tamaño mínimo específico para Windows
                iconify=True,  # Inicialmente iconificado (será revertido después)
            )
        else:
            # Configuración para otros sistemas (Linux, macOS)
            self._toplevel = ttk.Toplevel(
                transient=self.master,  # Hace que el diálogo sea transitorio respecto a su maestro
                title=self._title,  # Establece el título configurado en __init__
                resizable=(0, 0),  # No permite redimensionar (ni horizontal ni verticalmente)
                windowtype="dialog",  # Específica de sistemas no-Windows, marca como ventana de diálogo
                iconify=True,  # Inicialmente iconificado (será revertido después)
            )

        # Restablece el estado de iconificación (oculta temporalmente la ventana)
        self._toplevel.withdraw()  # Necesario porque se creó con iconify=True

        # Vincula la tecla Escape para cerrar el diálogo
        self._toplevel.bind("<Escape>", lambda _: self._toplevel.destroy())

        # Crea los widgets del diálogo llamando a los métodos template
        self.create_body(self._toplevel)  # Crea el contenido principal del diálogo
        self.create_buttonbox(self._toplevel)  # Crea los botones (Aceptar, Cancelar, etc.)

        # Actualiza la ventana antes de mostrarla para asegurar que todo está
        # correctamente dimensionado y posicionado
        self._toplevel.update_idletasks()

    @property
    def result(self):
        """
        Retorna el resultado del diálogo.

        Esta propiedad proporciona acceso de solo lectura al resultado del diálogo,
        que se establece típicamente cuando el usuario interactúa con los botones
        del diálogo y se cierra.

        El valor específico depende de la implementación de la subclase y de cómo
        establezca `self._result` en sus manejadores de eventos. Los valores comunes
        incluyen:

        - `None`: El valor predeterminado, generalmente indica que el diálogo no
                  se ha cerrado o que no se ha establecido un resultado.
        - `True`/`False`: Indica una respuesta afirmativa o negativa.
        - Cadenas como `"ok"`, `"cancel"`, `"yes"`, `"no"`, etc.
        - Objetos o valores específicos según la funcionalidad del diálogo.

        Returns:
            El valor almacenado en `self._result`, que puede ser de cualquier tipo
            según cómo la subclase lo haya establecido.

        Ejemplo:
            ```python
            dialog = MyDialog(parent=main_window)
            dialog.show()
            if dialog.result:
                # El usuario confirmó la acción
                perform_action()
            else:
                # El usuario canceló o cerró el diálogo
                pass
            ```
        """
        # Simplemente retorna el valor almacenado en el atributo interno
        return self._result  # Podría ser None, True, False, una cadena, o cualquier otro valor