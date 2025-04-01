import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
import random


class ThemeEngineDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Demostración Completa de ThemeEngine")
        self.root.geometry("900x700")

        # Configuración de tema inicial
        self.current_theme = "default"

        # Crear notebook para organizar los widgets en pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Crear las pestañas
        self.create_theme_tab()
        self.create_buttons_tab()
        self.create_inputs_tab()
        self.create_display_tab()
        self.create_layout_tab()
        self.create_advanced_tab()

        # Barra de estado
        self.status_var = ttk.StringVar(value="ThemeEngine Demo - Versión 1.0")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, bootstyle=INFO)
        status_bar.pack(side=BOTTOM, fill=X)

    def create_theme_tab(self):
        """Pestaña para selección de temas y colores"""
        theme_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(theme_frame, text="Temas y Colores")

        # Selector de temas
        themes_frame = ttk.Labelframe(theme_frame, text="Temas Disponibles", padding=10)
        themes_frame.pack(fill=X, pady=5)

        themes = ["default", "dark", "light", "cosmo", "superhero", "cyborg", "vapor", "litera"]
        theme_var = ttk.StringVar(value=self.current_theme)

        for theme in themes:
            rb = ttk.Radiobutton(
                themes_frame,
                text=theme.capitalize(),
                value=theme,
                variable=theme_var,
                command=lambda t=theme: self.change_theme(t)
            )
            rb.pack(side=LEFT, padx=5)

        # Paleta de colores
        colors_frame = ttk.Labelframe(theme_frame, text="Paleta de Colores", padding=10)
        colors_frame.pack(fill=BOTH, expand=YES, pady=10)

        color_groups = {
            "Primarios": [PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER],
            "Tonos": [LIGHT, DARK],
            "Estados": [ACTIVE, DISABLED],
            #"Otros": [INVERSE, BORDER, BACKGROUND]
        }

        row = 0
        for group_name, colors in color_groups.items():
            group_label = ttk.Label(colors_frame, text=group_name + ":", font=("-size", 12, "-weight", "bold"))
            group_label.grid(row=row, column=0, sticky=W, pady=(10, 5))
            row += 1

            for i, color in enumerate(colors):
                color_frame = ttk.Frame(colors_frame, bootstyle=color, height=40, width=100)
                color_frame.grid(row=row, column=i, padx=5, pady=5, sticky=NSEW)

                color_label = ttk.Label(colors_frame, text=color)
                color_label.grid(row=row + 1, column=i, padx=5, sticky=N)

            row += 2

        # Ajustar columnas
        for i in range(6):
            colors_frame.columnconfigure(i, weight=1)

    def create_buttons_tab(self):
        """Pestaña con demostración de botones"""
        buttons_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(buttons_frame, text="Botones")

        # Tipos de botones
        basic_frame = ttk.Labelframe(buttons_frame, text="Botones Básicos", padding=10)
        basic_frame.pack(fill=X, pady=5)

        for style in [PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER]:
            btn = ttk.Button(
                basic_frame,
                text=f"Botón {style}",
                bootstyle=style
            )
            btn.pack(side=LEFT, padx=5, pady=5)

        # Botones de tamaños
        size_frame = ttk.Labelframe(buttons_frame, text="Tamaños de Botones", padding=10)
        size_frame.pack(fill=X, pady=5)

        sizes = [("Grande", "lg"), ("Normal", ""), ("Pequeño", "sm"), ("Extra Pequeño", "xs")]

        for name, size in sizes:
            btn = ttk.Button(
                size_frame,
                text=name,
                bootstyle=(INFO, size)
            )
            btn.pack(side=LEFT, padx=5, pady=5)

        # Botones de enlace
        link_frame = ttk.Labelframe(buttons_frame, text="Botones de Enlace", padding=10)
        link_frame.pack(fill=X, pady=5)

        for style in [PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER]:
            btn = ttk.Button(
                link_frame,
                text=f"Enlace {style}",
                bootstyle=(style, "link")
            )
            btn.pack(side=LEFT, padx=5, pady=5)

        # Botones de contorno
        outline_frame = ttk.Labelframe(buttons_frame, text="Botones de Contorno", padding=10)
        outline_frame.pack(fill=X, pady=5)

        for style in [PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER]:
            btn = ttk.Button(
                outline_frame,
                text=f"Contorno {style}",
                bootstyle=(style, "outline")
            )
            btn.pack(side=LEFT, padx=5, pady=5)

        # Grupo de botones
        group_frame = ttk.Labelframe(buttons_frame, text="Grupo de Botones", padding=10)
        group_frame.pack(fill=X, pady=5)

        btn_group = ttk.Frame(group_frame)
        btn_group.pack(pady=10)

        for style in [PRIMARY, SUCCESS, WARNING]:
            btn = ttk.Button(
                btn_group,
                text=f"Opción {style}",
                bootstyle=style
            )
            btn.pack(side=LEFT)

        # Botones con iconos
        icon_frame = ttk.Labelframe(buttons_frame, text="Botones con Iconos", padding=10)
        icon_frame.pack(fill=X, pady=5)

        icons = ["add", "remove", "settings", "info", "warning", "error"]

        for i, icon in enumerate(icons):
            btn = ttk.Button(
                icon_frame,
                text=f" {icon.capitalize()}",
                bootstyle=(PRIMARY, "outline"),
                image=f"icon_{icon}",
                compound=LEFT
            )
            btn.pack(side=LEFT, padx=5, pady=5)

    def create_inputs_tab(self):
        """Pestaña con elementos de entrada"""
        inputs_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(inputs_frame, text="Entradas")

        # Entradas de texto
        entry_frame = ttk.Labelframe(inputs_frame, text="Campos de Texto", padding=10)
        entry_frame.pack(fill=X, pady=5)

        ttk.Label(entry_frame, text="Entrada normal:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(entry_frame, width=30).grid(row=0, column=1, padx=5, pady=5, sticky=W)

        ttk.Label(entry_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(entry_frame, width=30, show="•").grid(row=1, column=1, padx=5, pady=5, sticky=W)

        ttk.Label(entry_frame, text="Con placeholder:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        placeholder_entry = ttk.Entry(entry_frame, width=30)
        placeholder_entry.insert(0, "Escribe aquí...")
        placeholder_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        ttk.Label(entry_frame, text="Deshabilitado:").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(entry_frame, width=30, state=DISABLED).grid(row=3, column=1, padx=5, pady=5, sticky=W)

        # Área de texto
        text_frame = ttk.Labelframe(inputs_frame, text="Área de Texto", padding=10)
        text_frame.pack(fill=X, pady=5)

        text_area = ttk.Text(text_frame, width=40, height=5)
        text_area.pack(fill=X, padx=5, pady=5)
        text_area.insert(END, "Esta es un área de texto donde puedes escribir varias líneas de contenido.")

        # Checkbox
        check_frame = ttk.Labelframe(inputs_frame, text="Casillas de Verificación", padding=10)
        check_frame.pack(fill=X, pady=5)

        for style in [PRIMARY, SUCCESS, WARNING, DANGER]:
            var = ttk.BooleanVar()
            cb = ttk.Checkbutton(
                check_frame,
                text=f"Opción {style}",
                variable=var,
                bootstyle=style
            )
            cb.pack(side=LEFT, padx=10, pady=5)

        # Switches
        switch_frame = ttk.Labelframe(inputs_frame, text="Interruptores", padding=10)
        switch_frame.pack(fill=X, pady=5)

        for style in [PRIMARY, SUCCESS, WARNING, DANGER]:
            var = ttk.BooleanVar()
            sw = ttk.Checkbutton(
                switch_frame,
                text=f"Switch {style}",
                variable=var,
                bootstyle=(style, "round-toggle")
            )
            sw.pack(side=LEFT, padx=10, pady=5)

        # Radio buttons
        radio_frame = ttk.Labelframe(inputs_frame, text="Botones de Radio", padding=10)
        radio_frame.pack(fill=X, pady=5)

        radio_var = ttk.IntVar(value=0)

        for i, style in enumerate([PRIMARY, SUCCESS, WARNING, DANGER]):
            rb = ttk.Radiobutton(
                radio_frame,
                text=f"Opción {i + 1}",
                variable=radio_var,
                value=i,
                bootstyle=style
            )
            rb.pack(side=LEFT, padx=10, pady=5)

        # Combobox
        combo_frame = ttk.Labelframe(inputs_frame, text="Cuadros Desplegables", padding=10)
        combo_frame.pack(fill=X, pady=5)

        ttk.Label(combo_frame, text="Combobox:").pack(side=LEFT, padx=5)
        options = ["Opción 1", "Opción 2", "Opción 3", "Opción 4", "Opción 5"]
        combo = ttk.Combobox(combo_frame, values=options, width=15)
        combo.current(0)
        combo.pack(side=LEFT, padx=5, pady=5)

        # Selectores numéricos
        spinbox_frame = ttk.Labelframe(inputs_frame, text="Selectores Numéricos", padding=10)
        spinbox_frame.pack(fill=X, pady=5)

        ttk.Label(spinbox_frame, text="Spinbox:").pack(side=LEFT, padx=5)
        spin = ttk.Spinbox(spinbox_frame, from_=0, to=100, width=10)
        spin.set(50)
        spin.pack(side=LEFT, padx=5, pady=5)

    def create_display_tab(self):
        """Pestaña con elementos de visualización"""
        display_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(display_frame, text="Visualización")

        # Labels
        label_frame = ttk.Labelframe(display_frame, text="Etiquetas", padding=10)
        label_frame.pack(fill=X, pady=5)

        for style in [PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER]:
            lbl = ttk.Label(
                label_frame,
                text=f"Etiqueta {style}",
                bootstyle=style
            )
            lbl.pack(side=LEFT, padx=5, pady=5)

        # Barras de progreso
        progress_frame = ttk.Labelframe(display_frame, text="Barras de Progreso", padding=10)
        progress_frame.pack(fill=X, pady=5)

        for i, style in enumerate([PRIMARY, SUCCESS, WARNING, DANGER]):
            value = random.randint(10, 90)
            ttk.Label(progress_frame, text=f"{style}:").grid(row=i, column=0, padx=5, pady=5, sticky=W)
            pb = ttk.Progressbar(
                progress_frame,
                bootstyle=style,
                value=value,
                length=300
            )
            pb.grid(row=i, column=1, padx=5, pady=5, sticky=W)
            ttk.Label(progress_frame, text=f"{value}%").grid(row=i, column=2, padx=5, pady=5, sticky=W)

        # Barras de progreso circulares
        circular_frame = ttk.Labelframe(display_frame, text="Progreso Circular", padding=10)
        circular_frame.pack(fill=X, pady=5)

        for style in [PRIMARY, SUCCESS, WARNING, DANGER]:
            value = random.randint(10, 90)
            meter = ttk.Meter(
                circular_frame,
                bootstyle=style,
                amountused=value,
                interactive=True,
                metersize=150,
                subtext="completado",
                textright="%"
            )
            meter.pack(side=LEFT, padx=10, pady=10)

        # Alertas/Mensajes
        alert_frame = ttk.Labelframe(display_frame, text="Alertas", padding=10)
        alert_frame.pack(fill=X, pady=5)

        for style in [SUCCESS, INFO, WARNING, DANGER]:
            alert = ttk.Label(
                alert_frame,
                text=f"Mensaje de {style}: Esto es un ejemplo de alerta informativa.",
                bootstyle=(style, "inverse"),
                padding=10
            )
            alert.pack(fill=X, pady=5)

    def create_layout_tab(self):
        """Pestaña con elementos de layout"""
        layout_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(layout_frame, text="Layout")

        # Separadores
        separator_frame = ttk.Labelframe(layout_frame, text="Separadores", padding=10)
        separator_frame.pack(fill=X, pady=5)

        ttk.Label(separator_frame, text="Separador horizontal:").pack(anchor=W, pady=5)
        ttk.Separator(separator_frame, bootstyle=PRIMARY).pack(fill=X, pady=10)

        h_frame = ttk.Frame(separator_frame)
        h_frame.pack(fill=X, pady=10)

        ttk.Label(h_frame, text="Izquierda").pack(side=LEFT, padx=5)
        ttk.Separator(h_frame, bootstyle=DANGER, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=10, pady=5)
        ttk.Label(h_frame, text="Centro").pack(side=LEFT, padx=5)
        ttk.Separator(h_frame, bootstyle=DANGER, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=10, pady=5)
        ttk.Label(h_frame, text="Derecha").pack(side=LEFT, padx=5)

        # Paneles
        panel_frame = ttk.Labelframe(layout_frame, text="Paneles", padding=10)
        panel_frame.pack(fill=X, pady=5)

        # Panel con borde y titulo
        panel1 = ttk.Frame(panel_frame, bootstyle=SECONDARY)
        panel1.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)

        panel1_header = ttk.Frame(panel1, bootstyle=(SECONDARY, "inverse"))
        panel1_header.pack(fill=X)
        ttk.Label(panel1_header, text="Panel con Título", bootstyle=(SECONDARY, "inverse")).pack(padx=5, pady=5)

        panel1_content = ttk.Frame(panel1, padding=10)
        panel1_content.pack(fill=BOTH, expand=YES)
        ttk.Label(panel1_content, text="Contenido del panel").pack(pady=20)

        # Panel con sombra
        panel2 = ttk.Frame(panel_frame, bootstyle=PRIMARY)
        panel2.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)

        ttk.Label(panel2, text="Panel con Sombra", padding=10).pack()

        # Tarjetas (cards)
        cards_frame = ttk.Labelframe(layout_frame, text="Tarjetas", padding=10)
        cards_frame.pack(fill=X, pady=5)

        card_styles = [PRIMARY, SUCCESS, WARNING]

        for style in card_styles:
            card = ttk.Frame(cards_frame, bootstyle=style)
            card.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)

            card_header = ttk.Frame(card, bootstyle=(style, "inverse"))
            card_header.pack(fill=X)
            ttk.Label(card_header, text=f"Tarjeta {style}", bootstyle=(style, "inverse")).pack(padx=5, pady=5)

            card_content = ttk.Frame(card, padding=10)
            card_content.pack(fill=BOTH, expand=YES)
            ttk.Label(card_content, text="Contenido de la tarjeta").pack(pady=10)

            ttk.Button(card_content, text="Acción", bootstyle=style).pack(pady=5)

        # Acordeón
        accordion_frame = ttk.Labelframe(layout_frame, text="Acordeón", padding=10)
        accordion_frame.pack(fill=BOTH, expand=YES, pady=5)

        for i in range(1, 4):
            section = ttk.Labelframe(accordion_frame, text=f"Sección {i}", padding=10, bootstyle=PRIMARY)
            section.pack(fill=X, pady=2)

            content = ttk.Label(section,
                                text=f"Contenido expandible para la sección {i}. Haz clic en la cabecera para expandir/contraer.")
            content.pack(pady=10)

    def create_advanced_tab(self):
        """Pestaña con widgets avanzados"""
        advanced_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(advanced_frame, text="Avanzado")

        # Pestañas anidadas
        tabs_frame = ttk.Labelframe(advanced_frame, text="Pestañas Anidadas", padding=10)
        tabs_frame.pack(fill=X, pady=5)

        nested_notebook = ttk.Notebook(tabs_frame)
        nested_notebook.pack(fill=X, pady=5)

        for i, style in enumerate([PRIMARY, SUCCESS, WARNING]):
            tab = ttk.Frame(nested_notebook, padding=10)
            nested_notebook.add(tab, text=f"Pestaña {i + 1}")

            ttk.Label(tab, text=f"Contenido de la pestaña {i + 1}").pack(pady=20)

        # Slider/Scale
        slider_frame = ttk.Labelframe(advanced_frame, text="Deslizadores", padding=10)
        slider_frame.pack(fill=X, pady=5)

        ttk.Label(slider_frame, text="Horizontal:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        h_scale = ttk.Scale(
            slider_frame,
            from_=0,
            to=100,
            length=200,
            value=50,
            bootstyle=SUCCESS
        )
        h_scale.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        ttk.Label(slider_frame, text="Vertical:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        v_scale = ttk.Scale(
            slider_frame,
            from_=0,
            to=100,
            length=200,
            orient=VERTICAL,
            value=50,
            bootstyle=DANGER
        )
        v_scale.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # DateEntry
        date_frame = ttk.Labelframe(advanced_frame, text="Selectores de Fecha", padding=10)
        date_frame.pack(fill=X, pady=5)

        ttk.Label(date_frame, text="Fecha:").pack(side=LEFT, padx=5)
        date_entry = ttk.DateEntry(date_frame, bootstyle=INFO)
        date_entry.pack(side=LEFT, padx=5, pady=5)

        # Treeview
        tree_frame = ttk.Labelframe(advanced_frame, text="Vista de Árbol", padding=10)
        tree_frame.pack(fill=BOTH, expand=YES, pady=5)

        columns = ("nombre", "edad", "ciudad")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=5)

        tree.heading("nombre", text="Nombre")
        tree.heading("edad", text="Edad")
        tree.heading("ciudad", text="Ciudad")

        data = [
            ("Juan Pérez", 28, "Madrid"),
            ("Ana García", 34, "Barcelona"),
            ("Carlos López", 45, "Valencia"),
            ("María Rodríguez", 31, "Sevilla"),
            ("David Martínez", 39, "Bilbao")
        ]

        for item in data:
            tree.insert("", END, values=item)

        tree.pack(fill=BOTH, expand=YES, pady=5)

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def change_theme(self, theme_name):
        """Cambia el tema de la aplicación"""
        try:
            self.root.style.theme_use(theme_name)
            self.current_theme = theme_name
            self.status_var.set(f"Tema cambiado a: {theme_name}")
        except Exception as e:
            self.status_var.set(f"Error al cambiar el tema: {str(e)}")


def main():
    app = ttk.Window()
    ThemeEngineDemo(app)
    app.mainloop()


if __name__ == "__main__":
    main()