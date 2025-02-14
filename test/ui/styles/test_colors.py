import unittest
from ui.styles.color import Colors


class TestColors(unittest.TestCase):
    def setUp(self):
        """Configura un conjunto de colores de prueba."""
        self.colors = Colors(
            primary='#007bff',
            secondary='#6c757d',
            success='#28a745',
            info='#17a2b8',
            warning='#ffc107',
            danger='#dc3545',
            light='#f8f9fa',
            dark='#343a40',
            bg='#ffffff',
            fg='#000000',
            selectbg='#0075e5',
            selectfg='#ffffff',
            border='#ced4da',
            inputfg='#495057',
            inputbg='#ffffff',
            active='#0056b3'
        )

    def test_get_color(self):
        """Prueba la obtención de colores específicos."""
        self.assertEqual(self.colors.get_color('primary'), '#007bff')
        self.assertEqual(self.colors.get_color('secondary'), '#6c757d')
        self.assertIsNone(self.colors.get_color('non_existent'))

    def test_set_color(self):
        """Prueba la modificación de colores."""
        self.colors.set_color('primary', '#0066cc')
        self.assertEqual(self.colors.get_color('primary'), '#0066cc')

        # No debería modificar colores inexistentes
        self.colors.set_color('non_existent', '#ffffff')
        self.assertIsNone(self.colors.get_color('non_existent'))

    def test_get_foreground_color(self):
        """Prueba la obtención de colores de texto apropiados."""
        self.assertEqual(self.colors.get_foreground_color('light'), '#343a40')
        self.assertEqual(self.colors.get_foreground_color('dark'), '#f8f9fa')
        self.assertEqual(
            self.colors.get_foreground_color('other'),
            self.colors.get_color('selectfg')
        )

    def test_get_primary_colors(self):
        """Prueba la obtención de la lista de colores primarios."""
        primary_colors = self.colors.get_primary_colors()
        self.assertEqual(len(primary_colors), 6)
        self.assertIn('primary', primary_colors)
        self.assertIn('secondary', primary_colors)
        self.assertIn('success', primary_colors)
        self.assertIn('info', primary_colors)
        self.assertIn('warning', primary_colors)
        self.assertIn('danger', primary_colors)

    def test_get_all_colors(self):
        """Prueba la obtención de todos los colores disponibles."""
        all_colors = self.colors.get_all_colors()
        self.assertEqual(len(all_colors), 16)  # Número total de colores definidos
        self.assertIn('primary', all_colors)
        self.assertIn('bg', all_colors)
        self.assertIn('fg', all_colors)
        self.assertIn('active', all_colors)

    def test_string_representation(self):
        """Prueba la representación en string de la clase."""
        str_rep = str(self.colors)
        self.assertIn('Colors(', str_rep)
        self.assertIn('primary=#007bff', str_rep)
        self.assertIn('secondary=#6c757d', str_rep)

    def test_hex_to_rgb(self):
        """Prueba la conversión de hexadecimal a RGB."""
        # Prueba con color blanco
        r, g, b = self.colors.hex_to_rgb('#ffffff')
        self.assertAlmostEqual(r, 1.0)
        self.assertAlmostEqual(g, 1.0)
        self.assertAlmostEqual(b, 1.0)

        # Prueba con color negro
        r, g, b = self.colors.hex_to_rgb('#000000')
        self.assertAlmostEqual(r, 0.0)
        self.assertAlmostEqual(g, 0.0)
        self.assertAlmostEqual(b, 0.0)

        # Prueba con color primario
        r, g, b = self.colors.hex_to_rgb('#007bff')
        self.assertAlmostEqual(r, 0.0)
        self.assertAlmostEqual(g, 0.482352941, places=6)
        self.assertAlmostEqual(b, 1.0)

    def test_rgb_to_hex(self):
        """Prueba la conversión de RGB a hexadecimal."""
        # Prueba con color blanco
        hex_color = Colors.rgb_to_hex(1.0, 1.0, 1.0)
        self.assertEqual(hex_color.lower(), '#ffffff')

        # Prueba con color negro
        hex_color = Colors.rgb_to_hex(0.0, 0.0, 0.0)
        self.assertEqual(hex_color.lower(), '#000000')

        # Prueba con color azul (primary)
        # Usamos los valores exactos que obtenemos de la conversión inversa
        r, g, b = self.colors.hex_to_rgb('#007bff')
        hex_color = Colors.rgb_to_hex(r, g, b)
        self.assertEqual(hex_color.lower(), '#007bff')


if __name__ == '__main__':
    unittest.main()