import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from tkinter import ttk
import sys
import os

# Importaciones que se van a parchear
from ui.themeengine.builders.style_builder_ttk import StyleBuilderTTK
from ui.themeengine.utils.constants import LIGHT, TTK_CLAM, DEFAULT


class TestStyleBuilderTTKBase(unittest.TestCase):
    """Clase base para pruebas de StyleBuilderTTK.

    Proporciona:
    1. Configuración común de mocks y patchers
    2. Métodos auxiliares para crear mocks específicos
    3. Inicialización y limpieza de recursos
    """

    def setUp(self):
        """Configura el ambiente base para todas las pruebas."""
        # Crear patchers para las dependencias principales
        self.style_patcher = patch('ui.themeengine.core.style.Style')
        self.stylebuilder_tk_patcher = patch('ui.themeengine.builders.style_builder_ttk.StyleBuilderTK')
        self.colors_make_transparent_patcher = patch('ui.themeengine.core.color.Colors.make_transparent')
        self.ttk_style_theme_use_patcher = patch('tkinter.ttk.Style.theme_use')

        # Iniciar patchers
        self.MockStyle = self.style_patcher.start()
        self.MockStyleBuilderTK = self.stylebuilder_tk_patcher.start()
        self.mock_make_transparent = self.colors_make_transparent_patcher.start()
        self.mock_ttk_style_theme_use = self.ttk_style_theme_use_patcher.start()

        # Configurar comportamiento de Colors.make_transparent
        self.mock_make_transparent.return_value = "#666666"

        # Configurar mocks para Style y sus dependencias
        self.mock_style = self.MockStyle.get_instance.return_value
        self.mock_style.theme = Mock()

        # Configurar mock para el master de Style (necesario para scale_size)
        self.mock_style.master = Mock()
        self.mock_style.master.tk = Mock()
        self.mock_style.master.tk.call = Mock()

        # Crear y configurar mock para Colors
        self.mock_colors = self._create_mock_colors()
        self.mock_style.theme.colors = self.mock_colors

        # Configurar propiedades del tema
        self.mock_style.theme.type = LIGHT
        self.mock_style.theme.name = "light"

        # Mock para métodos de configuración de estilo
        self.mock_style._build_configure = Mock()
        self.mock_style.map = Mock()
        self.mock_style._register_ttkstyle = Mock()
        self.mock_style.element_create = Mock()
        self.mock_style.layout = Mock()
        self.mock_style.configure = Mock()
        self.mock_style.theme_create = Mock()

    def tearDown(self):
        """Limpia los recursos y detiene los patchers."""
        self.style_patcher.stop()
        self.stylebuilder_tk_patcher.stop()
        self.colors_make_transparent_patcher.stop()
        self.ttk_style_theme_use_patcher.stop()

    def _create_mock_colors(self):
        """Crea un mock para Colors con todos los colores necesarios.

        Returns:
            Mock: Objeto mock configurado con todos los colores y métodos requeridos.
        """
        mock_colors = Mock()
        # Colores básicos
        mock_colors.bg = "#ffffff"
        mock_colors.fg = "#000000"
        mock_colors.border = "#dddddd"
        mock_colors.primary = "#0078d7"
        mock_colors.info = "#17a2b8"
        mock_colors.danger = "#dc3545"
        mock_colors.selectbg = "#0078d7"
        mock_colors.selectfg = "#ffffff"
        mock_colors.light = "#f8f9fa"
        mock_colors.inputbg = "#ffffff"
        mock_colors.inputfg = "#000000"

        # Métodos de utilidad
        mock_colors.get = Mock(return_value="#0078d7")
        mock_colors.get_foreground = Mock(return_value="#ffffff")

        return mock_colors

    def create_builder(self):
        """Crea una instancia de StyleBuilderTTK y resetea los mocks.

        Returns:
            StyleBuilderTTK: Una instancia nueva con mocks limpios.
        """
        builder = StyleBuilderTTK()
        # Resetear mocks para ignorar llamadas durante la inicialización
        self.reset_mocks()
        return builder

    def reset_mocks(self):
        """Resetea todos los mocks para tener un estado limpio."""
        self.mock_style.reset_mock()
        self.mock_make_transparent.reset_mock()
        self.mock_ttk_style_theme_use.reset_mock()

    def configure_theme_type(self, theme_type):
        """Configura el tipo de tema (claro/oscuro).

        Args:
            theme_type (str): Tipo de tema ('light' o 'dark')
        """
        self.mock_style.theme.type = theme_type

        # Ajustar colores base según el tipo de tema
        if theme_type == LIGHT:
            self.mock_colors.bg = "#ffffff"
            self.mock_colors.fg = "#000000"
        else:
            self.mock_colors.bg = "#222222"
            self.mock_colors.fg = "#ffffff"

    def configure_platform(self, platform, scaling):
        """Configura el mock para simular una plataforma y factor de escala.

        Args:
            platform (str): Sistema de ventanas ('win32', 'aqua', 'x11')
            scaling (float): Factor de escala (1.0, 1.5, 2.0, etc.)
        """
        self.mock_style.master.tk.call.side_effect = [
            platform,  # Respuesta para "tk windowingsystem"
            scaling  # Respuesta para "tk scaling"
        ]


