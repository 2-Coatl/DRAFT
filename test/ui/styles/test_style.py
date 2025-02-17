# DRAFT/tests/ui/styles/test_style.py

import pytest
from tkinter import TclError
from ui.styles.theme_definition import ThemeDefinition
from ui.styles.core.style import Style
from ui.styles.color import Colors
from ui.styles.constants import STANDARD_THEMES, DEFAULT_THEME
from ui.styles.notifications.publisher import Publisher
from ui.styles.notifications.channel import Channel

class TestStyle:
    """Pruebas para la clase Style.

    Verifica:
    1. Implementación del patrón Singleton
    2. Gestión de temas
    3. Notificaciones de cambios
    4. Registro de estilos
    """

    @pytest.fixture(autouse=True)
    def setup_style(self):
        """Fixture que prepara el entorno para las pruebas.

        Se ejecuta automáticamente antes y después de cada prueba,
        limpiando el estado del Singleton y los suscriptores.
        """
        Style.instance = None
        self.style = Style(DEFAULT_THEME)
        Publisher.clear_subscribers()
        yield
        Style.instance = None
        Publisher.clear_subscribers()


    def test_singleton_pattern(self):
        """Verifica que Style implementa correctamente el patrón Singleton.

        Prueba:
        1. Que múltiples instancias sean la misma
        2. Que get_instance retorne la misma instancia
        3. Que la instancia se mantenga única
        """
        style1 = Style()
        style2 = Style()
        assert style1 is style2, "Las instancias style1 y style2 deberían ser la misma"
        assert style1 is Style.get_instance(), "get_instance debería retornar la misma instancia"
        assert Style.instance is style1, "La instancia almacenada debería ser la misma"


    def test_default_theme(self):
        """Verifica que se establece correctamente el tema por defecto.

        Prueba:
        1. Que el tema inicial sea el tema por defecto
        2. Que el tema tenga la configuración correcta
        """
        assert self.style.theme.name == DEFAULT_THEME, "El tema inicial debería ser el tema por defecto"
        assert self.style.theme in self.style._theme_definitions.values(), "El tema debería estar en las definiciones"
        assert isinstance(self.style.theme, ThemeDefinition), "El tema debería ser una instancia de ThemeDefinition"


    def test_get_instance_creates_instance(self):
        """Verifica el comportamiento de get_instance.

        Prueba:
        1. Que get_instance cree una instancia si no existe
        2. Que la instancia creada sea válida
        3. Que se almacene correctamente como instancia única
        """
        Style.instance = None
        instance = Style.get_instance()
        assert isinstance(instance, Style), "get_instance debería retornar una instancia de Style"
        assert instance is Style.instance, "La instancia debería almacenarse en Style.instance"


