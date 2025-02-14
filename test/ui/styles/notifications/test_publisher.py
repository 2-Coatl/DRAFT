import pytest
from ui.styles.notifications.publisher import Publisher
from ui.styles.notifications.channel import Channel


class TestPublisher:
    """Pruebas para la clase Publisher."""

    def setup_method(self):
        """Preparación antes de cada prueba."""
        Publisher.clear_subscribers()

    def test_subscriber_count(self):
        """Verifica el conteo correcto de suscriptores."""
        assert Publisher.subscriber_count() == 0
        Publisher.subscribe("test", lambda: None, Channel.TTK)
        assert Publisher.subscriber_count() == 1

    def test_subscribe_unsubscribe(self):
        """Verifica la suscripción y desuscripción de widgets."""
        Publisher.subscribe("widget1", lambda: None, Channel.TTK)
        assert Publisher.subscriber_count() == 1

        Publisher.unsubscribe("widget1")
        assert Publisher.subscriber_count() == 0

    def test_get_subscribers(self):
        """Verifica la obtención de suscriptores por canal."""
        Publisher.subscribe("ttk_widget", lambda: None, Channel.TTK)
        Publisher.subscribe("std_widget", lambda: None, Channel.STD)

        ttk_subs = Publisher.get_subscribers(Channel.TTK)
        std_subs = Publisher.get_subscribers(Channel.STD)

        assert len(ttk_subs) == 1
        assert len(std_subs) == 1
        assert ttk_subs[0].name == "ttk_widget"
        assert std_subs[0].name == "std_widget"

    def test_publish_message(self):
        """Verifica el envío correcto de mensajes a los suscriptores."""
        test_data = []

        def callback(data):
            test_data.append(data)

        Publisher.subscribe("test_widget", callback, Channel.TTK)
        Publisher.publish_message(Channel.TTK, "test_message")

        assert len(test_data) == 1
        assert test_data[0] == "test_message"

    def test_clear_subscribers(self):
        """Verifica la limpieza total de suscriptores."""
        Publisher.subscribe("widget1", lambda: None, Channel.TTK)
        Publisher.subscribe("widget2", lambda: None, Channel.STD)

        assert Publisher.subscriber_count() == 2
        Publisher.clear_subscribers()
        assert Publisher.subscriber_count() == 0

if __name__ == '__main__':
    pytest.main()