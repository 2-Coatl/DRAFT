"""Módulo de gestión de estilos y temas"""
# Importar componentes principales del núcleo
from ui.themeengine.core.top_level import Toplevel
from ui.themeengine.core.window import Window
from ui.themeengine.core.style import Style
from ui.themeengine.utils.bootstyle import Bootstyle

#  Importar widgets
from ui.themeengine.widgets import *

# Configurar el sistema de temas
Bootstyle.setup_ttktheming_api()

#  Importar widgets personalizados
from ui.themeengine.widgets.scrolled.scrolled_frame import ScrolledFrame
from ui.themeengine.widgets.scrolled.scrolled_text import ScrolledText
from ui.themeengine.dialogs.base import Dialog
from ui.themeengine.dialogs.message_dialog import MessageDialog