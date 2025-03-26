import ui.themeengine as ttk
from ui.themeengine.utils.constants import *

def main():
    app = ttk.Window()

    frame = ttk.Frame(padding=10)
    frame.pack(padx=10, pady=10)

    for color in app.style.colors:
        b = ttk.Button(frame, text=color, bootstyle=color)
        b.pack(side=LEFT, padx=5, pady=5)

    app.mainloop()


if __name__ == "__main__":
    main()