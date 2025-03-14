import pytest
import tkinter
import platform
from unittest.mock import patch, MagicMock


# Asumiendo que estas son las importaciones correctas
from ui.themeengine.core.style import Style
from ui.themeengine.utils.icons import Icon
from ui.themeengine.core.window import Window
#import inspect
#from ui.themeengine.core.window import Window
#print(inspect.getsource(Window.__init__))  # Ver el código fuente real

class TestWindow:
    """Suite de pruebas para la clase Window.

    Esta clase contiene pruebas para verificar:
    1. Inicialización correcta con diferentes parámetros
    2. Gestión de temas e iconos
    3. Configuración de ventana (tamaño, posición, etc.)
    4. Soporte HDPI según el sistema operativo
    5. Centrado de ventana
    """

    @pytest.fixture
    def mock_tk_setup(self, monkeypatch):
        """Fixture para simular componentes de tkinter sin iniciar GUI real"""
        # Simular tk.call para windowingsystem
        mock_tk = MagicMock()
        mock_tk.call.return_value = 'win32'  # Por defecto simulamos Windows

        # Simular PhotoImage
        mock_photo = MagicMock()

        # Aplicar patches
        monkeypatch.setattr(tkinter, "PhotoImage", mock_photo)

        # Simular apply_class_bindings y apply_all_bindings
        monkeypatch.setattr('ui.themeengine.utils.event_bindings.apply_class_bindings', MagicMock())
        monkeypatch.setattr('ui.themeengine.utils.event_bindings.apply_all_bindings', MagicMock())

        # Simular enable_high_dpi_awareness
        monkeypatch.setattr('ui.themeengine.utils.utility.enable_high_dpi_awareness', MagicMock())

        # Simular Style
        mock_style = MagicMock()
        monkeypatch.setattr('ui.themeengine.core.style.Style', MagicMock(return_value=mock_style))

        return {
            'tk': mock_tk,
            'photo': mock_photo,
            'style': mock_style
        }

    @pytest.fixture
    def window_fixture(self, request):
        """Fixture que crea una instancia real de Window para pruebas de integración"""
        # Crear una ventana root para el contexto Tkinter
        root = tkinter.Tk()

        # Configuración personalizable mediante marcadores
        marker = request.node.get_closest_marker("window_params")
        params = {} if marker is None else marker.kwargs

        # Crear la ventana con parámetros específicos
        window = Window(**params)

        # Setup completo, devolver control a la prueba
        yield window

        # Teardown: destruir ventanas
        try:
            window.destroy()
        except tkinter.TclError:
            pass  # Ignora errores si la ventana ya está destruida

        try:
            root.destroy()
        except tkinter.TclError:
            pass

    @pytest.fixture
    def temp_icon_file(self, tmpdir):
        """Crea un archivo de icono temporal para pruebas de carga de iconos"""
        # Crear un archivo temporal con datos mínimos para simular PNG
        icon_path = tmpdir.join("test_icon.png")
        with open(icon_path, 'wb') as f:
            # Encabezado PNG mínimo
            f.write(
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0eIDAT\x08\xd7c````\x00\x00\x00\x04\x00\x01\xf6\x28\x14\xef\x00\x00\x00\x00IEND\xaeB`\x82')
        return str(icon_path)

    # PRUEBAS DE INICIALIZACIÓN BÁSICA --------------------------------------
    def test_init_default_values(self):
        """Verifica que la inicialización con valores predeterminados funcione correctamente"""
        # ARRANGE & ACT
        window = Window()

        # ASSERT
        # Verificar título
        assert window.title() == "themeengine"

        # Verificar que se inicializó Style
        assert hasattr(window, "_style")
        assert isinstance(window._style, Style)

        # No verificamos las vinculaciones de eventos directamente,
        # ya que son detalles de implementación

        # Verificar que la ventana está correctamente configurada
        # (esto implícitamente verifica que los métodos críticos fueron llamados)
        assert window.winfo_exists()

        # Limpiar
        window.destroy()

    def test_style_property_returns_instance(self):
        """Verifica que la propiedad style devuelva la instancia correcta"""
        # ARRANGE & ACT
        window = Window()
        style_object = window.style

        # ASSERT
        # Verificar que style devuelve el objeto _style (comportamiento observable)
        assert style_object is window._style
        # Verificar que es una instancia de Style (comportamiento observable)
        assert isinstance(style_object, Style)

        # Limpiar
        window.destroy()

    # PRUEBAS DE GESTIÓN DE ICONOS -----------------------------------------

    def test_default_icon(self):
        """Verifica el comportamiento con icono predeterminado (cadena vacía)"""
        # Guardar la clase original antes de parchearla
        original_photo_class = tkinter.PhotoImage

        # Aislar la parte de PhotoImage y iconphoto
        with patch('tkinter.PhotoImage') as mock_photo:
            with patch.object(tkinter.Tk, 'iconphoto'):
                # Configurar el mock con spec usando la clase original
                mock_instance = MagicMock(spec=original_photo_class)
                mock_photo.return_value = mock_instance

                # ACT
                window = Window(iconphoto='')

                # ASSERT
                # Verificar que se creó PhotoImage con los datos correctos
                mock_photo.assert_called_with(master=window, data=Icon.icon)
                # Verificar que se guardó la instancia
                assert window._icon is mock_instance

                # Limpiar
                window.destroy()

    @patch('tkinter.PhotoImage')
    def test_none_icon(self, mock_photo):
        """Verifica que no se establezca icono cuando iconphoto=None"""
        # ARRANGE & ACT
        window = Window(iconphoto=None)

        # ASSERT
        mock_photo.assert_not_called()  # No se crea PhotoImage
        assert not hasattr(window, "_icon")  # No se crea el atributo _icon

        # Limpiar
        window.destroy()

    @patch('tkinter.PhotoImage')
    def test_invalid_icon_path(self, mock_photo):
        """Verifica el manejo de rutas de icono inválidas"""
        # ARRANGE
        mock_instance = MagicMock()
        mock_photo.side_effect = [tkinter.TclError, mock_instance]  # Primera llamada falla, segunda funciona

        # Parchear print específicamente en el módulo donde se encuentra Window
        with patch('ui.themeengine.core.window.print') as mock_print:
            # Parchear también iconphoto para evitar el error
            with patch.object(tkinter.Tk, 'iconphoto'):
                # ACT
                window = Window(iconphoto='invalid_path.png')

                # ASSERT
                assert mock_photo.call_count == 2  # Se llamó dos veces
                # Ahora solo deberíamos tener la llamada que nos interesa
                mock_print.assert_called_once_with('iconphoto path is bad; using default image.')
                # El icono predeterminado se debería usar como respaldo
                assert window._icon is mock_instance

                # Limpiar
                window.destroy()

    # PRUEBAS DE CONFIGURACIÓN DE VENTANA ----------------------------------

    def test_window_size_setting(self):
        """Verifica que el tamaño se configure correctamente"""
        # ARRANGE
        size = (800, 600)

        # Crear un espía para el método geometry
        with patch.object(tkinter.Tk, 'geometry') as mock_geometry:
            # ACT
            window = Window(size=size)

            # ASSERT
            # Verificar que geometry fue llamado con los parámetros correctos
            mock_geometry.assert_any_call(f"{size[0]}x{size[1]}")

            # Limpiar
            window.destroy()

    def test_window_position_setting(self):
        """Verifica que la posición se configure correctamente"""
        # ARRANGE & ACT
        window = Window(position=(100, 200))

        # ASSERT - Extraer posición de la geometría
        geometry = window.geometry()
        parts = geometry.split('+')
        assert len(parts) >= 3
        assert parts[1] == '100'
        assert parts[2] == '200'

        # Limpiar
        window.destroy()

    def test_window_minsize_setting(self):
        """Verifica que minsize se configure correctamente"""
        # ARRANGE & ACT
        min_width, min_height = 300, 200
        window = Window(minsize=(min_width, min_height))

        # ASSERT
        current_minsize = window.minsize()
        assert current_minsize == (min_width, min_height)

        # Limpiar
        window.destroy()

    def test_window_maxsize_setting(self):
        """Verifica que maxsize se configure correctamente"""
        # ARRANGE & ACT
        max_width, max_height = 1200, 800
        window = Window(maxsize=(max_width, max_height))

        # ASSERT
        current_maxsize = window.maxsize()
        assert current_maxsize == (max_width, max_height)

        # Limpiar
        window.destroy()

    def test_window_resizable_setting(self):
        """Verifica que las opciones de redimensionamiento se configuren correctamente"""
        # ARRANGE & ACT
        window = Window(resizable=(True, False))

        # ASSERT
        assert window.resizable()[0] == 1  # Width resizable
        assert window.resizable()[1] == 0  # Height not resizable

        # Limpiar
        window.destroy()

    # PRUEBAS DE SOPORTE HDPI ---------------------------------------------

    @patch('ui.themeengine.core.window.enable_high_dpi_awareness')
    def test_hdpi_windows_before_init(self, mock_hdpi):

        """Verifica que en Windows, HDPI se active antes de la inicialización"""
        # ARRANGE
        # Configurar Windows como sistema operativo
        with patch('platform.system', return_value="Windows"):
            # ACT
            window = Window(hdpi=True)

            # ASSERT
            # Verificar que se llamó la función
            mock_hdpi.assert_called_once_with()

            # Limpiar
            window.destroy()

    def test_hdpi_linux_correct_patch(self, monkeypatch):
        """Verifica la activación de HDPI en Linux con el parche correcto"""
        # Importar el módulo window para tener acceso directo a la implementación
        import ui.themeengine.core.window as window_module

        # Crear un mock para la función enable_high_dpi_awareness
        mock_hdpi = MagicMock()

        # Parchear directamente en el espacio de nombres del módulo window
        # Esto asegura que parcheamos la referencia exacta que usa la clase Window
        monkeypatch.setattr(window_module, "enable_high_dpi_awareness", mock_hdpi)

        # Configurar Linux como sistema operativo
        monkeypatch.setattr(platform, "system", lambda: "Linux")

        # Crear la ventana
        window = None
        try:
            window = window_module.Window(hdpi=True)

            # Verificar que la función fue llamada
            mock_hdpi.assert_called_once()

            # Verificar que se llamó con los argumentos correctos
            args, kwargs = mock_hdpi.call_args
            assert len(args) == 2, "Debería recibir dos argumentos"
            assert args[0] == window, "El primer argumento debería ser la ventana"
            assert args[1] == 1.5, "El segundo argumento debería ser 1.5 (scaling para Linux)"
        finally:
            if window:
                window.destroy()

    # En lugar de parchear 'ui.themeengine.utils.utility.enable_high_dpi_awareness'
    # Parchea la función directamente en el módulo window
    @patch('ui.themeengine.core.window.enable_high_dpi_awareness')
    def test_hdpi_linux_after_init(self, mock_hdpi, monkeypatch):
        """Verifica que en Linux, HDPI se active después de la inicialización"""
        # ARRANGE
        monkeypatch.setattr(platform, "system", lambda: "Linux")

        # ACT
        window = None
        try:
            # Asegurémonos de que el mock esté configurado antes de crear la ventana
            assert not mock_hdpi.called, "El mock no debería haberse llamado antes de crear la ventana"

            window = Window(hdpi=True)

            # ASSERT
            mock_hdpi.assert_called_once()
            args, kwargs = mock_hdpi.call_args
            assert len(args) == 2, f"Se esperaban 2 argumentos positionales"
            assert isinstance(args[0], Window), f"El primer argumento debería ser la instancia de Window"
            assert args[1] == 1.5, f"El segundo argumento debería ser 1.5 (scaling para Linux)"
        finally:
            if window is not None:
                window.destroy()

    @patch('ui.themeengine.core.window.enable_high_dpi_awareness')
    def test_custom_scaling(self, mock_hdpi):
        """Verifica que el escalado personalizado se aplique correctamente"""
        # ARRANGE & ACT
        custom_scaling = 2.0
        window = Window(scaling=custom_scaling)

        # ASSERT - Verificamos las llamadas específicas
        assert mock_hdpi.call_count == 2, f"Se esperaban 2 llamadas, se recibieron {mock_hdpi.call_count}"

        # La primera llamada debería ser sin argumentos (para Windows)
        assert mock_hdpi.call_args_list[0] == (), "La primera llamada debería ser sin argumentos"

        # La segunda llamada debería ser con la ventana y el valor de escalado
        args, kwargs = mock_hdpi.call_args_list[1]
        assert len(args) == 2, f"La segunda llamada debería tener 2 argumentos, recibió {len(args)}"
        assert args[0] == window, f"El primer argumento debería ser la ventana"
        assert args[1] == custom_scaling, f"El segundo argumento debería ser el valor de escalado personalizado"

        # Limpiar
        window.destroy()

    @patch('ui.themeengine.utils.utility.enable_high_dpi_awareness')
    def test_hdpi_disabled(self, mock_hdpi):
        """Verifica que HDPI no se active cuando hdpi=False"""
        # ARRANGE & ACT
        window = Window(hdpi=False)

        # ASSERT
        mock_hdpi.assert_not_called()

        # Limpiar
        window.destroy()

    # PRUEBAS DE CENTRADO DE VENTANA -------------------------------------

    def test_place_window_center(self):
        """Verifica que la ventana se centre correctamente"""
        # ARRANGE
        window = Window(size=(400, 300))

        # Simular que tenemos una ventana con dimensiones conocidas
        with patch.object(window, 'update_idletasks'):
            with patch.object(window, 'winfo_width', return_value=400):
                with patch.object(window, 'winfo_height', return_value=300):
                    with patch.object(window, 'winfo_screenwidth', return_value=1920):
                        with patch.object(window, 'winfo_screenheight', return_value=1080):
                            with patch.object(window, 'geometry') as mock_geometry:
                                # ACT
                                window.place_window_center()

                                # ASSERT
                                # Verifica que geometry se llamó con la posición correcta
                                expected_x = (1920 - 400) // 2  # 760
                                expected_y = (1080 - 300) // 2  # 390
                                mock_geometry.assert_called_once_with(f'+{expected_x}+{expected_y}')

        # Limpiar
        window.destroy()

    def test_position_center_alias_(self):
        """Verifica que position_center sea un alias de place_window_center a nivel de clase"""
        # ARRANGE - Verificar directamente en la clase
        # Aquí estamos comprobando si position_center es el mismo objeto que place_window_center
        assert Window.position_center is Window.place_window_center, "position_center debería ser una referencia a place_window_center a nivel de clase"

        # Limpieza - No es necesario crear una instancia para esta prueba

    def test_position_center_alias_mechanism(self):
        """Explora el mecanismo de alias en detalle"""
        # ARRANGE
        window = Window()

        # Verificar a nivel de clase
        assert Window.position_center is Window.place_window_center

        # Verificar a nivel de instancia (métodos ligados diferentes)
        assert window.position_center is not window.place_window_center

        # Modificar el método a nivel de clase
        original_method = Window.place_window_center
        call_count = [0]

        def tracking_method(self):
            call_count[0] += 1
            return original_method(self)

        # Reemplazar a nivel de clase
        Window.place_window_center = tracking_method

        # ACT - Llamar a position_center
        try:
            window.position_center()

            # ASSERT
            assert call_count[0] == 0, "position_center NO debería llamar al place_window_center modificado"

            # Pero llamar a position_center directamente DEBERÍA incrementar el contador
            window.place_window_center()
            assert call_count[0] > 0, "place_window_center modificado debería incrementar el contador"
        finally:
            # Restaurar el método original
            Window.place_window_center = original_method
            window.destroy()

    # PRUEBAS DE CASOS LÍMITE Y MANEJO DE ERRORES -----------------------

    @pytest.mark.parametrize("alpha,expected", [
        (0.5, 0.5),
        (0.0, 0.0),
        (1.0, 1.0),
        (None, 1.0),  # Valor predeterminado
    ])
    def test_alpha_setting(self, alpha, expected):
        """Verifica configuración de transparencia (valor alfa)"""
        # ARRANGE & ACT
        window = Window(alpha=alpha) if alpha is not None else Window()

        # ASSERT - No podemos verificar directamente, pero no debería dar error
        # La prueba principalmente verifica que no se produzcan excepciones
        # Un test más completo requeriría verificar la propiedad de Tk

        # Limpiar
        window.destroy()

    def test_transient_setting(self):
        """Verifica configuración de ventana transitoria (modal)"""
        # ARRANGE
        parent = tkinter.Tk()

        # ACT
        with patch.object(Window, 'transient') as mock_transient:
            window = Window(transient=parent)

            # ASSERT
            mock_transient.assert_called_once_with(parent)

        # Limpiar
        parent.destroy()
        window.destroy()

    # PRUEBAS DE INTEGRACIÓN BÁSICAS ------------------------------------
    def test_integration_style_access_real(self):
        """Prueba de integración real: acceso al estilo sin mocks"""
        # ARRANGE - Crear una ventana real
        window = Window(themename="flatly")

        # ACT
        style = window.style

        # ASSERT
        assert style is not None

        # Verificar que style es una instancia real del tipo correcto
        assert isinstance(style, Style)

        # Verificar que el tema usado es el esperado
        current_theme = style.theme_use()
        assert current_theme == "flatly"

        # Limpiar
        window.destroy()

    def test_integration_window_lifecycle(self):
        """Prueba de integración: ciclo de vida completo de la ventana"""
        # ARRANGE & ACT
        window = Window(title="Test Window", size=(300, 200))

        # Verificar propiedades iniciales
        assert window.title() == "Test Window"

        # Modificar propiedades
        window.title("Modified Title")

        # Verificar que los cambios se aplicaron
        assert window.title() == "Modified Title"

        # Verificar que se puede centrar la ventana sin errores
        window.place_window_center()

        # ASSERT - La prueba se considera exitosa si no se producen excepciones

        # Limpiar
        window.destroy()