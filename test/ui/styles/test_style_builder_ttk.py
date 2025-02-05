import unittest
from unittest.mock import Mock, patch
from ui.styles.style_builder_ttk import StyleBuilderTTK
from ui.styles.colors import Colors
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.constants import Keywords


class TestStyleBuilderTTK(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        # Mock de Colors
        self.colors_mock = Mock(spec=Colors)
        self.colors_mock.get.side_effect = lambda x: {
            'primary': '#007bff',
            'selectfg': '#ffffff',
            'bg': '#ffffff',
            'fg': '#212529',
            'selectbg': '#0063ce'
        }.get(x)
        self.colors_mock.update_hsv.return_value = '#0056b3'

        # Mock de ThemeDefinition
        self.theme_mock = Mock(spec=ThemeDefinition)
        self.theme_mock.is_light = True

        # Instancia de StyleBuilderTTK
        self.builder = StyleBuilderTTK(self.colors_mock, self.theme_mock)
        self.builder.style = Mock()  # Mock del estilo ttk

    def test_name_to_method(self):
        """Prueba la obtención de métodos por nombre."""
        method = self.builder.name_to_method("create_button_style")
        self.assertIsNotNone(method)
        self.assertTrue(callable(method))

        method = self.builder.name_to_method("nonexistent_method")
        self.assertIsNone(method)

    def test_create_button_style(self):
        """Prueba la creación de estilo de botón."""
        self.builder.create_button_style("primary")

        self.builder.style.configure.assert_called_with(
            "TButton",
            foreground="#ffffff",
            background="#007bff",
            padding=(10, 5)
        )

        self.builder.style.map.assert_called()

    def test_create_outline_button_style(self):
        """Prueba la creación de estilo de botón con contorno."""
        self.builder.create_outline_button_style("primary")

        self.builder.style.configure.assert_called_with(
            "primary.Outline.TButton",
            foreground="#007bff",
            background="#ffffff",
            bordercolor="#007bff",
            padding=(10, 5)
        )

        self.builder.style.map.assert_called()

    def test_get_style_elements(self):
        """Prueba la extracción de elementos de un nombre de estilo."""
        test_cases = [
            (
                "primary.outline.horizontal.TButton",
                ("primary", "Outline", "Horizontal", "TButton")
            ),
            (
                "TButton",
                ("", "", "", "TButton")
            ),
            (
                "success.round.TButton",
                ("success", "Round", "", "TButton")
            ),
            (
                "info.link.TLabel",
                ("info", "Link", "", "TLabel")
            )
        ]

        for style_name, expected in test_cases:
            with self.subTest(style_name=style_name):
                result = self.builder._get_style_elements(style_name)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()