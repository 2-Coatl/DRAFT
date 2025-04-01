import threading
import time
import random
import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine.dialogs.alert.message_dialog import MessageDialog


class DataProcessingApplication:
    """
    Aplicación de demostración que simula un procesamiento de datos
    y muestra notificaciones mediante MessageDialog
    """

    def __init__(self, root):
        """Inicializa la aplicación"""
        self.root = root
        self.root.title("Procesador de Datos - Demostración")
        self.root.geometry("800x600")

        # Variables de control
        self.is_processing = False
        self.processed_items = 0
        self.total_items = 0
        self.process_cancelled = False

        # Variables para widgets
        self.progress_var = ttk.DoubleVar(value=0.0)
        self.status_var = ttk.StringVar(value="Listo para iniciar")
        self.items_var = ttk.StringVar(value="")

        # Crear la interfaz
        self._create_widgets()

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Título de la aplicación
        title = ttk.Label(
            main_frame,
            text="Simulador de Procesamiento de Datos",
            font="-size 16 -weight bold"
        )
        title.pack(pady=(0, 20))

        # Panel de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding=10)
        config_frame.pack(fill=X, expand=NO, pady=(0, 20))

        # Número de elementos a procesar
        items_frame = ttk.Frame(config_frame)
        items_frame.pack(fill=X, pady=5)

        ttk.Label(items_frame, text="Elementos a procesar:").pack(side=LEFT, padx=(0, 10))

        self.items_entry = ttk.Entry(items_frame, width=10)
        self.items_entry.insert(0, "100")
        self.items_entry.pack(side=LEFT)

        # Panel de estado
        status_frame = ttk.LabelFrame(main_frame, text="Estado del Proceso", padding=10)
        status_frame.pack(fill=X, expand=NO, pady=(0, 20))

        # Barra de progreso
        ttk.Label(status_frame, text="Progreso:").pack(anchor=W, pady=(0, 5))

        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            mode="determinate",
            bootstyle="success"
        )
        self.progress_bar.pack(fill=X, pady=(0, 10))

        # Texto de estado
        ttk.Label(status_frame, textvariable=self.status_var, font="-size 12").pack(anchor=W)
        ttk.Label(status_frame, textvariable=self.items_var).pack(anchor=W, pady=(5, 0))

        # Panel de acciones
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=X, expand=NO, pady=(0, 20))

        # Botones de acción
        self.start_button = ttk.Button(
            actions_frame,
            text="Iniciar Procesamiento",
            command=self.start_processing,
            bootstyle="success",
            width=25
        )
        self.start_button.pack(side=LEFT, padx=(0, 10))

        self.cancel_button = ttk.Button(
            actions_frame,
            text="Cancelar",
            command=self.cancel_processing,
            bootstyle="danger",
            width=15,
            state=DISABLED
        )
        self.cancel_button.pack(side=LEFT)

        # Área de registro (log)
        log_frame = ttk.LabelFrame(main_frame, text="Registro de Actividad", padding=10)
        log_frame.pack(fill=BOTH, expand=YES)

        # Texto de registro con scroll
        self.log_text = ttk.Text(log_frame, height=10, width=70, wrap=WORD)
        self.log_text.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.log_text.config(yscrollcommand=scrollbar.set)
        self.log_text.configure(state=DISABLED)

        # Agregar mensajes iniciales al log
        self.add_log("Aplicación iniciada")
        self.add_log("Sistema listo para procesar datos")

    def add_log(self, message):
        """Agrega un mensaje al registro de actividad"""
        self.log_text.configure(state=NORMAL)
        self.log_text.insert(END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(END)
        self.log_text.configure(state=DISABLED)

    def start_processing(self):
        """Inicia el procesamiento de datos en un hilo separado"""
        # Validar la entrada
        try:
            self.total_items = int(self.items_entry.get())
            if self.total_items <= 0:
                raise ValueError("El número debe ser positivo")
        except ValueError as e:
            self.show_error_dialog(f"Número inválido de elementos: {str(e)}")
            return

        # Reiniciar variables
        self.processed_items = 0
        self.process_cancelled = False
        self.progress_var.set(0.0)

        # Actualizar UI
        self.status_var.set("Procesando datos...")
        self.items_var.set(f"0 de {self.total_items} elementos procesados")
        self.start_button.configure(state=DISABLED)
        self.cancel_button.configure(state=NORMAL)

        # Registrar inicio
        self.add_log(f"Iniciando procesamiento de {self.total_items} elementos")

        # Iniciar hilo de procesamiento
        self.is_processing = True
        threading.Thread(target=self._processing_thread, daemon=True).start()

    def _processing_thread(self):
        """Hilo de procesamiento simulado"""
        start_time = time.time()

        for i in range(self.total_items):
            if self.process_cancelled:
                break

            # Simular procesamiento
            process_time = random.uniform(0.01, 0.1)
            time.sleep(process_time)

            # Actualizar progreso
            self.processed_items += 1
            progress = (self.processed_items / self.total_items) * 100

            # Actualizar UI desde el hilo principal
            self.root.after(0, self._update_progress, progress, process_time)

            # Simular error aleatorio (5% de probabilidad)
            if random.random() < 0.05 and not self.process_cancelled:
                self.root.after(0, self._handle_error, i + 1)
                return

        # Proceso completado o cancelado
        elapsed_time = time.time() - start_time

        if not self.process_cancelled:
            self.root.after(0, self._process_completed, elapsed_time)
        else:
            self.root.after(0, self._process_cancelled, elapsed_time)

    def _update_progress(self, progress, process_time):
        """Actualiza la interfaz con el progreso actual"""
        self.progress_var.set(progress)
        self.items_var.set(f"{self.processed_items} de {self.total_items} elementos procesados")

        # Ocasionalmente agregar detalles al log (no para cada elemento)
        if self.processed_items % 10 == 0 or self.processed_items == self.total_items:
            self.add_log(f"Procesado elemento {self.processed_items} ({process_time:.3f}s)")

    def _handle_error(self, item_number):
        """Maneja un error simulado durante el procesamiento"""
        self.is_processing = False
        self.add_log(f"ERROR: Problema al procesar el elemento {item_number}")
        self.status_var.set("Error en el procesamiento")

        self.start_button.configure(state=NORMAL)
        self.cancel_button.configure(state=DISABLED)

        # Mostrar diálogo de error
        self.show_error_dialog(
            f"Se ha producido un error al procesar el elemento {item_number}.\n"
            f"Se han procesado {self.processed_items} de {self.total_items} elementos."
        )

    def _process_completed(self, elapsed_time):
        """Maneja la finalización exitosa del procesamiento"""
        self.is_processing = False
        self.add_log(f"Procesamiento completado en {elapsed_time:.2f} segundos")
        self.status_var.set("Procesamiento completado")

        self.start_button.configure(state=NORMAL)
        self.cancel_button.configure(state=DISABLED)

        # Mostrar diálogo de éxito
        dialog = MessageDialog(
            message=f"Se han procesado {self.processed_items} elementos correctamente en {elapsed_time:.2f} segundos.",
            title="Operación completada",
            buttons=["Aceptar:success"],
            alert=True
        )
        result = dialog.show()

        self.add_log(f"Diálogo cerrado. Resultado: {result}")

    def _process_cancelled(self, elapsed_time):
        """Maneja la cancelación del procesamiento"""
        self.is_processing = False
        self.add_log(f"Procesamiento cancelado después de {elapsed_time:.2f} segundos")
        self.status_var.set("Procesamiento cancelado")

        self.start_button.configure(state=NORMAL)
        self.cancel_button.configure(state=DISABLED)

        # Mostrar diálogo informativo
        dialog = MessageDialog(
            message=f"Procesamiento cancelado.\nSe procesaron {self.processed_items} de {self.total_items} elementos.",
            title="Operación cancelada",
            buttons=["Aceptar:primary"],
            alert=True
        )
        result = dialog.show()

        self.add_log(f"Diálogo cerrado. Resultado: {result}")

    def cancel_processing(self):
        """Cancela el procesamiento en curso"""
        if self.is_processing:
            self.process_cancelled = True
            self.add_log("Cancelando el procesamiento...")
            self.status_var.set("Cancelando...")

    def show_error_dialog(self, message):
        """Muestra un diálogo de error"""
        dialog = MessageDialog(
            message=message,
            title="Error",
            buttons=["Cerrar:danger"],
            alert=True
        )
        dialog.show()

        self.add_log("Se mostró un diálogo de error")


def main():
    """Función principal"""
    # Crear la ventana raíz
    root = ttk.Window()

    # Inicializar la aplicación
    app = DataProcessingApplication(root)

    # Iniciar el bucle principal
    root.mainloop()


if __name__ == "__main__":
    main()