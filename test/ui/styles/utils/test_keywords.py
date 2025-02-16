import pytest
import tkinter as tk
from tkinter import ttk
from ui.styles.utils.keywords import Keywords


class TestKeywords:
    """Pruebas para la clase de utilidad Keywords."""

    @pytest.fixture
    def root(self):
        """Fixture que proporciona una ventana raíz."""
        root = tk.Tk()
        yield root
        root.destroy()

    def test_ttkstyle_widget_class_from_string(self):
        """Verifica la identificación de clase de widget desde string."""
        # Casos de prueba con strings válidos
        assert Keywords.ttkstyle_widget_class(string="primary.TButton") == "button"
        assert Keywords.ttkstyle_widget_class(string="Danger.TLabel") == "label"
        assert Keywords.ttkstyle_widget_class(string="Success.TProgressbar") == "progressbar"

        # Casos con strings inválidos
        assert Keywords.ttkstyle_widget_class(string="InvalidWidget") == ""
        assert Keywords.ttkstyle_widget_class(string="") == ""

    def test_ttkstyle_widget_class_from_widget(self, root):
        """Verifica la identificación de clase de widget desde objeto widget."""
        # Crear widgets de prueba
        button = ttk.Button(root)
        label = ttk.Label(root)
        entry = ttk.Entry(root)

        # Verificar identificación correcta
        assert Keywords.ttkstyle_widget_class(widget=button) == "button"
        assert Keywords.ttkstyle_widget_class(widget=label) == "label"
        assert Keywords.ttkstyle_widget_class(widget=entry) == "entry"

    def test_ttkstyle_widget_class_no_input(self):
        """Verifica el comportamiento cuando no se proporcionan argumentos."""
        assert Keywords.ttkstyle_widget_class() == ""

    def test_ttkstyle_widget_class_case_insensitive(self):
        """Verifica que la identificación es insensible a mayúsculas/minúsculas."""
        assert Keywords.ttkstyle_widget_class(string="PRIMARY.TBUTTON") == "button"
        assert Keywords.ttkstyle_widget_class(string="danger.tlabel") == "label"