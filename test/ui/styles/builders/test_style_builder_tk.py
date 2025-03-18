# =============================================================================
# SECCIÓN 0: IMPORTACIONES Y CONFIGURACIÓN INICIAL
# =============================================================================
# Este archivo contiene pruebas unitarias y de integración para StyleBuilderTK
# organizadas en una estructura jerárquica de clases para maximizar la
# reutilización de código y mantener las pruebas bien estructuradas.
# =============================================================================

import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch

from ui.themeengine.core.color import Colors
from ui.themeengine.utils.constants import LIGHT, DARK
from ui.themeengine.builders.style_builder_tk import StyleBuilderTK


# =============================================================================
# SECCIÓN 1: CLASE BASE DE PRUEBAS - FIXTURES Y CONFIGURACIÓN COMÚN
# =============================================================================

class StyleBuilderTKTestBase(unittest.TestCase):
    """Clase base para pruebas del motor de estilos de widgets Tkinter nativos.

    Esta clase base proporciona:
    1. Inicialización y limpieza del entorno Tkinter
    2. Configuración de mocks para componentes dependientes
    3. Métodos auxiliares para crear widgets de prueba
    4. Patching centralizado de dependencias externas
    """

    @classmethod
    def setUpClass(cls):
        """Prepara el entorno Tkinter una sola vez para todas las pruebas.

        Configura:
        - Una ventana root que servirá para todas las pruebas
        - Oculta la ventana para evitar interrupciones visuales
        """
        cls.root = tk.Tk()
        cls.root.withdraw()  # Ocultar ventana durante las pruebas

    @classmethod
    def tearDownClass(cls):
        """Limpia los recursos de Tkinter al finalizar todas las pruebas."""
        cls.root.destroy()

    def setUp(self):
        """Configura el entorno para cada prueba individual.

        Prepara:
        - Mocks para componentes dependientes (Style, ThemeDefinition, Colors)
        - Configuración de colores y temas para pruebas
        - Patching de Style.get_instance()
        - Instancia fresca de StyleBuilderTK para cada prueba
        """

        # Crear mocks para Style, ThemeDefinition y Colors
        self.mock_colors = MagicMock()
        self.mock_theme = MagicMock()
        self.mock_style = MagicMock()

        # Configurar propiedades de los mocks
        self.mock_style.theme = self.mock_theme
        self.mock_style.master = self.root

        # Configurar colores para pruebas
        self._setup_mock_colors()

        # Asignar el objeto Colors real al mock_style
        self.mock_style.colors = self.mock_colors  # <-- Asignar después de configurar los colores

        # Configurar tema (claro por defecto)
        self.mock_theme.type = LIGHT

        # Patch para Style.get_instance()
        self.style_patcher = patch('ui.themeengine.core.style.Style.get_instance',
                                   return_value=self.mock_style)
        self.mock_get_instance = self.style_patcher.start()

        # Crear instancia de StyleBuilderTK para pruebas
        self.style_builder = StyleBuilderTK()

    def tearDown(self):
        """Limpia recursos después de cada prueba."""
        self.style_patcher.stop()

    def _setup_mock_colors(self):
        """Configura colores de prueba en el mock de Colors."""
        # Crear una instancia real de Colors en lugar de un MagicMock
        self.mock_colors = Colors(
            primary="#0078D7",
            secondary="#6c757d",
            success="#28a745",
            info="#17a2b8",
            warning="#ffc107",
            danger="#dc3545",
            light="#f8f9fa",
            dark="#343a40",
            bg="#FFFFFF",
            fg="#000000",
            selectbg="#CCE8FF",
            selectfg="#000000",
            border="#D0D0D0",
            inputfg="#000000",
            inputbg="#F0F0F0",
            active="#D4D4D4"
        )

    def create_widget(self, widget_class, **kwargs):
        """Crea una instancia de widget para pruebas.

        Args:
            widget_class: Clase Tkinter a instanciar
            **kwargs: Argumentos adicionales para el constructor

        Returns:
            Una instancia del widget solicitado
        """
        if widget_class == tk.Tk:
            # Para Tk usamos el root ya creado
            return self.root
        return widget_class(self.root, **kwargs)

    def set_theme_type(self, theme_type):
        """Cambia el tipo de tema para pruebas.

        Args:
            theme_type: Tipo de tema (LIGHT o DARK)
        """
        self.mock_theme.type = theme_type


# =============================================================================
# SECCIÓN 2: PRUEBAS DE FUNCIONALIDAD BÁSICA DE STYLEBUILDER
# =============================================================================

