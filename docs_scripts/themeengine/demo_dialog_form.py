import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine import Dialog
from ui.themeengine.dialogs.alert.message_dialog import MessageDialog


class FormDialog(Dialog):
    """
    Diálogo con un formulario de entrada de datos complejo.

    Esta implementación intenta usar los widgets estándar (Spinbox, Combobox,
    Radiobutton) y solo recurre a alternativas si es necesario.
    """

    def __init__(self, parent=None, title="Formulario", data=None, alert=False):
        """
        Inicializa un diálogo de formulario.

        Parameters:
            parent (Widget, optional): Widget padre del diálogo.
            title (str, optional): Título del diálogo.
            data (dict, optional): Datos iniciales para el formulario.
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

        # Para detectar si podemos usar widgets estándar
        self._use_standard_widgets = True

        super().__init__(parent, title, alert)

    def create_body(self, master):
        """
        Crea el cuerpo del diálogo con el formulario.

        Parameters:
            master (Widget): Widget padre donde se crearán los elementos.
        """
        # Frame principal con padding y scrollbar
        container = ttk.Frame(master)
        container.pack(fill=BOTH, expand=YES)

        # Canvas para permitir scroll
        canvas = ttk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        # Frame interior para el contenido
        body_frame = ttk.Frame(canvas, padding=15)
        canvas_window = canvas.create_window((0, 0), window=body_frame, anchor=NW)

        # Título del formulario
        title_label = ttk.Label(
            body_frame,
            text="Complete los siguientes datos",
            font="-size 14 -weight bold"
        )
        title_label.pack(pady=(0, 15), anchor=W)

        # Sección datos personales
        personal_frame = ttk.Labelframe(body_frame, text="Datos Personales", padding=10)
        personal_frame.pack(fill=X, pady=(0, 10))

        # Campo nombre
        name_frame = ttk.Frame(personal_frame)
        name_frame.pack(fill=X, pady=5)

        name_label = ttk.Label(name_frame, text="Nombre completo:", width=15, anchor=W)
        name_label.pack(side=LEFT, padx=(0, 5))

        name_entry = ttk.Entry(name_frame, textvariable=self._vars["name"], width=30)
        name_entry.pack(side=LEFT, fill=X, expand=YES)

        # Campo email
        email_frame = ttk.Frame(personal_frame)
        email_frame.pack(fill=X, pady=5)

        email_label = ttk.Label(email_frame, text="Correo electrónico:", width=15, anchor=W)
        email_label.pack(side=LEFT, padx=(0, 5))

        email_entry = ttk.Entry(email_frame, textvariable=self._vars["email"], width=30)
        email_entry.pack(side=LEFT, fill=X, expand=YES)

        # Campo edad - Intentar usar Spinbox primero
        age_frame = ttk.Frame(personal_frame)
        age_frame.pack(fill=X, pady=5)

        age_label = ttk.Label(age_frame, text="Edad:", width=15, anchor=W)
        age_label.pack(side=LEFT, padx=(0, 5))

        try:
            # Intento usar Spinbox
            age_spinbox = ttk.Spinbox(
                age_frame,
                from_=18,
                to=100,
                textvariable=self._vars["age"],
                width=5
            )
            age_spinbox.pack(side=LEFT)

        except Exception as e:
            print(f"Error al crear Spinbox: {e}. Usando alternativa.")
            self._use_standard_widgets = False

            # Control personalizado para la edad como alternativa
            age_control_frame = ttk.Frame(age_frame)
            age_control_frame.pack(side=LEFT)

            # Función para incrementar/decrementar edad
            def change_age(increment):
                current = self._vars["age"].get()
                new_value = current + increment
                if 18 <= new_value <= 100:
                    self._vars["age"].set(new_value)

            # Botón menos
            minus_btn = ttk.Button(
                age_control_frame,
                text="-",
                width=2,
                command=lambda: change_age(-1)
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
                command=lambda: change_age(1)
            )
            plus_btn.pack(side=LEFT)

        # Campo género - Intentar usar Combobox primero
        gender_frame = ttk.Frame(personal_frame)
        gender_frame.pack(fill=X, pady=5)

        gender_label = ttk.Label(gender_frame, text="Género:", width=15, anchor=W)
        gender_label.pack(side=LEFT, padx=(0, 5))

        gender_values = ["Masculino", "Femenino", "No binario", "Prefiero no decir"]

        try:
            # Intento usar Combobox
            gender_combobox = ttk.Combobox(
                gender_frame,
                textvariable=self._vars["gender"],
                values=gender_values,
                width=15
            )
            gender_combobox.pack(side=LEFT)

        except Exception as e:
            print(f"Error al crear Combobox: {e}. Usando alternativa.")
            self._use_standard_widgets = False

            # Uso modificado del Entry como alternativa
            gender_entry = ttk.Entry(
                gender_frame,
                textvariable=self._vars["gender"],
                width=15
            )
            gender_entry.pack(side=LEFT)

            # Menú desplegable manual como alternativa
            gender_menu = ttk.Menubutton(
                gender_frame,
                text="Seleccionar",
                bootstyle=SECONDARY
            )
            gender_menu.pack(side=LEFT, padx=5)

            # Crear menú
            gender_dropdown = ttk.Menu(gender_menu)

            # Usar configure en lugar de asignación directa
            gender_menu.configure(menu=gender_dropdown)

            # Añadir opciones al menú
            for value in gender_values:
                gender_dropdown.add_command(
                    label=value,
                    command=lambda v=value: self._vars["gender"].set(v)
                )

            # Para mantener referencia
            self.gender_entry = gender_entry

        # Sección preferencias
        prefs_frame = ttk.Labelframe(body_frame, text="Preferencias", padding=10)
        prefs_frame.pack(fill=X, pady=(0, 10))

        # Suscripción
        subscription_check = ttk.Checkbutton(
            prefs_frame,
            text="Suscribirse al boletín de noticias",
            variable=self._vars["subscription"],
            bootstyle=SUCCESS
        )
        subscription_check.pack(anchor=W, pady=5)

        # Notificaciones - Intentar usar Radiobuttons primero
        notify_frame = ttk.Frame(prefs_frame)
        notify_frame.pack(fill=X, pady=5)

        notify_label = ttk.Label(notify_frame, text="Notificaciones vía:", width=15, anchor=W)
        notify_label.pack(side=LEFT, padx=(0, 5))

        notify_options = ["email", "sms", "push", "ninguna"]
        notify_texts = ["Email", "SMS", "Push", "Ninguna"]

        option_frame = ttk.Frame(notify_frame)
        option_frame.pack(side=LEFT, fill=X)

        try:
            # Intento usar Radiobuttons
            for option, text in zip(notify_options, notify_texts):
                radio = ttk.Radiobutton(
                    option_frame,
                    text=text,
                    value=option,
                    variable=self._vars["notifications"]
                )
                radio.pack(side=LEFT, padx=5)

        except Exception as e:
            print(f"Error al crear Radiobuttons: {e}. Usando alternativa.")
            self._use_standard_widgets = False

            # Utilizar botones en vez de radiobuttons como alternativa
            # Crear función para seleccionar opción
            def select_option(option):
                self._vars["notifications"].set(option)
                # Actualizar apariencia de botones
                for btn, opt in option_buttons:
                    if opt == option:
                        btn.configure(bootstyle=INFO)
                    else:
                        btn.configure(bootstyle=(INFO, "outline"))

            # Crear botones para cada opción
            option_buttons = []
            for option, text in zip(notify_options, notify_texts):
                is_selected = self._vars["notifications"].get() == option
                style = INFO if is_selected else (INFO, "outline")

                btn = ttk.Button(
                    option_frame,
                    text=text,
                    bootstyle=style,
                    command=lambda opt=option: select_option(opt),
                    width=8
                )
                btn.pack(side=LEFT, padx=2)
                option_buttons.append((btn, option))

        # Sección comentarios
        comments_frame = ttk.Labelframe(body_frame, text="Comentarios Adicionales", padding=10)
        comments_frame.pack(fill=X, pady=(0, 10))

        comments_text = ttk.Text(comments_frame, height=5, width=40)
        comments_text.pack(fill=X, pady=5)
        comments_text.insert("1.0", self._vars["comments"].get())

        # Función para actualizar la variable cuando cambie el texto
        def update_comments(*args):
            self._vars["comments"].set(comments_text.get("1.0", "end-1c").strip())

        comments_text.bind("<KeyRelease>", update_comments)

        # Ajustar canvas al contenido
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

            # Ajustar ancho del canvas al frame interior
            width = body_frame.winfo_reqwidth()
            canvas.itemconfigure(canvas_window, width=width)

        body_frame.bind("<Configure>", update_scrollregion)

        # Establecer el foco inicial en el campo de nombre
        self._initial_focus = name_entry

    def create_buttonbox(self, master):
        """
        Crea la caja de botones del diálogo.

        Parameters:
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
        """
        self._result = None
        if self._toplevel:
            self._toplevel.destroy()

    def _on_help(self):
        """
        Manejador para el botón de ayuda.
        """
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

        Parameters:
            message (str): Mensaje de error a mostrar.
        """
        error_dialog = MessageDialog(
            parent=self._toplevel,
            title="Error",
            message=message,
            icon=DANGER,
            buttons=["Aceptar"]
        )
        error_dialog.show()


