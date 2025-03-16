import unittest
import tkinter as tk
from contextlib import contextmanager
from unittest.mock import patch, MagicMock

# Importa tus clases específicas
from ui.themeengine.core.window import Window
from ui.themeengine.core.top_level import Toplevel


# =============================================================================
# SECCIÓN 1: FIXTURES Y CONFIGURACIÓN BASE
# =============================================================================

class TestWindowToplevelBase(unittest.TestCase):
    """
    Clase base para todas las pruebas de integración Window-Toplevel.

    Proporciona los fixtures comunes y métodos auxiliares para:
    1. Crear y limpiar el contexto Tkinter
    2. Crear y gestionar instancias de Window y Toplevel
    3. Manejar actualizaciones y sincronización de la interfaz
    """

    def setUp(self):
        """
        Prepara el ambiente para cada prueba.

        1. Parcha funciones relevantes para evitar comportamientos visuales
        2. Inicializa variables de estado para seguimiento
        """
        # Parchar mainloop para evitar bloqueo durante pruebas
        self.mainloop_patch = patch('tkinter.Tk.mainloop')
        self.mainloop_mock = self.mainloop_patch.start()

        # Parchar update_idletasks para evitar actualizaciones visuales
        self.update_patch = patch('tkinter.Tk.update_idletasks')
        self.update_mock = self.update_patch.start()

        # Parchar place_window_center para evitar cálculos de geometría
        self.center_patch = patch.object(Toplevel, 'place_window_center')
        self.center_mock = self.center_patch.start()

        # Bandera para seguimiento de recursos
        self._resources_created = False

    def tearDown(self):
        """
        Limpia los recursos después de cada prueba.

        1. Destruye ventanas creadas
        2. Detiene parches activos
        3. Ejecuta el recolector de basura
        """
        # Detener parches
        self.mainloop_patch.stop()
        self.update_patch.stop()
        self.center_patch.stop()

        # Destruir ventanas si existen
        if hasattr(self, 'root') and hasattr(self.root, 'destroy'):
            try:
                if self.root.winfo_exists():
                    self.root.destroy()
            except tk.TclError:
                pass

        if hasattr(self, 'toplevel') and hasattr(self.toplevel, 'destroy'):
            try:
                if self.toplevel.winfo_exists():
                    self.toplevel.destroy()
            except tk.TclError:
                pass

        # Forzar liberación de recursos
        import gc
        gc.collect()

    def create_window(self, **kwargs):
        """
        Crea una instancia de Window con los parámetros especificados.

        Args:
            **kwargs: Argumentos para el constructor de Window

        Returns:
            Window: La instancia creada
        """
        self.root = Window(**kwargs)
        self._resources_created = True
        return self.root

    def create_toplevel(self, **kwargs):
        """
        Crea una instancia de Toplevel con los parámetros especificados.

        Asegura que exista una ventana raíz antes de crear el Toplevel.

        Args:
            **kwargs: Argumentos para el constructor de Toplevel

        Returns:
            Toplevel: La instancia creada
        """
        # Verificar si necesitamos crear una nueva ventana raíz
        if not hasattr(self, 'root') or not hasattr(self.root, 'winfo_exists') or not self.root.winfo_exists():
            # Si la ventana raíz no existe o está destruida, crear una nueva
            self.root = self.create_window()

        # Ahora crear el Toplevel
        self.toplevel = Toplevel(**kwargs)
        return self.toplevel

    @contextmanager
    def gestionar_patchers(self, patchers):
        """
        Gestor de contexto para manejar inicio/limpieza de patchers.

        Args:
            patchers: Diccionario de patchers a gestionar

        Yields:
            dict: Diccionario de mocks activos
        """
        mocks = {}
        for name, patcher in patchers.items():
            mocks[name] = patcher.start()

        try:
            yield mocks
        finally:
            for patcher in patchers.values():
                patcher.stop()


# =============================================================================
# SECCIÓN 2: PRUEBAS DE INTEGRACIÓN
# =============================================================================

