import tkinter as tk
from models.user import User


class DashboardWindow(tk.Toplevel):
    def __init__(self, usuario: User):
        super().__init__()

        self.usuario = usuario
        self.title(f"Dashboard - {usuario.nombre}")
        self.geometry("400x300")

        # Frame principal
        self.frame = tk.Frame(self, padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        # Información del usuario
        self.crear_seccion_usuario()

        # Botones de acción según rol
        self.crear_botones_rol()

    def crear_seccion_usuario(self):
        frame_usuario = tk.Frame(self.frame)
        frame_usuario.pack(fill='x', pady=10)

        tk.Label(
            frame_usuario,
            text=f"Usuario: {self.usuario.nombre}\nRol: {self.usuario.rol}",
            justify='left'
        ).pack(anchor='w')

    def crear_botones_rol(self):
        frame_botones = tk.Frame(self.frame)
        frame_botones.pack(pady=20)

        if self.usuario.rol == 1:  # Admin
            tk.Button(
                frame_botones,
                text="Gestionar Usuarios",
                command=self.gestionar_usuarios
            ).pack(pady=5)

        tk.Button(
            frame_botones,
            text="Cerrar Sesión",
            command=self.destroy
        ).pack(pady=5)

    def gestionar_usuarios(self):
        # Por implementar
        pass