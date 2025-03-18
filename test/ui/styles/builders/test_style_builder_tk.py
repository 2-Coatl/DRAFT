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

from ui.themeengine.communication.channel import Channel
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
        self.mock_style.colors = self.mock_colors
        self.mock_style.master = self.root

        # Configurar colores para pruebas
        self._setup_mock_colors()

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
        self.mock_colors.bg = "#FFFFFF"
        self.mock_colors.fg = "#000000"
        self.mock_colors.primary = "#0078D7"
        self.mock_colors.selectbg = "#CCE8FF"
        self.mock_colors.selectfg = "#000000"
        self.mock_colors.inputbg = "#F0F0F0"
        self.mock_colors.inputfg = "#000000"
        self.mock_colors.border = "#D0D0D0"

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
        """Verifica la configuración correcta de menús.

        Prueba:
        - Estilización adecuada de menús
        - Configuración de tearoff y colores
        """
        # ARRANGE: Crear menú
        menu = tk.Menu(self.root)

        # ACT: Aplicar estilo
        self.style_builder.update_menu_style(menu)

        # ASSERT: Verificar configuraciones clave
        self.assertEqual(menu.cget("background"), self.mock_colors.bg)
        self.assertEqual(menu.cget("foreground"), self.mock_colors.fg)
        self.assertEqual(menu.cget("activebackground"), self.mock_colors.selectbg)
        self.assertEqual(menu.cget("activeforeground"), self.mock_colors.selectfg)
        self.assertEqual(menu.cget("tearoff"), 0)  # tearoff desactivado



# =============================================================================
# SECCIÓN 4: PRUEBAS DE INTEGRACIÓN Y CASOS LÍMITE
# =============================================================================

