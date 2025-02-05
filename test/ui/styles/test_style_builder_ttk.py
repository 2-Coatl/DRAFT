import unittest
from unittest.mock import Mock, patch
from tkinter import ttk
from ui.styles.style_builder_ttk import StyleBuilderTTK
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.constants import STANDARD_THEMES


class TestStyleBuilderTTK(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        # Mock del objeto Style
        self.style_mock = Mock()

        # Crear un tema real para las pruebas
        self.theme = ThemeDefinition(
            name='test_theme',
            colors=STANDARD_THEMES['light']['colors']
        )

        # Configurar el mock de Style
        self.style_mock.theme = self.theme

        # Crear el builder
        self.builder = StyleBuilderTTK(self.style_mock)

    def test_theme_property(self):
        """Prueba el acceso a la propiedad theme."""
        self.assertEqual(self.builder.theme, self.theme)

    def test_colors_property(self):
        """Prueba el acceso a la propiedad colors."""
        self.assertEqual(self.builder.colors, self.theme.colors)

    def test_name_to_method(self):
        """Prueba la obtención de métodos por nombre."""
        # Método existente
        method = self.builder.name_to_method("create_button_style")
        self.assertIsNotNone(method)
        self.assertTrue(callable(method))

        # Método inexistente
        method = self.builder.name_to_method("nonexistent_method")
        self.assertIsNone(method)

        # Nombre vacío
        method = self.builder.name_to_method("")
        self.assertIsNone(method)

    def test_create_button_style(self):
        """Prueba la creación de estilo de botón."""
        # Sin color específico
        self.builder.create_button_style()
        self.style_mock.configure.assert_called_with(
            "TButton",
            foreground=self.theme.colors.selectfg,
            background=self.theme.colors.primary,
            padding=(10, 5)
        )

        # Con color específico
        self.builder.create_button_style("success")
        self.style_mock.configure.assert_called_with(
            "TButton",
            foreground=self.theme.colors.selectfg,
            background=self.theme.colors.success,
            padding=(10, 5)
        )

    def test_create_outline_button_style(self):
        """Prueba la creación de estilo de botón con contorno."""
        # Sin color específico
        self.builder.create_outline_button_style()
        self.style_mock.configure.assert_called_with(
            "Outline.TButton",
            foreground=self.theme.colors.primary,
            background=self.theme.colors.bg,
            bordercolor=self.theme.colors.primary,
            padding=(10, 5)
        )

        # Con color específico
        self.builder.create_outline_button_style("success")
        self.style_mock.configure.assert_called_with(
            "success.Outline.TButton",
            foreground=self.theme.colors.success,
            background=self.theme.colors.bg,
            bordercolor=self.theme.colors.success,
            padding=(10, 5)
        )

    def test_update_combobox_popdown_style(self):
        """Prueba la actualización del popdown de Combobox."""
        # Mock del Combobox y su popdown
        combobox_mock = Mock(spec=ttk.Combobox)
        popdown_mock = Mock()
        combobox_mock.winfo_children.return_value = [popdown_mock]

        self.builder.update_combobox_popdown_style(combobox_mock)

        popdown_mock.configure.assert_called_with(
            background=self.theme.colors.bg,
            foreground=self.theme.colors.fg,
            selectbackground=self.theme.colors.selectbg,
            selectforeground=self.theme.colors.selectfg
        )

        # Prueba manejo de errores
        combobox_mock.winfo_children.return_value = []
        self.builder.update_combobox_popdown_style(combobox_mock)  # No debería lanzar error


if __name__ == '__main__':
    unittest.main()