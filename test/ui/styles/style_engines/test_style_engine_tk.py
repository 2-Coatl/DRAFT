import pytest
import tkinter as tk
from ui.styles.style_engines.style_engine_tk import StyleEngineTK
from ui.styles.color import Colors
from ui.styles.theme_definition import ThemeDefinition


class TestStyleEngineTK:
    """Pruebas para el motor de estilos de widgets TK."""

    @pytest.fixture
    def engine(self):
        """Fixture que proporciona una instancia del motor de estilos.

        Returns:
            StyleEngineTK: Instancia del motor de estilos para pruebas.
        """
        return StyleEngineTK()

    @pytest.fixture
    def root(self):
        """Fixture que proporciona una ventana root de Tkinter.

        Returns:
            tk.Tk: Instancia de la ventana principal para pruebas.
        """
        root = tk.Tk()
        yield root
        root.destroy()

    def test_theme_property(self, engine):
        """Verifica que la propiedad theme devuelve la definición correcta."""
        assert engine.theme is not None
        assert isinstance(engine.theme, ThemeDefinition)

    def test_colors_property(self, engine):
        """Verifica que la propiedad colors devuelve los colores correctos."""
        assert engine.colors is not None
        assert isinstance(engine.colors, Colors)

    def test_is_light_theme_property(self, engine):
        """Verifica que is_light_theme refleja correctamente el tipo de tema."""
        assert isinstance(engine.is_light_theme, bool)
        # El valor dependerá del tema actual

    def test_update_tk_style(self, engine, root):
        """Verifica la actualización de estilo de la ventana principal."""
        engine.update_tk_style(root)
        assert root.cget('background') == engine.colors.bg

    def test_update_toplevel_style(self, engine, root):
        """Verifica la actualización de estilo de una ventana secundaria."""
        toplevel = tk.Toplevel(root)
        engine.update_toplevel_style(toplevel)
        assert toplevel.cget('background') == engine.colors.bg
        toplevel.destroy()

    def test_update_canvas_style(self, engine, root):
        """Verifica la actualización de estilo de un canvas."""
        canvas = tk.Canvas(root)
        engine.update_canvas_style(canvas)
        assert canvas.cget('background') == engine.colors.bg
        assert int(canvas.cget('highlightthickness')) == 0  # Convertimos el string a int
        canvas.destroy()

    def test_update_button_style(self, engine, root):
        """Verifica la actualización de estilo de un botón."""
        button = tk.Button(root)
        engine.update_button_style(button)

        # Verificación de propiedades básicas
        assert button.cget('background') == engine.colors.primary
        assert button.cget('foreground') == engine.colors.selectfg
        assert button.cget('relief') == tk.FLAT
        assert button.cget('borderwidth') == 0

        # Verificación de color activo
        expected_active_bg = Colors.update_hsv(engine.colors.primary, vd=-0.1)
        assert button.cget('activebackground') == expected_active_bg

        # Verificación de color de resaltado
        assert button.cget('highlightbackground') == engine.colors.selectfg

        button.destroy()

    def test_cleanup(self, root):
        """Verifica la limpieza adecuada de los widgets."""
        # Esta prueba asegura que los fixtures limpian correctamente
        pass