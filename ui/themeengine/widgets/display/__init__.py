"""
UI Theme Engine - Display Widgets
================================

Colección de widgets especializados para visualización de datos y estados.

Este módulo proporciona componentes visuales diseñados para representar
información de manera gráfica e intuitiva, permitiendo mostrar valores,
progreso y estados de manera visualmente efectiva.

Widgets disponibles:
------------------
- FloodGauge: Indicador de progreso personalizado con efecto de llenado
- Meter: Widget de medición tipo dial/gauge para representar valores en un rango

Widgets planeados para futuras versiones:
----------------------------------------
- StatusIndicator: Indicador visual para mostrar estados (activo/inactivo, error/advertencia/ok)
- LevelBar: Barra horizontal o vertical para mostrar niveles (batería, volumen, intensidad)
- ColorDisplay: Widget para mostrar y visualizar colores
- Sparkline: Gráfico minimalista de línea para visualizar tendencias
- ProgressRing: Indicador circular de progreso
- NumberDisplay: Pantalla especializada para valores numéricos con formato
- IconDisplay: Widget para mostrar íconos según estado o tema
- Badge: Pequeño indicador superpuesto para contadores o notificaciones
- Timeline: Visualización de eventos en secuencia temporal
- Histogram: Visualización simple de distribuciones de datos

"""

# Importaciones de módulos internos del paquete
from ui.themeengine.widgets.display.floodgauge import FloodGauge
from ui.themeengine.widgets.display.meter import Meter

# API pública
__all__ = [
    'FloodGauge',
    'Meter',
]