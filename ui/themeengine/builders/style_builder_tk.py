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