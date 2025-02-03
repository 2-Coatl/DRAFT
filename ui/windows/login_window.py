import tkinter as tk
from tkinter import ttk
from services.auth_service import AuthService
from ui.windows.dashboard_window import DashboardWindow
from ui.components.styled_button import StyledButton
from ui.components.custom_dialog import CustomDialog
from ui.styles.colors import ColorScheme
from ui.config.settings import AppSettings


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()
        self.title("Login")
        self.geometry("300x150")
        self.configure(bg=ColorScheme.BACKGROUND)

        # Frame principal
        frame = ttk.Frame(
            self,
            padding=AppSettings.PADDING['large'],
            style="Custom.TFrame"
        )
        frame.pack(expand=True)

        # Campos
        ttk.Label(
            frame,
            text="Nombre:",
            font=AppSettings.get_font('default'),
            style="Custom.TLabel"
        ).pack()

        self.nombre_entry = ttk.Entry(
            frame,
            style="Custom.TEntry",
            font=AppSettings.get_font('default')
        )
        self.nombre_entry.pack(pady=AppSettings.PADDING['small'])

        # Botón de ingreso
        StyledButton(
            frame,
            text="Ingresar",
            command=self.login,
            button_type='primary'
        ).pack(pady=AppSettings.PADDING['medium'])

        # Centrar la ventana
        self.center_window()

        # Dar foco al campo de nombre
        self.nombre_entry.focus()

    def login(self):
        nombre = self.nombre_entry.get()

        if not nombre:
            self.show_error("Por favor ingrese un nombre")
            return

        usuario = self.auth_service.login(nombre)
        if usuario:
            self.withdraw()  # Oculta la ventana de login
            dashboard = DashboardWindow(usuario)
            dashboard.protocol(
                "WM_DELETE_WINDOW",
                lambda: (self.deiconify(), dashboard.destroy())
            )
        else:
            self.show_error("Usuario no encontrado")

    def show_error(self, message):
        CustomDialog(
            self,
            "Error",
            message,
            ["Aceptar"],
            dialog_type='error'
        )

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')