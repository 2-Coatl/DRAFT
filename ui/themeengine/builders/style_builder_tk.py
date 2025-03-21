import tkinter as tk
from ui.themeengine.core.color import Colors
from ui.themeengine.core.theme import ThemeDefinition
from ui.themeengine.utils.constants import LIGHT


class StyleBuilderTK:
    """Motor de estilos para widgets Tkinter nativos.

    Esta clase se encarga de aplicar y actualizar los estilos de los widgets
    Tkinter tradicionales que no utilizan el sistema de estilos ttk. Implementa
    el patrón Strategy para encapsular algoritmos específicos de estilización
    para cada tipo de widget.

    Roles principales:
    - Proporciona métodos update_*_style() para cada tipo de widget nativo
    - Es instanciada y mantenida por StyleBuilderTTK
    - Se utiliza dinámicamente a través de Bootstyle.update_tk_widget_style()
    - Aplica estilos directamente mediante configure() en los widgets

    Los widgets con autostyle=True (por defecto) son procesados automáticamente
    por el decorador Bootstyle.override_tk_widget_constructor, que invoca los
    métodos apropiados de esta clase. Cuando cambia el tema de la aplicación,
    los estilos se actualizan siguiendo el mismo proceso.

    Nota: A pesar de su nombre, esta clase no implementa el patrón Builder tradicional,
    sino que modifica widgets existentes en lugar de construir nuevos objetos.
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

    def update_listbox_style(self, widget: tk.Listbox) -> None:
        """Actualiza el estilo de un control Listbox.

        Este método configura múltiples propiedades visuales para un widget Listbox
        para que coincida con el tema actual. Establece un estilo plano con un borde
        fino, configura colores específicos para el texto y fondo normales, así como
        para los elementos seleccionados. El color del borde varía según si el tema
        es claro u oscuro para mantener un contraste adecuado.

        Args:
            widget (tk.Listbox): Objeto Listbox que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            El método establece activestyle="none" para eliminar el subrayado u otros
            indicadores visuales del elemento activo, proporcionando una apariencia
            más limpia y moderna.
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

        # Configurar múltiples propiedades visuales del Listbox
        widget.configure(
            foreground=self.colors.inputfg,  # Color del texto de los elementos
            background=self.colors.inputbg,  # Color de fondo del control
            selectbackground=self.colors.selectbg, # Color de fondo de los elementos seleccionados
            selectforeground=self.colors.selectfg, # Color de texto de los elementos seleccionados
            highlightcolor=self.colors.primary, # Color del borde cuando tiene foco (usa color primario para destacar)
            highlightbackground=bordercolor, # Color del borde cuando no tiene foco (varía según el tema)
            highlightthickness=1, # Establecer un borde fino de 1 píxel
            activestyle="none", # Desactiva el estilo visual para el elemento activo (subrayado) - Proporciona una apariencia más limpia y moderna
            relief=tk.FLAT, # Eliminar el efecto 3D tradicional para un aspecto más moderno
        )

    def update_menubutton_style(self, widget: tk.Menubutton) -> None:
        """Actualiza el estilo de un botón de menú.

        Este método configura múltiples propiedades visuales para un widget Menubutton
        para que coincida con el tema actual. Establece un estilo plano sin bordes
        y usa el color primario del tema como fondo. Para el estado activo (cuando
        el cursor está sobre el botón), se utiliza una versión ligeramente más oscura
        del color primario para proporcionar feedback visual.

        Args:
            widget (tk.Menubutton): Objeto Menubutton que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.
        """
        # Crear un color más oscuro para el estado activo del botón de menú
        # Reduce el valor (brightness) del color primario en un 20%
        # para proporcionar feedback visual cuando el usuario interactúa con el botón
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.2)

        # Configurar propiedades visuales del Menubutton
        widget.configure(

            background=self.colors.primary, # Color de fondo principal usando el color primario del tema
            foreground=self.colors.selectfg, # Color del texto usando el color de texto para elementos seleccionados que normalmente contrasta bien con el color primario
            activebackground=activebackground, # Color de fondo cuando el cursor está sobre el botón o cuando se presiona -  Usa una versión más oscura del color primario para feedback visual
            activeforeground=self.colors.selectfg, # Color del texto en estado activo, Mantiene el mismo color que el texto normal para consistencia
            borderwidth=0, # Elimina el borde del botón para un aspecto más plano y moderno
        )

    def update_menu_style(self, widget: tk.Menu) -> None:
        """Actualiza el estilo de un menú.

        Este método configura múltiples propiedades visuales para un widget Menu
        para que coincida con el tema actual. Establece un estilo plano sin bordes
        y desactiva la función de separación (tearoff). Configura colores para los
        estados normal y activo, así como el color para elementos de menú como
        checkbuttons o radiobuttons.

        Args:
            widget (tk.Menu): Objeto Menu que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.
        """
        # Configurar múltiples propiedades visuales del menú
        widget.configure(
            # Desactiva la función de separación (tearoff) que permite al usuario
            # desprender el menú - generalmente no se usa en interfaces modernas
            tearoff=False,
            activebackground=self.colors.selectbg, # Color de fondo cuando un elemento del menú está activo (cursor encima) # Usa el color de fondo de selección del tema
            activeforeground=self.colors.selectfg, # Color del texto cuando un elemento del menú está activo, usa el color de texto de selección del tema
            foreground=self.colors.fg, # Color del texto normal de los elementos del menú, Usa el color de texto estándar del tema
            selectcolor=self.colors.primary, # Color para elementos de menú tipo checkbutton o radiobutton, usa el color primario del tema para destacar elementos seleccionados
            background=self.colors.bg, # Color de fondo general del menú, Usa el color de fondo estándar del tema
            relief=tk.FLAT, # Elimina el efecto 3D tradicional para un aspecto más moderno
            borderwidth=0, # Elimina el borde del menú para un aspecto más plano y moderno
        )

    def update_labelframe_style(self, widget: tk.LabelFrame) -> None:
        """Actualiza el estilo de un marco con etiqueta.

        Este método configura múltiples propiedades visuales para un widget LabelFrame
        para que coincida con el tema actual. Establece un borde fino y configura
        los colores del texto y fondo. El color del borde varía según si el tema
        es claro u oscuro para mantener un contraste adecuado.

        Args:
            widget (tk.LabelFrame): Objeto LabelFrame que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

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

        # Configurar propiedades visuales del LabelFrame
        widget.configure(
            highlightcolor=bordercolor, # Color del borde de resaltado cuando el widget tiene foco, Usa el color determinado según el tipo de tema
            foreground=self.colors.fg, # Color del texto de la etiqueta del LabelFrame, Usa el color de texto estándar del tema
            borderwidth=1, # Establece un borde fino de 1 píxel alrededor del marco
            highlightthickness=0, # Desactiva el borde adicional que aparecería cuando el widget tiene foco
            background=self.colors.bg, # Color de fondo del LabelFrame, Usa el color de fondo estándar del tema
        )

    def update_text_style(self, widget: tk.Text) -> None:
        """Actualiza el estilo de un área de texto.

        Este método configura múltiples propiedades visuales para un widget Text
        para que coincida con el tema actual. Establece un estilo plano con un borde
        fino, configura colores para el texto, fondo, selección y cursor, y añade
        padding interno para mejor legibilidad. El color del borde varía según si el
        tema es claro u oscuro para mantener un contraste adecuado.

        Args:
            widget (tk.Text): Objeto Text que se va a estilizar.

        Returns:
            None: Este método no retorna ningún valor, modifica el widget in-place.

        Nota:
            El método verifica y ajusta el color de foco si es necesario para evitar
            valores de sistema como "SystemButtonFace" que podrían no ser coherentes
            con el tema. La configuración de fuente está comentada para permitir que
            el widget mantenga su configuración original.

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

        # Obtener el color actual de resaltado para personalizarlo
        # Esto es necesario para mantener consistencia con el estado actual del widget
        focuscolor = widget.cget("highlightbackground")

        # Si el color es el valor por defecto del sistema o igual al color de borde,
        # usar el color de borde determinado por el tema
        # Esto evita valores de sistema como "SystemButtonFace" que podrían no
        # ser coherentes con el tema actual
        if focuscolor in ["SystemButtonFace", bordercolor]:
            focuscolor = bordercolor

        # Configurar propiedades visuales del widget Text
        widget.configure(
            background=self.colors.inputbg,# Color de fondo del área de texto, usa el color específico para fondos de entrada
            foreground=self.colors.inputfg, # Color del texto, usa el color específico para texto de entrada
            highlightcolor=focuscolor, # Color del borde cuando el widget tiene foco, usa el valor determinado anteriormente
            highlightbackground=bordercolor, # Color del borde cuando el widget no tiene foco, usa el color determinado según el tipo de tema
            insertbackground=self.colors.inputfg, # Color del cursor de texto (caret), usa el mismo color que el texto para coherencia#
            selectbackground=self.colors.selectbg, # Color de fondo del texto seleccionado
            selectforeground=self.colors.selectfg, # Color del texto seleccionado
            insertwidth=1, # Ancho del cursor en píxeles, valor fino y moderno
            highlightthickness=1, # Grosor del borde de resaltado, borde fino pero visible
            relief=tk.FLAT, # Estilo de relieve, elimina el efecto 3D tradicional
            padx=5, # Padding interno horizontal, evita que el texto toque los bordes
            pady=5, # Padding interno vertical, evita que el texto toque los bordes

            # Configuración de fuente (comentada)
            # Posiblemente para permitir que el widget mantenga su fuente original
            # font="TkDefaultFont",
        )