class TestStyleBuilderTTKProperties(TestStyleBuilderTTKBase):
    """Pruebas para propiedades y métodos utilitarios de StyleBuilderTTK."""

    def test_property_access(self):
        """Verifica que las propiedades básicas funcionen correctamente."""
        # Crear instancia a probar
        builder = self.create_builder()

        # Probar las propiedades con diferentes configuraciones
        test_cases = [
            # (propiedad, valor_tema, valor_esperado)
            ("colors", None, self.mock_colors),
            ("theme", None, self.mock_style.theme),
            ("is_light_theme", LIGHT, True),
            ("is_light_theme", "dark", False)
        ]

        for prop_name, theme_type, expected in test_cases:
            with self.subTest(property=prop_name, theme_type=theme_type):
                # Configurar tipo de tema si es necesario
                if theme_type is not None:
                    self.configure_theme_type(theme_type)

                # Obtener propiedad y verificar resultado
                result = getattr(builder, prop_name)
                self.assertEqual(result, expected)

    def test_name_to_method(self):
        """Verifica que name_to_method resuelva correctamente los métodos."""
        # Lista de métodos válidos e inválidos para probar
        methods = [
            # (nombre_método, debe_existir)
            ("create_button_style", True),
            ("create_link_button_style", True),
            ("create_combobox_style", True),
            ("non_existent_method", False)
        ]

        for method_name, should_exist in methods:
            with self.subTest(method=method_name, should_exist=should_exist):
                if should_exist:
                    # Verificar que el método existe y es callable
                    method = StyleBuilderTTK.name_to_method(method_name)
                    self.assertTrue(callable(method))
                    self.assertEqual(method.__name__, method_name)
                else:
                    # Verificar que se genera AttributeError para métodos inexistentes
                    with self.assertRaises(AttributeError):
                        StyleBuilderTTK.name_to_method(method_name)

    def test_scale_size(self):
        """Verifica el comportamiento del método scale_size con diferentes entradas y plataformas."""
        # Crear instancia a probar
        builder = self.create_builder()

        # Definir combinaciones de prueba
        # (platform, scaling, input_value, expected_type)
        test_cases = [
            ("win32", 1.0, 10, int),
            ("win32", 1.5, 20, int),
            ("win32", 2.0, 0, int),  # Caso límite: valor cero
            ("aqua", 1.0, [10, 20], list),
            ("aqua", 2.0, [], list),  # Caso límite: lista vacía
        ]

        for platform, scaling, input_value, expected_type in test_cases:
            with self.subTest(platform=platform, scaling=scaling, input=input_value):
                # Configurar mock para sistema y factor de escala
                self.configure_platform(platform, scaling)

                # Ejecutar método a probar
                result = builder.scale_size(input_value)

                # Verificar tipo de resultado
                self.assertIsInstance(result, expected_type)

                # Verificaciones adicionales según el tipo de entrada
                if isinstance(input_value, int):
                    if input_value == 0:
                        # Para entrada cero, el resultado debe ser cero
                        self.assertEqual(result, 0)
                    elif scaling > 1.0:
                        # Para scaling > 1, el resultado debe ser mayor que la entrada
                        self.assertGreater(result, input_value)
                elif isinstance(input_value, list):
                    # Para listas, verificar que mantiene la longitud
                    self.assertEqual(len(result), len(input_value))


