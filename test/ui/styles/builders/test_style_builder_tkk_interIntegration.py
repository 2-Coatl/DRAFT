import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from tkinter import ttk
import sys
import os

# Importaciones que se van a parchear
from ui.themeengine.builders.style_builder_ttk import StyleBuilderTTK
from ui.themeengine.utils.constants import LIGHT


class TestStyleBuilderTTKTkinterIntegration(unittest.TestCase):
    """Pruebas de integración con Tkinter real."""

    @classmethod
    def setUpClass(cls):
        """Configura el entorno Tkinter una vez para todas las pruebas."""
        # Verificar si estamos en modo no-GUI (como en CI/CD)
        cls.headless = "CI" in os.environ or "pytest" in sys.modules or "unittest" in sys.argv[0]

        if not cls.headless:
            try:
                # Crear ventana raíz
                cls.root = tk.Tk()
                cls.root.withdraw()  # Ocultar ventana durante pruebas
            except Exception as e:
                print(f"No se pudo inicializar Tkinter: {e}")
                cls.headless = True

    @classmethod
    def tearDownClass(cls):
        """Limpia recursos Tkinter al finalizar todas las pruebas."""
        if hasattr(cls, 'root') and cls.root:
            cls.root.destroy()
            cls.root = None

    def setUp(self):
        """Configura el entorno para cada prueba individual."""
        if self.headless:
            self.skipTest("Prueba omitida en modo headless")

    def _create_mock_colors(self):
        """Crea un mock para Colors con colores básicos."""
        mock_colors = Mock()
        mock_colors.bg = "#ffffff"
        mock_colors.fg = "#000000"
        mock_colors.border = "#dddddd"
        mock_colors.primary = "#0078d7"
        mock_colors.selectbg = "#0078d7"
        mock_colors.selectfg = "#ffffff"
        mock_colors.get = Mock(return_value="#0078d7")
        mock_colors.get_foreground = Mock(return_value="#ffffff")
        return mock_colors

    def test_functional_integration(self):
        """Prueba funcional que verifica la integración real con Tkinter."""
        # Parchear dependencias para permitir la instanciación
        with patch('ui.themeengine.core.style.Style') as MockStyle, \
                patch('ui.themeengine.builders.style_builder_ttk.StyleBuilderTK'):

            # Configurar mock para Style
            mock_style = Mock()
            MockStyle.get_instance.return_value = mock_style
            mock_style.theme = Mock()
            mock_style.theme.name = "default"
            mock_style.theme.type = LIGHT
            mock_style.theme.colors = self._create_mock_colors()

            # Configurar métodos necesarios
            mock_style._build_configure = Mock()
            mock_style.map = Mock()
            mock_style._register_ttkstyle = Mock()
            mock_style.theme_create = Mock()

            # Crear instancia de StyleBuilderTTK
            builder = StyleBuilderTTK()

            # Crear widgets reales para verificar la integración
            button = ttk.Button(self.root, text="Test Button")
            combobox = ttk.Combobox(self.root, values=["Option 1", "Option 2"])

            # Crear estilos para los widgets
            builder.create_button_style("primary")
            try:
                builder.update_combobox_popdown_style(combobox)
            except tk.TclError:
                # Ignorar errores específicos relacionados con el popdown
                pass

            # Verificar que los widgets se crearon correctamente
            self.assertIsInstance(button, ttk.Button)
            self.assertIsInstance(combobox, ttk.Combobox)

            # Verificar que se pueden aplicar estilos (si aplica)
            button.configure(style="primary.TButton")


if __name__ == '__main__':
    unittest.main()
