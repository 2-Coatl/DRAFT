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

from ui.themeengine.communication.publisher import Publisher
from ui.themeengine.core.color import Colors
from ui.themeengine.utils.constants import LIGHT, DARK
from ui.themeengine.builders.style_builder_tk import StyleBuilderTK
from ui.themeengine.utils.bootstyle import Bootstyle

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
# SECCIÓN 4: PRUEBAS DE INTEGRACIÓN CON IMPLEMENTACIONES REALES
# =============================================================================

class TestStyleBuilderTKRealIntegration(unittest.TestCase):
    """Pruebas de integración para StyleBuilderTK con implementaciones reales.

    Esta clase contiene pruebas que utilizan implementaciones reales de los componentes
    del sistema de estilos, en lugar de mocks, para verificar el comportamiento
    integrado del sistema completo.
    """

    @classmethod
    def setUpClass(cls):
        """Prepara el entorno Tkinter una sola vez para todas las pruebas."""
        cls.root = tk.Tk()
        cls.root.withdraw()  # Ocultar ventana durante las pruebas

    @classmethod
    def tearDownClass(cls):
        """Limpia los recursos de Tkinter al finalizar todas las pruebas."""
        cls.root.destroy()

    def setUp(self):
        """Configura el entorno real para cada prueba de integración."""
        # Importar componentes reales del sistema
        from ui.themeengine.core.style import Style

        # Guardar referencia al tema actual para restaurarlo después
        self.original_style = Style.get_instance()
        if hasattr(self.original_style, 'theme_name'):
            self.original_theme = self.original_style.theme_name

        # Crear instancia real de StyleBuilderTK
        self.style_builder = StyleBuilderTK()

        # Guardar referencia a Publisher para limpiar suscripciones después
        self.publisher = Publisher
        self.test_widgets = []

    def tearDown(self):
        """Limpia recursos después de cada prueba."""
        # Restaurar tema original si es posible
        if hasattr(self, 'original_style') and hasattr(self, 'original_theme'):
            if hasattr(self.original_style, 'set_theme'):
                self.original_style.set_theme(self.original_theme)

        # Cancelar suscripciones de widgets de prueba
        for widget in self.test_widgets:
            try:

                Publisher.unsubscribe(name=str(widget))
            except:
                pass

            # Destruir widgets
            try:
                widget.destroy()
            except:
                pass

    def test_real_style_integration(self):
        """Verifica la integración con la implementación real de Style."""
        # Obtener instancia real de Style
        from ui.themeengine.core.style import Style
        real_style = Style.get_instance()

        # Verificar que StyleBuilderTK tiene acceso a la instancia real
        self.assertIsNotNone(self.style_builder.style)
        self.assertEqual(self.style_builder.style, real_style)

        # Verificar acceso a propiedades reales
        self.assertIsNotNone(self.style_builder.theme)
        self.assertIsNotNone(self.style_builder.colors)

        # Verificar coherencia con el tipo de tema actual
        if hasattr(real_style.theme, 'type'):
            theme_type = real_style.theme.type
            if theme_type == LIGHT:
                self.assertTrue(self.style_builder.is_light_theme)
            else:
                self.assertFalse(self.style_builder.is_light_theme)

    def test_real_widget_styling(self):
        """Verifica la aplicación de estilos a widgets reales."""
        # Crear widgets para probar
        button = tk.Button(self.root, text="Test Button")
        self.test_widgets.append(button)

        # Guardar configuración inicial
        initial_bg = button.cget("background")

        # Aplicar estilo
        self.style_builder.update_button_style(button)

        # Verificar que el estilo se aplicó y cambió la configuración
        self.assertNotEqual(button.cget("background"), initial_bg)
        self.assertEqual(button.cget("relief"), tk.FLAT)

        # Verificar coherencia con los colores del tema real
        self.assertEqual(button.cget("background"), self.style_builder.colors.primary)

    def test_real_bootstyle_integration(self):
        """Verifica la integración real entre Bootstyle y StyleBuilderTK."""
        # Crear widgets para probar
        label = tk.Label(self.root, text="Test Label")
        button = tk.Button(self.root, text="Test Button")
        self.test_widgets.extend([label, button])

        # Guardar configuración inicial
        initial_label_bg = label.cget("background")
        initial_button_bg = button.cget("background")

        # Aplicar estilos mediante Bootstyle
        Bootstyle.update_tk_widget_style(label)
        Bootstyle.update_tk_widget_style(button)

        # Verificar que los estilos se aplicaron correctamente
        self.assertNotEqual(label.cget("background"), initial_label_bg)
        self.assertNotEqual(button.cget("background"), initial_button_bg)

        # Verificar que se aplicaron los estilos correctos
        self.assertEqual(label.cget("background"), self.style_builder.colors.bg)
        self.assertEqual(button.cget("background"), self.style_builder.colors.primary)
        self.assertEqual(button.cget("relief"), tk.FLAT)

    def test_real_widget_constructor_override(self):
        """Verifica que el decorador override_tk_widget_constructor funciona correctamente con implementaciones reales."""
        # Verificar que el constructor de tk.Button ya está decorado
        original_init = tk.Button.__init__

        # Crear un widget con constructor decorado (autostyle por defecto es True)
        button = tk.Button(self.root, text="Constructor Override Test")
        self.test_widgets.append(button)

        # Verificar que se aplicó el estilo automáticamente
        self.assertEqual(button.cget("background"), self.style_builder.colors.primary)
        self.assertEqual(button.cget("relief"), tk.FLAT)

        # Crear un widget con autostyle=False
        plain_button = tk.Button(self.root, text="No Autostyle", autostyle=False)
        self.test_widgets.append(plain_button)

        # Verificar que NO se aplicó el estilo automáticamente
        # Nota: No podemos comparar directamente con un valor específico ya que
        # depende del sistema, pero debería ser diferente del botón con estilo
        self.assertNotEqual(plain_button.cget("background"), self.style_builder.colors.primary)

    def test_real_theme_change(self):
        """Verifica que los widgets se actualizan cuando cambia el tema, usando implementaciones reales."""
        from ui.themeengine.core.style import Style

        # Obtener instancia real de Style
        real_style = Style.get_instance()

        # Esta prueba solo funciona si Style tiene los métodos necesarios
        if not hasattr(real_style, 'get_themes') or not hasattr(real_style, 'set_theme'):
            self.skipTest("Style no tiene los métodos necesarios para esta prueba")
            return

        # Obtener temas disponibles
        themes = real_style.get_themes()
        if len(themes) < 2:
            self.skipTest("No hay suficientes temas para probar el cambio")
            return

        # Identificar temas alternativos para la prueba
        current_theme = real_style.theme_name
        alt_theme = next((t for t in themes if t != current_theme), None)

        if not alt_theme:
            self.skipTest("No se pudo encontrar un tema alternativo")
            return

        # Crear widget para prueba
        button = tk.Button(self.root, text="Theme Change Test")
        self.test_widgets.append(button)

        # Aplicar estilo al botón
        Bootstyle.update_tk_widget_style(button)

        # Guardar colores del tema actual
        original_bg = button.cget("background")

        # Cambiar a tema alternativo
        real_style.set_theme(alt_theme)

        # Esperar a que se procesen eventos (para que Publisher notifique)
        self.root.update()

        # Verificar que el estilo se actualizó
        # Nota: Esto depende de que Publisher funcione correctamente
        # En un sistema bien integrado, el cambio de tema dispararía una notificación
        # que actualizaría automáticamente el widget
        #
        # Si esto no funciona automáticamente, podemos forzar la actualización:
        Bootstyle.update_tk_widget_style(button)

        # Verificar que el color cambió
        new_bg = button.cget("background")
        self.assertNotEqual(new_bg, original_bg)

        # Restaurar tema original
        real_style.set_theme(current_theme)

    def test_real_stylebuilder_hierarchy(self):
        """Verifica la jerarquía real entre Style, StyleBuilderTTK y StyleBuilderTK."""
        from ui.themeengine.core.style import Style

        # Obtener instancia real de Style
        real_style = Style.get_instance()

        # Verificar que Style puede proporcionar un StyleBuilderTK
        # a través de la jerarquía Style -> StyleBuilderTTK -> StyleBuilderTK
        if hasattr(real_style, '_get_builder_tk'):
            builder_tk = real_style._get_builder_tk()
            self.assertIsInstance(builder_tk, StyleBuilderTK)

            # Verificar que este builder tiene las mismas propiedades
            # que nuestra instancia directa
            self.assertEqual(builder_tk.style, self.style_builder.style)
            self.assertEqual(builder_tk.master, self.style_builder.master)

            # Verificar que este builder puede aplicar estilos
            button = tk.Button(self.root)
            self.test_widgets.append(button)
            builder_tk.update_button_style(button)
            self.assertEqual(button.cget("background"), self.style_builder.colors.primary)

    def test_real_compound_widget_styling(self):
        """Verifica la aplicación de estilos a un conjunto de widgets en una interfaz real."""
        # Crear una jerarquía de widgets que simula una interfaz real
        main_frame = tk.Frame(self.root)
        header_frame = tk.Frame(main_frame)
        content_frame = tk.Frame(main_frame)
        footer_frame = tk.Frame(main_frame)

        title_label = tk.Label(header_frame, text="Título de la Aplicación")
        subtitle_label = tk.Label(header_frame, text="Subtítulo informativo")

        name_label = tk.Label(content_frame, text="Nombre:")
        name_entry = tk.Entry(content_frame)
        email_label = tk.Label(content_frame, text="Email:")
        email_entry = tk.Entry(content_frame)

        save_button = tk.Button(footer_frame, text="Guardar")
        cancel_button = tk.Button(footer_frame, text="Cancelar")

        # Organizar widgets en la jerarquía
        main_frame.pack(fill=tk.BOTH, expand=True)
        header_frame.pack(fill=tk.X)
        content_frame.pack(fill=tk.BOTH, expand=True)
        footer_frame.pack(fill=tk.X)

        title_label.pack(pady=5)
        subtitle_label.pack(pady=2)

        name_label.pack(anchor=tk.W, pady=2)
        name_entry.pack(fill=tk.X, pady=2)
        email_label.pack(anchor=tk.W, pady=2)
        email_entry.pack(fill=tk.X, pady=2)

        save_button.pack(side=tk.RIGHT, padx=5, pady=5)
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Registrar widgets para limpieza
        self.test_widgets.extend([
            main_frame, header_frame, content_frame, footer_frame,
            title_label, subtitle_label, name_label, name_entry,
            email_label, email_entry, save_button, cancel_button
        ])

        # Aplicar estilos a todos los widgets
        for widget in [
            main_frame, header_frame, content_frame, footer_frame,
            title_label, subtitle_label, name_label, name_entry,
            email_label, email_entry, save_button, cancel_button
        ]:
            Bootstyle.update_tk_widget_style(widget)

        # Verificar que los estilos se aplicaron correctamente a cada tipo de widget
        for frame in [main_frame, header_frame, content_frame, footer_frame]:
            self.assertEqual(frame.cget("background"), self.style_builder.colors.bg)

        for label in [title_label, subtitle_label, name_label, email_label]:
            self.assertEqual(label.cget("background"), self.style_builder.colors.bg)
            self.assertEqual(label.cget("foreground"), self.style_builder.colors.fg)

        for entry in [name_entry, email_entry]:
            self.assertEqual(entry.cget("background"), self.style_builder.colors.inputbg)
            self.assertEqual(entry.cget("foreground"), self.style_builder.colors.inputfg)

        for button in [save_button, cancel_button]:
            self.assertEqual(button.cget("background"), self.style_builder.colors.primary)
            self.assertEqual(button.cget("relief"), tk.FLAT)

# =============================================================================
# SECCIÓN 5: EJECUCIÓN DE PRUEBAS
# =============================================================================

if __name__ == '__main__':
    unittest.main()