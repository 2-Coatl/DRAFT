import pytest
from ui.styles.themes import ThemeBase
from ui.styles.colors import Colors


def test_theme_base_cannot_be_instantiated():
    with pytest.raises(TypeError):
        ThemeBase()


class MockTheme(ThemeBase):
    @property
    def name(self) -> str:
        return "mock_theme"

    def get_colors(self) -> Colors:
        return Colors(primary="#000000", secondary="#ffffff")


def test_mock_theme_implementation():
    theme = MockTheme()
    assert theme.name == "mock_theme"
    assert isinstance(theme.get_colors(), Colors)


def test_mock_theme_colors():
    theme = MockTheme()
    colors = theme.get_colors()
    assert colors.primary == "#000000"
    assert colors.secondary == "#ffffff"