import pytest
from ui.styles.utils.keywords import Keywords


class TestKeywords:
    """Pruebas para la clase de utilidad Keywords."""

    @pytest.fixture
    def keywords(self):
        """Fixture que proporciona una instancia de Keywords para las pruebas."""
        return Keywords()

    def test_colors_list_not_empty(self):
        """Verifica que la lista de colores no esté vacía y contenga valores válidos."""
        assert len(Keywords.COLORS) > 0
        assert "primary" in Keywords.COLORS
        assert "secondary" in Keywords.COLORS
        assert "success" in Keywords.COLORS

    def test_orients_list_contains_valid_values(self):
        """Verifica que la lista de orientaciones contenga los valores correctos."""
        assert set(Keywords.ORIENTS) == {"horizontal", "vertical"}

    def test_color_pattern_matches(self):
        """Verifica que el patrón de color coincida con colores válidos."""
        # Casos válidos
        for color in Keywords.COLORS:
            assert Keywords.COLOR_PATTERN.match(color)

        # Casos inválidos
        assert not Keywords.COLOR_PATTERN.match("invalid_color")
        assert not Keywords.COLOR_PATTERN.match("")
        assert not Keywords.COLOR_PATTERN.match("not_a_color")

    def test_class_pattern_matches(self):
        """Verifica que el patrón de clase coincida con clases válidas."""
        # Casos válidos
        for widget_class in Keywords.CLASSES:
            assert Keywords.CLASS_PATTERN.match(widget_class)

        # Casos inválidos
        assert not Keywords.CLASS_PATTERN.match("invalid_widget")
        assert not Keywords.CLASS_PATTERN.match("")
        assert not Keywords.CLASS_PATTERN.match("not_a_widget")

    def test_type_pattern_matches(self):
        """Verifica que el patrón de tipo coincida con tipos válidos."""
        # Casos válidos
        for style_type in Keywords.TYPES:
            assert Keywords.TYPE_PATTERN.match(style_type)

        # Casos inválidos
        assert not Keywords.TYPE_PATTERN.match("invalid_type")
        assert not Keywords.TYPE_PATTERN.match("")
        assert not Keywords.TYPE_PATTERN.match("not_a_type")

    def test_orient_pattern_matches(self):
        """Verifica que el patrón de orientación coincida con orientaciones válidas."""
        # Casos válidos
        for orient in Keywords.ORIENTS:
            assert Keywords.ORIENT_PATTERN.match(orient)

        # Casos inválidos
        assert not Keywords.ORIENT_PATTERN.match("diagonal")
        assert not Keywords.ORIENT_PATTERN.match("")
        assert not Keywords.ORIENT_PATTERN.match("not_an_orientation")