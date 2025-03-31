"""
UI Theme Engine - Alert Dialogs
==============================

Colección especializada de diálogos para notificaciones y alertas al usuario.

Este módulo proporciona diálogos diseñados específicamente para comunicar
información, advertencias y errores al usuario de manera clara y consistente.

Diálogos disponibles:
-------------------
- MessageDialog: Diálogo de mensajes básico y personalizable
- MessageBox: Cuadro de mensaje simple
"""

# Importaciones de módulos internos del paquete
from ui.themeengine.dialogs.alert.message_dialog import MessageDialog
#from ui.themeengine.dialogs.alert.message_box import MessageBox

# Definir la API pública de este subpaquete
__all__ = [
    'MessageDialog',
 #   'MessageBox',
]