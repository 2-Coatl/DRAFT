import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine.dialogs.base import Dialog


class LoginDialog(Dialog):
    """
    Diálogo de inicio de sesión que solicita nombre de usuario y contraseña.

    Esta clase extiende la clase base Dialog e implementa los métodos abstractos
    create_body y create_buttonbox para crear un diálogo de inicio de sesión
    funcional.

    Ejemplo de uso:
        login_dialog = LoginDialog(parent=main_window)
        login_dialog.show()

        if login_dialog.result:
            if login_dialog.result == "recover_password":
                # Usuario solicitó recuperación de contraseña
                handle_password_recovery()
            else:
                # Usuario inició sesión correctamente
                username = login_dialog.result["username"]
                password = login_dialog.result["password"]
                remember = login_dialog.result["remember"]
                authenticate_user(username, password, remember)
    """

    def __init__(self, parent=None, title="Inicio de Sesión", alert=False):
        """
        Inicializa un diálogo de inicio de sesión.

        Args:
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

        Args:
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

        Args:
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

        Valida las credenciales ingresadas y establece el resultado
        del diálogo si son válidas.
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

        Establece el resultado como None y cierra el diálogo.
        """
        self._result = None
        if self._toplevel:
            self._toplevel.destroy()

    def _on_recover_password(self):
        """
        Manejador para el enlace de recuperación de contraseña.

        Establece el resultado como "recover_password" y cierra el diálogo.
        """
        self._result = "recover_password"
        if self._toplevel:
            self._toplevel.destroy()

    def _show_error(self, message):
        """
        Muestra un mensaje de error en un diálogo secundario.

        Args:
            message (str): Mensaje de error a mostrar.
        """
        # En una implementación real, este método utilizaría una clase MessageDialog
        # Sin embargo, para evitar dependencias, usamos una implementación simplificada
        error_toplevel = ttk.Toplevel(self._toplevel)
        error_toplevel.title("Error")
        error_toplevel.transient(self._toplevel)
        error_toplevel.resizable(False, False)

        # Frame principal con padding
        frame = ttk.Frame(error_toplevel, padding=15)
        frame.pack(fill=BOTH, expand=YES)

        # Icono de error y mensaje
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=BOTH, expand=YES, pady=(0, 15))

        icon_label = ttk.Label(
            content_frame,
            text="❌",
            font="-size 32",
            bootstyle=DANGER
        )
        icon_label.pack(side=LEFT, padx=(0, 15))

        message_label = ttk.Label(
            content_frame,
            text=message,
            justify=LEFT,
            wraplength=300
        )
        message_label.pack(side=LEFT, fill=BOTH, expand=YES)

        # Botón Aceptar
        ok_button = ttk.Button(
            frame,
            text="Aceptar",
            command=error_toplevel.destroy,
            bootstyle=PRIMARY
        )
        ok_button.pack(side=RIGHT)

        # Hacer el diálogo modal
        error_toplevel.grab_set()
        error_toplevel.focus_set()

        # Centrar en el diálogo padre
        error_toplevel.update_idletasks()
        parent_x = self._toplevel.winfo_rootx()
        parent_y = self._toplevel.winfo_rooty()
        parent_width = self._toplevel.winfo_width()
        parent_height = self._toplevel.winfo_height()

        dialog_width = error_toplevel.winfo_width()
        dialog_height = error_toplevel.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        error_toplevel.geometry(f"+{x}+{y}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear ventana raíz
    root = ttk.Window()
    root.title("Prueba de LoginDialog")
    root.geometry("400x200")


    # Función para mostrar el diálogo
    def show_dialog():
        dialog = LoginDialog(root)
        dialog.show()

        # Mostrar resultado
        if dialog.result is None:
            print("Inicio de sesión cancelado")
        elif dialog.result == "recover_password":
            print("Se solicitó recuperación de contraseña")
        else:
            print(f"Usuario: {dialog.result['username']}")
            print(f"Recordar: {dialog.result['remember']}")


    # Botón para mostrar el diálogo
    btn = ttk.Button(root, text="Iniciar Sesión", command=show_dialog)
    btn.pack(padx=20, pady=20)

    # Iniciar bucle de eventos
    root.mainloop()