import tkinter
from typing import Optional, Tuple, Union

from ui.themeengine.core.style import Style


class Toplevel(tkinter.Toplevel):
    """
    Una clase que envuelve tkinter.Toplevel para proporcionar una API más conveniente
    con funcionalidades adicionales. Para más información sobre los métodos heredados
    de `Toplevel`, consulte la documentación de tcl/tk y Python.

    Ejemplos:
        ```python
        app = Toplevel(title="Mi Ventana", size=(800, 600))
        app.place_window_center()
        # Centrar en pantalla
        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str = "themeengine",
            iconphoto: str = '',
            size: Optional[Tuple[int, int]] = None,
            position: Optional[Tuple[int, int]] = None,
            minsize: Optional[Tuple[int, int]] = None,
            maxsize: Optional[Tuple[int, int]] = None,
            resizable: Optional[Tuple[bool, bool]] = None,
            transient: Optional[Union[tkinter.Tk, tkinter.Widget]] = None,
            overrideredirect: bool = False,
            windowtype: Optional[str] = None,
            topmost: bool = False,
            toolwindow: bool = False,
            alpha: float = 1.0,
            **kwargs,
    ) -> None:
        """
        Inicializa una nueva ventana Toplevel con la configuración especificada.

        Parámetros:
            title (str):
                El título que aparece en la barra de título de la aplicación.

            iconphoto (str):
                Ruta a la imagen utilizada como icono de la barra de título.
                Internamente, esto se pasa al método `Tk.iconphoto`.
                Por defecto, se utiliza el icono de la aplicación.

            size (Tuple[int, int]):
                El ancho y alto de la ventana de la aplicación.
                Internamente, este argumento se pasa al método
                `Toplevel.geometry`.

            position (Tuple[int, int]):
                La posición horizontal y vertical de la ventana en
                la pantalla relativa a la coordenada superior izquierda.
                Internamente, esto se pasa al método `Toplevel.geometry`.

            minsize (Tuple[int, int]):
                Especifica las dimensiones mínimas permitidas para la
                ventana. Internamente, este argumento se pasa al método
                `Toplevel.minsize`.

            maxsize (Tuple[int, int]):
                Especifica las dimensiones máximas permitidas para la
                ventana. Internamente, este argumento se pasa al método
                `Toplevel.maxsize`.

            resizable (Tuple[bool, bool]):
                Especifica si el usuario puede redimensionar interactivamente
                la ventana toplevel. Debe pasar dos argumentos que especifiquen
                esta bandera para las dimensiones _horizontal_ y _vertical_.
                Esto puede ajustarse después de crear la ventana usando
                el método `Toplevel.resizable`.

            transient (Union[Tk, Widget]):
                Indica al gestor de ventanas que este widget es
                transitorio con respecto al widget maestro. Internamente,
                esto se pasa al método `Toplevel.transient`.

            overrideredirect (bool):
                Indica al gestor de ventanas que ignore este widget si
                es True. Internamente, este argumento se procesa como
                `Toplevel.overrideredirect(1)`.

            windowtype (str):
                En X11, solicita que la ventana sea interpretada por
                el gestor de ventanas como siendo del tipo especificado. Internamente,
                esto se pasa a `Toplevel.attributes('-type', windowtype)`.

                Vea la [opción -type](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm#M64)
                para una lista de opciones disponibles.

            topmost (bool):
                Especifica si esta es una ventana de nivel superior (se muestra por encima
                de todas las demás ventanas). Internamente, esto es procesado por la ventana
                como `Toplevel.attributes('-topmost', 1)`.

            toolwindow (bool):
                En Windows, especifica un estilo de ventana de herramientas. Internamente,
                esto se procesa como `Toplevel.attributes('-toolwindow', 1)`.

            alpha (float):
                En Windows, especifica el nivel de transparencia alfa del
                toplevel. Donde no es compatible, alfa permanece en 1.0. Internamente,
                esto se procesa como `Toplevel.attributes('-alpha', alpha)`.

            **kwargs (Dict):
                Otros argumentos de palabra clave opcionales.
        """

        # Extraer el parámetro especial 'iconify' si existe en kwargs
        # Este parámetro indica si la ventana debe minimizarse inicialmente
        if 'iconify' in kwargs:
            iconify = kwargs.pop('iconify')  # Extraer y eliminar 'iconify' de kwargs
        else:
            iconify = None  # Si no se proporciona, establecer como None

        # Inicializar la clase base tkinter.Toplevel con los argumentos restantes
        super().__init__(**kwargs)

        # Detectar el sistema de ventanas activo ('win32', 'x11', 'aqua')
        # Esto se usará para comportamientos específicos de plataforma más adelante
        self.winsys = self.tk.call('tk', 'windowingsystem')

        # Si se solicitó iconificación inicial, minimizar la ventana
        # Esto hace que la ventana aparezca como un icono en la barra de tareas
        if iconify:
            self.iconify()  # Minimizar la ventana utilizando el método heredado de tkinter.Toplevel


        # Configurar icono personalizado si se especificó una ruta
        if iconphoto != '':
            try:
                # Cargar imagen desde archivo (soporta formatos: GIF, PGM, PPM, PNG)
                self._icon: tkinter.PhotoImage = tkinter.PhotoImage(
                    file=iconphoto,  # Ruta al archivo de imagen
                    master=self  # Asociar imagen con esta ventana
                )

                # Establecer como icono de la ventana y futuras ventanas
                self.iconphoto(True, self._icon)
            except tkinter.TclError:
                # Falló la carga de la imagen, usar icono predeterminado
                print('iconphoto path is bad; using default image.')

        # Establecer el título de la ventana
        self.title(title)  # title: str

        # Configurar el tamaño de la ventana (ancho x alto en píxeles)
        if size is not None:  # size: Optional[Tuple[int, int]]
            width, height = size  # width, height: int
            self.geometry(f'{width}x{height}')  # Formato: 'anchoxalto'  (ej: '800x600')

        # Configurar la posición de la ventana (coordenadas x, y en pantalla)
        if position is not None:  # position: Optional[Tuple[int, int]]
            xpos, ypos = position  # xpos, ypos: int
            self.geometry(f"+{xpos}+{ypos}")  # Formato: '+x+y' (ej: '+100+200')

        # Configurar el tamaño mínimo de la ventana si se especificó
        if minsize is not None:
            width, height = minsize  # Extraer ancho y alto mínimos de la tupla
            self.minsize(width, height)  # Establecer límite inferior de redimensionamiento

        # Configurar el tamaño máximo de la ventana si se especificó
        if maxsize is not None:
            width, height = maxsize  # Extraer ancho y alto máximos de la tupla
            self.maxsize(width, height)  # Establecer límite superior de redimensionamiento

        # Configurar si la ventana puede redimensionarse interactivamente
        if resizable is not None:
            width, height = resizable  # Extraer valores para ejes horizontal y vertical
            self.resizable(width, height)  # True permite redimensionar, False lo impide

        # Establecer esta ventana como transitoria respecto a otra ventana
        if transient is not None:
            # Esto hace que la ventana se comporte como dependiente de su maestra:
            # - Siempre aparece encima de su maestra
            # - Se minimiza cuando se minimiza la maestra
            # - Generalmente se cierra cuando se cierra la maestra
            self.transient(transient)

        # Eliminar decoraciones de ventana del sistema si se solicita
        if overrideredirect:
            # Esto elimina la barra de título, bordes y botones de control
            # Útil para ventanas personalizadas, pero requiere implementar
            # mecanismos propios para mover y cerrar la ventana
            self.overrideredirect(1)

        # Configurar tipo específico de ventana en sistemas X11
        if windowtype is not None:
            if self.winsys == 'x11':  # self.winsys: str - Sistema de ventanas detectado
                # Establece el tipo de ventana para el gestor de ventanas X11
                # Ver: https://tcl.tk/man/tcl8.6/TkCmd/wm.htm#M64 para opciones válidas
                self.attributes("-type", windowtype)

        # Establecer ventana como "siempre visible" (todas las plataformas)
        if topmost:  # topmost: bool
            # Valor 1 (True) activa la propiedad topmost
            self.attributes("-topmost", 1)  # La ventana permanece sobre otras ventanas

        # Configurar estilo de ventana de herramientas en Windows
        if toolwindow:  # toolwindow: bool
            if self.winsys == 'win32':  # Solo en Windows
                # Valor 1 (True) activa el estilo de ventana de herramientas
                self.attributes("-toolwindow", 1)  # Barra de título reducida, solo botón cerrar

        # Configurar nivel de transparencia de la ventana
        if alpha is not None:  # alpha: Optional[float] (rango 0.0 a 1.0)
            # Manejo especial para sistemas X11 (Linux)
            if self.winsys == 'x11':  # self.winsys: str
                # En X11 debemos esperar a que la ventana sea visible antes
                # de establecer transparencia, o podría no aplicarse
                self.wait_visibility(self)  # Bloquea hasta que la ventana aparece

            # Aplicar transparencia a toda la ventana
            # - 1.0: Completamente opaca
            # - 0.5: 50% transparente
            # - 0.0: Completamente transparente (pero aún interactiva)
            self.attributes("-alpha", alpha)  # Establece nivel de transparencia


    @property
    def style(self) -> 'Style':
        """
        Proporciona acceso al objeto de estilo del framework themeengine.

        Returns:
            Style: Una instancia del objeto Style para configurar temas y apariencia
        """
        # Crear una nueva instancia del objeto Style
        return Style()

    def place_window_center(self) -> None:
        """
        Posiciona la ventana en el centro de la pantalla.

        Nota: El cálculo no tiene en cuenta la altura de la barra de título del
        sistema operativo, por lo que la ventana aparecerá ligeramente por encima
        del centro exacto de la pantalla.

        Returns:
            None: No devuelve ningún valor, su efecto es modificar la posición de la ventana.

        Ejemplo:
            ```python
            window = Toplevel(title="Ventana Centrada")
            window.geometry("400x300")  # Establecer tamaño
            window.place_window_center()  # Centrar en pantalla
            ```
        """
        # Actualizar tareas pendientes para asegurar mediciones correctas
        self.update_idletasks()

        # Obtener dimensiones en píxeles (valores enteros)
        w_height: int = self.winfo_height()  # Alto de la ventana
        w_width: int = self.winfo_width()  # Ancho de la ventana
        s_height: int = self.winfo_screenheight()  # Alto de la pantalla
        s_width: int = self.winfo_screenwidth()  # Ancho de la pantalla

        # Calcular coordenadas centrales
        xpos: int = (s_width - w_width) // 2  # Posición horizontal centrada
        ypos: int = (s_height - w_height) // 2  # Posición vertical centrada

        # Mover la ventana a la posición calculada
        self.geometry(f'+{xpos}+{ypos}')

    # Proporcionar un alias para el método (ambos nombres funcionan)
    position_center = place_window_center  # type: ignore


