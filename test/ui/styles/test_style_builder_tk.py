import unittest
from unittest.mock import Mock
from ui.styles.style_builder_tk import StyleBuilderTK
from ui.styles.colors import Colors
from ui.styles.theme_definition import ThemeDefinition


class TestStyleBuilderTK(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        # Mock de Colors
        self.colors_mock = Mock(spec=Colors)
        self.colors_mock.get.side_effect = lambda x: {
            'primary': '#007bff',
            'selectfg': '#ffffff',
            'active': '#0056b3',
            'bg': '#ffffff',
            'fg': '#212529',
            'inputbg': '#ffffff',
            'inputfg': '#495057'
        }.get(x)

        # Mock de ThemeDefinition
        self.theme_mock = Mock(spec=ThemeDefinition)

        # Instancia de StyleBuilderTK
        self.builder = StyleBuilderTK(self.colors_mock, self.theme_mock)

    def test_update_button_style(self):
        """Prueba la actualización de estilo de botón."""
        button_mock = Mock()
        self.builder.update_button_style(button_mock)

        button_mock.configure.assert_called_once_with(
            bg='#007bff',
            fg='#ffffff',
            activebackground='#0056b3',
            activeforeground='#ffffff'
        )

    def test_update_label_style(self):
        """Prueba la actualización de estilo de label."""
        label_mock = Mock()
        self.builder.update_label_style(label_mock)

        label_mock.configure.assert_called_once_with(
            bg='#ffffff',
            fg='#212529'
        )

    def test_update_entry_style(self):
        """Prueba la actualización de estilo de entry."""
        entry_mock = Mock()
        self.builder.update_entry_style(entry_mock)

        entry_mock.configure.assert_called_once_with(
            bg='#ffffff',
            fg='#495057',
            insertbackground='#495057'
        )

    def test_update_frame_style(self):
        """Prueba la actualización de estilo de frame."""
        frame_mock = Mock()
        self.builder.update_frame_style(frame_mock)

        frame_mock.configure.assert_called_once_with(
            bg='#ffffff'
        )


if __name__ == '__main__':
    unittest.main()