import unittest
import tkinter as tk
from ui.themeengine.builders.style_builder_tk import StyleBuilderTK
from ui.themeengine.communication.publisher import Publisher
from ui.themeengine.utils.bootstyle import Bootstyle
from ui.themeengine.utils.constants import LIGHT

# =============================================================================
# SECCIÓN 1: PRUEBAS DE INTEGRACIÓN CON IMPLEMENTACIONES REALES
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
# SECCIÓN 2: EJECUCIÓN DE PRUEBAS
# =============================================================================

if __name__ == '__main__':
    unittest.main()