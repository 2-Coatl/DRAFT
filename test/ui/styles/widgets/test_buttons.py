"""Pruebas para botones estilizados"""
import unittest
from tkinter import ttk
import tkinter as tk
from ui.styles.widgets.buttons import StyledButton
from ui.styles.theme_manager import ThemeManager
from ui.styles.events import Publisher

class TestStyledButton(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.theme_manager = ThemeManager()

    def test_button_creation(self):
        """Probar creación básica del botón"""
        button = StyledButton(self.root, text="Test")
        self.assertIsInstance(button, StyledButton)
        self.assertIsInstance(button, ttk.Button)

    def test_button_style_update(self):
        """Probar actualización de estilo con cambio de tema"""
        button = StyledButton(self.root, text="Test")
        initial_style = button.cget('style')

        # Cambiar tema
        current_theme = self.theme_manager.current_theme.name
        new_theme = 'sandstone' if current_theme == 'superhero' else 'superhero'
        self.theme_manager.set_theme(new_theme)

        # Verificar que el estilo se actualizó
        self.assertEqual(button.cget('style'), initial_style)

    def test_button_cleanup(self):
        """Probar limpieza al destruir el botón"""
        button = StyledButton(self.root, text="Test")
        widget_id = button.widget_id
        button.destroy()
        # Verificar que no está en los suscriptores
        self.assertNotIn(widget_id, Publisher._subscribers)

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()