import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine.widgets.scrolled.scrolled_frame import ScrolledFrame

def main():
    app = ttk.Window()

    # Crear un ScrolledFrame
    sf = ScrolledFrame(app, autohide=True)
    sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # Iterar directamente sobre los colores como en el ejemplo original
    for color in app.style.colors:
        b = ttk.Button(sf, text=color, bootstyle=color)
        b.pack(padx=5, pady=5)

    app.mainloop()

if __name__ == "__main__":
    main()