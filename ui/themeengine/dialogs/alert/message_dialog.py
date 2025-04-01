import textwrap
import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine import Dialog
from ui.themeengine.localization import MessageCatalog


class MessageDialog(Dialog):
    """
    Diálogo modal simple para mostrar mensajes con botones interactivos.

    Esta clase permite crear ventanas emergentes que muestran un mensaje al usuario
    junto con un conjunto configurable de botones. El diálogo bloquea la interacción
    con otras ventanas hasta que el usuario selecciona uno de los botones, devolviendo
    el texto del botón seleccionado como resultado.

    Características principales:
    - Muestra un mensaje con formato y ajuste automático de texto
    - Permite incluir un icono junto al mensaje
    - Soporta botones personalizables con diferentes estilos visuales
    - Ofrece traducción automática de textos mediante MessageCatalog
    - Permite ejecutar comandos asociados a la interacción del usuario

    La clase implementa el patrón Template Method a través de su herencia de Dialog,
    proporcionando implementaciones específicas para los métodos abstractos
    create_body() y create_buttonbox().

    Ejemplos:
        # Diálogo básico con botones predeterminados
        dialog = MessageDialog("¿Desea guardar los cambios?")
        result = dialog.show()
        if result == "OK":
            # Realizar acción de guardado

        # Diálogo personalizado con botones específicos
        dialog = MessageDialog(
            message="El archivo contiene cambios sin guardar.",
            title="Advertencia",
            buttons=["No guardar:danger", "Cancelar:secondary", "Guardar:success"],
            default="Guardar",
            icon="warning.png"
        )
        result = dialog.show()
    """

    def __init__(
        self,
        message,
        title=" ",
        buttons=None,
        command=None,
        width=50,
        parent=None,
        alert=False,
        default=None,
        padding=(20, 20),
        icon=None,
        **kwargs,
    ):
        """
        Inicializa un diálogo modal para mostrar mensajes con botones configurables.

        Este constructor prepara todos los atributos necesarios para crear un diálogo
        modal que muestra un mensaje con botones interactivos. El diálogo no se muestra
        inmediatamente después de la inicialización; es necesario llamar al método `show()`
        para visualizarlo.

        Parámetros:
            message (str):
                Mensaje principal a mostrar en el diálogo.

            title (str, opcional):
                Título que aparece en la barra de título de la ventana.
                Valor predeterminado: " "
                Nota: Este parámetro se ignora en Mac OS X, donde las guías de
                diseño de la plataforma prohíben el uso de títulos en este tipo
                de diálogos.

            buttons (List[str], opcional):
                Lista de botones que aparecerán en la parte inferior del diálogo.
                Cada elemento puede ser simplemente el texto del botón, o puede
                incluir un estilo específico usando el formato "texto:estilo".
                Por ejemplo: ["OK", "Cancel"] o ["OK:success", "Cancel:danger"].
                Si no se especifica un estilo, se usa "primary" por defecto.
                Valor predeterminado: ["Cancel:secondary", "OK:primary"] (traducidos)

            command (Callable, opcional):
                Función a invocar cuando el usuario cierra el diálogo.
                Valor predeterminado: None

            width (int, opcional):
                Número máximo de caracteres por línea en el mensaje. Si el texto
                excede este límite, se realizará un ajuste automático de línea.
                Valor predeterminado: 50

            parent (Widget, opcional):
                Widget padre del diálogo. Determina la posición relativa y
                el comportamiento modal.
                Valor predeterminado: None

            alert (bool, opcional):
                Si es True, hace sonar la campana del sistema al mostrar el diálogo.
                Valor predeterminado: False

            default (str, opcional):
                Texto del botón predeterminado que responderá a la tecla Enter.
                Si no se especifica, se usará el botón más a la derecha.
                Valor predeterminado: None

            padding (Union[int, Tuple[int, int]], opcional):
                Espaciado interno entre el borde del diálogo y su contenido.
                Puede ser un solo valor o una tupla (horizontal, vertical).
                Valor predeterminado: (20, 20)

            icon (Union[str, bytes], opcional):
                Ruta a un archivo de imagen o datos de imagen a mostrar junto al mensaje.
                Valor predeterminado: None

            **kwargs:
                Argumentos adicionales. Opciones soportadas:
                - localize (bool): Si es True, traduce automáticamente los textos
                  de los botones mediante MessageCatalog.

        Ejemplos:
            # Diálogo básico con botones predeterminados
            dialog = MessageDialog("¿Desea guardar los cambios?")
            result = dialog.show()

            # Diálogo personalizado con botones específicos y un icono
            dialog = MessageDialog(
                message="El archivo contiene cambios sin guardar.",
                title="Advertencia",
                buttons=["No guardar:danger", "Cancelar:secondary", "Guardar:success"],
                default="Guardar",
                icon="warning.png"
            )
            result = dialog.show()

            # Diálogo con una función de callback
            def on_close():
                print("El diálogo se ha cerrado")

            dialog = MessageDialog(
                message="Operación completada con éxito.",
                command=on_close
            )
            dialog.show()
        """
        # Llama al constructor de la clase base Dialog
        # Establece el widget padre, título y comportamiento de alerta
        super().__init__(parent, title, alert)

        # Almacena los parámetros como atributos de instancia con prefijo _
        # para uso interno en otros métodos de la clase
        self._message = message  # Ej: "¿Desea guardar los cambios?"
        self._command = command  # Ej: una función callback o None
        self._width = width  # Ej: 50 (caracteres por línea)
        self._alert = alert  # Ej: False (sin sonido de alerta)
        self._default = default  # Ej: "OK" (botón predeterminado)
        self._padding = padding  # Ej: (20, 20) (px horizontal y vertical)
        self._icon = icon  # Ej: "warning.png" o datos de imagen

        # Extrae la opción de localización de los argumentos adicionales
        # Si localize=True, se traducirán los textos de los botones personalizados
        self._localize = kwargs.get("localize")  # Ej: True, False o None

        # Configura los botones predeterminados si no se proporcionaron
        if buttons is None:
            # Crea botones "Cancel" y "OK" traducidos con estilos específicos
            # Ej: ["Cancelar:secondary", "Aceptar:primary"] en español
            self._buttons = [
                f"{MessageCatalog.translate('Cancel')}:secondary",
                f"{MessageCatalog.translate('OK')}:primary",
            ]
        else:
            # Usa los botones proporcionados por el usuario
            # Ej: ["No guardar:danger", "Cancelar:secondary", "Guardar:success"]
            self._buttons = buttons

    def create_body(self, master):
        """
        Sobrescribe el método de la clase base para crear el cuerpo del diálogo.

        Este método construye el área principal del diálogo que contiene el mensaje
        y, opcionalmente, un icono. El mensaje se divide en líneas y se ajusta
        automáticamente según el ancho máximo especificado en el constructor.

        El método maneja dos formas de proporcionar un icono:
        1. Como datos de imagen directamente
        2. Como ruta a un archivo de imagen

        Parámetros:
            master (Widget):
                El widget contenedor donde se construirá el cuerpo del diálogo.
                Normalmente proporcionado por la clase base Dialog.

        Retorna:
            None: El método modifica la interfaz gráfica pero no devuelve valores.

        Efectos:
            - Crea un frame contenedor dentro del widget master
            - Si hay un icono válido, lo muestra a la izquierda
            - Si hay un mensaje, lo muestra con ajuste automático de línea
            - El contenedor se expande para llenar el espacio horizontal disponible

        Notas:
            - Los mensajes pueden incluir saltos de línea explícitos con '\n'
            - Cada línea del mensaje se ajusta individualmente según el ancho máximo
            - Si el icono no puede cargarse, se muestra un mensaje de error en consola
        """
        # Crea un contenedor principal con el padding definido en el constructor
        # Ej: padding=(20, 20) crea un frame con 20px de espacio en cada lado
        container = ttk.Frame(master, padding=self._padding)

        # Si se proporcionó un icono, intenta cargarlo y mostrarlo
        if self._icon:
            try:
                # Primer intento: asume que self._icon contiene datos de imagen
                # Ej: datos PNG o GIF en formato base64 o bytes
                self._img = ttk.PhotoImage(data=self._icon)
                icon_lbl = ttk.Label(container, image=self._img)
                icon_lbl.pack(side=LEFT, padx=5)  # Icono a la izquierda con 5px de margen
            except:
                try:
                    # Segundo intento: asume que self._icon es una ruta de archivo
                    # Ej: "warning.png", "icons/info.gif"
                    self._img = ttk.PhotoImage(file=self._icon)
                    icon_lbl = ttk.Label(container, image=self._img)
                    icon_lbl.pack(side=LEFT, padx=5)
                except:
                    # Si ningún intento funciona, sólo muestra un mensaje en la consola
                    # No se muestra ningún error visual al usuario final
                    print("MessageDialog icon is invalid")

        # Si hay un mensaje, procésalo y muéstralo
        if self._message:
            # Divide el mensaje en líneas individuales usando \n como separador
            # Ej: "Línea 1\nLínea 2" → ["Línea 1", "Línea 2"]
            for msg in self._message.split("\n"):
                # Ajusta cada línea según el ancho máximo (self._width)
                # Ej: Con width=20, "Este es un mensaje largo" →
                # ["Este es un", "mensaje largo"] → "Este es un\nmensaje largo"
                message = "\n".join(textwrap.wrap(msg, width=self._width))

                # Crea una etiqueta para mostrar esta parte del mensaje
                message_label = ttk.Label(container, text=message)

                # Empaqueta la etiqueta con 3px de espacio inferior
                # fill=X hace que la etiqueta use todo el ancho disponible
                # anchor=N alinea el texto en la parte superior
                message_label.pack(pady=(0, 3), fill=X, anchor=N)

        # Finalmente, empaqueta todo el contenedor en el master
        # fill=X y expand=True hacen que use todo el ancho disponible
        container.pack(fill=X, expand=True)

    def create_buttonbox(self, master):
        """
        Sobrescribe el método de la clase base para crear la caja de botones del diálogo.

        Este método construye el área inferior del diálogo que contiene los botones
        interactivos que permiten al usuario responder al mensaje. Los botones se crean
        y configuran según la lista `_buttons` definida en la inicialización.

        Características principales:
        - Los botones se muestran de derecha a izquierda
        - Cada botón puede tener un estilo visual específico (usando el formato "texto:estilo")
        - Se puede definir un botón predeterminado que responde a la tecla Enter
        - Los textos de los botones pueden traducirse automáticamente
        - Se establece un orden de traversía del foco de izquierda a derecha

        Parámetros:
            master (Widget):
                El widget contenedor donde se construirá la caja de botones.
                Normalmente proporcionado por la clase base Dialog.

        Retorna:
            None: El método modifica la interfaz gráfica pero no devuelve valores.

        Efectos:
            - Crea un frame contenedor con los botones configurados
            - Configura cada botón para que llame a `on_button_press` cuando se active
            - Establece el botón predeterminado y vincula la tecla Enter a él
            - Configura el foco inicial para cuando se muestre el diálogo
            - Añade un separador visual entre el cuerpo del mensaje y los botones

        Notas:
            - El formato para definir botones es "texto:estilo" (ej. "OK:primary")
            - Si no se especifica estilo, se usa "secondary" como predeterminado
            - Si _localize es True, los textos de los botones se traducen automáticamente
        """
        # Crea un frame contenedor para los botones con un padding de 5px
        frame = ttk.Frame(master, padding=(5, 5))

        # Lista para almacenar referencias a todos los botones creados
        button_list = []

        # Procesa los botones en orden inverso (de derecha a izquierda en la UI)
        # Ejemplo: ["Cancel", "OK"] se mostrará como [OK] [Cancel]
        for i, button in enumerate(self._buttons[::-1]):
            # Divide la definición del botón por ":" para separar texto y estilo
            # Ejemplo: "OK:primary" -> ["OK", "primary"]
            cnf = button.split(":")

            # Determina el texto y estilo del botón
            if len(cnf) == 2:
                # Si hay dos partes, usa la primera como texto y la segunda como estilo
                # Ejemplo: "OK:primary" -> text="OK", bootstyle="primary"
                text, bootstyle = cnf
            else:
                # Si no hay separador, usa todo como texto y asigna estilo predeterminado
                # Ejemplo: "Cancel" -> text="Cancel", bootstyle="secondary"
                text = cnf[0]
                bootstyle = "secondary"

            # Si la localización está activada, traduce el texto del botón
            # Ejemplo: "Cancel" -> "Cancelar" (en español)
            if self._localize == True:
                text = MessageCatalog.translate(text)

            # Crea el botón con el texto y estilo determinados
            btn = ttk.Button(frame, bootstyle=bootstyle, text=text)

            # Configura el comando que se ejecutará cuando se haga clic
            # La lambda captura el botón actual mediante el parámetro por defecto
            btn.configure(command=lambda b=btn: self.on_button_press(b))

            # Empaqueta el botón a la derecha con margen horizontal de 2px
            btn.pack(padx=2, side=RIGHT)

            # Ajusta el orden de apilamiento para que el foco se mueva de izquierda a derecha
            btn.lower()

            # Guarda una referencia al botón en la lista
            button_list.append(btn)

            # Determina si este botón debe ser el foco inicial
            if self._default is not None and text == self._default:
                # Si coincide con el botón predeterminado especificado
                # Ejemplo: default="OK" y este botón es "OK"
                self._initial_focus = btn
            elif self._default is None and i == 0:
                # Si no hay botón predeterminado y este es el primer botón procesado
                # (el último en la lista original, el más a la derecha en la UI)
                self._initial_focus = btn

        # Vincula la tecla Enter para activar el último botón procesado
        # Nota: Esto podría no ser el botón predeterminado
        self._toplevel.bind("<Return>", lambda _, b=btn: b.invoke())
        self._toplevel.bind("<KP_Enter>", lambda _, b=btn: b.invoke())

        # Añade un separador horizontal entre el cuerpo del mensaje y los botones
        ttk.Separator(self._toplevel).pack(fill=X)

        # Empaqueta el frame de botones en la parte inferior
        frame.pack(side=BOTTOM, fill=X, anchor=S)

        # Si no se ha establecido un foco inicial (ningún botón coincidió con _default),
        # usa el primer botón de la lista (el más a la derecha)
        if not self._initial_focus:
            self._initial_focus = button_list[0]

    def on_button_press(self, button):
        """
        Maneja el evento de presionar un botón en el diálogo.

        Este método se ejecuta cuando el usuario hace clic en uno de los botones
        del diálogo. Realiza tres operaciones principales:
        1. Guarda el texto del botón como resultado del diálogo
        2. Ejecuta el comando asociado (si existe)
        3. Cierra la ventana del diálogo

        El resultado guardado puede ser recuperado después de que el diálogo
        se cierra, típicamente a través del valor retornado por el método `show()`.

        Parámetros:
            button (ttk.Button):
                El objeto botón que fue presionado. Debe tener un atributo "text"
                que identifica la acción seleccionada.

        Retorna:
            None: El método no devuelve valores explícitamente.

        Efectos:
            - Almacena el texto del botón en `self._result`
            - Ejecuta `self._command()` si existe
            - Destruye la ventana del diálogo

        Notas:
            - El comando asociado se ejecuta sin argumentos, no recibe información
              sobre qué botón fue presionado.
            - La ventana se destruye después de guardar el resultado y ejecutar
              el comando, asegurando que esas operaciones puedan completarse.
        """
        # Extrae el texto del botón y lo almacena como resultado del diálogo
        # Ejemplo: Si el botón muestra "OK", self._result será "OK"
        self._result = button["text"]

        # Obtiene el comando asociado con el diálogo
        # Este comando habría sido configurado durante la inicialización
        command = self._command

        # Si existe un comando, lo ejecuta
        # Nota: El comando no recibe información sobre qué botón fue presionado
        if command is not None:
            command()

        # Finalmente, destruye la ventana del diálogo
        # Esto ocurre después de guardar el resultado y ejecutar el comando
        self._toplevel.destroy()

    def show(self, position=None):
        """
        Crea y muestra el diálogo de mensaje como una ventana emergente.

        Este método visualiza el diálogo configurado con el mensaje y botones
        especificados durante la inicialización. El diálogo se muestra como una
        ventana modal, lo que significa que bloquea la interacción con otras ventanas
        de la aplicación hasta que el usuario responda.

        La implementación delega la funcionalidad a la clase base Dialog, que se
        encarga de construir la interfaz, mostrar la ventana y manejar la interacción
        del usuario.

        Parámetros:
            position (Tuple[int, int], opcional):
                Coordenadas (x, y) en píxeles donde se debe posicionar la esquina
                superior izquierda del diálogo. Si es None, el diálogo se centra
                respecto a la ventana padre o la pantalla.
                Valor predeterminado: None

        Retorna:
            str: El texto del botón presionado por el usuario, que identifica la
                 acción seleccionada. Este valor es establecido por el método
                 `on_button_press` cuando el usuario interactúa con un botón.

        Ejemplos:
            # Mostrar un diálogo centrado
            dialog = MessageDialog("¿Desea guardar los cambios?")
            result = dialog.show()
            if result == "OK":
                # Realizar acción de guardado

            # Mostrar un diálogo en una posición específica
            dialog = MessageDialog("Operación completada")
            dialog.show(position=(200, 150))
        """
        # Delega la creación y visualización del diálogo a la clase base Dialog
        # La clase base se encarga de:
        # 1. Construir la interfaz (crear cuerpo y botones)
        # 2. Mostrar la ventana en la posición especificada o centrada
        # 3. Manejar la interacción del usuario
        # 4. Devolver el resultado cuando se cierra el diálogo
        return super().show(position)
