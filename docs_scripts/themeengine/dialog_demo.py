import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine.dialogs.base import Dialog
import random


class LoginDialog(Dialog):
    """
    Diálogo de inicio de sesión que solicita nombre de usuario y contraseña.

    Esta clase extiende la clase base Dialog e implementa los métodos abstractos
    create_body y create_buttonbox para crear un diálogo de inicio de sesión
    funcional.
    """

    def __init__(self, parent=None, title="Inicio de Sesión", alert=False):
        """
        Inicializa un diálogo de inicio de sesión.

        Parameters:
            parent (Widget, optional): Widget padre del diálogo.
            title (str, optional): Título del diálogo.
            alert (bool, optional): Si se debe emitir un sonido al mostrar.
        """
        super().__init__(parent, title, alert)

        # Variables para almacenar los valores ingresados
        self.username_var = ttk.StringVar()
        self.password_var = ttk.StringVar()
        self.remember_var = ttk.BooleanVar(value=False)

    def create_body(self, master):
        """
        Crea el cuerpo del diálogo con campos para usuario y contraseña.

        Parameters:
            master (Widget): Widget padre donde se crearán los elementos.
        """
        # Crear un frame principal con padding
        body_frame = ttk.Frame(master, padding=15)
        body_frame.pack(fill=BOTH, expand=YES)

        # Logo o imagen (simulada con un label)
        logo_label = ttk.Label(
            body_frame,
            text="🔒",
            font="-size 32",
            bootstyle=PRIMARY
        )
        logo_label.pack(pady=(0, 15))

        # Mensaje de bienvenida
        welcome_label = ttk.Label(
            body_frame,
            text="Bienvenido al sistema",
            font="-size 14 -weight bold"
        )
        welcome_label.pack(pady=(0, 15))

        # Frame para campos de entrada
        input_frame = ttk.Frame(body_frame)
        input_frame.pack(fill=X, pady=5)

        # Campo de usuario
        username_frame = ttk.Frame(input_frame)
        username_frame.pack(fill=X, pady=5)

        username_label = ttk.Label(username_frame, text="Usuario:", width=12, anchor=E)
        username_label.pack(side=LEFT, padx=(0, 5))

        username_entry = ttk.Entry(username_frame, textvariable=self.username_var, width=25)
        username_entry.pack(side=LEFT, fill=X, expand=YES)

        # Campo de contraseña
        password_frame = ttk.Frame(input_frame)
        password_frame.pack(fill=X, pady=5)

        password_label = ttk.Label(password_frame, text="Contraseña:", width=12, anchor=E)
        password_label.pack(side=LEFT, padx=(0, 5))

        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            width=25,
            show="•"  # Ocultar la contraseña
        )
        password_entry.pack(side=LEFT, fill=X, expand=YES)

        # Opción para recordar credenciales
        remember_check = ttk.Checkbutton(
            input_frame,
            text="Recordar mis datos",
            variable=self.remember_var,
            bootstyle=INFO
        )
        remember_check.pack(anchor=W, pady=10)

        # Establecer el foco inicial en el campo de usuario
        self._initial_focus = username_entry

    def create_buttonbox(self, master):
        """
        Crea la caja de botones del diálogo.

        Parameters:
            master (Widget): Widget padre donde se crearán los botones.
        """
        # Frame para los botones con padding
        button_frame = ttk.Frame(master)
        button_frame.pack(fill=X, padx=15, pady=(0, 15))

        # Botón de cancelar
        cancel_button = ttk.Button(
            button_frame,
            text="Cancelar",
            command=self._on_cancel,
            bootstyle=SECONDARY
        )
        cancel_button.pack(side=RIGHT, padx=(5, 0))

        # Botón de iniciar sesión
        login_button = ttk.Button(
            button_frame,
            text="Iniciar Sesión",
            command=self._on_login,
            bootstyle=PRIMARY
        )
        login_button.pack(side=RIGHT)

        # Enlace para recuperar contraseña
        recover_link = ttk.Button(
            button_frame,
            text="¿Olvidaste tu contraseña?",
            command=self._on_recover_password,
            bootstyle=(SECONDARY, "link")
        )
        recover_link.pack(side=LEFT)

    def _on_login(self):
        """
        Manejador para el botón de inicio de sesión.
        """
        # Verificar que se hayan ingresado credenciales
        if not self.username_var.get():
            self._show_error("Por favor ingrese su nombre de usuario.")
            return

        if not self.password_var.get():
            self._show_error("Por favor ingrese su contraseña.")
            return

        # En una aplicación real, aquí verificaríamos las credenciales
        # Simular verificación exitosa
        self._result = {
            "username": self.username_var.get(),
            "password": self.password_var.get(),
            "remember": self.remember_var.get()
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

    def _on_recover_password(self):
        """
        Manejador para el enlace de recuperación de contraseña.
        """
        self._result = "recover_password"
        if self._toplevel:
            self._toplevel.destroy()

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
            icon=ERROR,
            buttons=["Aceptar"]
        )
        error_dialog.show()


