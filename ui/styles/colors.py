# ui/styles/colors.py

class Colors:
    """Define la estructura de colores para un tema.

    Esta clase actúa como contenedor de colores sin valores predeterminados,
    permitiendo que cada tema defina sus propios valores.

    Attributes:
        primary (str): Color principal del tema
        secondary (str): Color secundario del tema
        bg (str): Color de fondo
        fg (str): Color de texto
        selectbg (str): Color de fondo para selección
        selectfg (str): Color de texto para selección
        border (str): Color de bordes
    """

    def __init__(self, **colors):
        """Inicializa un nuevo objeto Colors.

        Args:
            **colors: Diccionario de colores a configurar
        """
        for name, value in colors.items():
            setattr(self, name, value)

    def get_color(self, name):
        """Obtiene un color por su nombre.

        Args:
            name (str): Nombre del color a obtener

        Returns:
            str: Valor hexadecimal del color

        Raises:
            AttributeError: Si el color no existe
        """
        return getattr(self, name)