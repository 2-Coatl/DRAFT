import unittest
from tkinter import TclError
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.style import Style
from ui.styles.color import Colors
from ui.styles.constants import STANDARD_THEMES, DEFAULT_THEME


class TestStyle(unittest.TestCase):
    """Test suite para la clase Style."""

    def setUp(self):
        """Inicializa el ambiente de prueba."""
        Style.instance = None
        self.style = Style(DEFAULT_THEME)

    def tearDown(self):
        """Limpia después de cada test."""
        Style.instance = None

    def test_singleton_pattern(self):
        """Verifica que Style implementa correctamente el patrón Singleton."""
        style1 = Style()
        style2 = Style()
        self.assertIs(style1, style2)
        self.assertIs(style1, Style.get_instance())

    def test_default_theme(self):
        """Verifica que se establece el tema por defecto."""
        self.assertEqual(self.style.theme.name, DEFAULT_THEME)

    def test_theme_registration(self):
        """Verifica el registro correcto de temas."""
        test_theme = ThemeDefinition(
            name="test_theme",
            colors=STANDARD_THEMES[DEFAULT_THEME]['colors'],
            themetype=STANDARD_THEMES[DEFAULT_THEME]['type']
        )
        self.style.register_theme(test_theme)

        self.assertIn("test_theme", self.style.theme_names())
        self.assertIn("test_theme", self.style._theme_names)
        self.assertEqual(
            self.style._theme_definitions["test_theme"],
            test_theme
        )

    def test_theme_switching(self):
        """Verifica el cambio entre temas."""
        # Usando los temas reales
        self.style.theme_use('cosmo')
        self.assertEqual(self.style.theme.name, 'cosmo')

        self.style.theme_use('flatly')
        self.assertEqual(self.style.theme.name, 'flatly')

    def test_invalid_theme(self):
        """Verifica el manejo de temas inválidos."""
        with self.assertRaises(TclError):
            self.style.theme_use('non_existent_theme')

    def test_colors_property(self):
        """Verifica que colors devuelve los colores del tema actual."""
        self.style.theme_use(DEFAULT_THEME)
        colors = self.style.colors
        self.assertIsInstance(colors, Colors)
        self.assertEqual(
            colors,
            self.style._theme_definitions[DEFAULT_THEME].colors
        )

    def test_theme_objects_initialization(self):
        """Verifica la inicialización del estado básico de los temas."""
        self.assertIn(DEFAULT_THEME, self.style._theme_objects)
        self.assertIsNone(self.style._theme_objects[DEFAULT_THEME])

    def test_standard_themes_loaded(self):
        """Verifica que los temas estándar se cargan correctamente."""
        for theme_name in STANDARD_THEMES:
            self.assertIn(theme_name, self.style.theme_names())

    def test_get_instance_creates_instance(self):
        """Verifica que get_instance crea una instancia si no existe."""
        Style.instance = None
        instance = Style.get_instance()
        self.assertIsInstance(instance, Style)
        self.assertIs(instance, Style.instance)

if __name__ == '__main__':
    unittest.main()