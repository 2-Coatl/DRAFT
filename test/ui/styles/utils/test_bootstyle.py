import pytest
import re
from tkinter import ttk
import tkinter as tk
from ui.styles.utils.bootstyle import Bootstyle
from ui.styles.utils.keywords import Keywords


class TestBootstyle:
    """Pruebas para la clase utilitaria Bootstyle."""

    @pytest.fixture
    def root(self):
        """Fixture que proporciona una instancia de tk.Tk para las pruebas."""
        root = tk.Tk()
        yield root
        root.destroy()

    def test_ttkstyle_widget_class_from_string(self):
        """Verifica la extracción de la clase del widget desde una cadena."""
        # Casos válidos
        assert Bootstyle.ttkstyle_widget_class(string="button") == "button"
        assert Bootstyle.ttkstyle_widget_class(string="TButton") == "button"
        assert Bootstyle.ttkstyle_widget_class(string="primary.TButton") == "button"

        # Casos inválidos
        assert Bootstyle.ttkstyle_widget_class(string="invalid") == ""
        assert Bootstyle.ttkstyle_widget_class(string="") == ""

    def test_ttkstyle_widget_class_from_widget(self, root):
        """Verifica la extracción de la clase del widget desde un widget TTK."""
        # Crear widgets para prueba
        button = ttk.Button(root)
        entry = ttk.Entry(root)

        # Verificar clases
        assert Bootstyle.ttkstyle_widget_class(widget=button) == "button"
        assert Bootstyle.ttkstyle_widget_class(widget=entry) == "entry"

        # Caso sin widget
        assert Bootstyle.ttkstyle_widget_class() == ""

    def test_ttkstyle_widget_type(self):
        """Verifica la extracción del tipo de widget desde una cadena."""
        # Casos válidos
        assert Bootstyle.ttkstyle_widget_type("outline.TButton") == "outline"
        assert Bootstyle.ttkstyle_widget_type("link.TLabel") == "link"
        assert Bootstyle.ttkstyle_widget_type("round.primary.TButton") == "round"

        # Múltiples tipos en la cadena (debe retornar el primero que encuentre)
        assert Bootstyle.ttkstyle_widget_type("outline.round.TButton") == "outline"

        # Casos inválidos
        assert Bootstyle.ttkstyle_widget_type("TButton") == ""
        assert Bootstyle.ttkstyle_widget_type("") == ""
        assert Bootstyle.ttkstyle_widget_type("invalid.type") == ""

        # Verificar con todos los tipos definidos en Keywords
        for widget_type in Keywords.TYPES:
            assert Bootstyle.ttkstyle_widget_type(f"{widget_type}.TButton") == widget_type

    def test_ttkstyle_widget_orient_from_string(self):
        """Verifica la extracción de la orientación desde una cadena."""
        # Casos válidos
        assert Bootstyle.ttkstyle_widget_orient(string="horizontal.TProgressbar") == "horizontal"
        assert Bootstyle.ttkstyle_widget_orient(string="vertical.TScale") == "vertical"

        # Casos inválidos
        assert Bootstyle.ttkstyle_widget_orient(string="TProgressbar") == ""
        assert Bootstyle.ttkstyle_widget_orient(string="") == ""

    def test_ttkstyle_widget_orient_from_kwargs(self):
        """Verifica la extracción de la orientación desde kwargs."""
        # Casos completos
        assert Bootstyle.ttkstyle_widget_orient(orient="horizontal") == "horizontal"
        assert Bootstyle.ttkstyle_widget_orient(orient="vertical") == "vertical"

        # Casos abreviados
        assert Bootstyle.ttkstyle_widget_orient(orient="h") == "horizontal"
        assert Bootstyle.ttkstyle_widget_orient(orient="v") == "vertical"

        # Caso con otros kwargs
        assert Bootstyle.ttkstyle_widget_orient(other="value", orient="horizontal") == "horizontal"

    def test_ttkstyle_widget_orient_from_widget(self, root):
        """Verifica la extracción de la orientación desde un widget."""
        # Widgets con orientación
        progressbar = ttk.Progressbar(root, orient="horizontal")
        scale = ttk.Scale(root, orient="vertical")

        assert Bootstyle.ttkstyle_widget_orient(widget=progressbar) == "horizontal"
        assert Bootstyle.ttkstyle_widget_orient(widget=scale) == "vertical"

        # Widget sin orientación
        button = ttk.Button(root)
        assert Bootstyle.ttkstyle_widget_orient(widget=button) == ""

        # Sin widget
        assert Bootstyle.ttkstyle_widget_orient() == ""

    def test_ttkstyle_widget_orient_priority(self, root):
        """Verifica que se respete la prioridad en la obtención de la orientación."""
        progressbar = ttk.Progressbar(root, orient="horizontal")

        # String tiene prioridad sobre kwargs y widget
        assert Bootstyle.ttkstyle_widget_orient(
            widget=progressbar,
            string="vertical.TProgressbar",
            orient="horizontal"
        ) == "vertical"

        # kwargs tienen prioridad sobre widget
        assert Bootstyle.ttkstyle_widget_orient(
            widget=progressbar,
            orient="vertical"
        ) == "vertical"

    @staticmethod
    def ttkstyle_widget_color(string: str) -> str:
        """Encuentra y retorna el color del widget.

        Busca en la cadena proporcionada un patrón que coincida con
        alguno de los colores definidos en el sistema.

        Args:
            string: La cadena de texto a parsear.

        Returns:
            El color encontrado o cadena vacía si no hay coincidencia.
        """
        _color = re.search(Keywords.COLOR_PATTERN, string.lower())
        if _color is None:
            return ""
        else:
            widget_color = _color.group(0)
            return widget_color

    def test_ttkstyle_widget_color(self):
        """Verifica la extracción del color desde una cadena."""
        # Casos válidos
        assert Bootstyle.ttkstyle_widget_color("primary.TButton") == "primary"
        assert Bootstyle.ttkstyle_widget_color("success.Outline.TButton") == "success"
        assert Bootstyle.ttkstyle_widget_color("warning.round.TButton") == "warning"

        # Casos con múltiples coincidencias (debe retornar la primera)
        assert Bootstyle.ttkstyle_widget_color("primary.success.TButton") == "primary"

        # Casos inválidos
        assert Bootstyle.ttkstyle_widget_color("TButton") == ""
        assert Bootstyle.ttkstyle_widget_color("") == ""
        assert Bootstyle.ttkstyle_widget_color("invalid.color") == ""

    def test_ttkstyle_widget_color_all_keywords(self):
        """Verifica que funcione con todos los colores definidos en Keywords."""
        for color in Keywords.COLORS:
            # Probar color al inicio del string
            assert Bootstyle.ttkstyle_widget_color(f"{color}.TButton") == color
            # Probar color en medio del string
            assert Bootstyle.ttkstyle_widget_color(f"outline.{color}.TButton") == color
            # Probar color en mayúsculas
            assert Bootstyle.ttkstyle_widget_color(f"{color.upper()}.TButton") == color

    def test_ttkstyle_widget_color_case_insensitive(self):
        """Verifica que la búsqueda de color sea insensible a mayúsculas/minúsculas."""
        test_cases = [
            ("PRIMARY.TButton", "primary"),
            ("Success.TButton", "success"),
            ("WARNING.TButton", "warning"),
            ("DaNgEr.TButton", "danger")
        ]

        for input_str, expected in test_cases:
            assert Bootstyle.ttkstyle_widget_color(input_str) == expected

    def test_ttkstyle_name_basic(self):
        """Verifica la construcción básica de nombres de estilo."""
        assert Bootstyle.ttkstyle_name(string="button") == "TButton"
        assert Bootstyle.ttkstyle_name(string="primary.button") == "primary.TButton"
        assert Bootstyle.ttkstyle_name(string="outline.button") == "Outline.TButton"

    def test_ttkstyle_name_with_all_components(self):
        """Verifica la construcción de nombres con todos los componentes."""
        # Color + Tipo + Orientación + Clase
        assert Bootstyle.ttkstyle_name(
            string="primary.outline.horizontal.progressbar"
        ) == "primary.Outline.Horizontal.TProgressbar"

        # Color + Tipo + Clase
        assert Bootstyle.ttkstyle_name(
            string="success.round.button"
        ) == "success.Round.TButton"

    def test_ttkstyle_name_with_widget(self, root):
        """Verifica la construcción de nombres usando un widget."""
        button = ttk.Button(root)
        progressbar = ttk.Progressbar(root, orient="horizontal")

        assert Bootstyle.ttkstyle_name(widget=button) == "TButton"
        assert Bootstyle.ttkstyle_name(
            widget=progressbar,
            string="primary"
        ) == "primary.Horizontal.TProgressbar"

    def test_ttkstyle_name_with_kwargs(self):
        """Verifica la construcción de nombres usando kwargs."""
        assert Bootstyle.ttkstyle_name(
            string="primary.progressbar",
            orient="horizontal"
        ) == "primary.Horizontal.TProgressbar"

        assert Bootstyle.ttkstyle_name(
            string="success.scale",
            orient="v"
        ) == "success.Vertical.TScale"

    def test_ttkstyle_name_case_handling(self):
        """Verifica el manejo correcto de mayúsculas/minúsculas."""
        test_cases = [
            ("PRIMARY.BUTTON", "primary.TButton"),
            ("success.OUTLINE.button", "success.Outline.TButton"),
            ("Warning.Horizontal.Progressbar", "warning.Horizontal.TProgressbar")
        ]

        for input_str, expected in test_cases:
            assert Bootstyle.ttkstyle_name(string=input_str) == expected

    def test_ttkstyle_name_empty_components(self):
        """Verifica el manejo de componentes vacíos."""
        assert Bootstyle.ttkstyle_name() == ""
        assert Bootstyle.ttkstyle_name(string="") == ""
        assert Bootstyle.ttkstyle_name(string="invalid") == ""

    def test_ttkstyle_method_name_basic(self):
        """Verifica la construcción básica de nombres de método."""
        assert Bootstyle.ttkstyle_method_name(string="button") == "create_button_style"
        assert Bootstyle.ttkstyle_method_name(string="outline.button") == "create_outline_button_style"
        assert Bootstyle.ttkstyle_method_name(string="primary.button") == "create_button_style"

    def test_ttkstyle_method_name_with_widget(self, root):
        """Verifica la construcción de nombres de método usando widgets."""
        button = ttk.Button(root)
        entry = ttk.Entry(root)

        assert Bootstyle.ttkstyle_method_name(widget=button) == "create_button_style"
        assert Bootstyle.ttkstyle_method_name(widget=entry) == "create_entry_style"
        assert Bootstyle.ttkstyle_method_name(
            widget=button,
            string="outline"
        ) == "create_outline_button_style"

    def test_ttkstyle_method_name_invalid_inputs(self):
        """Verifica el manejo de entradas inválidas."""
        assert Bootstyle.ttkstyle_method_name() == ""
        assert Bootstyle.ttkstyle_method_name(string="") == ""
        assert Bootstyle.ttkstyle_method_name(string="invalid") == ""
        assert Bootstyle.ttkstyle_method_name(string="primary") == ""

    def test_ttkstyle_method_name_case_sensitivity(self):
        """Verifica que el método sea insensible a mayúsculas/minúsculas."""
        test_cases = [
            ("BUTTON", "create_button_style"),
            ("Outline.Button", "create_outline_button_style"),
            ("OUTLINE.BUTTON", "create_outline_button_style")
        ]

        for input_str, expected in test_cases:
            assert Bootstyle.ttkstyle_method_name(string=input_str) == expected