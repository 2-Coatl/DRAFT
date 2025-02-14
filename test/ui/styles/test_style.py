import pytest
from tkinter import TclError
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.style import Style
from ui.styles.color import Colors
from ui.styles.constants import STANDARD_THEMES, DEFAULT_THEME
from ui.styles.notifications.publisher import Publisher
from ui.styles.notifications.channel import Channel

class TestStyle:
    """Pruebas para la clase Style."""

    @pytest.fixture(autouse=True)
    def setup_style(self):
        """Fixture que se ejecuta automáticamente antes de cada prueba."""
        Style.instance = None
        self.style = Style(DEFAULT_THEME)
        yield
        Style.instance = None

    def test_singleton_pattern(self):
        """Verifica que Style implementa correctamente el patrón Singleton."""
        style1 = Style()
        style2 = Style()
        assert style1 is style2
        assert style1 is Style.get_instance()

    def test_default_theme(self):
        """Verifica que se establece el tema por defecto."""
        assert self.style.theme.name == DEFAULT_THEME

    def test_theme_registration(self):
        """Verifica el registro correcto de temas."""
        test_theme = ThemeDefinition(
            name="test_theme",
            colors=STANDARD_THEMES[DEFAULT_THEME]['colors'],
            themetype=STANDARD_THEMES[DEFAULT_THEME]['type']
        )
        self.style.register_theme(test_theme)

        assert "test_theme" in self.style.theme_names()
        assert "test_theme" in self.style._theme_names
        assert self.style._theme_definitions["test_theme"] == test_theme

    def test_theme_switching(self):
        """Verifica el cambio entre temas."""
        self.style.theme_use('cosmo')
        assert self.style.theme.name == 'cosmo'

        self.style.theme_use('flatly')
        assert self.style.theme.name == 'flatly'

    def test_invalid_theme(self):
        """Verifica el manejo de temas inválidos."""
        with pytest.raises(TclError):
            self.style.theme_use('non_existent_theme')

    def test_colors_property(self):
        """Verifica que colors devuelve los colores del tema actual."""
        self.style.theme_use(DEFAULT_THEME)
        colors = self.style.colors
        assert isinstance(colors, Colors)
        assert colors == self.style._theme_definitions[DEFAULT_THEME].colors

    def test_theme_objects_initialization(self):
        """Verifica la inicialización del estado básico de los temas."""
        assert DEFAULT_THEME in self.style._theme_objects
        assert self.style._theme_objects[DEFAULT_THEME] is None

    @pytest.mark.parametrize("theme_name", STANDARD_THEMES.keys())
    def test_standard_themes_loaded(self, theme_name):
        """Verifica que los temas estándar se cargan correctamente."""
        assert theme_name in self.style.theme_names()

    def test_get_instance_creates_instance(self):
        """Verifica que get_instance crea una instancia si no existe."""
        Style.instance = None
        instance = Style.get_instance()
        assert isinstance(instance, Style)
        assert instance is Style.instance


    @pytest.fixture(autouse=True)
    def setup_style(self):
        """Fixture que se ejecuta automáticamente antes de cada prueba."""
        Style.instance = None
        self.style = Style(DEFAULT_THEME)
        Publisher.clear_subscribers()  # Limpiamos suscriptores antes de cada prueba
        yield
        Style.instance = None
        Publisher.clear_subscribers()  # Limpiamos suscriptores después de cada prueba

    def test_theme_change_notifications(self):
        """Verifica que se envían las notificaciones al cambiar de tema."""
        # Almacenamos los mensajes recibidos
        ttk_messages = []
        std_messages = []

        # Registramos callbacks para ambos canales
        Publisher.subscribe(
            "ttk_test",
            lambda theme: ttk_messages.append(theme),
            Channel.TTK
        )
        Publisher.subscribe(
            "std_test",
            lambda theme: std_messages.append(theme),
            Channel.STD
        )

        # Cambiamos el tema
        new_theme = 'flatly'
        self.style.theme_use(new_theme)

        # Verificamos que ambos canales recibieron la notificación
        assert ttk_messages == [new_theme]
        assert std_messages == [new_theme]

    def test_theme_change_multiple_subscribers(self):
        """Verifica que múltiples suscriptores reciben las notificaciones."""
        ttk_count = 0
        std_count = 0

        # Registramos múltiples callbacks
        def ttk_callback(theme):
            nonlocal ttk_count
            ttk_count += 1

        def std_callback(theme):
            nonlocal std_count
            std_count += 1

        # Suscribimos múltiples widgets
        for i in range(3):
            Publisher.subscribe(f"ttk_test_{i}", ttk_callback, Channel.TTK)
            Publisher.subscribe(f"std_test_{i}", std_callback, Channel.STD)

        # Cambiamos el tema
        self.style.theme_use('flatly')

        # Verificamos que todos los suscriptores recibieron la notificación
        assert ttk_count == 3
        assert std_count == 3