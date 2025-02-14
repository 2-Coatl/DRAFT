import pytest
from ui.styles.notifications.channel import Channel

class TestChannel:
    """Pruebas para la enumeración Channel."""

    @pytest.mark.parametrize("canal,valor", [
        (Channel.STD, 1),
        (Channel.TTK, 2)
    ])
    def test_valores_canales(self, canal, valor):
        """Verifica que los canales tengan los valores correctos."""
        assert canal.value == valor

    def test_cantidad_canales(self):
        """Verifica que existan solo los canales necesarios."""
        assert len(Channel) == 2

    def test_tipos_canales(self):
        """Verifica que existan los tipos específicos de canales."""
        assert Channel.STD in Channel
        assert Channel.TTK in Channel

    def test_inmutabilidad_canales(self):
        """Verifica que los canales no puedan ser modificados."""
        with pytest.raises(AttributeError):
            Channel.STD = 3

if __name__ == '__main__':
    pytest.main()