def main():
    """
    Función principal que muestra una demostración del diálogo de formulario.
    """
    # Crear ventana principal
    app = ttk.Window()
    app.title("Demostración de Formulario")
    app.geometry("500x300")

    # Frame principal con padding
    main_frame = ttk.Frame(app, padding=20)
    main_frame.pack(fill=BOTH, expand=YES)

    # Título
    title_label = ttk.Label(
        main_frame,
        text="Demostración de Formulario",
        font="-size 16 -weight bold"
    )
    title_label.pack(pady=(0, 20))

    # Descripción
    desc_label = ttk.Label(
        main_frame,
        text="Este ejemplo intenta usar widgets estándar (Spinbox, Combobox, " +
             "Radiobutton) y solo recurre a alternativas si encuentra errores.",
        wraplength=450
    )
    desc_label.pack(pady=(0, 20))

    # Frame para el botón
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=X, pady=10)

    # Función para mostrar diálogo de formulario
    def show_form_dialog():
        # Datos iniciales
        initial_data = {
            "name": "Usuario Demo",
            "email": "usuario@ejemplo.com",
            "age": 25,
            "gender": "Masculino",
            "subscription": True,
            "notifications": "email",
            "comments": "Este es un comentario de ejemplo para mostrar cómo se completan los campos automáticamente."
        }

        dialog = FormDialog(parent=app, title="Formulario de Datos", data=initial_data)
        dialog.show()

        # Mostrar resultado
        if dialog.result:
            result_text = f"Formulario guardado para: {dialog.result['name']}"
            if dialog.result["subscription"]:
                result_text += f"\nUsuario suscrito, notificaciones vía: {dialog.result['notifications']}"
            result_var.set(result_text)

            # Mostrar si se usaron widgets estándar
            if hasattr(dialog, '_use_standard_widgets'):
                widget_text = "Se utilizaron widgets estándar." if dialog._use_standard_widgets else "Se utilizaron alternativas a widgets."
                widget_var.set(widget_text)
        else:
            result_var.set("Formulario cancelado")

    # Botón para diálogo de formulario
    form_button = ttk.Button(
        button_frame,
        text="Abrir Formulario",
        command=show_form_dialog,
        bootstyle=SUCCESS,
        width=20
    )
    form_button.pack(pady=5)

    # Variables para mostrar el resultado
    result_var = ttk.StringVar()
    widget_var = ttk.StringVar()

    # Frame para mostrar el resultado
    result_frame = ttk.Labelframe(main_frame, text="Resultado", padding=10)
    result_frame.pack(fill=X, pady=(20, 0))

    result_label = ttk.Label(
        result_frame,
        textvariable=result_var,
        wraplength=450
    )
    result_label.pack(pady=5)

    widget_label = ttk.Label(
        result_frame,
        textvariable=widget_var,
        wraplength=450,
        foreground="blue"
    )
    widget_label.pack(pady=5)

    # Iniciar la aplicación
    app.mainloop()


if __name__ == "__main__":
    main()