class MessageDialog(Dialog):
    """
    Diálogo para mostrar mensajes simples con iconos y botones personalizables.
    """

    def __init__(self, parent=None, title="Mensaje", message="",
                 icon=INFO, buttons=["Aceptar", "Cancelar"], alert=False):
        """
        Inicializa un diálogo de mensaje.

        Parameters:
            parent (Widget, optional): Widget padre del diálogo.
            title (str, optional): Título del diálogo.
            message (str): Mensaje a mostrar en el diálogo.
            icon (str, optional): Tipo de icono (INFO, WARNING, ERROR, SUCCESS).
            buttons (list, optional): Lista de textos para los botones.
            alert (bool, optional): Si se debe emitir un sonido al mostrar.
        """
        self._message = message
        self._icon = icon
        self._buttons = buttons
        super().__init__(parent, title, alert)

    def create_body(self, master):
        """
        Crea el cuerpo del diálogo con el mensaje e icono.

        Parameters:
            master (Widget): Widget padre donde se crearán los elementos.
        """
        # Frame principal con padding
        body_frame = ttk.Frame(master, padding=15)
        body_frame.pack(fill=BOTH, expand=YES)

        # Frame para el icono y mensaje
        content_frame = ttk.Frame(body_frame)
        content_frame.pack(fill=BOTH, expand=YES)

        # Icono según tipo
        icon_text = {
            INFO: "ℹ️",
            WARNING: "⚠️",
            ERROR: "❌",
            SUCCESS: "✅",
        }.get(self._icon, "ℹ️")

        icon_label = ttk.Label(
            content_frame,
            text=icon_text,
            font="-size 32",
            bootstyle=self._icon
        )
        icon_label.pack(side=LEFT, padx=(0, 15))

        # Mensaje
        message_label = ttk.Label(
            content_frame,
            text=self._message,
            justify=LEFT,
            wraplength=300
        )
        message_label.pack(side=LEFT, fill=BOTH, expand=YES)

    def create_buttonbox(self, master):
        """
        Crea la caja de botones del diálogo.

        Parameters:
            master (Widget): Widget padre donde se crearán los botones.
        """
        # Frame para los botones con padding
        button_frame = ttk.Frame(master)
        button_frame.pack(fill=X, padx=15, pady=(0, 15))

        # Crear botones según la lista proporcionada
        for i, button_text in enumerate(self._buttons):
            # El primer botón tiene estilo principal, los demás secundario
            style = PRIMARY if i == 0 else SECONDARY

            # Crear el botón
            button = ttk.Button(
                button_frame,
                text=button_text,
                command=lambda text=button_text: self._on_button(text),
                bootstyle=style
            )

            # Posicionar los botones de derecha a izquierda
            button.pack(side=RIGHT, padx=(5, 0) if i > 0 else 0)

            # El primer botón recibe el foco inicial
            if i == 0:
                self._initial_focus = button

    def _on_button(self, button_text):
        """
        Manejador para los botones.

        Parameters:
            button_text (str): Texto del botón que se presionó.
        """
        self._result = button_text
        if self._toplevel:
            self._toplevel.destroy()


