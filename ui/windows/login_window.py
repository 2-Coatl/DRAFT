import tkinter as tk
from tkinter import messagebox
from services.auth_service import AuthService
from ui.windows.dashboard_window import DashboardWindow


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()
        self.title("Login")
        self.geometry("300x150")

        # Frame principal
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True)

        # Campos
        tk.Label(frame, text="Nombre:").pack()
        self.nombre_entry = tk.Entry(frame)
        self.nombre_entry.pack(pady=5)

        # Botones
        tk.Button(frame, text="Ingresar", command=self.login).pack(pady=10)

    def login(self):
        nombre = self.nombre_entry.get()

        if not nombre:
            messagebox.showerror("Error", "Por favor ingrese un nombre")
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
            messagebox.showerror("Error", "Usuario no encontrado")