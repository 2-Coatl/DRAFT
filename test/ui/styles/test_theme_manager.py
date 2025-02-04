from unittest.mock import Mock
from ui.styles.theme_manager import ThemeManager
from ui.styles.events import Channel, Publisher


def test_theme_change_notification():
    # Preparar
    tm = ThemeManager()
    mock_callback = Mock()
    Publisher.subscribe("test_widget", mock_callback, Channel.STD)

    # Ejecutar
    tm.set_theme("sandstone")

    # Verificar
    mock_callback.assert_called_once()
    # Limpiar
    Publisher.unsubscribe("test_widget")


def test_theme_manager_singleton():
    tm1 = ThemeManager()
    tm2 = ThemeManager()
    assert tm1 is tm2
    assert tm1._available_themes == tm2._available_themes


def test_invalid_theme_no_notification():
    tm = ThemeManager()
    mock_callback = Mock()
    Publisher.subscribe("test_widget", mock_callback, Channel.STD)

    assert tm.set_theme("nonexistent") is False
    mock_callback.assert_not_called()

    Publisher.unsubscribe("test_widget")