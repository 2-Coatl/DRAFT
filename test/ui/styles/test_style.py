import pytest
from tkinter import TclError
from ui.theming.constants import DEFAULT_THEME, LIGHT
from ui.theming.style import Style
from ui.theming.theme_definition import ThemeDefinition


class TestStyle:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Prepara el ambiente para las pruebas."""
        if hasattr(Style, 'instance'):
            Style.instance = None
        # Inicializar con el tema por defecto definido en constantes
        self.style = Style(theme=DEFAULT_THEME)  # Será 'cosmo'
        yield
        if hasattr(Style, 'instance'):
            Style.instance = None

    def test_singleton_pattern(self):
        """Verifica el patrón Singleton de la clase Style."""
        style1 = Style()
        style2 = Style()
        assert style1 is style2
        assert Style.get_instance() is style1

    def test_init_with_default_theme(self):
        """Verifica la inicialización con tema predeterminado."""
        assert hasattr(self.style, 'theme')
        assert self.style.theme is not None

    def test_get_instance_returns_singleton(self):
        """Verifica que get_instance retorna la instancia correcta."""
        retrieved_style = Style.get_instance()
        assert self.style is retrieved_style

    def test_init_collections(self):
        """Verifica la inicialización de las colecciones."""
        assert isinstance(self.style._theme_objects, dict)
        assert isinstance(self.style._theme_definitions, dict)
        assert isinstance(self.style._theme_names, set)
        assert isinstance(self.style._theme_styles, dict)
        assert isinstance(self.style._style_registry, set)

    def test_configure_query(self):
        """Verifica la consulta de configuración de estilo."""
        # Configurar un estilo de prueba
        test_style = "TButton"
        self.style.configure(test_style, background="black")

        # Consultar la configuración
        result = self.style.configure(test_style, "background")
        assert result is not None

    def test_style_exists_in_theme(self):
        """Verifica la detección correcta de estilos existentes."""
        # Registrar un estilo de prueba
        test_style = "TButton"
        self.style._register_ttkstyle(test_style)

        # Verificar existencia
        assert self.style.style_exists_in_theme(test_style)

    def test_register_ttkstyle(self):
        """Verifica el registro correcto de estilos TTK."""
        test_style = "TButton"
        self.style._register_ttkstyle(test_style)

        # Verificar registro global
        assert test_style in self.style._style_registry
        # Verificar registro en tema actual
        assert test_style in self.style._theme_styles[self.style.theme.name]

    def test_build_configure(self):
        """Verifica la configuración base de estilos."""
        test_style = "TButton"
        test_config = {"background": "black", "foreground": "white"}

        self.style._build_configure(test_style, **test_config)
        result = self.style.configure(test_style)

        # Verificar que la configuración se aplicó
        assert result is not None

    def test_theme_names(self):
        """Verifica la obtención de nombres de temas."""
        themes = self.style.theme_names()
        assert isinstance(themes, list)
        assert len(themes) > 0

    def test_theme_use_query(self):
        """Verifica la consulta del tema actual."""
        current_theme = self.style.theme_use()
        assert isinstance(current_theme, str)

    def test_theme_use_change(self):
        """Verifica el cambio de tema."""
        # Usar un tema que sabemos existe en STANDARD_THEMES
        self.style.theme_use('flatly')
        assert self.style.theme is not None
        assert self.style.theme.name == 'flatly'


    def test_register_theme(self):
        """Verifica el registro de un nuevo tema."""
        test_theme = ThemeDefinition(
            name="test_theme",
            themetype=LIGHT,  # Usar la constante definida
            colors={
                'primary': '#007bff',
                'secondary': '#6c757d',
                'bg': '#ffffff',
                'fg': '#212529',
                'selectbg': '#0063ce',
                'selectfg': '#ffffff',
                'border': '#dee2e6'
            }
        )
        self.style.register_theme(test_theme)
        assert "test_theme" in self.style._theme_names

    def test_invalid_theme_raises_error(self):
        """Verifica que se lance error con tema inválido."""
        with pytest.raises(TclError):
            self.style.theme_use("tema_inexistente")

    def test_load_themes(self):
        """Verifica la carga inicial de temas."""
        # Verificar que hay temas cargados
        assert len(self.style._theme_definitions) > 0
        assert len(self.style._theme_names) > 0

    def test_colors_property(self):
        """Verifica la obtención de colores del tema."""
        colors = self.style.colors
        assert colors is not None

    def test_colors_with_invalid_theme(self):
        """Verifica el manejo de colores con tema inválido."""
        # Guardamos el tema actual antes de establecerlo a None
        current_theme = self.style.theme
        self.style.theme = None
        colors = self.style.colors
        assert isinstance(colors, list)
        assert len(colors) == 0
        # Restauramos el tema para no afectar otras pruebas
        self.style.theme = current_theme

    def test_get_builder(self):
        """Verifica la obtención del constructor de estilos."""
        # Usamos el tema por defecto que sabemos existe
        builder = self.style._get_builder()
        assert builder is not None
        assert builder == self.style._theme_objects[DEFAULT_THEME]

    def test_get_builder_tk(self):
        """Verifica la obtención del constructor tk."""
        builder_tk = self.style._get_builder_tk()
        assert builder_tk is not None

    def test_create_ttk_styles_on_theme_change(self):
        """Verifica la recreación de estilos al cambiar de tema."""
        # Registrar un estilo de prueba
        test_style = "TButton"
        self.style._register_ttkstyle(test_style)

        # Cambiar a un nuevo tema
        new_theme = "default"  # Asumiendo que existe este tema
        self.style.theme_use(new_theme)

        # Verificar que el estilo existe en el nuevo tema
        assert self.style.style_exists_in_theme(test_style)