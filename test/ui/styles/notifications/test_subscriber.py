import pytest
from ui.styles.notifications.subscriber import Subscriber
from ui.styles.notifications.channel import Channel


class TestSubscriber:
    """Pruebas para la clase Subscriber."""

    def test_creacion_subscriber(self):
        """Verifica la correcta creación de un suscriptor."""

        def dummy_callback(): pass

        subscriber = Subscriber("test_widget", dummy_callback, Channel.TTK)

        assert subscriber.name == "test_widget"
        assert subscriber.callback == dummy_callback
        assert subscriber.channel == Channel.TTK

    def test_atributos_requeridos(self):
        """Verifica que no se puedan crear suscriptores sin atributos requeridos."""

        def dummy_callback(): pass

        with pytest.raises(TypeError):
            Subscriber()

        with pytest.raises(TypeError):
            Subscriber("test_widget")

        with pytest.raises(TypeError):
            Subscriber("test_widget", dummy_callback)

    def test_tipos_atributos(self):
        """Verifica que los atributos sean del tipo correcto."""

        def dummy_callback(): pass

        subscriber = Subscriber("test_widget", dummy_callback, Channel.STD)

        assert isinstance(subscriber.name, str)
        assert callable(subscriber.callback)
        assert isinstance(subscriber.channel, Channel)

if __name__ == '__main__':
    pytest.main()