class TestStyleBuilderTKFunctionality(StyleBuilderTKTestBase):
    """Pruebas de funcionalidad para StyleBuilderTK.

    Esta clase contiene pruebas para verificar:
    1. Inicialización correcta y acceso a propiedades
    2. Aplicación de estilos a widgets fundamentales
    3. Comportamiento diferenciado según tipo de tema
    4. Integración apropiada con el sistema de temas y colores
    """

    def test_initialization(self):
        """Verifica que StyleBuilderTK se inicialice correctamente.

        Prueba:
        - La obtención correcta de la instancia singleton de Style
        - El establecimiento correcto de referencias internas
        """
        # Verificar que StyleBuilderTK obtiene la instancia de Style
        self.mock_get_instance.assert_called_once()

        # Verificar que las referencias se establecen correctamente
        self.assertEqual(self.style_builder.style, self.mock_style)
        self.assertEqual(self.style_builder.master, self.root)

    def test_properties(self):
        """Verifica que las propiedades theme, colors e is_light_theme funcionen correctamente.

        Prueba:
        - Acceso correcto a theme y colors
        - Determinación correcta del tipo de tema
        """
        # Verificar propiedades
        self.assertEqual(self.style_builder.theme, self.mock_theme)
        self.assertEqual(self.style_builder.colors, self.mock_colors)
        self.assertTrue(self.style_builder.is_light_theme)

        # Cambiar tipo de tema a oscuro y verificar
        self.set_theme_type(DARK)
        self.assertFalse(self.style_builder.is_light_theme)

    def test_fundamental_widgets(self):
        """Verifica la actualización de estilos para widgets fundamentales.

        Prueba:
        - Configuración correcta de ventana principal (Tk)
        - Configuración correcta de contenedores (Frame)
        - Configuración correcta de elementos de texto (Label)
        """
        # Definir widgets fundamentales a probar
        widget_types = [
            (tk.Tk, 'update_tk_style', 'bg'),
            (tk.Frame, 'update_frame_style', 'bg'),
            (tk.Label, 'update_label_style', 'bg')
        ]

        for widget_class, method_name, color_attr in widget_types:
            with self.subTest(f"Probando {method_name}"):
                # ARRANGE: Crear instancia del widget
                widget = self.create_widget(widget_class)

                # Configurar el widget con un valor inicial diferente
                widget.configure(background="#000000")

                # ACT: Aplicar estilo
                getattr(self.style_builder, method_name)(widget)

                # ASSERT: Verificar que se aplicó el color correcto
                expected_color = getattr(self.mock_colors, color_attr)
                self.assertEqual(widget.cget("background"), expected_color)

                # Limpiar widget si no es root
                if widget_class != tk.Tk:
                    widget.destroy()


# =============================================================================
# SECCIÓN 3: PRUEBAS ESPECÍFICAS PARA DIFERENTES TIPOS DE WIDGETS
# =============================================================================

class TestStyleBuilderTKWidgetSpecific(StyleBuilderTKTestBase):
    """Pruebas específicas para diferentes tipos de widgets.

    Esta clase contiene pruebas para verificar:
    1. Comportamiento con widgets interactivos
    2. Adaptación según tipo de tema
    3. Configuraciones especiales para widgets complejos
    """

    def test_interactive_widgets(self):
        """Verifica la actualización de estilos para widgets interactivos.

        Prueba:
        - Configuración correcta de botones
        - Configuración correcta de campos de entrada
        - Aplicación de estilos planos modernos
        """
        # Definir widgets interactivos a probar
        widget_types = [
            (tk.Button, 'update_button_style', 'primary'),
            (tk.Entry, 'update_entry_style', 'inputbg')
        ]

        for widget_class, method_name, bg_color_attr in widget_types:
            with self.subTest(f"Probando {method_name}"):
                # ARRANGE: Crear instancia del widget
                widget = self.create_widget(widget_class)

                # ACT: Aplicar estilo
                getattr(self.style_builder, method_name)(widget)

                # ASSERT: Verificar que se aplicó el color correcto
                expected_color = getattr(self.mock_colors, bg_color_attr)
                self.assertEqual(widget.cget("background"), expected_color)

                # Verificar estilo plano
                self.assertEqual(widget.cget("relief"), tk.FLAT)

                # Limpiar widget
                widget.destroy()

    def test_theme_dependent_styling(self):
        """Verifica que los estilos se adapten según el tipo de tema (claro/oscuro).

        Prueba:
        - Adaptación correcta de bordes y colores según tipo de tema
        - Widgets que tienen comportamiento específico por tipo de tema
        """
        # Configurar widgets que varían según tipo de tema
        widgets_to_test = [
            (tk.Entry, 'update_entry_style'),
            (tk.Spinbox, 'update_spinbox_style')
        ]

        # Probar con tema claro
        self.set_theme_type(LIGHT)
        for widget_class, method_name in widgets_to_test:
            with self.subTest(f"Tema claro - {method_name}"):
                # ARRANGE
                widget = self.create_widget(widget_class)

                # ACT
                getattr(self.style_builder, method_name)(widget)

                # ASSERT: En tema claro, el borde debe ser el color border estándar
                self.assertEqual(widget.cget("highlightbackground"), self.mock_colors.border)
                widget.destroy()

        # Probar con tema oscuro
        self.set_theme_type(DARK)
        for widget_class, method_name in widgets_to_test:
            with self.subTest(f"Tema oscuro - {method_name}"):
                # ARRANGE
                widget = self.create_widget(widget_class)

                # ACT
                getattr(self.style_builder, method_name)(widget)

                # ASSERT: En tema oscuro, el borde debe ser el color selectbg
                self.assertEqual(widget.cget("highlightbackground"), self.mock_colors.selectbg)
                widget.destroy()

    def test_menu_styling(self):
        """Verifica la configuración correcta de menús."""
        # ARRANGE: Crear menú
        menu = tk.Menu(self.root)

        # ACT: Aplicar estilo
        self.style_builder.update_menu_style(menu)

        # ASSERT: Verificar configuraciones clave
        # Convertir los valores obtenidos a string para comparar
        self.assertEqual(str(menu.cget("background")), str(self.mock_colors.bg))
        self.assertEqual(str(menu.cget("foreground")), str(self.mock_colors.fg))
        self.assertEqual(str(menu.cget("activebackground")), str(self.mock_colors.selectbg))
        self.assertEqual(str(menu.cget("activeforeground")), str(self.mock_colors.selectfg))

# =============================================================================
# SECCIÓN 4: EJECUCIÓN DE PRUEBAS
# =============================================================================

if __name__ == '__main__':
    unittest.main()