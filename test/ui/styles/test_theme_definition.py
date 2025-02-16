import unittest
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.constants import STANDARD_THEMES, LIGHT, DARK


class TestThemeDefinition(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        self.light_colors = STANDARD_THEMES['light']['colors']
        self.dark_colors = STANDARD_THEMES['dark']['colors']

    def test_light_theme(self):
        """Prueba la creación de un tema claro."""
        theme = ThemeDefinition(
            name='light_theme',
            colors=self.light_colors
        )  # themetype por defecto es LIGHT

        self.assertEqual(theme.name, 'light_theme')
        self.assertEqual(theme.type, LIGHT)
        self.assertEqual(theme.colors.primary, '#007bff')

    def test_dark_theme(self):
        """Prueba la creación de un tema oscuro."""
        theme = ThemeDefinition(
            name='dark_theme',
            colors=self.dark_colors,
            themetype=DARK
        )

        self.assertEqual(theme.name, 'dark_theme')
        self.assertEqual(theme.type, DARK)
        self.assertEqual(theme.colors.primary, '#375a7f')

    def test_repr(self):
        """Prueba la representación string del tema."""
        theme = ThemeDefinition(
            name='test_theme',
            colors=self.light_colors
        )

        repr_str = repr(theme)
        self.assertIn("name=test_theme", repr_str)
        self.assertIn("type=light", repr_str)
        self.assertIn("colors=", repr_str)


if __name__ == '__main__':
    unittest.main()