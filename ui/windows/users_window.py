import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService


class UsersWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Usuarios")
        self.geometry("500x400")
        self.auth_service = AuthService()

        # Frame principal
        self.frame = tk.Frame(self, padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        # Lista de usuarios
        self.crear_lista_usuarios()

        # Formulario de nuevo usuario
        self.crear_formulario()

    def crear_lista_usuarios(self):
        # Frame para la lista
        list_frame = ttk.LabelFrame(self.frame, text="Usuarios", padding=10)
        list_frame.pack(fill='both', expand=True)

        # Crear Treeview
        columns = ('ID', 'Nombre', 'Rol')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill='both', expand=True)
        self.cargar_usuarios()

    def crear_formulario(self):
        # Frame para el formulario
        form_frame = ttk.LabelFrame(self.frame, text="Nuevo Usuario", padding=10)
        form_frame.pack(fill='x', pady=10)

        # Frame para campos
        campos_frame = tk.Frame(form_frame)
        campos_frame.pack(pady=10)

        # Campos
        tk.Label(campos_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = tk.Entry(campos_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Rol (1=Admin, 2=Usuario):").grid(row=1, column=0, padx=5, pady=5)
        self.rol_entry = tk.Entry(campos_frame)
        self.rol_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botón registrar (ahora más visible)
        tk.Button(
            form_frame,
            text="Guardar Usuario",
            bg="#4CAF50",  # Verde
            fg="white",
            width=20,
            command=self.registrar_usuario
        ).pack(pady=10)

    def cargar_usuarios(self):
        # Limpiar lista actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Recargar usuarios desde storage
        for user in self.auth_service.get_all_users():  # Necesitaremos añadir este método
            self.tree.insert('', 'end', values=(user.id, user.nombre, user.rol))

    def registrar_usuario(self):
        try:
            nombre = self.nombre_entry.get()
            rol = int(self.rol_entry.get())

            if rol not in [1, 2]:
                messagebox.showerror("Error", "Rol debe ser 1 (Admin) o 2 (Usuario)")
                return

            usuario = self.auth_service.registrar(nombre, rol)
            messagebox.showinfo("Éxito", f"Usuario {usuario.nombre} registrado")

            # Limpiar formulario y recargar lista
            self.nombre_entry.delete(0, 'end')
            self.rol_entry.delete(0, 'end')
            self.cargar_usuarios()

        except ValueError:
            messagebox.showerror("Error", "Rol debe ser un número")