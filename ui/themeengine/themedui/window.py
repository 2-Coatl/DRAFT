import tkinter
import platform
from typing import Optional, Union, Tuple

from ui.themeengine.core.style import Style
from ui.themeengine.utils.event_bindings import apply_class_bindings, apply_all_bindings
from ui.themeengine.utils.utility import enable_high_dpi_awareness
from ui.themeengine.utils.icons import Icon

class Window(tkinter.Tk):
    """Una clase que envuelve la clase tkinter.Tk para proporcionar una
    API más conveniente con funcionalidades adicionales. Para más
    información sobre cómo usar los métodos heredados de `Tk`, consulte la
    [documentación de tcl/tk](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm)
    y la [documentación de Python](https://docs.python.org/3/library/tkinter.html#tkinter.Tk).

    Ejemplos:

        ```python
        app = Window(title="Mi Aplicación", themename="flatly")
        app.mainloop()
        ```

    Args:
        title (str, opcional): Título para la ventana principal.
        themename (str, opcional): Nombre del tema a aplicar a la ventana.
        **kwargs: Argumentos adicionales pasados a tkinter.Tk.

    Returns:
        Window: Una instancia de ventana principal mejorada con capacidades de temas.
    """

    def __init__(
        self,
        title: str = "themeengine",
        themename: str = "flatly",
        iconphoto: str = '',
        size: Optional[Tuple[int, int]] = None,
        position: Optional[Tuple[int, int]] = None,
        minsize: Optional[Tuple[int, int]] = None,
        maxsize: Optional[Tuple[int, int]] = None,
        resizable: Optional[Tuple[bool, bool]] = None,
        hdpi: bool = True,
        scaling: Optional[float] = None,
        transient: Optional[Union[tkinter.Tk, tkinter.Widget]] = None,
        overrideredirect: bool = False,
        alpha: float = 1.0,
    ):
        """Inicializa una nueva instancia de la ventana principal.

        Parámetros:
            title (str):
                El título que aparece en la barra de título de la aplicación.
                Por defecto es "themeengine".

            themename (str):
                El nombre del tema ttkbootstrap que se aplicará a la
                aplicación. Por defecto es "flatly".

            iconphoto (str):
                Ruta a la imagen utilizada como ícono de la barra de título.
                Internamente se pasa al método `Tk.iconphoto` y la imagen será
                el ícono predeterminado para todas las ventanas.
                Se utiliza una imagen ttkbootstrap de forma predeterminada. Para
                deshabilitar este comportamiento, establezca el valor en `None` y use
                los métodos `Tk.iconphoto` o `Tk.iconbitmap` directamente.

            size (Tuple[int, int]):
                El ancho y alto de la ventana de la aplicación.
                Internamente, este argumento se pasa al método
                `Window.geometry`.

            position (Tuple[int, int]):
                La posición horizontal y vertical de la ventana en
                la pantalla relativa a la coordenada superior izquierda.
                Internamente se pasa al método `Window.geometry`.

            minsize (Tuple[int, int]):
                Especifica las dimensiones mínimas permitidas para la
                ventana. Internamente, este argumento se pasa al
                método `Window.minsize`.

            maxsize (Tuple[int, int]):
                Especifica las dimensiones máximas permitidas para la
                ventana. Internamente, este argumento se pasa al
                método `Window.maxsize`.

            resizable (Tuple[bool, bool]):
                Especifica si el usuario puede redimensionar interactivamente
                la ventana. Debe pasar dos argumentos que especifiquen
                esta bandera para las dimensiones _horizontal_ y _vertical_.
                Esto se puede ajustar después de crear la ventana utilizando
                el método `Window.resizable`.

            hdpi (bool):
                Habilita soporte de alta resolución para Windows OS. Esta opción está
                habilitada de forma predeterminada.

            scaling (float):
                Establece el factor de escala actual utilizado por Tk para convertir
                entre unidades físicas (por ejemplo, puntos, pulgadas o
                milímetros) y píxeles. El argumento number es un
                número de punto flotante que especifica el número de píxeles
                por punto en la pantalla de la ventana.

            transient (Union[Tk, Widget]):
                Instruye al gestor de ventanas que este widget es
                transitorio con respecto al widget maestro. Internamente
                se pasa al método `Window.transient`.

            overrideredirect (bool):
                Instruye al gestor de ventanas que ignore este widget si
                es True. Internamente, este argumento se pasa al
                método `Window.overrideredirect(1)`.

            alpha (float):
                En Windows, especifica el nivel de transparencia alpha de la
                ventana principal. Donde no se admite, alpha permanece en 1.0. Internamente,
                esto se procesa como `Toplevel.attributes('-alpha', alpha)`.

        Examples:
            Ventana básica con tema predeterminado:
            ```python
            app = Window(title="Mi Aplicación")
            app.mainloop()
            ```

            Ventana con tamaño y posición específicos:
            ```python
            app = Window(
                title="Ventana Posicionada",
                size=(800, 600),
                position=(100, 100)
            )
            ```

            Ventana con transparencia y sin bordes:
            ```python
            splash = Window(
                title="Splash Screen",
                overrideredirect=True,
                alpha=0.9
            )
            ```
        """

        # Determinar el sistema operativo una vez
        self.os_name = platform.system()

        # Para Windows, activar soporte HDPI antes de inicializar
        if hdpi and self.os_name == "Windows":
            enable_high_dpi_awareness()

        # Inicializar la clase base
        super().__init__()
        self.winsys = self.tk.call('tk', 'windowingsystem')

        # Para Linux o si se especificó scaling, aplicar después de inicializar
        if scaling is not None or (hdpi and self.os_name == "Linux"):
            # Usar un valor predeterminado para scaling en Linux si no se proporcionó
            scaling_value = scaling if scaling is not None else 1.5
            enable_high_dpi_awareness(self, scaling_value)

        # Configurar el título de la ventana
        self.title(title)

        # Si iconphoto es None, no establecer ningún ícono
        if iconphoto is not None:
            # Caso 1: Utilizar el ícono predeterminado si se proporciona una cadena vacía
            if iconphoto == '':
                # Crear un objeto PhotoImage con los datos del ícono predeterminado
                self._icon = tkinter.PhotoImage(master=self, data=Icon.icon)
                # Establecer como ícono predeterminado para todas las ventanas (True)
                self.iconphoto(True, self._icon)
            else:
                try:
                    # Caso 2: Cargar la imagen desde la ruta proporcionada por el usuario
                    self._icon = tkinter.PhotoImage(file=iconphoto, master=self)
                    # Establecer como ícono predeterminado para todas las ventanas
                    self.iconphoto(True, self._icon)
                except tkinter.TclError:
                    # Caso 3: Si la carga falla, utilizar el ícono predeterminado como respaldo
                    # Mostrar mensaje de error
                    print('iconphoto path is bad; using default image.')
                    # Cargar el ícono predeterminado
                    self._icon = tkinter.PhotoImage(data=Icon.icon, master=self)
                    # Establecer como ícono predeterminado
                    self.iconphoto(True, self._icon)

        # Configurar dimensiones de la ventana si se especificaron
        if size is not None:
            width, height = size  # Desempaquetar ancho y alto
            self.geometry(f"{width}x{height}")  # Formato: "anchoXalto"

        # Configurar posición de la ventana si se especificó
        if position is not None:
            xpos, ypos = position  # Desempaquetar coordenadas x e y
            self.geometry(f"+{xpos}+{ypos}")  # Formato: "+x+y"

        # Establecer límites mínimos de tamaño si se especificaron
        if minsize is not None:
            width, height = minsize
            self.minsize(width, height)  # Ej: self.minsize(300, 200)

        # Establecer límites máximos de tamaño si se especificaron
        if maxsize is not None:
            width, height = maxsize
            self.maxsize(width, height)  # Ej: self.maxsize(1200, 800)

        # Configurar opciones de redimensionamiento si se especificaron
        if resizable is not None:
            width, height = resizable  # Desempaquetar valores booleanos
            self.resizable(width, height)  # Ej: self.resizable(True, False)

        # Establecer ventana como transitoria (modal) si se proporcionó un padre
        if transient is not None:
            self.transient(transient)  # Hace que esta ventana sea modal respecto al padre

        # Eliminar decoraciones de ventana si se solicitó
        if overrideredirect:
            self.overrideredirect(1)  # Elimina barra de título y bordes

        # Configurar transparencia de la ventana si se especificó
        if alpha is not None:
            # En sistemas X11 (Linux), es necesario esperar a que la ventana
            # sea visible antes de aplicar transparencia para evitar problemas
            if self.winsys == 'x11':  # 'x11' = Linux
                # Bloquear hasta que la ventana sea visible
                self.wait_visibility(self)

            # Establecer nivel de transparencia (0.0=transparente, 1.0=opaco)
            # Ejemplo: alpha=0.8 → ventana al 80% de opacidad
            self.attributes("-alpha", alpha)

        # Aplicar vinculaciones de eventos específicas para cada clase de widget
        # Esto configura comportamientos como Ctrl+A para seleccionar todo,
        # gestión del cursor según estado, activación de botones con Enter, etc.
        apply_class_bindings(self)

        # Aplicar vinculaciones de eventos globales para todos los widgets
        # Esto configura la propagación de eventos de visibilidad y
        # la limpieza automática de recursos cuando se destruyen widgets
        apply_all_bindings(self)

        # Inicializar o acceder al sistema de estilos
        # Crea/obtiene una instancia única de Style con el tema especificado
        # Esta instancia se comparte entre todas las ventanas (patrón singleton)
        self._style = Style(themename)


    @property
    def style(self) -> Style:
        """Proporciona acceso al objeto Style para gestión de temas y estilos.

        Esta propiedad permite acceder a la instancia compartida de Style,
        que gestiona todos los temas, colores y configuraciones visuales
        de la aplicación.

        Returns:
            Style: Objeto singleton que gestiona los temas y estilos TTK.

        Examples:
            ```python
            window = Window(title="Mi App")

            # Cambiar el tema actual
            window.style.theme_use("darkly")

            # Acceder a colores del tema actual
            primary_color = window.style.colors.primary
            ```
        """
        return self._style


    def place_window_center(self):
        """Posiciona la ventana en el centro exacto de la pantalla.

        Calcula las coordenadas necesarias para centrar la ventana
        en la pantalla, basándose en las dimensiones actuales de ambas.

        Nota: No tiene en cuenta la altura de la barra de título.
        """
        # Procesar todas las operaciones pendientes de la interfaz
        # Esto garantiza que las dimensiones de la ventana estén actualizadas
        self.update_idletasks()

        # Obtener las dimensiones actuales de la ventana
        w_height = self.winfo_height()  # Altura de la ventana en píxeles
        w_width = self.winfo_width()  # Ancho de la ventana en píxeles

        # Obtener las dimensiones totales de la pantalla
        s_height = self.winfo_screenheight()  # Altura de la pantalla en píxeles
        s_width = self.winfo_screenwidth()  # Ancho de la pantalla en píxeles

        # Calcular las coordenadas para centrar la ventana
        # La división entera (//) asegura que las coordenadas sean números enteros
        xpos = (s_width - w_width) // 2  # Posición horizontal centrada
        ypos = (s_height - w_height) // 2  # Posición vertical centrada

        # Aplicar la nueva posición usando el formato '+x+y'
        # Este formato de geometry() solo cambia la posición, no el tamaño
        self.geometry(f'+{xpos}+{ypos}')


    # Crear un alias para mayor flexibilidad en el API
    # Ambos nombres apuntan al mismo método
    position_center = place_window_center  # alias