from ui.styles.themes.superhero import SuperheroTheme


def test_superhero_theme_properties():
    theme = SuperheroTheme()
    assert theme.name == "superhero"
    assert theme.type == "dark"


def test_superhero_colors():
    theme = SuperheroTheme()
    colors = theme.get_colors()

    # Verificar colores principales
    assert colors.primary == "#4c9be8"
    assert colors.secondary == "#4e5d6c"

    # Verificar colores de interfaz
    assert colors.bg == "#2b3e50"
    assert colors.fg == "#ffffff"

    # Verificar colores de estado
    assert colors.selectbg == "#526170"
    assert colors.selectfg == "#ffffff"


def test_superhero_color_access():
    theme = SuperheroTheme()
    colors = theme.get_colors()
    assert colors.get_color('primary') == "#4c9be8"
    assert colors.get_color('border') == "#222222"