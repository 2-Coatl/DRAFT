import unittest
from tkinter import ttk
import tkinter as tk
from ui.styles.events import Channel, Publisher
from ui.styles.theme_manager import ThemeManager

class TestThemeManagerEvents(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.theme_manager = ThemeManager()
        self.callback_called = False
        self.theme_name_received = None

    def test_theme_change_notification(self):
        """Probar que el cambio de tema notifica correctamente"""
        def callback(*args):
            self.callback_called = True
            if args:
                self.theme_name_received = args[0]

        # Crear un widget y suscribirlo
        test_button = ttk.Button(self.root)
        widget_id = str(test_button.winfo_id())
        Publisher.subscribe(widget_id, callback, Channel.TTK)

        # Cambiar tema
        self.theme_manager.set_theme('sandstone')

        # Verificar notificación
        self.assertTrue(self.callback_called)
        self.assertEqual(self.theme_name_received, 'sandstone')

    def tearDown(self):
        self.root.destroy()
        Publisher._subscribers.clear()

if __name__ == '__main__':
    unittest.main()