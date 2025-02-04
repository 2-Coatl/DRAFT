from tkinter import ttk
from typing import Dict, Type, Optional
from .themes import ThemeBase
from .themes.sandstone import SandstoneTheme
from .themes.superhero import SuperheroTheme
from .events import Channel, Publisher


class ThemeManager:
    _instance = None
    _current_theme: Optional[ThemeBase] = None
    _available_themes: Dict[str, Type[ThemeBase]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa el gestor de temas"""
        # Registrar temas disponibles
        self.register_theme(SandstoneTheme)
        self.register_theme(SuperheroTheme)

        # Establecer tema por defecto
        self._current_theme = SuperheroTheme

    def register_theme(self, theme_class: Type[ThemeBase]) -> None:
        """Registra un nuevo tema"""
        self._available_themes[theme_class.name] = theme_class

    def get_available_themes(self) -> Dict[str, str]:
        """Retorna un diccionario de temas disponibles con su tipo"""
        return {name: theme.type for name, theme in self._available_themes.items()}

    def set_theme(self, theme_name: str) -> None:
        """Cambia al tema especificado y notifica a los observadores"""
        if theme_name not in self._available_themes:
            raise ValueError(f"Tema '{theme_name}' no encontrado")

        self._current_theme = self._available_themes[theme_name]
        self._apply_theme()

        # Notificar cambio de tema
        Publisher.publish_message(Channel.TTK, theme_name)
        Publisher.publish_message(Channel.STD, theme_name)

    def _apply_theme(self) -> None:
        """Aplica el tema actual a todos los widgets"""
        style = ttk.Style()
        theme = self._current_theme

        # Configuración general
        style.configure('.',
                       background=theme.colors['bg'],
                       foreground=theme.colors['fg'],
                       fieldbackground=theme.colors['inputbg'],
                       font=theme.fonts['default']
                       )


        # Configuración general
        style.configure('.',
                        background=theme.colors['bg'],
                        foreground=theme.colors['fg'],
                        fieldbackground=theme.colors['inputbg'],
                        font=theme.fonts['default']
                        )

        # Botones
        style.configure('TButton',
                        background=theme.colors['primary'],
                        foreground=theme.colors['fg'],
                        padding=theme.widgets['button']['padding']
                        )

        # Entradas
        style.configure('TEntry',
                        fieldbackground=theme.colors['inputbg'],
                        foreground=theme.colors['inputfg'],
                        padding=theme.widgets['entry']['padding']
                        )

        # Frames
        style.configure('TFrame',
                        background=theme.colors['bg']
                        )

        # Labels
        style.configure('TLabel',
                        background=theme.colors['bg'],
                        foreground=theme.colors['fg']
                        )

        # Treeview
        style.configure('Treeview',
                        background=theme.colors['bg'],
                        foreground=theme.colors['fg'],
                        fieldbackground=theme.colors['bg'],
                        rowheight=theme.widgets['treeview']['row_height']
                        )

        style.configure('Treeview.Heading',
                        background=theme.colors['secondary'],
                        foreground=theme.colors['fg']
                        )

        # Mapeos para estados de widgets
        style.map('TButton',
                  background=[('active', theme.colors['active'])],
                  foreground=[('active', theme.colors['fg'])]
                  )

        style.map('Treeview',
                  background=[('selected', theme.colors['selectbg'])],
                  foreground=[('selected', theme.colors['selectfg'])]
                  )

    @property
    def current_theme(self) -> ThemeBase:
        """Retorna el tema actual"""
        return self._current_theme

    def get_color(self, color_name: str) -> str:
        """Obtiene un color del tema actual"""
        return self._current_theme.colors.get(color_name)

    def get_font(self, font_type: str) -> tuple:
        """Obtiene una configuración de fuente del tema actual"""
        return self._current_theme.fonts.get(font_type)

    def get_spacing(self, size: str) -> int:
        """Obtiene un valor de espaciado del tema actual"""
        return self._current_theme.spacing.get(size)

    def get_widget_config(self, widget_type: str) -> dict:
        """Obtiene la configuración de un widget específico"""
        return self._current_theme.widgets.get(widget_type, {})