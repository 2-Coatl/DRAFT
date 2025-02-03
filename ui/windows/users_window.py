import tkinter as tk
from tkinter import ttk
from services.auth_service import AuthService
from ui.components.styled_button import StyledButton
from ui.components.scrolled_frame import ScrolledFrame
from ui.components.custom_dialog import CustomDialog
from ui.components.column_header import ColumnHeader
from ui.styles.colors import ColorScheme
from ui.config.settings import AppSettings


class UsersWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Usuarios")
        self.geometry("500x400")
        self.configure(bg=ColorScheme.BACKGROUND)
        self.auth_service = AuthService()

        # Frame principal con scroll
        self.main_frame = ScrolledFrame(self)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Usamos el frame scrolleable interno
        self.frame = self.main_frame.scrollable_frame

        # Lista de usuarios
        self.crear_lista_usuarios()

        # Formulario de nuevo usuario
        self.crear_formulario()

        # Centrar la ventana
        self.center_window()

    def crear_lista_usuarios(self):
        # Frame para la lista
        list_frame = ttk.LabelFrame(
            self.frame,
            text="Usuarios",
            padding=AppSettings.PADDING['medium'],
            style="Custom.TLabelframe"
        )
        list_frame.pack(fill='both', expand=True)

        # Crear Treeview con estilo personalizado
        columns = ('ID', 'Nombre', 'Rol')
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            style="Custom.Treeview"
        )

        # Configurar columnas con headers personalizados
        column_widths = {'ID': 80, 'Nombre': 200, 'Rol': 120}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Layout
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.cargar_usuarios()

    def crear_formulario(self):
        # Frame para el formulario
        form_frame = ttk.LabelFrame(
            self.frame,
            text="Nuevo Usuario",
            padding=AppSettings.PADDING['medium'],
            style="Custom.TLabelframe"
        )
        form_frame.pack(fill='x', pady=AppSettings.PADDING['medium'])

        # Frame para campos
        campos_frame = ttk.Frame(form_frame, style="Custom.TFrame")
        campos_frame.pack(pady=AppSettings.PADDING['medium'])

        # Campos
        self.crear_campo_formulario(campos_frame, "Nombre:", 0)
        self.crear_campo_formulario(campos_frame, "Rol:", 1)

        # Combobox para rol en lugar de entrada de texto
        self.rol_var = tk.StringVar()
        self.rol_combo = ttk.Combobox(
            campos_frame,
            textvariable=self.rol_var,
            values=["Administrador", "Usuario"],
            state="readonly",
            width=20
        )
        self.rol_combo.grid(row=1, column=1, padx=5, pady=5)
        self.rol_combo.set("Usuario")  # Valor por defecto

        # Botón guardar
        StyledButton(
            form_frame,
            text="Guardar Usuario",
            command=self.registrar_usuario,
            button_type='primary'
        ).pack(pady=AppSettings.PADDING['medium'])

    def crear_campo_formulario(self, parent, label_text, row):
        ttk.Label(
            parent,
            text=label_text,
            style="Custom.TLabel",
            font=AppSettings.get_font('default')
        ).grid(row=row, column=0, padx=5, pady=5, sticky='e')

        if label_text == "Nombre:":
            self.nombre_entry = ttk.Entry(
                parent,
                style="Custom.TEntry",
                font=AppSettings.get_font('default'),
                width=25
            )
            self.nombre_entry.grid(row=row, column=1, padx=5, pady=5)

    def cargar_usuarios(self):
        # Limpiar lista actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Recargar usuarios
        for user in self.auth_service.get_all_users():
            rol_texto = "Administrador" if user.rol == 1 else "Usuario"
            self.tree.insert('', 'end', values=(user.id, user.nombre, rol_texto))

    def registrar_usuario(self):
        try:
            nombre = self.nombre_entry.get()
            rol = 1 if self.rol_combo.get() == "Administrador" else 2

            if not nombre:
                self.show_error("El nombre es requerido")
                return

            usuario = self.auth_service.registrar(nombre, rol)
            self.show_success(f"Usuario {usuario.nombre} registrado exitosamente")

            # Limpiar formulario y recargar lista
            self.nombre_entry.delete(0, 'end')
            self.rol_combo.set("Usuario")
            self.cargar_usuarios()

        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        CustomDialog(self, "Error", message, ["Aceptar"], dialog_type='error')

    def show_success(self, message):
        CustomDialog(self, "Éxito", message, ["Aceptar"], dialog_type='success')

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')