class TestWindowToplevelIntegration(TestWindowToplevelBase):
    """
    Pruebas de integración entre las clases Window y Toplevel.

    Verifica:
    1. Interacción correcta entre ventana principal y ventanas secundarias
    2. Comportamiento coordinado con temas y estilos
    3. Parámetros compartidos y consistencia visual
    """

    def test_window_toplevel_creation(self):
        """
        Verifica la creación de Window y Toplevel con diferentes parámetros
        usando subTest para ejecutar múltiples casos de prueba.
        """
        # Casos de prueba para Window
        window_casos = [
            {"params": {"themename": "flatly", "alpha": 0.5, "size": (800, 600)},
             "expected": {"theme": "flatly", "alpha": 0.5}},
            {"params": {"themename": "cosmo", "alpha": 0.8, "size": (1024, 768)},
             "expected": {"theme": "cosmo", "alpha": 0.8}},
        ]

        # Casos de prueba para Toplevel
        toplevel_casos = [
            {"params": {"title": "My Toplevel", "alpha": 0.4, "size": (400, 300)},
             "expected": {"title": "My Toplevel", "alpha": 0.4}},
            {"params": {"title": "Settings Dialog", "alpha": 0.9, "size": (600, 400)},
             "expected": {"title": "Settings Dialog", "alpha": 0.9}},
            {"params": {"title": "About Window", "toolwindow": True},
             "expected": {"title": "About Window"}}
        ]

        # Probar casos de Window
        for i, caso in enumerate(window_casos):
            with self.subTest(f"Window case {i + 1}: {caso['params']}"):
                # Crear ventana con los parámetros del caso
                window = self.create_window(**caso['params'])

                # Verificar existencia
                self.assertTrue(window.winfo_exists())

                # Verificar tema si corresponde
                if 'theme' in caso['expected'] and hasattr(window, '_current_theme'):
                    self.assertEqual(window._current_theme, caso['expected']['theme'])

                # Verificar alpha si corresponde
                if 'alpha' in caso['expected'] and hasattr(window, 'attributes'):
                    alpha_value = window.attributes("-alpha")
                    self.assertAlmostEqual(alpha_value, caso['expected']['alpha'], places=1)

                # Limpiar para el siguiente subTest
                window.destroy()

        # Probar casos de Toplevel
        for i, caso in enumerate(toplevel_casos):
            with self.subTest(f"Toplevel case {i + 1}: {caso['params']}"):
                # Crear ventana secundaria con los parámetros del caso
                window = self.create_window()
                toplevel = self.create_toplevel(**caso['params'])

                # Verificar existencia
                self.assertTrue(toplevel.winfo_exists())

                # Verificar título si corresponde
                if 'title' in caso['expected']:
                    self.assertEqual(toplevel.title(), caso['expected']['title'])

                # Verificar alpha si corresponde
                if 'alpha' in caso['expected'] and hasattr(toplevel, 'attributes'):
                    toplevel_alpha = toplevel.attributes("-alpha")
                    self.assertAlmostEqual(toplevel_alpha, caso['expected']['alpha'], places=1)

                # Limpiar para el siguiente subTest
                toplevel.destroy()
                window.destroy()

    def test_window_center_calls(self):
        """
        Verifica que los métodos de centrado se llamen correctamente.
        """
        # Crear instancias con posicionamiento centrado
        with patch.object(Window, 'place_window_center') as window_center_mock:
            window = self.create_window(themename="flatly", size=(800, 600))
            window.place_window_center()

            # Verificar que se llamó al método de centrado
            window_center_mock.assert_called_once()

        # Verificar centrado de Toplevel
        with patch.object(Toplevel, 'place_window_center') as toplevel_center_mock:
            window = self.create_window()
            toplevel = self.create_toplevel(title="My Toplevel", size=(400, 300))
            toplevel.place_window_center()

            # Verificar que se llamó al método de centrado
            toplevel_center_mock.assert_called_once()

    def test_mainloop_interaction(self):
        """
        Verifica que mainloop se llame correctamente en Window.
        """
        # Crear instancias
        window = self.create_window(themename="flatly")
        toplevel = self.create_toplevel(title="My Toplevel")

        # Ejecutar mainloop
        with patch.object(Window, 'mainloop') as mainloop_mock:
            window.mainloop()

            # Verificar que se llamó al método mainloop
            mainloop_mock.assert_called_once()

    def test_theme_consistency(self):
        """
        Verifica que los temas se apliquen consistentemente
        entre Window y Toplevel usando subtests para múltiples temas.
        """
        # Lista de temas a probar
        temas = ["flatly", "cosmo"]

        for tema in temas:
            with self.subTest(f"Consistencia con tema: {tema}"):
                # Simular el singleton Style con un mock
                style_mock = MagicMock()

                # Parchar el acceso a Style() para que ambas clases usen el mismo objeto
                with patch('ui.themeengine.core.top_level.Style', return_value=style_mock):
                    with patch('ui.themeengine.core.window.Style', return_value=style_mock):
                        # Crear ventana con tema específico
                        window = self.create_window(themename=tema)

                        # Crear Toplevel
                        toplevel = self.create_toplevel(title=f"Toplevel con {tema}")

                        # Verificar consistencia de temas
                        # Nota: La implementación exacta dependerá de cómo manejas temas
                        self.assertEqual(toplevel.style, window.style)

                        # Verificar que sea el mock que creamos
                        self.assertIs(toplevel.style, style_mock)
                        self.assertIs(window.style, style_mock)

                        # Limpiar para el siguiente subtest
                        toplevel.destroy()
                        window.destroy()

    def test_position_center_algorithm(self):
        """
        Verifica que el algoritmo de centrado calcule correctamente
        las posiciones para Window y Toplevel.
        """
        # Detener temporalmente el parche del método place_window_center
        self.center_patch.stop()

        try:
            # Casos de prueba para algoritmo de centrado
            casos_centrado = [
                # Caso 1: Ventana estándar en monitor HD
                {
                    'ventana': 'Window',
                    'dimensiones': {
                        'ancho_ventana': 800, 'alto_ventana': 600,
                        'ancho_pantalla': 1920, 'alto_pantalla': 1080
                    },
                    'esperado': '+560+240'
                },
                # Caso 2: Ventana pequeña en monitor HD
                {
                    'ventana': 'Window',
                    'dimensiones': {
                        'ancho_ventana': 400, 'alto_ventana': 300,
                        'ancho_pantalla': 1920, 'alto_pantalla': 1080
                    },
                    'esperado': '+760+390'
                },
                # Caso 3: Toplevel estándar en monitor HD
                {
                    'ventana': 'Toplevel',
                    'dimensiones': {
                        'ancho_ventana': 600, 'alto_ventana': 400,
                        'ancho_pantalla': 1920, 'alto_pantalla': 1080
                    },
                    'esperado': '+660+340'
                },
                # Caso 4: Ventana grande en monitor pequeño
                {
                    'ventana': 'Window',
                    'dimensiones': {
                        'ancho_ventana': 1024, 'alto_ventana': 768,
                        'ancho_pantalla': 1366, 'alto_pantalla': 768
                    },
                    'esperado': '+171+0'
                }
            ]

            for i, caso in enumerate(casos_centrado):
                with self.subTest(f"Caso {i + 1}: {caso['ventana']} {caso['dimensiones']}"):
                    dims = caso['dimensiones']

                    # Crear una instancia de Toplevel usando tu método helper
                    toplevel = self.create_toplevel()

                    # Parchar los métodos de información pero NO place_window_center
                    with patch.object(toplevel, 'winfo_width', return_value=dims['ancho_ventana']), \
                            patch.object(toplevel, 'winfo_height', return_value=dims['alto_ventana']), \
                            patch.object(toplevel, 'winfo_screenwidth', return_value=dims['ancho_pantalla']), \
                            patch.object(toplevel, 'winfo_screenheight', return_value=dims['alto_pantalla']), \
                            patch.object(toplevel, 'update_idletasks'), \
                            patch.object(toplevel, 'geometry') as geometry_mock:
                        # Llamar al método real
                        toplevel.place_window_center()

                        # Calcular la posición esperada
                        x = (dims['ancho_pantalla'] - dims['ancho_ventana']) // 2
                        y = (dims['alto_pantalla'] - dims['alto_ventana']) // 2
                        geometria = f"+{x}+{y}"

                        # Verificar que se llamó a geometry con el valor esperado
                        geometry_mock.assert_called_once_with(geometria)
        finally:
            # Asegurarse de reiniciar el parche para otras pruebas
            self.center_patch = patch.object(Toplevel, 'place_window_center')
            self.center_mock = self.center_patch.start()

if __name__ == "__main__":
    unittest.main()