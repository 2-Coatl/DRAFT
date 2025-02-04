# tests/ui/styles/test_colors.py
from ui.styles.colors import Colors

def test_colors_empty_initialization():
    colors = Colors()
    assert not hasattr(colors, 'primary')
    assert not hasattr(colors, 'secondary')

def test_colors_with_values():
    custom_colors = {
        'primary': '#ff0000',
        'secondary': '#00ff00'
    }
    colors = Colors(**custom_colors)
    assert colors.primary == '#ff0000'
    assert colors.secondary == '#00ff00'

def test_get_color():
    colors = Colors(test='#ffffff')
    assert colors.get_color('test') == '#ffffff'

def test_get_nonexistent_color():
    colors = Colors()
    try:
        colors.get_color('nonexistent')
        assert False, "Debería lanzar AttributeError"
    except AttributeError:
        assert True