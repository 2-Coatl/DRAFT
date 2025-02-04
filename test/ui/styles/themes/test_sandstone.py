from ui.styles.themes.sandstone import SandstoneTheme


def test_sandstone_theme_properties():
    theme = SandstoneTheme()
    assert theme.name == "sandstone"
    assert theme.type == "light"


def test_sandstone_colors():
    theme = SandstoneTheme()
    colors = theme.get_colors()

    # Verificar colores principales
    assert colors.primary == "#325D88"
    assert colors.secondary == "#8e8c84"

    # Verificar colores de interfaz
    assert colors.bg == "#ffffff"
    assert colors.fg == "#3e3f3a"

    # Verificar colores de estado
    assert colors.selectbg == "#8e8c84"
    assert colors.selectfg == "#ffffff"


def test_sandstone_color_access():
    theme = SandstoneTheme()
    colors = theme.get_colors()
    assert colors.get_color('primary') == "#325D88"
    assert colors.get_color('border') == "#ced4da"