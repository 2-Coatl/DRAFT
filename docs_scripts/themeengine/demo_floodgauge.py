import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
import time


def main():
    # Crear la ventana principal
    app = ttk.Window(title="Demostración de Floodgauge", size=(600, 500))

    # Frame para controles
    control_frame = ttk.Frame(app)
    control_frame.pack(fill=X, padx=10, pady=10)

    # =====================================================================
    # 1. Gauge determinado con máscara de porcentaje
    # =====================================================================
    gauge_frame1 = ttk.Labelframe(app, text="Modo Determinado con Máscara")
    gauge_frame1.pack(fill=X, expand=YES, padx=10, pady=(0, 10))

    gauge1 = ttk.Floodgauge(
        master=gauge_frame1,
        bootstyle=INFO,
        font=(None, 15, 'bold'),
        mask='Memoria Usada {}%',
        value=25,
        mode='determinate'
    )
    gauge1.pack(fill=X, expand=YES, padx=10, pady=10)

    # Controles para gauge1
    gauge1_controls = ttk.Frame(gauge_frame1)
    gauge1_controls.pack(fill=X, padx=10, pady=5)

    ttk.Button(
        gauge1_controls,
        text="Incrementar",
        command=lambda: gauge1.step(10),
        bootstyle=PRIMARY
    ).pack(side=LEFT, padx=5)

    ttk.Button(
        gauge1_controls,
        text="Establecer a 75%",
        command=lambda: gauge1.configure(value=75),
        bootstyle=SUCCESS
    ).pack(side=LEFT, padx=5)

    ttk.Button(
        gauge1_controls,
        text="Reiniciar",
        command=lambda: gauge1.configure(value=0),
        bootstyle=DANGER
    ).pack(side=LEFT, padx=5)

    # =====================================================================
    # 2. Gauge indeterminado con animación
    # =====================================================================
    gauge_frame2 = ttk.Labelframe(app, text="Modo Indeterminado con Animación")
    gauge_frame2.pack(fill=X, expand=YES, padx=10, pady=(0, 10))

    gauge2 = ttk.Floodgauge(
        master=gauge_frame2,
        bootstyle=WARNING,
        text="Procesando datos...",
        mode='indeterminate',
        maximum=100
    )
    gauge2.pack(fill=X, expand=YES, padx=10, pady=10)

    # Controles para gauge2
    gauge2_controls = ttk.Frame(gauge_frame2)
    gauge2_controls.pack(fill=X, padx=10, pady=5)

    ttk.Button(
        gauge2_controls,
        text="Iniciar Animación",
        command=gauge2.start,
        bootstyle=PRIMARY
    ).pack(side=LEFT, padx=5)

    ttk.Button(
        gauge2_controls,
        text="Detener Animación",
        command=gauge2.stop,
        bootstyle=DANGER
    ).pack(side=LEFT, padx=5)

    ttk.Button(
        gauge2_controls,
        text="Cambiar Texto",
        command=lambda: gauge2.configure(text="Analizando archivos..."),
        bootstyle=INFO
    ).pack(side=LEFT, padx=5)

    # =====================================================================
    # 3. Gauge vertical
    # =====================================================================
    gauge_frame3 = ttk.Labelframe(app, text="Gauge Vertical")
    gauge_frame3.pack(side=LEFT, fill=Y, expand=YES, padx=(10, 5), pady=(0, 10))

    gauge3 = ttk.Floodgauge(
        master=gauge_frame3,
        bootstyle=SUCCESS,
        length=200,
        orient='vertical',
        value=50,
        maximum=100
    )
    gauge3.pack(fill=Y, expand=YES, padx=10, pady=10)

    # Controles para gauge3
    gauge3_controls = ttk.Frame(gauge_frame3)
    gauge3_controls.pack(fill=X, padx=10, pady=5)

    ttk.Button(
        gauge3_controls,
        text="+",
        command=lambda: gauge3.step(5),
        bootstyle=SUCCESS
    ).pack(side=LEFT, padx=5)

    ttk.Button(
        gauge3_controls,
        text="-",
        command=lambda: gauge3.configure(value=max(0, gauge3.variable.get() - 5)),
        bootstyle=DANGER
    ).pack(side=LEFT, padx=5)

    # =====================================================================
    # 4. Temporizador (usando el ejemplo anterior)
    # =====================================================================
    gauge_frame4 = ttk.Labelframe(app, text="Temporizador")
    gauge_frame4.pack(side=LEFT, fill=BOTH, expand=YES, padx=(5, 10), pady=(0, 10))

    # Configuración del temporizador
    total_seconds = 30  # 30 segundos
    start_time = None

    timer_gauge = ttk.Floodgauge(
        master=gauge_frame4,
        mask="Tiempo: {} seg",
        bootstyle=DANGER,
        maximum=total_seconds,
        font=(None, 12, 'bold')
    )
    timer_gauge.pack(fill=X, expand=YES, padx=10, pady=10)

    timer_running = False

    # Función de actualización
    def update_timer():
        nonlocal timer_running

        if not timer_running or start_time is None:
            return

        elapsed = time.time() - start_time
        remaining = max(0, total_seconds - elapsed)

        # Actualizar la barra
        timer_gauge.configure(value=remaining)

        # Formatear el texto
        timer_gauge.textvariable.set(f"Tiempo: {int(remaining)} seg")

        if remaining > 0:
            # Continuar actualizando
            app.after(100, update_timer)
        else:
            # Tiempo completado
            timer_gauge.configure(bootstyle=SUCCESS)
            timer_gauge.textvariable.set("¡Completado!")
            timer_running = False

    # Controles para el temporizador
    timer_controls = ttk.Frame(gauge_frame4)
    timer_controls.pack(fill=X, padx=10, pady=5)

    def start_timer():
        nonlocal start_time, timer_running
        if not timer_running:
            start_time = time.time()
            timer_running = True
            timer_gauge.configure(bootstyle=DANGER)
            update_timer()

    def stop_timer():
        nonlocal timer_running
        timer_running = False

    def reset_timer():
        nonlocal start_time, timer_running
        timer_running = False
        timer_gauge.configure(value=total_seconds, bootstyle=DANGER)
        timer_gauge.textvariable.set(f"Tiempo: {total_seconds} seg")

    ttk.Button(
        timer_controls,
        text="Iniciar",
        command=start_timer,
        bootstyle=SUCCESS
    ).pack(side=LEFT, padx=5)

    ttk.Button(
        timer_controls,
        text="Detener",
        command=stop_timer,
        bootstyle=WARNING
    ).pack(side=LEFT, padx=5)

    ttk.Button(
        timer_controls,
        text="Reiniciar",
        command=reset_timer,
        bootstyle=DANGER
    ).pack(side=LEFT, padx=5)

    # Inicializar el temporizador
    reset_timer()

    # Iniciar el bucle principal
    app.mainloop()


if __name__ == "__main__":
    main()