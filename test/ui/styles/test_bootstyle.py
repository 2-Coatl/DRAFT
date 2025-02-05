import unittest
from unittest.mock import Mock
from tkinter import ttk
from ui.styles.bootstyle import Bootstyle
from ui.styles.constants import Keywords


class TestBootstyle(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        # Mock de un widget TTK
        self.mock_widget = Mock(spec=ttk.Widget)
        self.mock_widget.winfo_class.return_value = "TButton"

    def test_ttkstyle_widget_class(self):
        """Prueba la detección de clase de widget."""
        # Desde string
        self.assertEqual(Bootstyle.ttkstyle_widget_class(string="Primary.TButton"), "button")
        self.assertEqual(Bootstyle.ttkstyle_widget_class(string="Outline.TEntry"), "entry")
        self.assertEqual(Bootstyle.ttkstyle_widget_class(string="invalid"), "")

        # Desde widget
        self.assertEqual(Bootstyle.ttkstyle_widget_class(self.mock_widget), "button")

        # Sin argumentos
        self.assertEqual(Bootstyle.ttkstyle_widget_class(), "")

    def test_ttkstyle_widget_type(self):
        """Prueba la detección de tipo de widget."""
        # Tipos válidos
        self.assertEqual(Bootstyle.ttkstyle_widget_type("Outline.TButton"), "outline")
        self.assertEqual(Bootstyle.ttkstyle_widget_type("Link.TLabel"), "link")
        self.assertEqual(Bootstyle.ttkstyle_widget_type("Round.Outline.TButton"), "round")

        # Tipo inválido
        self.assertEqual(Bootstyle.ttkstyle_widget_type("Invalid.TButton"), "")
        self.assertEqual(Bootstyle.ttkstyle_widget_type(""), "")

    def test_ttkstyle_widget_color(self):
        """Prueba la detección de color de widget."""
        # Colores válidos
        self.assertEqual(Bootstyle.ttkstyle_widget_color("Primary.TButton"), "primary")
        self.assertEqual(Bootstyle.ttkstyle_widget_color("Secondary.Outline.TButton"), "secondary")
        self.assertEqual(Bootstyle.ttkstyle_widget_color("Success.TLabel"), "success")

        # Color inválido
        self.assertEqual(Bootstyle.ttkstyle_widget_color("Invalid.TButton"), "")
        self.assertEqual(Bootstyle.ttkstyle_widget_color(""), "")

    def test_error_handling(self):
        """Prueba el manejo de errores."""
        # Widget que lanza excepción en cget
        mock_error_widget = Mock(spec=ttk.Widget)
        mock_error_widget.cget.side_effect = Exception("Test error")

        # No debería lanzar excepción
        self.assertEqual(Bootstyle.ttkstyle_widget_orient(mock_error_widget), "")

        # Widget inválido para winfo_class
        mock_invalid_widget = Mock(spec=ttk.Widget)
        mock_invalid_widget.winfo_class.side_effect = Exception("Test error")
        self.assertEqual(Bootstyle.ttkstyle_widget_class(mock_invalid_widget), "")

        # String inválido
        self.assertEqual(Bootstyle.ttkstyle_widget_class(string=None), "")
        self.assertEqual(Bootstyle.ttkstyle_widget_orient(string=None), "")


    def test_ttkstyle_widget_orient(self):
        """Prueba la detección de orientación de widget."""
        # Desde string
        self.assertEqual(
            Bootstyle.ttkstyle_widget_orient(string="Horizontal.TProgressbar"),
            "horizontal"
        )
        self.assertEqual(
            Bootstyle.ttkstyle_widget_orient(string="Vertical.TScrollbar"),
            "vertical"
        )

        # Desde kwargs
        self.assertEqual(
            Bootstyle.ttkstyle_widget_orient(orient="h"),
            "horizontal"
        )
        self.assertEqual(
            Bootstyle.ttkstyle_widget_orient(orient="v"),
            "vertical"
        )
        self.assertEqual(
            Bootstyle.ttkstyle_widget_orient(orient="horizontal"),
            "horizontal"
        )

        # Desde widget
        mock_oriented_widget = Mock(spec=ttk.Widget)
        mock_oriented_widget.cget.return_value = "horizontal"
        self.assertEqual(
            Bootstyle.ttkstyle_widget_orient(widget=mock_oriented_widget),
            "horizontal"
        )

        # Sin orientación
        self.assertEqual(Bootstyle.ttkstyle_widget_orient(), "")
        self.assertEqual(Bootstyle.ttkstyle_widget_orient(string="TButton"), "")

    # tests/ui/styles/test_bootstyle.py
    def test_ttkstyle_name(self):
        """Prueba la construcción de nombres de estilo ttk."""
        # Estilo completo
        self.assertEqual(
            Bootstyle.ttkstyle_name(string="primary.outline.horizontal.TButton"),
            "primary.Outline.Horizontal.TButton"
        )

        # Solo color y clase
        self.assertEqual(
            Bootstyle.ttkstyle_name(string="secondary.TLabel"),
            "secondary.TLabel"
        )

        # Solo clase
        self.assertEqual(
            Bootstyle.ttkstyle_name(string="TEntry"),
            "TEntry"
        )

        # Con widget
        self.mock_widget.winfo_class.return_value = "TButton"
        self.assertEqual(
            Bootstyle.ttkstyle_name(self.mock_widget, "primary"),
            "primary.TButton"
        )

    def test_ttkstyle_method_name(self):
        """Prueba la construcción de nombres de métodos de estilo."""
        # Estilo normal
        self.assertEqual(
            Bootstyle.ttkstyle_method_name(string="primary.outline.TButton"),
            "create_outline_button_style"
        )

        # Sin tipo
        self.assertEqual(
            Bootstyle.ttkstyle_method_name(string="primary.TButton"),
            "create_button_style"
        )

        # Con widget
        self.mock_widget.winfo_class.return_value = "TButton"
        self.assertEqual(
            Bootstyle.ttkstyle_method_name(self.mock_widget),
            "create_button_style"
        )

    def test_tkupdate_method_name(self):
        """Prueba la construcción de nombres de métodos de actualización."""
        self.mock_widget.winfo_class.return_value = "TButton"
        self.assertEqual(
            Bootstyle.tkupdate_method_name(self.mock_widget),
            "update_button_style"
        )

        self.mock_widget.winfo_class.return_value = "TEntry"
        self.assertEqual(
            Bootstyle.tkupdate_method_name(self.mock_widget),
            "update_entry_style"
        )


if __name__ == '__main__':
    unittest.main()