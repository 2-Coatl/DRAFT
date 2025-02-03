import tkinter as tk
from tkinter import ttk
from models.user import User
from ui.components.styled_button import StyledButton
from ui.components.scrolled_frame import ScrolledFrame
from ui.styles.colors import ColorScheme
from ui.config.settings import AppSettings


class DashboardWindow(tk.Toplevel):
    def __init__(self, usuario: User):
        super().__init__()

        self.usuario = usuario
        self.title(f"Dashboard - {usuario.nombre}")
        self.geometry("400x300")
        self.configure(bg=ColorScheme.BACKGROUND)

        # Frame principal con scroll
        self.main_frame = ScrolledFrame(self)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Usamos el frame scrolleable interno
        self.frame = self.main_frame.scrollable_frame

        # Información del usuario
        self.crear_seccion_usuario()

        # Botones de acción según rol
        self.crear_botones_rol()

        # Centrar la ventana
        self.center_window()

    def crear_seccion_usuario(self):
        frame_usuario = ttk.Frame(
            self.frame,
            style="Custom.TFrame"
        )
        frame_usuario.pack(fill='x', pady=AppSettings.PADDING['medium'])

        # Título de bienvenida
        ttk.Label(
            frame_usuario,
            text="Bienvenido/a",
            style="Custom.TLabel",
            font=AppSettings.get_font('title')
        ).pack(anchor='w')

        # Información del usuario
        ttk.Label(
            frame_usuario,
            text=f"Usuario: {self.usuario.nombre}",
            style="Custom.TLabel",
            font=AppSettings.get_font('default')
        ).pack(anchor='w', pady=(5, 0))

        ttk.Label(
            frame_usuario,
            text=f"Rol: {self.get_rol_nombre()}",
            style="Custom.TLabel",
            font=AppSettings.get_font('default')
        ).pack(anchor='w', pady=(2, 0))

    def crear_botones_rol(self):
        frame_botones = ttk.Frame(
            self.frame,
            style="Custom.TFrame"
        )
        frame_botones.pack(pady=AppSettings.PADDING['large'])

        if self.usuario.rol == 1:  # Admin
            StyledButton(
                frame_botones,
                text="Gestionar Usuarios",
                command=self.gestionar_usuarios,
                button_type='primary'
            ).pack(pady=AppSettings.PADDING['small'])

        StyledButton(
            frame_botones,
            text="Cerrar Sesión",
            command=self.destroy,
            button_type='secondary'
        ).pack(pady=AppSettings.PADDING['small'])

    def gestionar_usuarios(self):
        from ui.windows.users_window import UsersWindow
        UsersWindow()

    def get_rol_nombre(self):
        roles = {
            1: "Administrador",
            2: "Usuario"
        }
        return roles.get(self.usuario.rol, "Usuario")

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')