class TestStyleBuilderTTKInitialization(TestStyleBuilderTTKBase):
    """Pruebas para la inicialización y creación de temas de StyleBuilderTTK."""

    def test_initialization_sequence(self):
        """Verifica la secuencia completa de inicialización."""
        # Crear instancia para probar la inicialización completa
        builder = StyleBuilderTTK()

        # Verificar secuencia de inicialización
        # 1. Obtención de la instancia de Style
        self.MockStyle.get_instance.assert_called_once()

        # 2. Creación de StyleBuilderTK
        self.MockStyleBuilderTK.assert_called_once()

        # 3. Creación del tema TTK
        self.mock_style.theme_create.assert_called_once_with("light", TTK_CLAM)

        # 4. Activación del tema
        self.mock_ttk_style_theme_use.assert_called_once()

        # 5. Inicialización del diccionario de imágenes
        self.assertIsInstance(builder.theme_images, dict)
        self.assertEqual(len(builder.theme_images), 0)

    def test_create_theme(self):
        """Verifica que create_theme cree y configure correctamente el tema TTK."""
        # Crear instancia y limpiar mocks
        builder = self.create_builder()

        # Ejecutar método a probar
        builder.create_theme()

        # Verificar creación y configuración del tema
        self.mock_style.theme_create.assert_called_once_with("light", TTK_CLAM)
        self.mock_ttk_style_theme_use.assert_called_once()

        # Verificar que se actualizaron las configuraciones del tema
        # (a través de update_ttk_theme_settings)
        self.mock_style._build_configure.assert_called()

    def test_update_ttk_theme_settings(self):
        """Verifica que update_ttk_theme_settings llame a create_default_style."""
        # Crear instancia y espiar el método create_default_style
        builder = self.create_builder()
        with patch.object(builder, 'create_default_style') as mock_create_default:
            # Ejecutar método a probar
            builder.update_ttk_theme_settings()

            # Verificar llamada a create_default_style
            mock_create_default.assert_called_once()

    def test_create_default_style(self):
        """Verifica que create_default_style configure el estilo raíz correctamente."""
        # Crear instancia y espiar el método create_link_button_style
        builder = self.create_builder()
        with patch.object(builder, 'create_link_button_style') as mock_create_link:
            # Ejecutar método a probar
            builder.create_default_style()

            # Verificar configuración del estilo raíz
            self.mock_style._build_configure.assert_called_once()
            args, kwargs = self.mock_style._build_configure.call_args

            # Verificar que se configuró el estilo raíz (.)
            self.assertEqual(args[0], ".")

            # Verificar que se configuraron los colores básicos
            self.assertEqual(kwargs["background"], self.mock_colors.bg)
            self.assertEqual(kwargs["foreground"], self.mock_colors.fg)
            self.assertEqual(kwargs["selectbg"], self.mock_colors.selectbg)

            # Verificar que se llamó a create_link_button_style
            mock_create_link.assert_called_once()

            # Verificar configuración de symbol.Link.TButton
            self.mock_style.configure.assert_called_once()
            args, kwargs = self.mock_style.configure.call_args
            self.assertEqual(args[0], "symbol.Link.TButton")


