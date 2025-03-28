import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
import random
import time
from threading import Thread


class MeterDemo:
    """Clase para demostrar todas las funcionalidades del widget Meter"""

    def __init__(self, root):
        self.root = root
        root.title("Demostración del Widget Meter")
        root.geometry("1200x800")

        # Crear notebook para organizar las demostraciones
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Crear todas las pestañas de demostración
        self.create_basic_tab()
        self.create_styles_tab()
        self.create_types_tab()
        self.create_interactive_tab()
        self.create_striped_tab()
        self.create_animation_tab()
        self.create_realworld_tab()

    def create_basic_tab(self):
        """Pestaña con ejemplos básicos del Meter"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Básico")

        ttk.Label(
            tab,
            text="Ejemplos Básicos del Widget Meter",
            font=("-size 16 -weight bold")
        ).pack(pady=(0, 20))

        # Frame para los medidores
        meters_frame = ttk.Frame(tab)
        meters_frame.pack(fill=X)

        # Medidor básico
        basic_frame = ttk.Labelframe(meters_frame, text="Medidor básico", padding=15)
        basic_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter1 = ttk.Meter(
            basic_frame,
            metersize=180,
            padding=20,
            amountused=45,
            amounttotal=100,
            bootstyle=PRIMARY,
            subtext="Medidor simple"
        )
        meter1.pack(pady=10)

        controls = ttk.Frame(basic_frame)
        controls.pack(fill=X, pady=10)

        ttk.Button(
            controls,
            text="Aumentar",
            command=lambda: meter1.configure(amountused=min(100, meter1["amountused"] + 10))
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

        ttk.Button(
            controls,
            text="Disminuir",
            command=lambda: meter1.configure(amountused=max(0, meter1["amountused"] - 10))
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

        # Medidor con texto
        text_frame = ttk.Labelframe(meters_frame, text="Opciones de texto", padding=15)
        text_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter2 = ttk.Meter(
            text_frame,
            metersize=180,
            padding=20,
            amountused=75,
            amounttotal=100,
            textleft="$",
            textright=".00",
            bootstyle=SUCCESS,
            subtext="Con prefijo y sufijo"
        )
        meter2.pack(pady=10)

        controls2 = ttk.Frame(text_frame)
        controls2.pack(fill=X, pady=10)

        show_text_var = ttk.BooleanVar(value=True)

        def toggle_text():
            meter2.configure(showtext=show_text_var.get())

        ttk.Checkbutton(
            controls2,
            text="Mostrar texto",
            variable=show_text_var,
            command=toggle_text
        ).pack(side=LEFT, padx=5)

        # Medidor con configuración personalizada
        custom_frame = ttk.Labelframe(meters_frame, text="Personalizado", padding=15)
        custom_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter3 = ttk.Meter(
            custom_frame,
            metersize=180,
            padding=20,
            amountused=60,
            amounttotal=100,
            meterthickness=15,
            bootstyle=DANGER,
            textfont="-size 24 -weight bold",
            subtext="Personalizado",
            subtextfont="-size 12"
        )
        meter3.pack(pady=10)

        # Descripción
        desc_frame = ttk.Frame(tab, padding=10)
        desc_frame.pack(fill=X, pady=20)

        ttk.Label(
            desc_frame,
            text="El widget Meter proporciona una representación visual de un valor como un arco "
                 "circular o semicircular. Es altamente personalizable y puede mostrar el progreso "
                 "de operaciones o la cantidad de trabajo completado.",
            wraplength=800
        ).pack()

    def create_styles_tab(self):
        """Pestaña que muestra todos los estilos disponibles"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Estilos")

        ttk.Label(
            tab,
            text="Estilos Bootstrap para el Widget Meter",
            font=("-size 16 -weight bold")
        ).pack(pady=(0, 20))

        # Obtener todos los estilos bootstrap disponibles
        styles = [PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER, LIGHT, DARK]
        style_names = ["primary", "secondary", "success", "info", "warning", "danger", "light", "dark"]

        # Crear dos filas de medidores
        row1 = ttk.Frame(tab)
        row1.pack(fill=X, pady=10)

        row2 = ttk.Frame(tab)
        row2.pack(fill=X, pady=10)

        # Añadir un medidor para cada estilo
        for i, (style, name) in enumerate(zip(styles, style_names)):
            frame = ttk.Frame(row1 if i < 4 else row2, padding=10)
            frame.pack(side=LEFT, fill=BOTH, expand=YES)

            meter = ttk.Meter(
                frame,
                metersize=150,
                amountused=random.randint(30, 90),
                amounttotal=100,
                bootstyle=style,
                subtext=name.capitalize()
            )
            meter.pack(padx=10)

        # Descripción
        desc_frame = ttk.Frame(tab, padding=10)
        desc_frame.pack(fill=X, pady=20)

        ttk.Label(
            desc_frame,
            text="Los widgets Meter son compatibles con todos los estilos bootstrap proporcionados por el tema. "
                 "Estos estilos definen los colores usados para el indicador, el texto central y permiten una "
                 "integración visual coherente con el resto de la aplicación.",
            wraplength=800
        ).pack()

    def create_types_tab(self):
        """Pestaña que muestra los diferentes tipos de medidores"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Tipos")

        ttk.Label(
            tab,
            text="Tipos de Medidores y Configuraciones de Arco",
            font=("-size 16 -weight bold")
        ).pack(pady=(0, 20))

        # Frame para los medidores de diferentes tipos
        meters_frame = ttk.Frame(tab)
        meters_frame.pack(fill=X)

        # Medidor circular completo
        full_frame = ttk.Labelframe(meters_frame, text="Circular completo (360°)", padding=15)
        full_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_full = ttk.Meter(
            full_frame,
            metersize=180,
            amountused=75,
            metertype=FULL,
            bootstyle=PRIMARY,
            subtext="metertype=FULL"
        )
        meter_full.pack(pady=10)

        # Medidor semicircular
        semi_frame = ttk.Labelframe(meters_frame, text="Semicircular (270°)", padding=15)
        semi_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_semi = ttk.Meter(
            semi_frame,
            metersize=180,
            amountused=50,
            metertype=SEMI,
            bootstyle=SUCCESS,
            subtext="metertype=SEMI"
        )
        meter_semi.pack(pady=10)

        # Medidor personalizado con arcrange
        custom_arc_frame = ttk.Labelframe(meters_frame, text="Personalizado (arcrange=180)", padding=15)
        custom_arc_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_custom = ttk.Meter(
            custom_arc_frame,
            metersize=180,
            amountused=60,
            arcoffset=0,
            arcrange=180,
            bootstyle=INFO,
            subtext="Arco de 180°"
        )
        meter_custom.pack(pady=10)

        # Segunda fila para wedges
        wedge_frame = ttk.Frame(tab)
        wedge_frame.pack(fill=X, pady=20)

        ttk.Label(
            wedge_frame,
            text="Medidores con Indicador de Cuña (wedgesize)",
            font=("-size 14 -weight bold")
        ).pack(pady=(0, 20))

        # Tres ejemplos con diferentes wedgesize
        wedges_row = ttk.Frame(wedge_frame)
        wedges_row.pack(fill=X)

        for i, size in enumerate([5, 10, 15]):
            frame = ttk.Labelframe(wedges_row, text=f"wedgesize={size}", padding=15)
            frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

            meter = ttk.Meter(
                frame,
                metersize=150,
                amountused=random.randint(30, 70),
                amounttotal=100,
                wedgesize=size,
                bootstyle=[PRIMARY, SECONDARY, WARNING][i],
                subtext=f"Cuña de {size}°"
            )
            meter.pack(pady=10)

        # Descripción
        desc_frame = ttk.Frame(tab, padding=10)
        desc_frame.pack(fill=X, pady=20)

        ttk.Label(
            desc_frame,
            text="El widget Meter puede configurarse con diferentes formas de arco mediante los parámetros 'metertype', "
                 "'arcrange' y 'arcoffset'. Además, el parámetro 'wedgesize' permite crear medidores estilo reloj con un "
                 "indicador de cuña en lugar de un arco de progreso.",
            wraplength=800
        ).pack()

    def create_interactive_tab(self):
        """Pestaña que muestra medidores interactivos"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Interactivo")

        ttk.Label(
            tab,
            text="Medidores Interactivos",
            font=("-size 16 -weight bold")
        ).pack(pady=(0, 20))

        # Frame para los medidores interactivos
        meters_frame = ttk.Frame(tab)
        meters_frame.pack(fill=X)

        # Medidor interactivo simple
        simple_frame = ttk.Labelframe(meters_frame, text="Interactivo Simple", padding=15)
        simple_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_interactive = ttk.Meter(
            simple_frame,
            metersize=180,
            amountused=30,
            interactive=True,
            bootstyle=PRIMARY,
            subtext="Haz clic y arrastra",
            stepsize=5
        )
        meter_interactive.pack(pady=10)

        # Mostrar el valor actual
        value_var = ttk.StringVar(value="Valor: 30")

        def update_value_label(*_):
            value_var.set(f"Valor: {meter_interactive['amountused']}")

        meter_interactive.amountusedvar.trace_add("write", update_value_label)

        ttk.Label(simple_frame, textvariable=value_var).pack(pady=5)

        # Medidor interactivo con dial
        dial_frame = ttk.Labelframe(meters_frame, text="Dial Interactivo", padding=15)
        dial_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_dial = ttk.Meter(
            dial_frame,
            metersize=180,
            amountused=45,
            interactive=True,
            wedgesize=8,
            meterthickness=15,
            bootstyle=SUCCESS,
            subtext="Con indicador de cuña",
            stepsize=1
        )
        meter_dial.pack(pady=10)

        # Medidor con etiqueta de temperatura
        temp_frame = ttk.Labelframe(meters_frame, text="Control de Temperatura", padding=15)
        temp_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        # Función para cambiar el color según el valor
        def update_temp_style(*_):
            temp = meter_temp["amountused"]
            if temp < 20:
                meter_temp.configure(bootstyle=INFO)
            elif temp < 75:
                meter_temp.configure(bootstyle=SUCCESS)
            else:
                meter_temp.configure(bootstyle=DANGER)

        meter_temp = ttk.Meter(
            temp_frame,
            metersize=180,
            amountused=22,
            amounttotal=100,
            interactive=True,
            textright="°C",
            bootstyle=SUCCESS,
            subtext="Temperatura",
            stepsize=1
        )
        meter_temp.pack(pady=10)

        # Añadir rastreador para actualizar el estilo
        meter_temp.amountusedvar.trace_add("write", update_temp_style)

        # Descripción
        desc_frame = ttk.Frame(tab, padding=10)
        desc_frame.pack(fill=X, pady=20)

        ttk.Label(
            desc_frame,
            text="Los medidores pueden configurarse para ser interactivos estableciendo 'interactive=True'. "
                 "Esto permite al usuario ajustar el valor del medidor haciendo clic y arrastrando. "
                 "El parámetro 'stepsize' controla el incremento mínimo del valor.",
            wraplength=800
        ).pack()

    def create_striped_tab(self):
        """Pestaña que muestra medidores con rayas"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Con Rayas")

        ttk.Label(
            tab,
            text="Medidores con Rayas",
            font=("-size 16 -weight bold")
        ).pack(pady=(0, 20))

        # Frame para los medidores con rayas
        meters_frame = ttk.Frame(tab)
        meters_frame.pack(fill=X)

        # Diferentes grosores de rayas
        stripe_sizes = [2, 5, 10]
        colors = [PRIMARY, WARNING, DANGER]

        for i, (size, color) in enumerate(zip(stripe_sizes, colors)):
            frame = ttk.Labelframe(meters_frame, text=f"stripethickness={size}", padding=15)
            frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

            meter = ttk.Meter(
                frame,
                metersize=180,
                amountused=65,
                stripethickness=size,
                bootstyle=color,
                subtext=f"Rayas de {size}°"
            )
            meter.pack(pady=10)

        # Segunda fila con combinaciones
        combo_frame = ttk.Frame(tab)
        combo_frame.pack(fill=X, pady=20)

        ttk.Label(
            combo_frame,
            text="Combinaciones con wedgesize",
            font=("-size 14 -weight bold")
        ).pack(pady=(0, 20))

        # Medidores con rayas y cuña
        combo_row = ttk.Frame(combo_frame)
        combo_row.pack(fill=X)

        # Medidor semicircular con rayas
        semi_striped_frame = ttk.Labelframe(combo_row, text="Semicircular con rayas", padding=15)
        semi_striped_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_semi_striped = ttk.Meter(
            semi_striped_frame,
            metersize=180,
            amountused=50,
            metertype=SEMI,
            stripethickness=3,
            bootstyle=SUCCESS,
            subtext="Semi + Rayas"
        )
        meter_semi_striped.pack(pady=10)

        # Medidor con rayas y cuña
        wedge_striped_frame = ttk.Labelframe(combo_row, text="Con rayas y cuña", padding=15)
        wedge_striped_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_wedge_striped = ttk.Meter(
            wedge_striped_frame,
            metersize=180,
            amountused=75,
            stripethickness=4,
            wedgesize=10,
            bootstyle=INFO,
            subtext="Cuña + Rayas"
        )
        meter_wedge_striped.pack(pady=10)

        # Medidor con rayas interactivo
        interactive_striped_frame = ttk.Labelframe(combo_row, text="Interactivo con rayas", padding=15)
        interactive_striped_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        meter_interactive_striped = ttk.Meter(
            interactive_striped_frame,
            metersize=180,
            amountused=40,
            stripethickness=5,
            interactive=True,
            bootstyle=SECONDARY,
            subtext="Interactivo + Rayas"
        )
        meter_interactive_striped.pack(pady=10)

        # Descripción
        desc_frame = ttk.Frame(tab, padding=10)
        desc_frame.pack(fill=X, pady=20)

        ttk.Label(
            desc_frame,
            text="El parámetro 'stripethickness' permite crear un efecto de rayas en el indicador del medidor. "
                 "Un valor de 0 produce un indicador sólido, mientras que valores mayores crean rayas más gruesas. "
                 "Este efecto puede combinarse con otras características como cuñas o interactividad.",
            wraplength=800
        ).pack()

    def create_animation_tab(self):
        """Pestaña que muestra medidores animados"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Animación")

        ttk.Label(
            tab,
            text="Animando Medidores con el Método step()",
            font=("-size 16 -weight bold")
        ).pack(pady=(0, 20))

        # Frame para los controles principales
        controls_frame = ttk.Frame(tab)
        controls_frame.pack(fill=X, pady=10)

        # Botón para iniciar la animación en todos los medidores
        self.animation_running = False
        self.animation_thread = None

        def toggle_animation():
            if self.animation_running:
                self.animation_running = False
                animation_btn.configure(text="Iniciar Animación")
            else:
                self.animation_running = True
                animation_btn.configure(text="Detener Animación")

                # Iniciar thread de animación
                self.animation_thread = Thread(target=animate_meters)
                self.animation_thread.daemon = True
                self.animation_thread.start()

        animation_btn = ttk.Button(
            controls_frame,
            text="Iniciar Animación",
            command=toggle_animation,
            bootstyle=SUCCESS,
            width=20
        )
        animation_btn.pack(pady=10)

        # Frame para los medidores
        meters_frame = ttk.Frame(tab)
        meters_frame.pack(fill=X, pady=10)

        # Medidor básico con step
        basic_step_frame = ttk.Labelframe(meters_frame, text="step() Estándar", padding=15)
        basic_step_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        self.meter_step = ttk.Meter(
            basic_step_frame,
            metersize=180,
            amountused=0,
            bootstyle=PRIMARY,
            subtext="step(5)"
        )
        self.meter_step.pack(pady=10)

        # Medidor de rebote
        bounce_frame = ttk.Labelframe(meters_frame, text="Rebote Automático", padding=15)
        bounce_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        self.meter_bounce = ttk.Meter(
            bounce_frame,
            metersize=180,
            amountused=0,
            bootstyle=INFO,
            subtext="Rebota en límites"
        )
        self.meter_bounce.pack(pady=10)

        # Medidor con step y cambio de color
        color_step_frame = ttk.Labelframe(meters_frame, text="Cambio de Color", padding=15)
        color_step_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        self.meter_color = ttk.Meter(
            color_step_frame,
            metersize=180,
            amountused=0,
            bootstyle=SUCCESS,
            subtext="Color dinámico"
        )
        self.meter_color.pack(pady=10)

        # Función de animación que se ejecuta en un hilo separado
        def animate_meters():
            stepping_up = True
            color_cycle = [SUCCESS, WARNING, DANGER, INFO, PRIMARY]
            color_index = 0

            while self.animation_running:
                # Animar el primer medidor (incremento constante)
                self.meter_step.step(5)

                # Animar el segundo medidor (rebote automático)
                self.meter_bounce.step(2)

                # Animar el tercer medidor (con cambio de color)
                current = self.meter_color["amountused"]

                if stepping_up:
                    if current < 95:
                        self.meter_color.configure(amountused=current + 5)
                    else:
                        stepping_up = False
                        # Cambiar color
                        color_index = (color_index + 1) % len(color_cycle)
                        self.meter_color.configure(bootstyle=color_cycle[color_index])
                else:
                    if current > 5:
                        self.meter_color.configure(amountused=current - 5)
                    else:
                        stepping_up = True
                        # Cambiar color
                        color_index = (color_index + 1) % len(color_cycle)
                        self.meter_color.configure(bootstyle=color_cycle[color_index])

                # Pausa entre pasos
                time.sleep(0.1)

        # Descripción
        desc_frame = ttk.Frame(tab, padding=10)
        desc_frame.pack(fill=X, pady=20)

        ttk.Label(
            desc_frame,
            text="El método step() permite incrementar o decrementar el valor del medidor en una cantidad específica. "
                 "También implementa un comportamiento de 'rebote' en los límites: cuando el valor alcanza el máximo, "
                 "comienza a decrementar, y cuando alcanza cero, comienza a incrementar nuevamente.",
            wraplength=800
        ).pack()

    def create_realworld_tab(self):
        """Pestaña que muestra ejemplos de aplicaciones del mundo real"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Aplicaciones")

        ttk.Label(
            tab,
            text="Ejemplos de Aplicaciones Prácticas",
            font=("-size 16 -weight bold")
        ).pack(pady=(0, 20))

        # Frame para ejemplos de la primera fila
        row1 = ttk.Frame(tab)
        row1.pack(fill=X, pady=10)

        # Ejemplo: Monitoreo de recursos del sistema
        system_frame = ttk.Labelframe(row1, text="Monitoreo de Recursos", padding=15)
        system_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        # Frame para los medidores
        resource_frame = ttk.Frame(system_frame)
        resource_frame.pack(fill=X)

        # CPU
        cpu_frame = ttk.Frame(resource_frame, padding=5)
        cpu_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        ttk.Label(cpu_frame, text="CPU").pack()

        self.cpu_meter = ttk.Meter(
            cpu_frame,
            metersize=120,
            amountused=45,
            textright="%",
            bootstyle=PRIMARY,
            stripethickness=3
        )
        self.cpu_meter.pack()

        # RAM
        ram_frame = ttk.Frame(resource_frame, padding=5)
        ram_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        ttk.Label(ram_frame, text="RAM").pack()

        self.ram_meter = ttk.Meter(
            ram_frame,
            metersize=120,
            amountused=60,
            textright="%",
            bootstyle=INFO,
            stripethickness=3
        )
        self.ram_meter.pack()

        # Disco
        disk_frame = ttk.Frame(resource_frame, padding=5)
        disk_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        ttk.Label(disk_frame, text="Disco").pack()

        self.disk_meter = ttk.Meter(
            disk_frame,
            metersize=120,
            amountused=75,
            textright="%",
            bootstyle=SUCCESS,
            stripethickness=3
        )
        self.disk_meter.pack()

        # Botones de acción
        action_frame = ttk.Frame(system_frame, padding=(0, 15, 0, 0))
        action_frame.pack(fill=X)

        ttk.Button(
            action_frame,
            text="Refrescar Valores",
            command=self.update_resource_meters
        ).pack(fill=X)

        # Ejemplo: Control de temperatura
        temp_frame = ttk.Labelframe(row1, text="Control de Temperatura", padding=15)
        temp_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        self.temp_meter = ttk.Meter(
            temp_frame,
            metersize=170,
            amountused=22,
            amounttotal=40,
            metertype=SEMI,
            arcoffset=135,
            arcrange=270,
            textright="°C",
            meterthickness=15,
            bootstyle=SUCCESS,
            subtext="Temperatura"
        )
        self.temp_meter.pack(pady=5)

        # Controles para temperatura
        temp_control = ttk.Frame(temp_frame)
        temp_control.pack(fill=X, pady=(15, 0))

        ttk.Button(
            temp_control,
            text="▼",
            command=lambda: self.update_temperature(-1)
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

        ttk.Button(
            temp_control,
            text="▲",
            command=lambda: self.update_temperature(1)
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

        # Frame para ejemplos de la segunda fila
        row2 = ttk.Frame(tab)
        row2.pack(fill=X, pady=20)

        # Ejemplo: Progreso de descarga
        download_frame = ttk.Labelframe(row2, text="Progreso de Descarga", padding=15)
        download_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        self.download_meter = ttk.Meter(
            download_frame,
            metersize=170,
            amountused=0,
            amounttotal=100,
            textright="%",
            bootstyle=PRIMARY,
            stripethickness=2,
            subtext="0 MB / 100 MB"
        )
        self.download_meter.pack(pady=10)

        # Continuación del código de create_realworld_tab()
        dl_control = ttk.Frame(download_frame)
        dl_control.pack(fill=X, pady=(15, 0))

        # Variables para simulación de descarga
        self.download_running = False
        self.download_thread = None

        def toggle_download():
            if self.download_running:
                self.download_running = False
                download_btn.configure(text="Iniciar Descarga")
            else:
                self.download_running = True
                download_btn.configure(text="Pausar Descarga")

                # Reiniciar si ya completó
                if self.download_meter["amountused"] >= 100:
                    self.download_meter.configure(amountused=0)
                    self.download_meter.configure(subtext="0 MB / 100 MB")

                # Iniciar thread de descarga
                self.download_thread = Thread(target=simulate_download)
                self.download_thread.daemon = True
                self.download_thread.start()

        download_btn = ttk.Button(
            dl_control,
            text="Iniciar Descarga",
            command=toggle_download
        )
        download_btn.pack(side=LEFT, padx=5, fill=X, expand=YES)

        ttk.Button(
            dl_control,
            text="Cancelar",
            bootstyle=DANGER,
            command=lambda: (
                setattr(self, 'download_running', False),
                self.download_meter.configure(amountused=0),
                self.download_meter.configure(subtext="0 MB / 100 MB"),
                download_btn.configure(text="Iniciar Descarga")
            )
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

        # Simulación de descarga
        def simulate_download():
            while self.download_running and self.download_meter["amountused"] < 100:
                # Incrementar progreso
                current = self.download_meter["amountused"]
                progress = min(current + random.uniform(0.5, 2.0), 100)
                self.download_meter.configure(amountused=progress)

                # Actualizar subtexto
                downloaded = progress  # En MB para este ejemplo
                self.download_meter.configure(subtext=f"{downloaded:.1f} MB / 100 MB")

                # Cambiar estilo según progreso
                if progress < 30:
                    self.download_meter.configure(bootstyle=PRIMARY)
                elif progress < 70:
                    self.download_meter.configure(bootstyle=INFO)
                else:
                    self.download_meter.configure(bootstyle=SUCCESS)

                # Pausa entre actualizaciones
                time.sleep(0.1)

            # Si completó la descarga
            if self.download_meter["amountused"] >= 100:
                self.download_meter.configure(subtext="¡Descarga completa!")
                self.download_running = False
                self.root.after(0, lambda: download_btn.configure(text="Iniciar Descarga"))

        # Ejemplo: Medidor de satisfacción
        satisfaction_frame = ttk.Labelframe(row2, text="Valoración de Usuario", padding=15)
        satisfaction_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        self.rating_meter = ttk.Meter(
            satisfaction_frame,
            metersize=170,
            amountused=4,
            amounttotal=5,
            wedgesize=10,
            meterthickness=15,
            interactive=True,
            stepsize=1,
            bootstyle=PRIMARY,
            textright="/5",
            subtext="¡Puntúa tu experiencia!"
        )
        self.rating_meter.pack(pady=10)

        # Etiquetar según valoración
        self.rating_label = ttk.Label(
            satisfaction_frame,
            text="Muy bueno",
            font="-size 12"
        )
        self.rating_label.pack(pady=5)

        # Actualizar etiqueta al cambiar rating
        def update_rating_label(*_):
            rating = self.rating_meter["amountused"]
            labels = ["Muy malo", "Malo", "Regular", "Bueno", "Muy bueno"]
            colors = [DANGER, WARNING, SECONDARY, INFO, SUCCESS]

            # En caso de valores entre enteros, usar el entero más cercano
            rating_int = min(int(rating), 4)  # Asegurar índice válido

            self.rating_label.configure(text=labels[rating_int])
            self.rating_meter.configure(bootstyle=colors[rating_int])

        self.rating_meter.amountusedvar.trace_add("write", update_rating_label)

        # Descripción
        desc_frame = ttk.Frame(tab, padding=10)
        desc_frame.pack(fill=X, pady=20)

        ttk.Label(
            desc_frame,
            text="El widget Meter es extremadamente versátil y puede aplicarse en numerosos escenarios prácticos: "
                 "monitoreo de recursos del sistema, indicadores de progreso, controles de temperatura, "
                 "sistemas de valoración, visualización de estadísticas, y muchos más.",
            wraplength=800
        ).pack()

    def update_resource_meters(self):
        """Actualiza los medidores de recursos con valores aleatorios simulados"""
        # Simular valores de recursos
        cpu = random.randint(10, 95)
        ram = random.randint(30, 90)
        disk = random.randint(50, 98)

        # Actualizar medidores
        self.cpu_meter.configure(amountused=cpu)
        self.ram_meter.configure(amountused=ram)
        self.disk_meter.configure(amountused=disk)

        # Cambiar color según carga
        if cpu < 50:
            self.cpu_meter.configure(bootstyle=PRIMARY)
        elif cpu < 80:
            self.cpu_meter.configure(bootstyle=WARNING)
        else:
            self.cpu_meter.configure(bootstyle=DANGER)

        if ram < 60:
            self.ram_meter.configure(bootstyle=INFO)
        elif ram < 85:
            self.ram_meter.configure(bootstyle=WARNING)
        else:
            self.ram_meter.configure(bootstyle=DANGER)

        if disk < 70:
            self.disk_meter.configure(bootstyle=SUCCESS)
        elif disk < 90:
            self.disk_meter.configure(bootstyle=WARNING)
        else:
            self.disk_meter.configure(bootstyle=DANGER)

    def update_temperature(self, delta):
        """Actualiza el medidor de temperatura"""
        current = self.temp_meter["amountused"]
        new_temp = max(min(current + delta, 40), 10)  # Limitar entre 10 y 40

        self.temp_meter.configure(amountused=new_temp)

        # Actualizar color según temperatura
        if new_temp < 18:
            self.temp_meter.configure(bootstyle=INFO)
        elif new_temp < 24:
            self.temp_meter.configure(bootstyle=SUCCESS)
        elif new_temp < 30:
            self.temp_meter.configure(bootstyle=WARNING)
        else:
            self.temp_meter.configure(bootstyle=DANGER)

def main():
    """Función principal para ejecutar la demostración"""
    root = ttk.Window(themename="flatly")
    root.title("Demostración Completa del Widget Meter")

    # Crear la aplicación de demostración
    app = MeterDemo(root)

    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()