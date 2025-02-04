"""Pruebas para el sistema de eventos de temas"""
import unittest
from tkinter import ttk
import tkinter as tk
from ui.styles.events import Channel, Publisher


class TestEventSystem(unittest.TestCase):
    def setUp(self):
        """Preparar el ambiente de pruebas"""
        self.root = tk.Tk()
        self.test_button = ttk.Button(self.root)
        self.callback_called = False

    def test_subscription(self):
        """Probar suscripción y notificación"""
        def callback(*args):
            self.callback_called = True

        widget_id = str(self.test_button.winfo_id())
        Publisher.subscribe(widget_id, callback, Channel.TTK)
        self.assertIn(widget_id, Publisher._subscribers)
        Publisher.publish_message(Channel.TTK)
        self.assertTrue(self.callback_called)

    def test_unsubscribe(self):
        """Probar eliminación de suscripción"""
        widget_id = str(self.test_button.winfo_id())
        Publisher.subscribe(widget_id, lambda: None, Channel.TTK)
        Publisher.unsubscribe(widget_id)
        self.assertNotIn(widget_id, Publisher._subscribers)

    def tearDown(self):
        """Limpiar después de las pruebas"""
        self.root.destroy()
        Publisher._subscribers.clear()


if __name__ == '__main__':
    unittest.main()