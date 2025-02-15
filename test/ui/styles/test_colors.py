import pytest
from ui.styles.color import Colors


class TestColors:
    """Pruebas para la clase Colors."""

    @pytest.fixture
    def default_colors(self):
        """Fixture que proporciona una instancia de Colors con valores por defecto.

        Returns:
            Colors: Instancia con colores predeterminados para pruebas.
        """
        return Colors(
            primary="#007bff",
            secondary="#6c757d",
            success="#28a745",
            info="#17a2b8",
            warning="#ffc107",
            danger="#dc3545",
            light="#f8f9fa",
            dark="#343a40",
            bg="#ffffff",
            fg="#000000",
            selectbg="#0d6efd",
            selectfg="#ffffff",
            border="#dee2e6",
            inputfg="#000000",
            inputbg="#ffffff",
            active="#0d6efd"
        )

    def test_init(self, default_colors):
        """Verifica la inicialización correcta de Colors."""
        assert default_colors.primary == "#007bff"
        assert default_colors.secondary == "#6c757d"
        assert default_colors.success == "#28a745"
        # Verificamos algunos colores representativos
        assert default_colors.bg == "#ffffff"
        assert default_colors.fg == "#000000"

    def test_get_method(self, default_colors):
        """Verifica el funcionamiento del método get."""
        assert default_colors.get("primary") == "#007bff"
        assert default_colors.get("bg") == "#ffffff"
        assert default_colors.get("nonexistent") is None

    def test_set_method(self, default_colors):
        """Verifica el funcionamiento del método set."""
        default_colors.set("primary", "#ff0000")
        assert default_colors.primary == "#ff0000"
        assert default_colors.get("primary") == "#ff0000"

    def test_get_foreground(self, default_colors):
        """Verifica el método get_foreground."""
        assert default_colors.get_foreground("light") == default_colors.dark
        assert default_colors.get_foreground("dark") == default_colors.light
        assert default_colors.get_foreground("other") == default_colors.selectfg

    def test_make_transparent(self):
        """Verifica el método make_transparent."""
        # Negro con 50% de transparencia sobre blanco debe dar gris medio
        result = Colors.make_transparent(0.5, "#000000", "#ffffff")
        assert result.lower() == "#7f7f7f"

    def test_hex_to_rgb(self):
        """Verifica la conversión de hexadecimal a RGB."""
        r, g, b = Colors.hex_to_rgb("#ff0000")
        assert (r, g, b) == (1.0, 0.0, 0.0)

    def test_rgb_to_hex(self):
        """Verifica la conversión de RGB a hexadecimal."""
        hex_color = Colors.rgb_to_hex(1.0, 0.0, 0.0)
        assert hex_color.lower() == "#ff0000"

    def test_update_hsv(self):
        """Verifica la actualización de colores HSV."""
        # Aumentar el valor debe aclarar el color
        lighter = Colors.update_hsv("#ff0000", vd=0.1)
        assert lighter != "#ff0000"

        # Reducir la saturación debe hacer el color más gris
        desaturated = Colors.update_hsv("#ff0000", sd=-0.5)
        assert desaturated != "#ff0000"

    def test_iteration(self, default_colors):
        """Verifica la iteración sobre los colores principales."""
        colors_list = list(default_colors)
        assert len(colors_list) == 8  # Los 8 colores principales
        assert "primary" in colors_list
        assert "secondary" in colors_list

    def test_label_iter(self):
        """Verifica la iteración sobre todas las etiquetas de color."""
        all_labels = list(Colors.label_iter())
        assert len(all_labels) == 16  # Todos los colores
        assert "primary" in all_labels
        assert "bg" in all_labels
        assert "inputfg" in all_labels

    def test_repr(self, default_colors):
        """Verifica la representación en string del objeto."""
        repr_str = repr(default_colors)
        assert "primary" in repr_str
        assert "#007bff" in repr_str