import tkinter as tk
from ui.themeengine.core.color import Colors
from ui.themeengine.core.theme import ThemeDefinition
from ui.themeengine.utils.constants import LIGHT


class StyleBuilderTK:
    """Motor de estilos para widgets Tkinter nativos.

    Esta clase se encarga de aplicar y actualizar los estilos de los widgets
    Tkinter tradicionales. Sus métodos son de uso interno y no están diseñados
    para ser llamados directamente por el usuario final.

    Los widgets de Tkinter nativos necesitan una gestión especial de estilos
    ya que no utilizan el sistema de estilos de ttk. Este motor asegura que
    mantengan una apariencia consistente con los widgets ttk.
    """

    def __init__(self) -> None:
        """Inicializa el motor de estilos TK.

        Obtiene la instancia única de Style y establece las referencias necesarias
        para la gestión de estilos.
        """
        # La importación se realiza localmente para evitar dependencia circular
        # entre StyleBuilderTK y Style, que de otra manera causaría un error
        # de importación durante la carga del módulo
        from ui.themeengine.core.style import Style

        # Obtiene la instancia singleton de Style utilizando el método estático
        # get_instance(). No crea una nueva instancia, sino que recupera
        # la existente, garantizando que todos los componentes trabajen
        # con la misma configuración de estilos
        self.style = Style.get_instance()

        # Almacena una referencia directa al widget maestro (root) de la aplicación
        # para facilitar el acceso para las operaciones de estilo que lo necesiten.
        # El widget maestro (tk.Tk) es el widget principal que contiene toda la interfaz
        self.master = self.style.master

    @property
    def theme(self) -> ThemeDefinition:
        """Obtiene la definición del tema actual.

        Esta propiedad proporciona acceso de solo lectura a la definición del tema
        actualmente en uso. La definición incluye el nombre del tema, sus colores
        específicos y el tipo de tema (claro u oscuro).

        La propiedad delega la responsabilidad a la instancia de Style subyacente,
        manteniendo así la consistencia en toda la aplicación.

        Returns:
            ThemeDefinition: Objeto que define el tema en uso, incluyendo nombre,
                             colores (como objetos Colors) y tipo (light/dark).

        """
        # Accede a la propiedad theme del objeto Style
        # Style almacena la definición del tema actualmente seleccionado
        # Esta delegación mantiene un único punto de verdad para el tema actual
        return self.style.theme

    @property
    def colors(self) -> Colors:
        """Obtiene los colores del tema actual.
        Esta propiedad proporciona acceso directo y de solo lectura a la paleta
        de colores del tema actualmente en uso. Representa un atajo conveniente
        para acceder a los colores sin necesidad de obtener primero el objeto tema.

        La propiedad delega la responsabilidad a la instancia de Style subyacente,
        manteniendo así la consistencia en toda la aplicación.

        Returns:
            Colors: Objeto que contiene la paleta de colores actual, con atributos
                    para cada color definido (primary, background, text, etc.).
        """
        # Accede a la propiedad colors del objeto Style
        # Este es un acceso directo a los colores del tema actual
        # Equivalente a self.theme.colors pero más conveniente y eficiente
        return self.style.colors

    @property
    def is_light_theme(self) -> bool:
        """Determina si el tema actual es claro.

        La propiedad realiza una comparación con la constante LIGHT ('light'),
        asumiendo una dicotomía entre temas claros y oscuros.

        Returns:
            bool: True si el tema actual es claro (light), False si es oscuro (dark).
        """
        # Accede al tipo de tema (light/dark) de la instancia actual
        # La constante LIGHT tiene el valor 'light'
        # Retorna True si el tipo coincide con 'light', False en caso contrario
        return self.style.theme.type == LIGHT

    def update_tk_style(self, widget: tk.Tk) -> None:
        """Actualiza el estilo de la ventana principal.
        Este método configura el color de fondo de la ventana principal
        para que coincida con el color de fondo del tema actual. También
        establece la fuente predeterminada para todos los widgets de texto
        (Text y derivados) a la fuente estándar de Tk.

        Args:
            widget (tk.Tk): Ventana principal (root) de la aplicación tkinter
                            que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.
        """
        # Configura el color de fondo de la ventana principal para que
        # coincida con el color de fondo del tema actual.
        # Esto afecta al widget raíz y potencialmente influye en los widgets
        # hijos que heredan esta propiedad
        widget.configure(background=self.colors.bg)
        # Establece la fuente predeterminada para todos los widgets Text
        # El patrón '*Text*Font' afecta a cualquier widget cuyo nombre de clase
        # contenga 'Text' (como Text, ScrolledText, etc.)
        # 'TkDefaultFont' es la fuente predeterminada de Tk que se ajustará
        # según el sistema operativo y configuración
        widget.option_add('*Text*Font', 'TkDefaultFont')

    def update_toplevel_style(self, widget: tk.Toplevel) -> None:
        """Actualiza el estilo de una ventana secundaria.
        Este método configura el color de fondo de una ventana secundaria (Toplevel)
        para que coincida con el color de fondo del tema actual.

        Args:
            widget (tk.Toplevel): Objeto ventana secundaria (Toplevel) que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.
        """
        # Configura el color de fondo de la ventana secundaria (Toplevel)
        # para que coincida con el color de fondo del tema actual.
        widget.configure(background=self.colors.bg)

    def update_canvas_style(self, widget: tk.Canvas) -> None:
        """Actualiza el estilo de un canvas.

        Este método configura el color de fondo del Canvas para que coincida
        con el color de fondo del tema actual. También elimina el borde de
        resaltado que aparece cuando el Canvas recibe el foco, estableciendo
        highlightthickness a cero.

        Args:
            widget (tk.Canvas): Objeto Canvas que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.
        """
        widget.configure(
            # Establece el color de fondo igual al del tema actual
            background=self.colors.bg,
            # Elimina el borde de resaltado que aparece cuando el Canvas tiene el foco
            # Un valor de 0 hace que no se muestre ningún borde
            highlightthickness=0,
        )

    def update_button_style(self, widget: tk.Button) -> None:
        """Actualiza el estilo visual de un botón tkinter estándar.

        Este método configura múltiples propiedades visuales del botón para darle
        una apariencia moderna y plana que coincida con el tema actual. Establece
        colores para el estado normal y activo, elimina bordes y relieve, y ajusta
        colores de resaltado.

        Args:
            widget (tk.Button): Objeto botón que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            El color de fondo activo se calcula reduciendo el brillo del color primario
            en un 10% para dar un efecto visual al presionar el botón.
        """
        # Color de fondo principal del botón (usa el color primario del tema)
        background = self.colors.primary
        # Color del texto del botón (usa el color de texto para elementos seleccionados
        # que generalmente contrasta bien con el color primario)
        foreground = self.colors.selectfg
        # Color para cuando el botón está presionado (estado activo)
        # Reduce el brillo (value) del color primario en un 10% para dar
        # efecto visual de "presionado"
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.1)
        # Aplicar todas las propiedades de estilo al botón
        widget.configure(
            background=background, # Color de fondo en estado normal
            foreground=foreground,  # Color del texto
            relief=tk.FLAT, # Elimina el efecto 3D tradicional de los botones tkinter
            borderwidth=0, # Elimina el borde del botón
            activebackground=activebackground, # Color de fondo cuando el botón está presionado
            highlightbackground=self.colors.selectfg,  # Color del borde de resaltado cuando el botón tiene foco
        )

    def update_label_style(self, widget: tk.Label) -> None:
        """Actualiza el estilo de una etiqueta.

        Este método configura los colores de texto y fondo de una etiqueta (Label)
        para que coincidan con los colores estándar del tema actual. Las etiquetas
        utilizan los colores básicos del tema (fg y bg) sin modificaciones adicionales.

        Args:
            widget (tk.Label): Objeto etiqueta que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.
        """
        # Configura los colores básicos de la etiqueta
        # Utiliza los colores estándar del tema actual sin modificaciones

        # Aplicar los colores estándar del tema actual
        widget.configure(
            foreground=self.colors.fg,  # Color del texto (fg del tema)
            background=self.colors.bg  # Color de fondo (bg del tema)
        )

    def update_frame_style(self, widget: tk.Frame) -> None:
        """Actualiza el estilo de un Frame.

        Este método configura el color de fondo de un widget Frame para que coincida
        con el color de fondo estándar del tema actual. Los Frames son contenedores
        fundamentales en tkinter, por lo que este método es esencial para mantener
        la coherencia visual en la aplicación.

        Args:
            widget (tk.Frame): Objeto Frame que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.
        """
        # Configura el color de fondo del Frame para que coincida con
        # el color de fondo estándar del tema actual (self.colors.bg)
        #
        # Los Frames son contenedores fundamentales, por lo que esta
        # configuración afecta a la apariencia base de la aplicación
        widget.configure(background=self.colors.bg)


    def update_checkbutton_style(self, widget: tk.Checkbutton) -> None:
        """Actualiza el estilo de un botón de verificación.

        Este método configura múltiples propiedades de color para un widget Checkbutton
        para que coincida con el tema actual. Establece colores para los estados normal
        y activo, así como el color del área de selección.

        Args:
            widget (tk.Checkbutton): Objeto Checkbutton que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            El color de selección (selectcolor) se establece al color de fondo del tema,
            lo que puede afectar la visibilidad del indicador de selección dependiendo
            del tema y la plataforma.
        """
        # Aplicar los colores del tema actual al Checkbutton
        widget.configure(
            # Color de fondo cuando el cursor está sobre el widget o cuando
            # se presiona (estado activo). Usa el color de fondo estándar.
            activebackground=self.colors.bg,
            # Color del texto cuando el widget está en estado activo.
            # Usa el color primario para destacar el texto.
            activeforeground=self.colors.primary,
            # Color de fondo en estado normal.
            # Usa el color de fondo estándar del tema.
            background=self.colors.bg,
            # Color del texto en estado normal.
            # Usa el color de texto estándar del tema.
            foreground=self.colors.fg,
            # Color del fondo donde aparece el indicador de selección.
            # Usar el color de fondo del tema aquí puede afectar la visibilidad
            # del indicador dependiendo del tema y la plataforma.
            selectcolor=self.colors.bg,
        )

    def update_radiobutton_style(self, widget: tk.Radiobutton) -> None:
        """Actualiza el estilo de un botón de radio.

        Este método configura múltiples propiedades de color para un widget Radiobutton
        para que coincida con el tema actual. Establece colores para los estados normal
        y activo, así como el color del área de selección.

        Args:
            widget (tk.Radiobutton): Objeto Radiobutton que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            El color de selección (selectcolor) se establece al color de fondo del tema,
            lo que puede afectar la visibilidad del indicador de selección dependiendo
            del tema y la plataforma.
        """
        # Aplicar los colores del tema actual al Radiobutton
        widget.configure(
            # Color de fondo cuando el cursor está sobre el widget o cuando
            # se presiona (estado activo). Usa el color de fondo estándar.
            activebackground=self.colors.bg,
            # Color del texto cuando el widget está en estado activo.
            # Usa el color primario para destacar el texto.
            activeforeground=self.colors.primary,
            # Color de fondo en estado normal.
            # Usa el color de fondo estándar del tema.
            background=self.colors.bg,
            # Color del texto en estado normal.
            # Usa el color de texto estándar del tema.
            foreground=self.colors.fg,
            # Color del fondo donde aparece el indicador de selección (círculo).
            # Usar el color de fondo del tema aquí puede afectar la visibilidad
            # del indicador dependiendo del tema y la plataforma.
            selectcolor=self.colors.bg,
        )

    def update_entry_style(self, widget: tk.Entry) -> None:
        """Actualiza el estilo de un campo de entrada.

        Este método configura múltiples propiedades visuales para un widget Entry
        para que coincida con el tema actual. Establece un estilo plano con un borde
        fino, y configura colores específicos para el texto, fondo y cursor.
        El color del borde varía según si el tema es claro u oscuro para mantener
        un contraste adecuado.

        Args:
            widget (tk.Entry): Objeto Entry que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            El método diferencia entre temas claros y oscuros para determinar
            el color del borde, proporcionando mejor contraste visual en ambos casos.
        """
        # Determinar el color del borde según el tipo de tema
        # Esto proporciona mejor contraste visual en cada caso
        if self.is_light_theme:
            # En temas claros, usar el color de borde estándar
            bordercolor = self.colors.border
        else:
            # En temas oscuros, usar el color de fondo de selección
            # para un contraste más adecuado
            bordercolor = self.colors.selectbg

        # Configurar múltiples propiedades visuales del Entry
        widget.configure(
            relief=tk.FLAT,  # Eliminar el efecto 3D tradicional para un aspecto más moderno
            highlightthickness=1, # Establecer un borde fino de 1 píxel
            foreground=self.colors.inputfg, # Color del texto (específico para campos de entrada)
            highlightbackground=bordercolor, # Color del borde cuando no tiene foco (varía según el tema)
            highlightcolor=self.colors.primary, # Color del borde cuando tiene foco (usa color primario para destacar)
            background=self.colors.inputbg, # Color de fondo (específico para campos de entrada)
            insertbackground=self.colors.inputfg, # Color del cursor de texto (mismo que el texto para coherencia)
            insertwidth=1, # Ancho del cursor en píxeles (valor fino y moderno)
        )

    def update_scale_style(self, widget: tk.Scale) -> None:
        """Actualiza el estilo de un control deslizante.

        Este método configura múltiples propiedades visuales para un widget Scale
        para que coincida con el tema actual. Establece un estilo plano y moderno
        con colores coherentes con el tema. El color del borde varía según si el
        tema es claro u oscuro para mantener un contraste adecuado, y se utiliza
        una versión más oscura del color primario para el estado activo del deslizador.

        Args:
            widget (tk.Scale): Objeto Scale que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            El método oculta la visualización del valor numérico (showvalue=False)
            para una apariencia más limpia y minimalista.
        """
        # Determinar el color del borde según el tipo de tema
        # Esto proporciona mejor contraste visual en cada caso
        if self.is_light_theme:
            # En temas claros, usar el color de borde estándar
            bordercolor = self.colors.border
        else:
            # En temas oscuros, usar el color de fondo de selección
            # para un contraste más adecuado
            bordercolor = self.colors.selectbg

        # Crear un color más oscuro para el estado activo del deslizador
        # Reduce el valor (brightness) del color primario en un 20%
        # para proporcionar feedback visual cuando se arrastra el deslizador
        activecolor = Colors.update_hsv(self.colors.primary, vd=-0.2)

        # Configurar múltiples propiedades visuales del Scale
        widget.configure(
            background=self.colors.primary, # Color del deslizador (la parte móvil) usando el color primario
            showvalue=False, # Oculta la visualización del valor numérico para una apariencia más limpia
            sliderrelief=tk.FLAT, # Establece el estilo del deslizador a plano (sin efecto 3D)
            borderwidth=0, # Elimina el borde normal del widget
            activebackground=activecolor, # Color del deslizador cuando está activo (siendo arrastrado), Usa una versión más oscura del color primario
            highlightthickness=1, # Establece un borde fino de 1 píxel alrededor del control
            highlightcolor=bordercolor, # Color del borde cuando tiene foco
            highlightbackground=bordercolor, # Color del borde cuando no tiene foco (mismo valor para coherencia)
            troughcolor=self.colors.inputbg, # Color del canal por el que se desplaza el deslizador # Usa el color de fondo para campos de entrada
        )

    def update_spinbox_style(self, widget: tk.Spinbox) -> None:
        """Actualiza el estilo de un control Spinbox.
        Este método configura múltiples propiedades visuales para un widget Spinbox
        para que coincida con el tema actual. Establece un estilo plano con un borde
        fino, y configura colores específicos para el texto, fondo, botones y cursor.
        El color del borde varía según si el tema es claro u oscuro para mantener
        un contraste adecuado.

        Args:
            widget (tk.Spinbox): Objeto Spinbox que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            Algunas opciones como buttonuprelief y buttondownrelief se configuran pero
            aparentemente no tienen efecto en el widget Spinbox de tkinter, posiblemente
            debido a limitaciones de la implementación.
        """
        # Determinar el color del borde según el tipo de tema
        # Esto proporciona mejor contraste visual en cada caso
        if self.is_light_theme:
            # En temas claros, usar el color de borde estándar
            bordercolor = self.colors.border
        else:
            # En temas oscuros, usar el color de fondo de selección
            # para un contraste más adecuado
            bordercolor = self.colors.selectbg

        # Configurar múltiples propiedades visuales del Spinbox
        widget.configure(
            relief=tk.FLAT, # Eliminar el efecto 3D tradicional para un aspecto más moderno
            highlightthickness=1, # Establecer un borde fino de 1 píxel
            foreground=self.colors.inputfg, # Color del texto (específico para campos de entrada)
            highlightbackground=bordercolor, # Color del borde cuando no tiene foco (varía según el tema)
            highlightcolor=self.colors.primary, # Color del borde cuando tiene foco (usa color primario para destacar)
            background=self.colors.inputbg, # Color de fondo del campo de entrada
            buttonbackground=self.colors.inputbg, # Color de fondo de los botones incrementar/decrementar Usa el mismo color que el fondo del campo para coherencia
            insertbackground=self.colors.inputfg, # Color del cursor de texto (mismo que el texto para coherencia)
            insertwidth=1, # Ancho del cursor en píxeles (valor fino y moderno)
            # Las siguientes opciones están documentadas en tkinter pero
            # aparentemente no tienen efecto en el widget Spinbox
            buttonuprelief=tk.FLAT,  # Debería hacer el botón incrementar plano
            buttondownrelief=tk.SUNKEN,  # Debería hacer el botón decrementar hundido
        )