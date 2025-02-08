import unittest
from unittest.mock import Mock, patch
from tkinter import TclError
from ui.styles.style import Style
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.colors import Colors
from ui.styles.events import Publisher, Channel


class TestStyle(unittest.TestCase):
    def setUp(self):
        """Preparación antes de cada test."""
        # Limpiar el singleton para cada test
        Style.instance = None
        self.style = Style()

    def tearDown(self):
        """Limpieza después de cada test."""
        Style.instance = None
        Publisher.clear_subscribers()

    def test_singleton_pattern(self):
        """Verifica el patrón Singleton."""
        style1 = Style()
        style2 = Style()
        self.assertIs(style1, style2)

        # Verificar que mantiene el tema al crear nueva instancia
        style1.theme_use('dark')
        style3 = Style()
        self.assertEqual(style3.theme.name, 'dark')

    def test_theme_initialization(self):
        """Verifica la inicialización de temas."""
        # Verificar tema por defecto
        self.assertEqual(self.style.theme.name, Style.DEFAULT_THEME)

        # Verificar carga de temas estándar
        theme_names = self.style.theme_names()
        self.assertIn('light', theme_names)
        self.assertIn('dark', theme_names)

    def test_theme_switching(self):
        """Verifica el cambio de temas."""
        # Cambio a tema válido
        result = self.style.theme_use('dark')
        self.assertEqual(result, 'dark')
        self.assertEqual(self.style.theme.name, 'dark')

        # Intento de cambio a tema inválido
        with self.assertRaises(TclError):
            self.style.theme_use('nonexistent_theme')

    def test_style_registration(self):
        """Verifica el registro de estilos."""
        test_style = 'Test.TButton'
        self.style._register_ttkstyle(test_style)

        self.assertIn(test_style, self.style._style_registry)
        self.assertIn(
            test_style,
            self.style._theme_styles[self.style.theme.name]
        )

    def test_style_existence_check(self):
        """Verifica la comprobación de existencia de estilos."""
        test_style = 'Test.TButton'

        # Estilo no registrado
        self.assertFalse(self.style.style_exists_in_theme(test_style))

        # Registrar estilo
        self.style._register_ttkstyle(test_style)
        self.assertTrue(self.style.style_exists_in_theme(test_style))

    @patch('ui.styles.style.Publisher')
    def test_theme_change_notifications(self, mock_publisher):
        """Verifica las notificaciones de cambio de tema."""
        self.style.theme_use('dark')
        mock_publisher.publish_message.assert_called_with(Channel.STD)

    def test_color_access(self):
        """Verifica el acceso a colores del tema."""
        # Tema light
        self.style.theme_use('light')
        colors = self.style.colors
        self.assertIsInstance(colors, Colors)
        self.assertEqual(colors.primary, '#007bff')  # Valor del tema light

        # Tema dark
        self.style.theme_use('dark')
        colors = self.style.colors
        self.assertEqual(colors.primary, '#375a7f')  # Valor del tema dark

    def test_style_builder_access(self):
        """Verifica el acceso a los builders."""
        # Verificar acceso a builder válido
        builder = self.style._get_builder()
        self.assertIsNotNone(builder)

        # Verificar error con tema inválido
        Style.instance = None
        style = Style()
        style.theme = None
        with self.assertRaises(TclError):
            style._get_builder()

    def test_configure_style(self):
        """Verifica la configuración de estilos."""
        test_style = 'Test.TButton'
        test_config = {'background': 'blue'}

        # Configurar nuevo estilo
        self.style.configure(test_style, **test_config)

        # Verificar registro
        self.assertTrue(self.style.style_exists_in_theme(test_style))

        # Verificar configuración
        result = self.style.configure(test_style, 'background')
        self.assertEqual(result, 'blue')


if __name__ == '__main__':
    unittest.main()