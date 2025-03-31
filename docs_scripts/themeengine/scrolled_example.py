import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine.widgets.containers.scrolled_frame import ScrolledFrame


def main():
    """
    Demostración completa de la implementación y funcionalidades del widget ScrolledFrame.
    Este ejemplo muestra todas las características principales del widget.
    """
    # Crear la ventana principal
    app = ttk.Window(title="Demostración Completa de ScrolledFrame", themename="flatly")
    app.geometry("800x600")  # Tamaño suficiente para mostrar todas las demostraciones

    # Crear un notebook para organizar las diferentes demostraciones
    notebook = ttk.Notebook(app)
    notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # ========== DEMOSTRACIÓN 1: Uso básico ==========
    # Mostrar el uso más básico del ScrolledFrame
    basic_tab = ttk.Frame(notebook)
    notebook.add(basic_tab, text="Uso Básico")

    # Cabecera explicativa
    ttk.Label(
        basic_tab,
        text="Uso básico de ScrolledFrame con altura fija",
        font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    # ScrolledFrame básico con altura fija
    sf_basic = ScrolledFrame(basic_tab, height=200)
    sf_basic.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # Agregar contenido suficiente para mostrar el desplazamiento
    for i in range(20):
        ttk.Button(sf_basic, text=f"Botón {i + 1}").pack(fill=X, padx=5, pady=5)

    # ========== DEMOSTRACIÓN 2: Autohide ==========
    # Mostrar la diferencia entre autohide=True y autohide=False
    autohide_tab = ttk.Frame(notebook)
    notebook.add(autohide_tab, text="Autohide")

    # Dividir la pestaña en dos columnas
    autohide_left = ttk.LabelFrame(autohide_tab, text="Con autohide=True")
    autohide_left.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=10)

    autohide_right = ttk.LabelFrame(autohide_tab, text="Con autohide=False")
    autohide_right.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10, pady=10)

    # ScrolledFrame con autohide=True
    sf_autohide = ScrolledFrame(autohide_left, autohide=True, height=300)
    sf_autohide.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    # ScrolledFrame con autohide=False
    sf_no_autohide = ScrolledFrame(autohide_right, autohide=False, height=300)
    sf_no_autohide.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    # Agregar el mismo contenido a ambos ScrolledFrames
    for i, color in enumerate(app.style.colors):
        # Crear botones con diferentes estilos
        ttk.Button(
            sf_autohide,
            text=f"autohide=True (mueve el cursor aquí)",
            bootstyle=color
        ).pack(fill=X, padx=5, pady=5)

        ttk.Button(
            sf_no_autohide,
            text=f"autohide=False (barra siempre visible)",
            bootstyle=color
        ).pack(fill=X, padx=5, pady=5)

    # ========== DEMOSTRACIÓN 3: Uso con Notebook ==========
    # Demostrar el uso de .container como indica la documentación
    notebook_tab = ttk.Frame(notebook)
    notebook.add(notebook_tab, text="Con Notebook")

    # Crear un Notebook dentro de la pestaña
    inner_notebook = ttk.Notebook(notebook_tab)
    inner_notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # Crear un ScrolledFrame para usar con el Notebook
    sf_for_notebook = ScrolledFrame(inner_notebook)

    # Notar el uso de .container como se menciona en la documentación
    inner_notebook.add(sf_for_notebook.container, text="ScrolledFrame en Notebook")

    # Agregar contenido al ScrolledFrame
    ttk.Label(
        sf_for_notebook,
        text="Este ScrolledFrame está dentro de un Notebook\nNota el uso de .container",
        font=("Helvetica", 10, "bold")
    ).pack(pady=10)

    for i in range(30):
        ttk.Label(sf_for_notebook, text=f"Elemento {i + 1}").pack(anchor=W, padx=5, pady=2)

    # ========== DEMOSTRACIÓN 4: Control manual de ScrolledFrame ==========
    # Demostrar el control programático de las barras de desplazamiento
    control_tab = ttk.Frame(notebook)
    notebook.add(control_tab, text="Control Manual")

    # Cabecera explicativa
    ttk.Label(
        control_tab,
        text="Control programático de la barra de desplazamiento",
        font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    # Crear un marco para los botones de control
    control_buttons = ttk.Frame(control_tab)
    control_buttons.pack(fill=X, padx=10, pady=5)

    # ScrolledFrame para demostrar el control manual
    sf_control = ScrolledFrame(control_tab, height=250)
    sf_control.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # Agregar contenido al ScrolledFrame
    for i in range(20):
        ttk.Label(sf_control, text=f"Línea de contenido {i + 1}").pack(anchor=W, padx=5, pady=3)

    # Funciones de control
    def show_scrollbar():
        sf_control.show_scrollbars()
        status_var.set("Barra de desplazamiento visible")

    def hide_scrollbar():
        sf_control.hide_scrollbars()
        status_var.set("Barra de desplazamiento oculta")

    def toggle_autohide():
        sf_control.autohide_scrollbar()
        status_var.set(f"Autohide {'activado' if sf_control.autohide else 'desactivado'}")

    def move_to_start():
        sf_control.yview_moveto(0.0)
        status_var.set("Desplazado al inicio")

    def move_to_middle():
        sf_control.yview_moveto(0.5)
        status_var.set("Desplazado al medio")

    def move_to_end():
        sf_control.yview_moveto(1.0)
        status_var.set("Desplazado al final")

    def scroll_down():
        sf_control.yview_scroll(5, UNITS)
        status_var.set("Desplazado hacia abajo 5 unidades")

    def scroll_up():
        sf_control.yview_scroll(-5, UNITS)
        status_var.set("Desplazado hacia arriba 5 unidades")

    def disable_scroll():
        sf_control.disable_scrolling()
        status_var.set("Desplazamiento con rueda desactivado")

    def enable_scroll():
        sf_control.enable_scrolling()
        status_var.set("Desplazamiento con rueda activado")

    # Agregar botones de control en filas
    ttk.Button(control_buttons, text="Mostrar barra", command=show_scrollbar).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(control_buttons, text="Ocultar barra", command=hide_scrollbar).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(control_buttons, text="Alternar autohide", command=toggle_autohide).grid(row=0, column=2, padx=5, pady=5)

    ttk.Button(control_buttons, text="Ir al inicio", command=move_to_start).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(control_buttons, text="Ir al medio", command=move_to_middle).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(control_buttons, text="Ir al final", command=move_to_end).grid(row=1, column=2, padx=5, pady=5)

    ttk.Button(control_buttons, text="Desplazar abajo", command=scroll_down).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(control_buttons, text="Desplazar arriba", command=scroll_up).grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(control_buttons, text="Deshabilitar rueda", command=disable_scroll).grid(row=3, column=0, padx=5, pady=5)
    ttk.Button(control_buttons, text="Habilitar rueda", command=enable_scroll).grid(row=3, column=1, padx=5, pady=5)

    # Variable para mostrar el estado actual
    status_var = ttk.StringVar(value="Prueba los controles para ver los cambios")
    ttk.Label(control_tab, textvariable=status_var).pack(pady=10)

    # ========== DEMOSTRACIÓN 5: ScrolledFrame con contenido dinámico ==========
    # Demostrar cómo el ScrolledFrame se adapta a contenido que cambia dinámicamente
    dynamic_tab = ttk.Frame(notebook)
    notebook.add(dynamic_tab, text="Contenido Dinámico")

    # Cabecera explicativa
    ttk.Label(
        dynamic_tab,
        text="ScrolledFrame con contenido dinámico",
        font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    # Marco para controles
    dynamic_controls = ttk.Frame(dynamic_tab)
    dynamic_controls.pack(fill=X, padx=10, pady=5)

    # ScrolledFrame para contenido dinámico
    sf_dynamic = ScrolledFrame(dynamic_tab, height=300, autohide=True)
    sf_dynamic.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # Lista para mantener los widgets creados
    widgets_list = []

    # Contador para los elementos añadidos
    counter = ttk.IntVar(value=0)

    # Funciones para manipular el contenido
    def add_one():
        idx = counter.get() + 1
        counter.set(idx)

        # Crear un marco para contener elementos relacionados
        frame = ttk.Frame(sf_dynamic)
        frame.pack(fill=X, padx=5, pady=5)
        widgets_list.append(frame)

        # Añadir elementos al marco
        ttk.Label(frame, text=f"Elemento {idx}").pack(side=LEFT, padx=5)

        # Obtener una lista de estilos para variar la apariencia
        styles = ["primary", "secondary", "success", "info", "warning", "danger"]
        style_idx = idx % len(styles)

        ttk.Button(
            frame,
            text="Botón",
            bootstyle=styles[style_idx]
        ).pack(side=RIGHT, padx=5)

        # Generar un evento para que ScrolledFrame actualice la vista
        sf_dynamic.event_generate("<<MapChild>>")

    def add_ten():
        for _ in range(10):
            add_one()

    def remove_last():
        if widgets_list:
            # Obtener y eliminar el último widget
            widget = widgets_list.pop()
            widget.destroy()

            # Actualizar el contador
            counter.set(counter.get() - 1)

            # Actualizar la vista
            sf_dynamic.yview()

    def clear_all():
        # Eliminar todos los widgets
        for widget in widgets_list:
            widget.destroy()

        # Limpiar la lista y reiniciar el contador
        widgets_list.clear()
        counter.set(0)

        # Actualizar la vista
        sf_dynamic.yview()

    # Agregar controles
    ttk.Button(dynamic_controls, text="Añadir uno", command=add_one).pack(side=LEFT, padx=5)
    ttk.Button(dynamic_controls, text="Añadir diez", command=add_ten).pack(side=LEFT, padx=5)
    ttk.Button(dynamic_controls, text="Quitar último", command=remove_last).pack(side=LEFT, padx=5)
    ttk.Button(dynamic_controls, text="Limpiar todo", command=clear_all).pack(side=LEFT, padx=5)
    ttk.Label(dynamic_controls, textvariable=counter, width=3).pack(side=RIGHT, padx=5)
    ttk.Label(dynamic_controls, text="Contador:").pack(side=RIGHT)

    # Añadir algunos elementos iniciales
    for _ in range(5):
        add_one()

    # ========== DEMOSTRACIÓN 6: Ajuste de scrollheight ==========
    # Demostrar el parámetro scrollheight vs height
    scrollheight_tab = ttk.Frame(notebook)
    notebook.add(scrollheight_tab, text="Scrollheight")

    # Dividir la pestaña en dos columnas
    scrollheight_left = ttk.LabelFrame(scrollheight_tab, text="Con scrollheight=None (ajuste automático)")
    scrollheight_left.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=10)

    scrollheight_right = ttk.LabelFrame(scrollheight_tab, text="Con scrollheight=500 (fijo)")
    scrollheight_right.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10, pady=10)

    # ScrolledFrame con scrollheight=None (por defecto)
    sf_auto = ScrolledFrame(scrollheight_left, height=200)
    sf_auto.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    # ScrolledFrame con scrollheight fijo
    sf_fixed = ScrolledFrame(scrollheight_right, height=200, scrollheight=500)
    sf_fixed.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    # Agregar el mismo contenido a ambos ScrolledFrames
    for i in range(15):
        ttk.Label(
            sf_auto,
            text=f"La altura del contenido se ajusta automáticamente {i + 1}"
        ).pack(anchor=W, padx=5, pady=3)

        ttk.Label(
            sf_fixed,
            text=f"La altura del contenido está fijada en 500px {i + 1}"
        ).pack(anchor=W, padx=5, pady=3)

    # Iniciar la aplicación
    app.mainloop()


if __name__ == "__main__":
    main()