class TestStyleBuilderTKIntegration(unittest.TestCase):
    """Pruebas de integración para StyleBuilderTK.

    Esta clase contiene pruebas para verificar:
    1. Integración con Style y StyleBuilderTTK
    2. Interacción con Bootstyle
    3. Comportamiento del sistema Publisher/Subscriber
    4. Comportamiento durante cambios de tema
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
        """Configura el entorno para cada prueba de integración."""
        # Patchear módulos y clases necesarias para pruebas de integración
        self.style_patcher = patch('ui.themeengine.core.style.Style')
        self.publisher_patcher = patch('ui.themeengine.utils.publisher.Publisher')
        self.builder_ttk_patcher = patch('ui.themeengine.builders.style_builder_ttk.StyleBuilderTTK')

        # Iniciar patchers y obtener los mocks
        self.mock_style = self.style_patcher.start()
        self.mock_publisher = self.publisher_patcher.start()
        self.mock_builder_ttk = self.builder_ttk_patcher.start()

        # Configurar mock de Style para que devuelva una instancia específica
        self.mock_style_instance = MagicMock()
        self.mock_style.get_instance.return_value = self.mock_style_instance

        # Configurar propiedades de la instancia Style
        self.mock_theme = MagicMock()
        self.mock_colors = MagicMock()
        self.mock_style_instance.theme = self.mock_theme
        self.mock_style_instance.colors = self.mock_colors
        self.mock_style_instance.master = self.root

        # Configurar colores para pruebas
        self.mock_colors.bg = "#FFFFFF"
        self.mock_colors.fg = "#000000"
        self.mock_colors.primary = "#0078D7"
        self.mock_colors.selectbg = "#CCE8FF"
        self.mock_colors.selectfg = "#000000"
        self.mock_colors.inputbg = "#F0F0F0"
        self.mock_colors.inputfg = "#000000"
        self.mock_colors.border = "#D0D0D0"

        # Configurar tema (claro por defecto)
        self.mock_theme.type = LIGHT

        # Crear instancia de StyleBuilderTK para pruebas
        self.style_builder = StyleBuilderTK()

    def tearDown(self):
        """Limpia recursos después de cada prueba."""
        self.style_patcher.stop()
        self.publisher_patcher.stop()
        self.builder_ttk_patcher.stop()

    def test_integration_with_style(self):
        """Verifica la integración entre StyleBuilderTK y Style."""
        # Verificar que StyleBuilderTK obtiene la instancia de Style
        self.mock_style.get_instance.assert_called_once()

        # Verificar que las referencias se establecen correctamente
        self.assertEqual(self.style_builder.style, self.mock_style_instance)
        self.assertEqual(self.style_builder.master, self.root)

        # Verificar acceso a propiedades de Style
        self.assertEqual(self.style_builder.theme, self.mock_theme)
        self.assertEqual(self.style_builder.colors, self.mock_colors)
        self.assertTrue(self.style_builder.is_light_theme)

    def test_integration_with_style_builder_ttk(self):
        """Verifica la integración entre StyleBuilderTTK y StyleBuilderTK."""
        # Crear una instancia mock de StyleBuilderTTK
        mock_builder_ttk_instance = MagicMock()

        # Asignar nuestra instancia de StyleBuilderTK al mock
        mock_builder_ttk_instance.style_builder_tk = self.style_builder

        # Verificar que StyleBuilderTTK puede acceder a los métodos de StyleBuilderTK
        button = tk.Button(self.root)
        mock_builder_ttk_instance.style_builder_tk.update_button_style(button)

        # Verificar que el estilo se aplicó
        self.assertEqual(button.cget("background"), self.mock_colors.primary)
        button.destroy()

    def test_bootstyle_integration(self):
        """Verifica la integración entre Bootstyle y StyleBuilderTK."""
        # Configurar el mock de Style para devolver nuestro StyleBuilderTK
        self.mock_style_instance._get_builder_tk.return_value = self.style_builder

        # Crear widget para prueba
        button = tk.Button(self.root)

        # Llamar al método de Bootstyle que debería usar StyleBuilderTK
        with patch('ui.themeengine.core.style.Style.get_instance', return_value=self.mock_style_instance):
            with patch('ui.themeengine.utils.bootstyle.StyleBuilderTK', spec=StyleBuilderTK) as mock_builder_class:
                # Configurar el mock para que getattr devuelva nuestro método
                mock_builder_class.update_Button_style = self.style_builder.update_button_style

                # Llamar al método de Bootstyle
                Bootstyle.update_tk_widget_style(button)

        # Verificar que el estilo se aplicó
        self.assertEqual(button.cget("background"), self.mock_colors.primary)
        button.destroy()

    def test_widget_constructor_override(self):
        """Verifica que el decorador override_tk_widget_constructor funciona correctamente."""

        # Crear una clase de widget de prueba con constructor decorado
        class TestWidget(tk.Frame):
            @Bootstyle.override_tk_widget_constructor
            def __init__(self, master=None, **kwargs):
                super().__init__(master, **kwargs)

        # Patchear Bootstyle.update_tk_widget_style
        with patch('ui.themeengine.utils.bootstyle.Bootstyle.update_tk_widget_style') as mock_update:
            # Patchear Publisher.subscribe
            with patch('ui.themeengine.utils.publisher.Publisher.subscribe') as mock_subscribe:
                # Crear instancia del widget
                widget = TestWidget(self.root)

                # Verificar que se llamó a update_tk_widget_style
                mock_update.assert_called_once_with(widget)

                # Verificar que se registró en Publisher
                mock_subscribe.assert_called_once()
                # Verificar los argumentos de la llamada a subscribe
                args, kwargs = mock_subscribe.call_args
                self.assertEqual(kwargs['name'], str(widget))
                self.assertEqual(kwargs['channel'], Channel.STD)

        # Limpiar
        widget.destroy()

    def test_theme_change_notification(self):
        """Verifica que los widgets se actualizan cuando cambia el tema."""
        # Crear un widget para prueba
        button = tk.Button(self.root)

        # Simular registro en Publisher
        with patch('ui.themeengine.utils.publisher.Publisher.subscribe') as mock_subscribe:
            # Aplicar constructor decorado manualmente
            Bootstyle.override_tk_widget_constructor(tk.Button.__init__)(button, self.root)

            # Verificar que se registró en Publisher
            mock_subscribe.assert_called_once()

            # Obtener el callback registrado
            args, kwargs = mock_subscribe.call_args
            callback = kwargs['callback']

            # Verificar que el callback actualiza el estilo
            with patch('ui.themeengine.utils.bootstyle.Bootstyle.update_tk_widget_style') as mock_update:
                # Ejecutar el callback como lo haría Publisher
                callback()

                # Verificar que se llamó a update_tk_widget_style
                mock_update.assert_called_once_with(button)

        # Limpiar
        button.destroy()

    def test_complete_style_flow(self):
        """Verifica el flujo completo del sistema de estilos."""
        # Simular el flujo completo:
        # 1. Crear Style
        # 2. Style crea StyleBuilderTTK
        # 3. StyleBuilderTTK crea StyleBuilderTK
        # 4. Crear widget con constructor decorado
        # 5. Cambiar tema
        # 6. Verificar que el widget se actualiza

        # 1-3. Crear mocks para todo el sistema
        mock_style = MagicMock()
        mock_builder_ttk = MagicMock()
        mock_builder_tk = MagicMock()

        # Configurar la cadena de dependencias
        mock_style.get_instance.return_value = mock_style
        mock_style._get_builder_ttk.return_value = mock_builder_tk
        mock_builder_ttk.style_builder_tk = mock_builder_tk

        # 4. Crear widget y simular constructor decorado
        button = tk.Button(self.root)

        # Registrar callback en Publisher
        callback = lambda: Bootstyle.update_tk_widget_style(button)
        self.mock_publisher.subscribe.return_value = None

        # Simular registro con Publisher
        with patch('ui.themeengine.utils.bootstyle.Bootstyle.update_tk_widget_style') as mock_update:
            # Aplicar estilo inicial
            mock_update(button)
            mock_update.assert_called_once_with(button)

            # 5. Simular cambio de tema
            with patch('ui.themeengine.core.style.Style.get_instance', return_value=mock_style):
                # Simular notificación de Publisher
                callback()

                # 6. Verificar que se llamó a update_tk_widget_style nuevamente
                self.assertEqual(mock_update.call_count, 2)

        # Limpiar
        button.destroy()

    def test_real_widget_chain(self):
        """Verifica que una cadena de widgets recibe estilos coherentemente."""
        # Crear una jerarquía de widgets
        frame = tk.Frame(self.root)
        inner_frame = tk.Frame(frame)
        button = tk.Button(inner_frame, text="Test Button")
        label = tk.Label(inner_frame, text="Test Label")
        entry = tk.Entry(inner_frame)

        # Aplicar estilos
        self.style_builder.update_frame_style(frame)
        self.style_builder.update_frame_style(inner_frame)
        self.style_builder.update_button_style(button)
        self.style_builder.update_label_style(label)
        self.style_builder.update_entry_style(entry)

        # Verificar coherencia de estilos en la jerarquía
        self.assertEqual(frame.cget("background"), self.mock_colors.bg)
        self.assertEqual(inner_frame.cget("background"), self.mock_colors.bg)
        self.assertEqual(button.cget("background"), self.mock_colors.primary)
        self.assertEqual(label.cget("background"), self.mock_colors.bg)
        self.assertEqual(entry.cget("background"), self.mock_colors.inputbg)

        # Verificar otros atributos específicos por tipo de widget
        self.assertEqual(button.cget("relief"), tk.FLAT)
        self.assertEqual(entry.cget("highlightbackground"), self.mock_colors.border)

        # Cambiar tipo de tema a oscuro
        self.mock_theme.type = DARK

        # Volver a aplicar estilos (como ocurriría en un cambio de tema)
        self.style_builder.update_frame_style(frame)
        self.style_builder.update_frame_style(inner_frame)
        self.style_builder.update_button_style(button)
        self.style_builder.update_label_style(label)
        self.style_builder.update_entry_style(entry)

        # Verificar que los estilos reflejan el tema oscuro
        # En tema oscuro, highlightbackground de Entry cambia a selectbg
        self.assertEqual(entry.cget("highlightbackground"), self.mock_colors.selectbg)

        # Limpiar
        frame.destroy()

# =============================================================================
# SECCIÓN 5: EJECUCIÓN DE PRUEBAS
# =============================================================================

if __name__ == '__main__':
    unittest.main()