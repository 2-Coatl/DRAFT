import unittest
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.themes.sandstone import SandstoneTheme
from ui.styles.themes.superhero import SuperheroTheme
from ui.styles.colors import Colors


class TestThemeDefinition(unittest.TestCase):

    def test_abstract_theme(self):
        """Prueba que ThemeDefinition no puede ser instanciada directamente."""
        with self.assertRaises(TypeError):
            ThemeDefinition("test", True)

    def test_light_theme_creation(self):
        """Prueba la creación del tema claro."""
        theme = SandstoneTheme()
        self.assertEqual(theme.name, "light")
        self.assertTrue(theme.is_light)
        self.assertIsNone(theme._colors)  # No se han cargado los colores aún

    def test_dark_theme_creation(self):
        """Prueba la creación del tema oscuro."""
        theme = SuperheroTheme()
        self.assertEqual(theme.name, "dark")
        self.assertFalse(theme.is_light)
        self.assertIsNone(theme._colors)  # No se han cargado los colores aún

    def test_get_colors(self):
        """Prueba la obtención de colores del tema."""
        theme = SandstoneTheme()
        colors = theme.get_colors()

        # Verifica que es una instancia de Colors
        self.assertIsInstance(colors, Colors)

        # Verifica que los colores son correctos
        self.assertEqual(colors.primary, '#007bff')
        self.assertEqual(colors.bg, '#ffffff')

        # Verifica que los colores se cachean
        self.assertIs(colors, theme.get_colors())

    def test_custom_theme(self):
        """Prueba la creación de un tema personalizado."""

        class CustomTheme(ThemeDefinition):
            def __init__(self):
                super().__init__("custom", is_light=True)

            def _get_theme_colors(self):
                return {
                    'primary': '#ff0000',
                    'secondary': '#00ff00',
                    'success': '#0000ff',
                    'info': '#17a2b8',
                    'warning': '#ffc107',
                    'danger': '#dc3545',
                    'light': '#f8f9fa',
                    'dark': '#343a40',
                    'bg': '#ffffff',
                    'fg': '#212529',
                    'selectbg': '#0063ce',
                    'selectfg': '#ffffff',
                    'border': '#dee2e6',
                    'inputfg': '#495057',
                    'inputbg': '#ffffff',
                    'active': '#0056b3'
                }

        theme = CustomTheme()
        colors = theme.get_colors()
        self.assertEqual(colors.primary, '#ff0000')
        self.assertEqual(colors.secondary, '#00ff00')

    def test_invalid_custom_theme(self):
        """Prueba que un tema con colores faltantes falla."""

        class InvalidTheme(ThemeDefinition):
            def __init__(self):
                super().__init__("invalid", is_light=True)

            def _get_theme_colors(self):
                return {
                    'primary': '#ff0000'  # Faltan colores requeridos
                }

        theme = InvalidTheme()
        with self.assertRaises(ValueError):
            theme.get_colors()

    def test_theme_string_representation(self):
        """Prueba la representación string de los temas."""
        light_theme = SandstoneTheme()
        dark_theme = SuperheroTheme()

        self.assertEqual(str(light_theme), "light (light theme)")
        self.assertEqual(str(dark_theme), "dark (dark theme)")

    def test_color_modifications(self):
        """Prueba modificaciones de colores en un tema."""
        theme = SandstoneTheme()
        colors = theme.get_colors()

        # Modifica un color y verifica que el cambio persiste
        original_primary = colors.primary
        lighter_primary = Colors.update_hsv(original_primary, vd=0.1)
        colors.set('primary', lighter_primary)

        self.assertEqual(colors.get('primary'), lighter_primary)
        self.assertNotEqual(colors.get('primary'), original_primary)

    def test_theme_color_consistency(self):
        """Prueba la consistencia de colores entre instancias del mismo tema."""
        theme1 = SandstoneTheme()
        theme2 = SandstoneTheme()

        colors1 = theme1.get_colors()
        colors2 = theme2.get_colors()

        # Verifica que los colores son iguales pero son instancias diferentes
        self.assertEqual(colors1.primary, colors2.primary)
        self.assertIsNot(colors1, colors2)


if __name__ == '__main__':
    unittest.main()