def test_theme_registration(self):
    """Verifica el registro correcto de temas.

    Prueba:
    1. Registro de un nuevo tema
    2. Almacenamiento en las colecciones correspondientes
    3. Accesibilidad del tema registrado
    """
    test_theme = ThemeDefinition(
        name="test_theme",
        colors=STANDARD_THEMES[DEFAULT_THEME]['colors'],
        themetype=STANDARD_THEMES[DEFAULT_THEME]['type']
    )
    self.style.register_theme(test_theme)

    # Verificar que el tema se registró correctamente
    assert "test_theme" in self.style._theme_names
    assert "test_theme" in self.style._theme_definitions
    assert self.style._theme_definitions["test_theme"] is test_theme
    assert "test_theme" in self.style.theme_names()

    def test_theme_switching(self):
        """Verifica el cambio entre temas.

        Prueba:
        1. Cambio a temas existentes
        2. Actualización correcta del tema actual
        3. Mantenimiento del estado del tema
        """
        # Cambio al tema 'cosmo'
        self.style.theme_use('cosmo')
        assert self.style.theme.name == 'cosmo'
        assert isinstance(self.style.theme, ThemeDefinition)

        # Cambio al tema 'flatly'
        self.style.theme_use('flatly')
        assert self.style.theme.name == 'flatly'
        assert isinstance(self.style.theme, ThemeDefinition)


    def test_invalid_theme(self):
        """Verifica el manejo de temas inválidos.

        Prueba:
        1. Que se lance una excepción al usar un tema inexistente
        2. Que el mensaje de error sea descriptivo
        """
        invalid_theme = 'non_existent_theme'
        with pytest.raises(TclError) as exc_info:
            self.style.theme_use(invalid_theme)
        assert str(invalid_theme) in str(exc_info.value)
        assert "no es un tema válido" in str(exc_info.value)


    @pytest.mark.parametrize("theme_name", STANDARD_THEMES.keys())
    def test_standard_themes_loaded(self, theme_name):
        """Verifica que los temas estándar se cargan correctamente.

        Prueba:
        1. Que cada tema estándar esté disponible
        2. Que se pueda acceder a cada tema
        3. Que los temas tengan la estructura correcta

        Args:
            theme_name: Nombre del tema a verificar (proporcionado por parametrize)
        """
        assert theme_name in self.style.theme_names()
        assert theme_name in self.style._theme_definitions
        theme_def = self.style._theme_definitions[theme_name]
        assert isinstance(theme_def, ThemeDefinition)

    def test_colors_property(self):
        """Verifica el comportamiento de la propiedad colors.

        Prueba:
        1. Obtención de colores del tema actual
        2. Consistencia de colores al cambiar de tema
        3. Manejo de caso cuando no hay tema
        """
        # Verificar colores con tema por defecto
        self.style.theme_use(DEFAULT_THEME)
        colors = self.style.colors
        assert isinstance(colors, Colors)
        assert colors == self.style._theme_definitions[DEFAULT_THEME].colors

        # Verificar que los colores cambian con el tema
        self.style.theme_use('flatly')
        new_colors = self.style.colors
        assert new_colors == self.style._theme_definitions['flatly'].colors
        assert new_colors != colors

    def test_theme_change_notifications(self):
        """Verifica el sistema de notificaciones al cambiar de tema.

        Prueba:
        1. Notificaciones en ambos canales (TTK y STD)
        2. Contenido correcto de las notificaciones
        3. Orden de las notificaciones
        """
        # Almacenar mensajes recibidos
        ttk_messages = []
        std_messages = []

        # Registrar callbacks para ambos canales
        Publisher.subscribe(
            "ttk_test",
            lambda theme: ttk_messages.append(theme),
            Channel.TTK
        )
        Publisher.subscribe(
            "std_test",
            lambda theme: std_messages.append(theme),
            Channel.STD
        )

        # Cambiar tema y verificar notificaciones
        new_theme = 'flatly'
        self.style.theme_use(new_theme)

        assert ttk_messages == [new_theme], "Canal TTK debería recibir la notificación"
        assert std_messages == [new_theme], "Canal STD debería recibir la notificación"

    def test_theme_change_multiple_subscribers(self):
        """Verifica notificaciones con múltiples suscriptores.

        Prueba:
        1. Múltiples suscriptores por canal
        2. Que todos los suscriptores reciban la notificación
        3. Orden y consistencia de las notificaciones
        """
        ttk_count = 0
        std_count = 0

        def ttk_callback(theme):
            nonlocal ttk_count
            ttk_count += 1

        def std_callback(theme):
            nonlocal std_count
            std_count += 1

        # Suscribir múltiples observadores
        for i in range(3):
            Publisher.subscribe(f"ttk_test_{i}", ttk_callback, Channel.TTK)
            Publisher.subscribe(f"std_test_{i}", std_callback, Channel.STD)

        # Cambiar tema y verificar notificaciones
        self.style.theme_use('flatly')

        assert ttk_count == 3, "Todos los suscriptores TTK deberían ser notificados"
        assert std_count == 3, "Todos los suscriptores STD deberían ser notificados"

    def test_style_exists_in_theme(self):
        """Verifica la detección de existencia de estilos en el tema.

        Prueba:
        1. Detección de estilos existentes
        2. Detección de estilos no existentes
        3. Comportamiento con diferentes temas
        """
        # Preparar un estilo de prueba
        test_style = "Test.TButton"
        current_theme = self.style.theme.name

        # Verificar estilo no existente
        assert not self.style.style_exists_in_theme(test_style)

        # Registrar y verificar estilo
        self.style._register_ttkstyle(test_style)
        assert self.style.style_exists_in_theme(test_style)

        # Verificar en otro tema
        self.style.theme_use('flatly')
        assert not self.style.style_exists_in_theme(test_style)

    def test_register_ttkstyle(self):
        """Verifica el registro de estilos TTK.

        Prueba:
        1. Registro en el registro global
        2. Registro en el tema específico
        3. Persistencia del registro
        """
        test_style = "Primary.TButton"
        current_theme = self.style.theme.name

        # Registrar estilo
        self.style._register_ttkstyle(test_style)

        # Verificar registro global
        assert test_style in self.style._style_registry

        # Verificar registro en tema actual
        assert test_style in self.style._theme_styles[current_theme]

        # Verificar que no está en otros temas
        self.style.theme_use('flatly')
        assert test_style not in self.style._theme_styles['flatly']

    def test_create_ttk_styles_on_theme_change(self):
        """Verifica la recreación de estilos al cambiar de tema.

        Prueba:
        1. Creación de estilos al cambiar de tema
        2. Mantenimiento de estilos registrados
        3. Aplicación correcta de estilos básicos
        """
        # Registrar algunos estilos de prueba
        test_styles = ["Primary.TButton", "Info.TLabel", "Success.TEntry"]
        current_theme = self.style.theme.name

        for style in test_styles:
            self.style._register_ttkstyle(style)

        # Cambiar tema y verificar recreación
        new_theme = 'flatly'
        self.style.theme_use(new_theme)

        # Verificar que los estilos se mantienen registrados
        for style in test_styles:
            assert style in self.style._style_registry
            assert not self.style.style_exists_in_theme(style)

        # Forzar recreación y verificar
        self.style._create_ttk_styles_on_theme_change()

        # Verificar que los estilos básicos se aplicaron
        for style in test_styles:
            assert style in self.style._theme_styles[new_theme]