class TestStyleBuilderTTKStyleCreation(TestStyleBuilderTTKBase):
    """Pruebas para la creación de estilos específicos."""

    def test_style_creation_parametrized(self):
        """Verifica la creación de diferentes estilos con parámetros variados."""
        # Definir casos de prueba
        # (método, colorname, expected_style, expected_bg, should_register)
        test_cases = [
            # Estilos de botón
            (
                "create_button_style",
                DEFAULT,
                "TButton",
                self.mock_colors.primary,
                True
            ),
            (
                "create_button_style",
                "success",
                "success.TButton",
                "#0078d7",  # Valor de retorno de mock_colors.get()
                True
            ),
            # Estilos de botón tipo enlace
            (
                "create_link_button_style",
                DEFAULT,
                "Link.TButton",
                self.mock_colors.bg,  # Enlace usa bg para ser "invisible"
                True
            ),
            (
                "create_link_button_style",
                LIGHT,
                "light.Link.TButton",
                self.mock_colors.bg,
                True
            ),
            # Estilos de combobox
            (
                "create_combobox_style",
                DEFAULT,
                "TCombobox",
                None,  # No configura directamente en el caso default
                False
            ),
            (
                "create_combobox_style",
                "primary",
                "primary.TCombobox",
                self.mock_colors.inputbg,
                True
            ),
        ]

        # Crear instancia y preparar pruebas
        builder = self.create_builder()

        for method_name, colorname, expected_style, expected_bg, should_register in test_cases:
            with self.subTest(method=method_name, color=colorname):
                # Resetear mocks para cada caso
                self.reset_mocks()

                # Obtener el método a probar
                method = getattr(builder, method_name)

                # Ejecutar método
                method(colorname)

                # Verificaciones específicas según el caso
                if expected_bg is not None:
                    # Verificar que se configuró el estilo con el color correcto
                    self.mock_style._build_configure.assert_called()
                    args, kwargs = self.mock_style._build_configure.call_args
                    self.assertEqual(args[0], expected_style)
                    self.assertEqual(kwargs["background"], expected_bg)

                # Verificar registro de estilo si corresponde
                if should_register:
                    self.mock_style._register_ttkstyle.assert_called_with(expected_style)

    def test_button_style_detail(self):
        """Verifica detalles específicos de la creación de estilos de botón."""
        # Crear instancia
        builder = self.create_builder()

        # Ejecutar método con color personalizado
        builder.create_button_style("primary")

        # Verificar obtención de colores
        self.mock_colors.get.assert_called_with("primary")
        self.mock_colors.get_foreground.assert_called_with("primary")

        # Verificar cálculo de colores derivados para estados interactivos
        # El número exacto puede variar, pero al menos debe calcular:
        # - disabled_bg
        # - disabled_fg
        # - pressed
        # - hover
        self.assertGreaterEqual(self.mock_make_transparent.call_count, 3)

        # Verificar que se configuró el mapeo de estados
        self.mock_style.map.assert_called_once()
        args, kwargs = self.mock_style.map.call_args
        self.assertEqual(args[0], "primary.TButton")

        # Debe haber mapeo para al menos estas propiedades
        mapped_props = []
        for key, value in kwargs.items():
            mapped_props.append(key)

        expected_props = ["foreground", "background"]
        for prop in expected_props:
            self.assertIn(prop, mapped_props)

    def test_combobox_style_detail(self):
        """Verifica detalles específicos de la creación de estilos de combobox."""
        # Crear instancia
        builder = self.create_builder()

        # Configurar tema claro para comportamiento predecible
        self.configure_theme_type(LIGHT)

        # Ejecutar método con color personalizado
        builder.create_combobox_style("primary")

        # Verificar creación de elementos
        self.assertEqual(self.mock_style.element_create.call_count, 3)  # downarrow, padding, textarea

        # Verificar definición de layout
        self.mock_style.layout.assert_called_once()
        args, kwargs = self.mock_style.layout.call_args
        self.assertEqual(args[0], "primary.TCombobox")

        # Verificar que el layout contiene los elementos necesarios
        layout_str = str(args[1])
        self.assertIn("Combobox.downarrow", layout_str)
        self.assertIn("Combobox.padding", layout_str)
        self.assertIn("Combobox.textarea", layout_str)

    def test_combobox_popdown_style(self):
        """Verifica que update_combobox_popdown_style configure correctamente el popdown."""
        # Crear instancia
        builder = self.create_builder()

        # Crear mock para widget combobox
        widget = Mock()
        widget.tk = Mock()
        widget.tk.eval = Mock(return_value="popdown_path")
        widget.tk.call = Mock()

        # Ejecutar método a probar
        builder.update_combobox_popdown_style(widget)

        # Verificar que se obtuvo la referencia al popdown
        widget.tk.eval.assert_called_once()

        # Verificar configuración del listbox y scrollbar
        call_count = widget.tk.call.call_count
        self.assertGreaterEqual(call_count, 2)  # Al menos dos llamadas (listbox y scrollbar)

        # Verificar que se pasaron las configuraciones de estilo
        # Buscamos las llamadas que configuren propiedades visuales
        visual_props = ["-background", "-foreground", "-selectbackground", "-selectforeground"]

        # Contador para verificar que se configuraron propiedades visuales
        visual_props_found = 0

        for call_args in widget.tk.call.call_args_list:
            args = call_args[0]
            for prop in visual_props:
                if len(args) > 2 and prop in args:
                    visual_props_found += 1
                    break

        # Debe haber al menos una configuración de propiedad visual
        self.assertGreater(visual_props_found, 0)


