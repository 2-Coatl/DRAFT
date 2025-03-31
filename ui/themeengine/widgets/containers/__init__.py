"""
UI Theme Engine - Containers
============================

Colección de widgets contenedores para la interfaz de usuario.

Este módulo proporciona contenedores versátiles que pueden utilizarse
como bloques de construcción para interfaces de usuario complejas,
facilitando la organización y distribución de elementos visuales.

Widgets disponibles:
------------------
- ScrolledFrame: Frame con capacidad de desplazamiento para contener múltiples widgets
- ScrolledText: Área de texto con funcionalidad de desplazamiento integrada

En futuras versiones, este paquete podría ampliarse con otros contenedores como:
- CollapsiblePane
- CardContainer
- TabContainer
- etc.

"""

# Importaciones de módulos internos del paquete
from ui.themeengine.widgets.containers.scrolled_frame import ScrolledFrame
from ui.themeengine.widgets.containers.scrolled_text import ScrolledText

# API pública
__all__ = [
    'ScrolledFrame',
    'ScrolledText',
]