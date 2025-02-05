import unittest
from ui.styles.events import Channel, Publisher, Subscriber

class TestEvents(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        Publisher.clear_subscribers()
        self.test_value = 0

    def callback_std(self, *args):
        """Callback de prueba para canal STD."""
        self.test_value += 1

    def callback_ttk(self, *args):
        """Callback de prueba para canal TTK."""
        self.test_value += 2

    def test_subscriber_count(self):
        """Prueba el conteo de suscriptores."""
        self.assertEqual(Publisher.subscriber_count(), 0)
        Publisher.subscribe("widget1", self.callback_std, Channel.STD)
        self.assertEqual(Publisher.subscriber_count(), 1)
        Publisher.subscribe("widget2", self.callback_ttk, Channel.TTK)
        self.assertEqual(Publisher.subscriber_count(), 2)

    def test_get_subscribers(self):
        """Prueba obtener suscriptores por canal."""
        Publisher.subscribe("widget1", self.callback_std, Channel.STD)
        Publisher.subscribe("widget2", self.callback_ttk, Channel.TTK)

        std_subs = Publisher.get_subscribers(Channel.STD)
        ttk_subs = Publisher.get_subscribers(Channel.TTK)

        self.assertEqual(len(std_subs), 1)
        self.assertEqual(len(ttk_subs), 1)
        self.assertEqual(std_subs[0].name, "widget1")
        self.assertEqual(ttk_subs[0].name, "widget2")

    def test_clear_subscribers(self):
        """Prueba limpiar todos los suscriptores."""
        Publisher.subscribe("widget1", self.callback_std, Channel.STD)
        Publisher.subscribe("widget2", self.callback_ttk, Channel.TTK)
        self.assertEqual(Publisher.subscriber_count(), 2)

        Publisher.clear_subscribers()
        self.assertEqual(Publisher.subscriber_count(), 0)
        self.assertEqual(len(Publisher.get_subscribers(Channel.STD)), 0)
        self.assertEqual(len(Publisher.get_subscribers(Channel.TTK)), 0)

    def test_subscriber_creation(self):
        """Prueba la creación de un suscriptor."""
        subscriber = Subscriber("test_widget", self.callback_std, Channel.STD)
        self.assertEqual(subscriber.name, "test_widget")  # Cambiado de widget_id a name
        self.assertEqual(subscriber.func, self.callback_std)  # Cambiado de callback a func
        self.assertEqual(subscriber.channel, Channel.STD)

    def test_publisher_subscribe(self):
        """Prueba la suscripción de widgets."""
        # Suscribir widget
        Publisher.subscribe("widget1", self.callback_std, Channel.STD)

        # Verificar usando subscriber_count y get_subscribers
        self.assertEqual(Publisher.subscriber_count(), 1)
        subscribers = Publisher.get_subscribers(Channel.STD)
        self.assertEqual(len(subscribers), 1)

        # Verificar datos del suscriptor
        subscriber = subscribers[0]
        self.assertEqual(subscriber.name, "widget1")
        self.assertEqual(subscriber.func, self.callback_std)
        self.assertEqual(subscriber.channel, Channel.STD)

    def test_publisher_unsubscribe(self):
        """Prueba la desuscripción de widgets."""
        # Suscribir y luego desuscribir
        Publisher.subscribe("widget1", self.callback_std, Channel.STD)
        self.assertEqual(Publisher.subscriber_count(), 1)

        Publisher.unsubscribe("widget1")
        self.assertEqual(Publisher.subscriber_count(), 0)
        self.assertEqual(len(Publisher.get_subscribers(Channel.STD)), 0)

        # Desuscribir widget inexistente no debe causar error
        Publisher.unsubscribe("nonexistent")

    def test_publish_message(self):
        """Prueba la publicación de mensajes."""
        # Suscribir widgets a diferentes canales
        Publisher.subscribe("widget_std", self.callback_std, Channel.STD)
        Publisher.subscribe("widget_ttk", self.callback_ttk, Channel.TTK)

        # Publicar en canal STD
        self.test_value = 0
        Publisher.publish_message(Channel.STD)
        self.assertEqual(self.test_value, 1)  # Solo callback_std se ejecutó

        # Publicar en canal TTK
        self.test_value = 0
        Publisher.publish_message(Channel.TTK)
        self.assertEqual(self.test_value, 2)  # Solo callback_ttk se ejecutó


if __name__ == '__main__':
    unittest.main()