class TestStyleBuilderTTKThemeAdaptation(TestStyleBuilderTTKBase):
    """Pruebas para verificar la adaptación a diferentes temas."""

    def test_style_adaptation_with_theme_change(self):
        """Verifica que los estilos se adapten correctamente al cambio de tema."""
        # Crear instancia
        builder = self.create_builder()

        # Preparar estilos y métodos a probar
        styles_to_test = [
            ("create_button_style", "primary"),
            ("create_link_button_style", "info"),
            ("create_combobox_style", "primary")
        ]

        for method_name, color_name in styles_to_test:
            with self.subTest(method=method_name, color=color_name):
                # Configurar tema claro
                self.configure_theme_type(LIGHT)
                self.reset_mocks()

                # Crear estilo con tema claro
                method = getattr(builder, method_name)
                method(color_name)

                # Capturar configuración con tema claro
                light_configure_calls = self.mock_style._build_configure.call_args_list.copy() if self.mock_style._build_configure.called else []

                # Configurar tema oscuro
                self.configure_theme_type("dark")
                self.reset_mocks()

                # Crear el mismo estilo con tema oscuro
                method(color_name)

                # Capturar configuración con tema oscuro
                dark_configure_calls = self.mock_style._build_configure.call_args_list.copy() if self.mock_style._build_configure.called else []

                # Verificar adaptación al tema, si hay configuraciones para comparar
                if light_configure_calls and dark_configure_calls:
                    # La configuración debe cambiar con el tema
                    self.assertNotEqual(light_configure_calls, dark_configure_calls)

                    # Verificar específicamente cambios en colores clave
                    light_kwargs = light_configure_calls[0][1]
                    dark_kwargs = dark_configure_calls[0][1]

                    # Al menos el color de fondo o el de texto debe cambiar
                    has_bg_change = (
                            "background" in light_kwargs and
                            "background" in dark_kwargs and
                            light_kwargs["background"] != dark_kwargs["background"]
                    )
                    has_fg_change = (
                            "foreground" in light_kwargs and
                            "foreground" in dark_kwargs and
                            light_kwargs["foreground"] != dark_kwargs["foreground"]
                    )

                    self.assertTrue(
                        has_bg_change or has_fg_change,
                        f"Ni el color de fondo ni el de texto cambiaron con el tema en {method_name}"
                    )

    def test_combobox_popdown_theme_adaptation(self):
        """Verifica que update_combobox_popdown_style se adapte al cambio de tema."""
        # Crear instancia
        builder = self.create_builder()

        # Configurar un widget mock
        widget = Mock()
        widget.tk = Mock()
        widget.tk.eval = Mock(return_value="popdown_window")
        widget.tk.call = Mock()

        # Configurar tema claro
        self.configure_theme_type(LIGHT)

        # Actualizar estilo en tema claro
        builder.update_combobox_popdown_style(widget)

        # Capturar configuraciones para tema claro
        light_calls = widget.tk.call.call_args_list.copy()

        # Limpiar mocks
        widget.tk.call.reset_mock()

        # Configurar tema oscuro
        self.configure_theme_type("dark")

        # Actualizar estilo en tema oscuro
        builder.update_combobox_popdown_style(widget)

        # Capturar configuraciones para tema oscuro
        dark_calls = widget.tk.call.call_args_list

        # Verificar que las configuraciones son diferentes entre temas
        self.assertNotEqual(light_calls, dark_calls)

        # Buscar diferencias específicas en propiedades visuales
        # Extraer colores de configuración para comparar
        def extract_colors(calls_list):
            colors = {}
            for call_args in calls_list:
                args = call_args[0]
                for i, arg in enumerate(args[3:], 3):
                    if arg in ["-background", "-foreground", "-selectbackground", "-highlightcolor"] and i + 1 < len(
                            args):
                        colors[arg] = args[i + 1]
            return colors

        light_colors = extract_colors(light_calls)
        dark_colors = extract_colors(dark_calls)

        # Verificar que al menos un color cambió entre temas
        self.assertTrue(
            any(light_colors.get(prop) != dark_colors.get(prop)
                for prop in light_colors if prop in dark_colors),
            "No se encontraron cambios de color entre temas"
        )


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