class FormDialog(Dialog):
    """
    Diálogo con un formulario de entrada de datos complejo.

    Nota: Esta implementación utiliza alternativas para algunos widgets
    que podrían causar conflictos (Combobox, Spinbox, Meter, Radiobutton)
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

        # Campo edad (utilizando Entry con botones + y - para evitar conflictos con Spinbox)
        age_frame = ttk.Frame(personal_frame)
        age_frame.pack(fill=X, pady=5)

        age_label = ttk.Label(age_frame, text="Edad:", width=15, anchor=W)
        age_label.pack(side=LEFT, padx=(0, 5))

        # Control personalizado para la edad
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

        # Campo género
        gender_frame = ttk.Frame(personal_frame)
        gender_frame.pack(fill=X, pady=5)

        gender_label = ttk.Label(gender_frame, text="Género:", width=15, anchor=W)
        gender_label.pack(side=LEFT, padx=(0, 5))

        # Uso modificado del Entry en lugar de Combobox
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
        gender_menu["menu"] = gender_dropdown

        # Añadir opciones al menú
        gender_values = ["Masculino", "Femenino", "No binario", "Prefiero no decir"]
        for value in gender_values:
            gender_dropdown.add_command(
                label=value,
                command=lambda v=value: self._vars["gender"].set(v)
            )

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

        # Notificaciones (simplificado para evitar posibles conflictos)
        notify_frame = ttk.Frame(prefs_frame)
        notify_frame.pack(fill=X, pady=5)

        notify_label = ttk.Label(notify_frame, text="Notificaciones vía:", width=15, anchor=W)
        notify_label.pack(side=LEFT, padx=(0, 5))

        # Utilizar botones en vez de radiobuttons para evitar posibles conflictos
        option_frame = ttk.Frame(notify_frame)
        option_frame.pack(side=LEFT, fill=X)

        # Crear función para seleccionar opción
        def select_option(option):
            self._vars["notifications"].set(option)
            # Actualizar apariencia de botones
            for btn, opt in option_buttons:
                if opt == option:
                    btn.configure(bootstyle=INFO)
                else:
                    btn.configure(bootstyle=(INFO, "outline"))

        # Opciones disponibles
        notify_options = ["email", "sms", "push", "ninguna"]
        notify_texts = ["Email", "SMS", "Push", "Ninguna"]

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

        # Verificar que no haya referencias a componentes eliminados
        # Esto es necesario porque reemplazamos gender_combobox con gender_entry y gender_menu
        self.gender_entry = gender_entry

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
            icon=ERROR,
            buttons=["Aceptar"]
        )
        error_dialog.show()


def main():
    """
    Función principal que muestra una demostración de los diferentes tipos de diálogos.

    Esta función crea una ventana principal con botones para mostrar
    tres tipos de diálogos: login, mensaje y formulario.

    Nota: Se han implementado alternativas para algunos widgets que pueden
    causar conflictos en el entorno específico de themeengine.
    """
    # Crear ventana principal
    app = ttk.Window()
    app.title("Demostración de Diálogos")
    app.geometry("500x400")

    # Frame principal con padding
    main_frame = ttk.Frame(app, padding=20)
    main_frame.pack(fill=BOTH, expand=YES)

    # Título
    title_label = ttk.Label(
        main_frame,
        text="Demostración de Diálogos",
        font="-size 16 -weight bold"
    )
    title_label.pack(pady=(0, 20))

    # Descripción
    desc_label = ttk.Label(
        main_frame,
        text="Seleccione un tipo de diálogo para ver la demostración:",
        wraplength=450
    )
    desc_label.pack(pady=(0, 20))

    # Frame para los botones
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(fill=X, pady=10)

    # Función para mostrar diálogo de login
    def show_login_dialog():
        dialog = LoginDialog(parent=app, alert=True)
        dialog.show()

        # Mostrar resultado
        if dialog.result:
            if dialog.result == "recover_password":
                result_text = "Se solicitó recuperación de contraseña"
            else:
                result_text = f"Inicio de sesión: {dialog.result['username']}"
            result_var.set(result_text)
        else:
            result_var.set("Inicio de sesión cancelado")

    # Función para mostrar diálogo de mensaje
    def show_message_dialog():
        dialog = MessageDialog(
            parent=app,
            title="Información",
            message="Esta es una demostración de un diálogo de mensaje.\n\n" +
                    "Los diálogos de mensaje son útiles para mostrar información, " +
                    "advertencias, errores o confirmaciones al usuario.",
            icon=INFO,
            buttons=["Aceptar", "Más Info"]
        )
        dialog.show()

        # Mostrar resultado
        result_var.set(f"Respuesta: {dialog.result}")

    # Función para mostrar diálogo de formulario
    def show_form_dialog():
        # Datos iniciales
        initial_data = {
            "name": "Usuario Demo",
            "email": "usuario@ejemplo.com",
            "age": 25
        }

        dialog = FormDialog(parent=app, title="Formulario de Datos", data=initial_data)
        dialog.show()

        # Mostrar resultado
        if dialog.result:
            result_text = f"Formulario guardado: {dialog.result['name']}"
            result_var.set(result_text)
        else:
            result_var.set("Formulario cancelado")

    # Botón para diálogo de login
    login_button = ttk.Button(
        buttons_frame,
        text="Diálogo de Login",
        command=show_login_dialog,
        bootstyle=PRIMARY,
        width=20
    )
    login_button.pack(pady=5)

    # Botón para diálogo de mensaje
    message_button = ttk.Button(
        buttons_frame,
        text="Diálogo de Mensaje",
        command=show_message_dialog,
        bootstyle=INFO,
        width=20
    )
    message_button.pack(pady=5)

    # Botón para diálogo de formulario
    form_button = ttk.Button(
        buttons_frame,
        text="Diálogo de Formulario",
        command=show_form_dialog,
        bootstyle=SUCCESS,
        width=20
    )
    form_button.pack(pady=5)

    # Variable para mostrar el resultado
    result_var = ttk.StringVar()

    # Frame para mostrar el resultado
    result_frame = ttk.Labelframe(main_frame, text="Resultado", padding=10)
    result_frame.pack(fill=X, pady=(20, 0))

    result_label = ttk.Label(
        result_frame,
        textvariable=result_var,
        wraplength=450
    )
    result_label.pack(pady=5)

    # Iniciar la aplicación
    app.mainloop()


if __name__ == "__main__":
    main()