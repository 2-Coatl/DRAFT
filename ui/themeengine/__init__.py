"""Módulo de gestión de estilos y temas"""
# 1. Importar componentes principales del núcleo
from ui.themeengine.core.top_level import Toplevel
from ui.themeengine.core.window import Window
from ui.themeengine.core.style import Style
from ui.themeengine.utils.bootstyle import Bootstyle

# 2. Importar widgets básicos de ttk
from ui.themeengine.widgets import *

# 3. Importar componentes, estándar de tkinter
from tkinter import font
from tkinter import Variable, StringVar, IntVar, BooleanVar, DoubleVar
from tkinter import Canvas, Menu, Text, PhotoImage

# 4. Configurar el sistema de temas

Bootstyle.setup_ttktheming_api()

# 5. Importar widgets personalizados
from ui.themeengine.widgets.scrolled.scrolled_frame import ScrolledFrame
from ui.themeengine.widgets.scrolled.scrolled_text import ScrolledText
from ui.themeengine.dialogs.base import Dialog
from ui.themeengine.dialogs.message_dialog import MessageDialog