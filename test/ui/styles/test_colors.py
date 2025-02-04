import unittest
from ui.styles.colors import Colors

class TestColors(unittest.TestCase):
    def setUp(self):
        """Configura los datos de prueba."""
        self.test_colors = {
            'primary': '#007bff',
            'secondary': '#6c757d',
            'success': '#28a745',
            'info': '#17a2b8',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'bg': '#ffffff',
            'fg': '#212529',
            'selectbg': '#0063ce',
            'selectfg': '#ffffff',
            'border': '#dee2e6',
            'inputfg': '#495057',
            'inputbg': '#ffffff',
            'active': '#0056b3'
        }
        self.colors = Colors(**self.test_colors)

    def test_initialization(self):
        """Prueba la inicialización correcta con todos los colores."""
        for name, value in self.test_colors.items():
            self.assertEqual(getattr(self.colors, name), value)

    def test_get_color(self):
        """Prueba el método get para obtener colores."""
        for name, value in self.test_colors.items():
            self.assertEqual(self.colors.get(name), value)
        self.assertIsNone(self.colors.get('nonexistent'))

    def test_set_color(self):
        """Prueba el método set para establecer colores."""
        self.colors.set('custom', '#123456')
        self.assertEqual(self.colors.get('custom'), '#123456')
        self.assertEqual(self.colors.custom, '#123456')

    def test_get_foreground(self):
        """Prueba la obtención del color de texto apropiado."""
        self.assertEqual(self.colors.get_foreground('light'), self.colors.dark)
        self.assertEqual(self.colors.get_foreground('dark'), self.colors.light)
        self.assertEqual(self.colors.get_foreground('primary'), self.colors.selectfg)

    def test_make_transparent(self):
        """Prueba la simulación de transparencia."""
        # Negro sobre blanco con 50% de transparencia debería dar gris
        transparent = Colors.make_transparent(0.5, '#000000', '#ffffff')
        self.assertEqual(transparent.lower(), '#7f7f7f')

    def test_color_conversion(self):
        """Prueba las conversiones entre formatos de color."""
        # Convertir blanco
        rgb = Colors.hex_to_rgb('#ffffff')
        self.assertEqual(rgb, (1, 1, 1))  # RGB normalizado

        # Convertir negro
        hex_color = Colors.rgb_to_hex(0, 0, 0)
        self.assertEqual(hex_color.lower(), '#000000')

    def test_update_hsv(self):
        """Prueba la modificación de colores mediante HSV."""
        base_color = '#ff0000'  # Rojo puro

        # Aumentar brillo
        lighter = Colors.update_hsv(base_color, vd=0.5)
        self.assertNotEqual(lighter, base_color)

        # Reducir saturación
        desaturated = Colors.update_hsv(base_color, sd=-0.5)
        self.assertNotEqual(desaturated, base_color)

        # Modificar matiz
        hue_shifted = Colors.update_hsv(base_color, hd=0.3)
        self.assertNotEqual(hue_shifted, base_color)

        # Verificar límites
        max_value = Colors.update_hsv(base_color, vd=2.0)  # Debería limitarse a 0.95
        self.assertNotEqual(max_value, base_color)
        min_value = Colors.update_hsv(base_color, vd=-2.0)  # Debería limitarse a 0.05
        self.assertNotEqual(min_value, base_color)

    def test_iteration(self):
        """Prueba la iteración sobre colores."""
        main_colors = list(self.colors)
        self.assertEqual(len(main_colors), 8)  # primary through dark
        self.assertIn('primary', main_colors)
        self.assertIn('secondary', main_colors)

        all_colors = list(Colors.label_iter())
        self.assertEqual(len(all_colors), 16)  # todos los colores
        self.assertIn('inputfg', all_colors)
        self.assertIn('active', all_colors)

    def test_representation(self):
        """Prueba la representación string del objeto."""
        repr_str = repr(self.colors)
        self.assertIsInstance(repr_str, str)
        self.assertIn('primary', repr_str)
        self.assertIn(self.test_colors['primary'], repr_str)

if __name__ == '__main__':
    unittest.main()