import unittest
from unittest.mock import Mock
from ui.styles.style_builder_tk import StyleBuilderTK
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.constants import STANDARD_THEMES


class TestStyleBuilderTK(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        # Mock del objeto Style
        self.style_mock = Mock()

        # Crear un tema real para las pruebas
        self.theme = ThemeDefinition(
            name='test_theme',
            colors=STANDARD_THEMES['light']['colors']
        )

        # Configurar el mock de Style para devolver el tema
        self.style_mock.theme = self.theme

        # Crear el builder
        self.builder = StyleBuilderTK(self.style_mock)

    def test_theme_property(self):
        """Prueba el acceso a la propiedad theme."""
        self.assertEqual(self.builder.theme, self.theme)

    def test_colors_property(self):
        """Prueba el acceso a la propiedad colors."""
        self.assertEqual(self.builder.colors, self.theme.colors)

    def test_update_window_style(self):
        """Prueba la actualización de estilo de ventana."""
        widget_mock = Mock()
        self.builder.update_window_style(widget_mock)
        widget_mock.configure.assert_called_with(
            background=self.theme.colors.bg
        )

    def test_update_button_style(self):
        """Prueba la actualización de estilo de botón."""
        widget_mock = Mock()
        self.builder.update_button_style(widget_mock)
        widget_mock.configure.assert_called_with(
            background=self.theme.colors.primary,
            foreground=self.theme.colors.selectfg,
            activebackground=self.theme.colors.active,
            activeforeground=self.theme.colors.selectfg,
            highlightbackground=self.theme.colors.border
        )

    def test_update_frame_style(self):
        """Prueba la actualización de estilo de frame."""
        widget_mock = Mock()
        self.builder.update_frame_style(widget_mock)
        widget_mock.configure.assert_called_with(
            background=self.theme.colors.bg,
            highlightbackground=self.theme.colors.border
        )

    def test_update_label_style(self):
        """Prueba la actualización de estilo de label."""
        widget_mock = Mock()
        self.builder.update_label_style(widget_mock)
        widget_mock.configure.assert_called_with(
            background=self.theme.colors.bg,
            foreground=self.theme.colors.fg
        )

    def test_update_entry_style(self):
        """Prueba la actualización de estilo de entry."""
        widget_mock = Mock()
        self.builder.update_entry_style(widget_mock)
        widget_mock.configure.assert_called_with(
            background=self.theme.colors.inputbg,
            foreground=self.theme.colors.inputfg,
            insertbackground=self.theme.colors.inputfg,
            selectbackground=self.theme.colors.selectbg,
            selectforeground=self.theme.colors.selectfg
        )


if __name__ == '__main__':
    unittest.main()