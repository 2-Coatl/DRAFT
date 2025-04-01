import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine.dialogs.alert.message_dialog import MessageDialog


def patch_button_getitem():
    """
    Aplica un monkeypatch temporal para solucionar el problema de button["text"]

    Esta función modifica temporalmente la clase Button para permitir
    el acceso a la propiedad 'text' usando la notación de corchetes,
    solucionando así el error que ocurre en MessageDialog.on_button_press()
    """
    # Obtener la clase Button original
    Button = ttk.Button

    # Función de reemplazo para __getitem__
    def patched_getitem(self, key):
        if key == "text":
            # Para la clave 'text', usar cget que es más seguro
            return self.cget("text")
        # De lo contrario, delegar al comportamiento original
        return self._orig_getitem(self, key)

    # Solo aplicar el parche si no se ha aplicado previamente
    if not hasattr(Button, "_orig_getitem"):
        # Guardar la implementación original
        Button._orig_getitem = Button.__getitem__

        # Reemplazar con nuestra versión parcheada
        Button.__getitem__ = patched_getitem

        print("Patch aplicado a Button.__getitem__")


class MessageDialogDemo:
    """
    Demostración completa de la clase MessageDialog

    Esta aplicación muestra todas las características y opciones
    disponibles en la clase MessageDialog.
    """

    def __init__(self, root):
        """Inicializa la aplicación de demostración"""
        # Aplicar el parche antes de usar MessageDialog
        patch_button_getitem()

        self.root = root
        self.root.title("Demostración de MessageDialog")
        self.root.geometry("800x600")

        # Iconos para la demostración (rutas ajustables según el proyecto)
        self.icon_paths = {}

        # Variable para seguimiento de resultados
        self.result_var = ttk.StringVar(value="Ninguna acción realizada aún")

        # Construir la interfaz
        self._create_widgets()

    def _create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Encabezado
        header = ttk.Label(
            main_frame,
            text="Demostración de MessageDialog",
            font="-size 16 -weight bold"
        )
        header.pack(pady=(0, 20))

        # Panel de ejemplos
        examples_frame = ttk.LabelFrame(main_frame, text="Ejemplos de MessageDialog", padding=10)
        examples_frame.pack(fill=BOTH, expand=YES)

        # Crear el panel de ejemplos
        self._create_examples_panel(examples_frame)

        # Panel de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultado", padding=10)
        results_frame.pack(fill=X, expand=NO, pady=(20, 0))

        # Mostrar el resultado
        result_label = ttk.Label(
            results_frame,
            textvariable=self.result_var,
            font="-size 12"
        )
        result_label.pack(fill=X)

    def _create_examples_panel(self, parent):
        """Crea el panel con ejemplos de diálogo"""
        # Usar grid para organizar los botones
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        # Diálogo básico
        ttk.Button(
            parent,
            text="Diálogo básico",
            command=self._show_basic_dialog,
            width=30
        ).grid(row=0, column=0, padx=10, pady=10, sticky=EW)

        # Diálogo de advertencia
        ttk.Button(
            parent,
            text="Diálogo de advertencia",
            command=self._show_warning_dialog,
            bootstyle="warning",
            width=30
        ).grid(row=0, column=1, padx=10, pady=10, sticky=EW)

        # Diálogo de error
        ttk.Button(
            parent,
            text="Diálogo de error",
            command=self._show_error_dialog,
            bootstyle="danger",
            width=30
        ).grid(row=1, column=0, padx=10, pady=10, sticky=EW)

        # Diálogo de confirmación
        ttk.Button(
            parent,
            text="Diálogo de confirmación",
            command=self._show_confirm_dialog,
            bootstyle="info",
            width=30
        ).grid(row=1, column=1, padx=10, pady=10, sticky=EW)

        # Diálogo con texto largo
        ttk.Button(
            parent,
            text="Diálogo con texto largo",
            command=self._show_long_text_dialog,
            bootstyle="secondary",
            width=30
        ).grid(row=2, column=0, padx=10, pady=10, sticky=EW)

        # Diálogo con callback
        ttk.Button(
            parent,
            text="Diálogo con callback",
            command=self._show_callback_dialog,
            bootstyle="success",
            width=30
        ).grid(row=2, column=1, padx=10, pady=10, sticky=EW)

        # Diálogo personalizado
        ttk.Button(
            parent,
            text="Diálogo personalizado",
            command=self._show_custom_dialog,
            bootstyle="primary",
            width=30
        ).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=EW)

    def _show_basic_dialog(self):
        """Muestra un diálogo básico"""
        dialog = MessageDialog(
            message="Este es un diálogo básico con botones predeterminados.",
            title="Diálogo Básico",
            parent=self.root
        )
        result = dialog.show()
        self.result_var.set(f"Botón seleccionado: {result}")

    def _show_warning_dialog(self):
        """Muestra un diálogo de advertencia"""
        dialog = MessageDialog(
            message="Esta acción no se puede deshacer. ¿Desea continuar?",
            title="Advertencia",
            buttons=["Cancelar:secondary", "Continuar:warning"],
            default="Cancelar",
            parent=self.root,
            alert=True
        )
        result = dialog.show()
        self.result_var.set(f"Botón seleccionado: {result}")

    def _show_error_dialog(self):
        """Muestra un diálogo de error"""
        dialog = MessageDialog(
            message="Ha ocurrido un error al procesar la solicitud.",
            title="Error",
            buttons=["Cerrar:danger"],
            parent=self.root,
            alert=True
        )
        result = dialog.show()
        self.result_var.set(f"Botón seleccionado: {result}")

    def _show_confirm_dialog(self):
        """Muestra un diálogo de confirmación"""
        dialog = MessageDialog(
            message="¿Desea guardar los cambios realizados?",
            title="Confirmar acción",
            buttons=["No:danger", "Cancelar:secondary", "Sí:success"],
            default="Sí",
            parent=self.root
        )
        result = dialog.show()
        self.result_var.set(f"Botón seleccionado: {result}")

    def _show_long_text_dialog(self):
        """Muestra un diálogo con texto largo"""
        message = """Este es un ejemplo de un mensaje largo que demuestra el ajuste automático de texto.

El sistema ajustará el texto según el ancho especificado, respetando los saltos de línea explícitos.

La clase MessageDialog utiliza textwrap para formatear adecuadamente el contenido y asegurar una buena presentación."""

        dialog = MessageDialog(
            message=message,
            title="Texto largo",
            width=40,  # Ancho máximo en caracteres
            parent=self.root
        )
        result = dialog.show()
        self.result_var.set(f"Botón seleccionado: {result}")

    def _show_callback_dialog(self):
        """Muestra un diálogo con callback"""

        def on_dialog_close():
            print("¡El diálogo se ha cerrado y el callback se ha ejecutado!")
            # Actualizar inmediatamente el resultado
            self.result_var.set(f"Botón seleccionado y callback ejecutado")

        dialog = MessageDialog(
            message="Este diálogo ejecutará una función cuando se cierre.",
            title="Demo Callback",
            command=on_dialog_close,
            parent=self.root
        )
        result = dialog.show()
        # El texto ya ha sido actualizado por el callback

    def _show_custom_dialog(self):
        """Muestra un diálogo personalizado con múltiples opciones"""
        dialog = MessageDialog(
            message="Seleccione una de las siguientes opciones:",
            title="Opciones personalizadas",
            buttons=[
                "Cancelar:secondary",
                "Opción 1:info",
                "Opción 2:success",
                "Opción 3:primary"
            ],
            default="Opción 2",
            parent=self.root,
            width=45
        )
        result = dialog.show()
        self.result_var.set(f"Botón seleccionado: {result}")


def main():
    """Función principal"""
    # Crear la ventana raíz
    root = ttk.Window()

    # Inicializar la aplicación
    app = MessageDialogDemo(root)

    # Iniciar el bucle principal
    root.mainloop()


if __name__ == "__main__":
    main()