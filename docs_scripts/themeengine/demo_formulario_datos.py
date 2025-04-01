import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine.dialogs.base import Dialog


class FormDialog(Dialog):
    """
    Diálogo con un formulario de entrada de datos complejo.

    Esta clase extiende Dialog para crear un formulario con múltiples campos
    que permite al usuario ingresar datos estructurados. Está diseñada para
    evitar conflictos con ciertos widgets avanzados reemplazándolos con
    alternativas más simples.

    Características:
    - Campos de texto para nombre y email
    - Control personalizado para edad
    - Selector de género con menú desplegable personalizado
    - Opciones de preferencias con checkboxes
    - Selección de método de notificación con botones de opción
    - Área de texto para comentarios
    - Validación básica de campos obligatorios
    - Soporte para scroll en formularios largos

    Ejemplo de uso:
        # Datos iniciales
        initial_data = {
            "name": "Usuario Demo",
            "email": "usuario@ejemplo.com",
            "age": 25
        }

        # Crear y mostrar el diálogo
        dialog = FormDialog(parent=app, title="Formulario de Datos", data=initial_data)
        dialog.show()

        # Obtener el resultado cuando se cierra el diálogo
        if dialog.result:
            print(f"Datos del formulario: {dialog.result}")
    """

    def __init__(self, parent=None, title="Formulario", data=None, alert=False):
        """
        Inicializa un diálogo de formulario.

        Args:
            parent (Widget, optional): Widget padre del diálogo.
            title (str, optional): Título del diálogo.
            data (dict, optional): Datos iniciales para rellenar el formulario.
            alert (bool, optional): Si se debe emitir un sonido al mostrar.
        """
        self._data = data or {}

        # Variables para los campos del formulario
        self._vars = {
            "name": ttk.StringVar(value=self._data.get("name", "")),
            "email": ttk.StringVar(value=self._data.get("email", "")),
            "age": ttk.IntVar(value=self._data.get("age", 18)),
            "gender": ttk.StringVar(value=self._data.get("gender", "")),
            "subscription": ttk.BooleanVar(value=self._data.get("subscription", False)),
            "notifications": ttk.StringVar(value=self._data.get("notifications", "email")),
            "comments": ttk.StringVar(value=self._data.get("comments", ""))
        }

        super().__init__(parent, title, alert)

    def create_body(self, master):
        """
        Crea el cuerpo del diálogo con el formulario.

        Este método implementa la interfaz gráfica del formulario, creando
        todos los widgets necesarios y sus disposiciones.

        Args:
            master (Widget): Widget padre donde se crearán los elementos.
        """
        # Estructura principal: contenedor con scroll
        self._create_scrollable_container(master)

        # Frame interior para el contenido
        body_frame = ttk.Frame(self._canvas, padding=15)
        self._canvas_window = self._canvas.create_window((0, 0), window=body_frame, anchor=NW)

        # Título del formulario
        self._create_title(body_frame)

        # Sección de datos personales
        personal_frame = self._create_personal_section(body_frame)

        # Sección de preferencias
        prefs_frame = self._create_preferences_section(body_frame)

        # Sección de comentarios
        comments_frame = self._create_comments_section(body_frame)

        # Configurar el canvas para ajustarse al contenido
        self._configure_scrollable_region(body_frame)

    def _create_scrollable_container(self, master):
        """
        Crea un contenedor con capacidad de desplazamiento.

        Args:
            master (Widget): El widget padre.
        """
        # Frame contenedor
        container = ttk.Frame(master)
        container.pack(fill=BOTH, expand=YES)

        # Canvas y scrollbar
        self._canvas = ttk.Canvas(container)
        self._scrollbar = ttk.Scrollbar(container, orient=VERTICAL, command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side=RIGHT, fill=Y)
        self._canvas.pack(side=LEFT, fill=BOTH, expand=YES)

    def _create_title(self, parent):
        """
        Crea el título del formulario.

        Args:
            parent (Widget): El widget padre.
        """
        title_label = ttk.Label(
            parent,
            text="Complete los siguientes datos",
            font="-size 14 -weight bold"
        )
        title_label.pack(pady=(0, 15), anchor=W)

    def _create_personal_section(self, parent):
        """
        Crea la sección de datos personales del formulario.

        Args:
            parent (Widget): El widget padre.

        Returns:
            Widget: El frame de la sección creada.
        """
        # Contenedor de la sección
        personal_frame = ttk.Labelframe(parent, text="Datos Personales", padding=10)
        personal_frame.pack(fill=X, pady=(0, 10))

        # Campo de nombre
        name_frame = ttk.Frame(personal_frame)
        name_frame.pack(fill=X, pady=5)

        name_label = ttk.Label(name_frame, text="Nombre completo:", width=15, anchor=W)
        name_label.pack(side=LEFT, padx=(0, 5))

        name_entry = ttk.Entry(name_frame, textvariable=self._vars["name"], width=30)
        name_entry.pack(side=LEFT, fill=X, expand=YES)

        # Campo de email
        email_frame = ttk.Frame(personal_frame)
        email_frame.pack(fill=X, pady=5)

        email_label = ttk.Label(email_frame, text="Correo electrónico:", width=15, anchor=W)
        email_label.pack(side=LEFT, padx=(0, 5))

        email_entry = ttk.Entry(email_frame, textvariable=self._vars["email"], width=30)
        email_entry.pack(side=LEFT, fill=X, expand=YES)

        # Control personalizado para la edad
        self._create_age_control(personal_frame)

        # Control personalizado para género
        self._create_gender_control(personal_frame)

        # Establecer el foco inicial en el campo de nombre
        self._initial_focus = name_entry

        return personal_frame

    def _create_age_control(self, parent):
        """
        Crea un control personalizado para la edad.

        Args:
            parent (Widget): El widget padre.
        """
        age_frame = ttk.Frame(parent)
        age_frame.pack(fill=X, pady=5)

        age_label = ttk.Label(age_frame, text="Edad:", width=15, anchor=W)
        age_label.pack(side=LEFT, padx=(0, 5))

        # Control personalizado para la edad
        age_control_frame = ttk.Frame(age_frame)
        age_control_frame.pack(side=LEFT)

        # Botón menos
        minus_btn = ttk.Button(
            age_control_frame,
            text="-",
            width=2,
            command=lambda: self._change_age(-1)
        )
        minus_btn.pack(side=LEFT)

        # Campo de entrada
        age_entry = ttk.Entry(
            age_control_frame,
            textvariable=self._vars["age"],
            width=3,
            justify=CENTER
        )
        age_entry.pack(side=LEFT, padx=2)

        # Botón más
        plus_btn = ttk.Button(
            age_control_frame,
            text="+",
            width=2,
            command=lambda: self._change_age(1)
        )
        plus_btn.pack(side=LEFT)

    def _change_age(self, increment):
        """
        Cambia el valor de la edad incrementándolo o decrementándolo.

        Args:
            increment (int): El valor a incrementar (positivo o negativo).
        """
        current = self._vars["age"].get()
        new_value = current + increment
        if 18 <= new_value <= 100:
            self._vars["age"].set(new_value)

    def _create_gender_control(self, parent):
        """
        Crea un control personalizado para seleccionar el género.

        Args:
            parent (Widget): El widget padre.
        """
        gender_frame = ttk.Frame(parent)
        gender_frame.pack(fill=X, pady=5)

        gender_label = ttk.Label(gender_frame, text="Género:", width=15, anchor=W)
        gender_label.pack(side=LEFT, padx=(0, 5))

        # Campo de entrada
        gender_entry = ttk.Entry(
            gender_frame,
            textvariable=self._vars["gender"],
            width=15
        )
        gender_entry.pack(side=LEFT)

        # Menú desplegable manual
        gender_menu = ttk.Menubutton(
            gender_frame,
            text="Seleccionar",
            bootstyle=SECONDARY
        )
        gender_menu.pack(side=LEFT, padx=5)

        # Crear menú
        gender_dropdown = ttk.Menu(gender_menu)
        gender_menu["menu"] = gender_dropdown

        # Añadir opciones al menú
        gender_values = ["Masculino", "Femenino", "No binario", "Prefiero no decir"]
        for value in gender_values:
            gender_dropdown.add_command(
                label=value,
                command=lambda v=value: self._vars["gender"].set(v)
            )

        # Guardar referencia para uso posterior
        self.gender_entry = gender_entry

    def _create_preferences_section(self, parent):
        """
        Crea la sección de preferencias del formulario.

        Args:
            parent (Widget): El widget padre.

        Returns:
            Widget: El frame de la sección creada.
        """
        # Contenedor de la sección
        prefs_frame = ttk.Labelframe(parent, text="Preferencias", padding=10)
        prefs_frame.pack(fill=X, pady=(0, 10))

        # Casilla de suscripción
        subscription_check = ttk.Checkbutton(
            prefs_frame,
            text="Suscribirse al boletín de noticias",
            variable=self._vars["subscription"],
            bootstyle=SUCCESS
        )
        subscription_check.pack(anchor=W, pady=5)

        # Control para seleccionar método de notificación
        self._create_notification_control(prefs_frame)

        return prefs_frame

    def _create_notification_control(self, parent):
        """
        Crea un control para seleccionar el método de notificación.

        Args:
            parent (Widget): El widget padre.
        """
        notify_frame = ttk.Frame(parent)
        notify_frame.pack(fill=X, pady=5)

        notify_label = ttk.Label(notify_frame, text="Notificaciones vía:", width=15, anchor=W)
        notify_label.pack(side=LEFT, padx=(0, 5))

        # Frame para las opciones
        option_frame = ttk.Frame(notify_frame)
        option_frame.pack(side=LEFT, fill=X)

        # Opciones disponibles
        notify_options = ["email", "sms", "push", "ninguna"]
        notify_texts = ["Email", "SMS", "Push", "Ninguna"]

        # Crear botones para cada opción
        self._option_buttons = []
        for option, text in zip(notify_options, notify_texts):
            is_selected = self._vars["notifications"].get() == option
            style = INFO if is_selected else (INFO, "outline")

            btn = ttk.Button(
                option_frame,
                text=text,
                bootstyle=style,
                command=lambda opt=option: self._select_notification_option(opt),
                width=8
            )
            btn.pack(side=LEFT, padx=2)
            self._option_buttons.append((btn, option))

    def _select_notification_option(self, option):
        """
        Establece la opción de notificación seleccionada.

        Args:
            option (str): La opción seleccionada.
        """
        self._vars["notifications"].set(option)
        # Actualizar apariencia de botones
        for btn, opt in self._option_buttons:
            if opt == option:
                btn.configure(bootstyle=INFO)
            else:
                btn.configure(bootstyle=(INFO, "outline"))

    def _create_comments_section(self, parent):
        """
        Crea la sección de comentarios del formulario.

        Args:
            parent (Widget): El widget padre.

        Returns:
            Widget: El frame de la sección creada.
        """
        # Contenedor de la sección
        comments_frame = ttk.Labelframe(parent, text="Comentarios Adicionales", padding=10)
        comments_frame.pack(fill=X, pady=(0, 10))

        # Área de texto para comentarios
        self._comments_text = ttk.Text(comments_frame, height=5, width=40)
        self._comments_text.pack(fill=X, pady=5)
        self._comments_text.insert("1.0", self._vars["comments"].get())

        # Actualizar variable cuando cambie el texto
        self._comments_text.bind("<KeyRelease>", self._update_comments)

        return comments_frame

    def _update_comments(self, event=None):
        """
        Actualiza la variable de comentarios con el contenido del área de texto.

        Args:
            event: Evento que disparó esta acción (por defecto None).
        """
        self._vars["comments"].set(self._comments_text.get("1.0", "end-1c").strip())

    def _configure_scrollable_region(self, body_frame):
        """
        Configura la región desplazable del canvas.

        Args:
            body_frame (Widget): El frame de contenido.
        """

        def update_scrollregion(event):
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

            # Ajustar ancho del canvas al frame interior
            width = body_frame.winfo_reqwidth()
            self._canvas.itemconfigure(self._canvas_window, width=width)

        body_frame.bind("<Configure>", update_scrollregion)

    def create_buttonbox(self, master):
        """
        Crea la caja de botones del diálogo.

        Args:
            master (Widget): Widget padre donde se crearán los botones.
        """
        # Frame para los botones con padding
        button_frame = ttk.Frame(master)
        button_frame.pack(fill=X, padx=15, pady=(0, 15))

        # Botón de guardar
        save_button = ttk.Button(
            button_frame,
            text="Guardar",
            command=self._on_save,
            bootstyle=SUCCESS
        )
        save_button.pack(side=RIGHT, padx=(5, 0))

        # Botón de cancelar
        cancel_button = ttk.Button(
            button_frame,
            text="Cancelar",
            command=self._on_cancel,
            bootstyle=SECONDARY
        )
        cancel_button.pack(side=RIGHT)

        # Botón de ayuda
        help_button = ttk.Button(
            button_frame,
            text="Ayuda",
            command=self._on_help,
            bootstyle=(INFO, "outline")
        )
        help_button.pack(side=LEFT)

    def _on_save(self):
        """
        Manejador para el botón de guardar.

        Valida y recopila los datos ingresados en el formulario,
        y cierra el diálogo si la validación es exitosa.
        """
        # Validar campos obligatorios
        if not self._vars["name"].get():
            self._show_error("El nombre es obligatorio.")
            return

        if not self._vars["email"].get():
            self._show_error("El correo electrónico es obligatorio.")
            return

        # Recopilar datos del formulario
        self._result = {
            "name": self._vars["name"].get(),
            "email": self._vars["email"].get(),
            "age": self._vars["age"].get(),
            "gender": self._vars["gender"].get(),
            "subscription": self._vars["subscription"].get(),
            "notifications": self._vars["notifications"].get(),
            "comments": self._vars["comments"].get()
        }

        # Cerrar el diálogo
        if self._toplevel:
            self._toplevel.destroy()

    def _on_cancel(self):
        """
        Manejador para el botón de cancelar.

        Establece el resultado como None y cierra el diálogo.
        """
        self._result = None
        if self._toplevel:
            self._toplevel.destroy()

    def _on_help(self):
        """
        Manejador para el botón de ayuda.

        Muestra un diálogo de ayuda con información sobre el formulario.
        """
        from .message_dialog import MessageDialog  # Importación local para evitar circularidad

        help_dialog = MessageDialog(
            parent=self._toplevel,
            title="Ayuda",
            message="Complete todos los campos marcados como obligatorios. " +
                    "Si tiene alguna duda, contacte con soporte técnico.",
            icon=INFO,
            buttons=["Entendido"]
        )
        help_dialog.show()

    def _show_error(self, message):
        """
        Muestra un mensaje de error en un diálogo secundario.

        Args:
            message (str): Mensaje de error a mostrar.
        """
        from .message_dialog import MessageDialog  # Importación local para evitar circularidad

        error_dialog = MessageDialog(
            parent=self._toplevel,
            title="Error",
            message=message,
            icon=ERROR,
            buttons=["Aceptar"]
        )
        error_dialog.show()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear ventana raíz
    root = ttk.Window()
    root.title("Prueba de FormDialog")
    root.geometry("400x200")

    # Datos iniciales
    initial_data = {
        "name": "Usuario Demo",
        "email": "usuario@ejemplo.com",
        "age": 25,
        "gender": "Masculino",
        "subscription": True,
        "notifications": "email",
        "comments": "Este es un comentario de prueba."
    }


    # Función para mostrar el diálogo
    def show_dialog():
        dialog = FormDialog(root, "Formulario de Ejemplo", initial_data)
        dialog.show()

        # Mostrar resultado
        if dialog.result:
            print("Resultado:", dialog.result)
        else:
            print("Diálogo cancelado")


    # Botón para mostrar el diálogo
    btn = ttk.Button(root, text="Mostrar Formulario", command=show_dialog)
    btn.pack(padx=20, pady=20)

    # Iniciar bucle de eventos
    root.mainloop()