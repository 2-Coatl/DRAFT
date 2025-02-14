from enum import Enum

class Channel(Enum):
    """Canales de comunicación para el sistema de notificaciones.

    Define los tipos de widgets que pueden recibir notificaciones de
    actualización de temas.

    Atributos:
        STD:
            Widgets tradicionales de tkinter (por ejemplo: Label, Button).
        TTK:
            Widgets temáticos de tkinter (por ejemplo: ttk.Label, ttk.Button).
    """

    STD = 1  # Widgets tradicionales
    TTK = 2  # Widgets temáticos

