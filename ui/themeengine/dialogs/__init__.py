"""
    Módulo de clases base para diálogos personalizables.

    Este módulo contiene diversas clases base de diálogos que pueden ser
    utilizadas para crear diálogos personalizados para el usuario final.
    Estas clases sirven como base para los métodos estáticos predefinidos
    en las clases contenedoras `Messagebox` y `Querybox`.

    Las clases incluidas en este módulo proporcionan:
      - Estructura fundamental para crear ventanas modales
      - Implementación de patrones comunes para interacción con usuarios
      - Mecanismos para personalizar apariencia y comportamiento
      - Gestión de eventos y respuestas del usuario

"""
from ui.themeengine.dialogs.base import Dialog
from ui.themeengine.dialogs.message_dialog import MessageDialog
