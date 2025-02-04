from typing import Tuple, Iterator
import colorsys
from PIL import ImageColor


class Colors:
    """Define la estructura de colores para un tema y proporciona métodos
    de manipulación de colores.

    Un objeto `Colors` está asociado a un `ThemeDefinition` y puede ser 
    accedido a través de `Style.colors` para el tema actual.

    Examples:
        ```python
        style = Style()

        # Acceso por atributo
        style.colors.primary

        # Acceso por método get
        style.colors.get('primary')

        # Iterar sobre colores principales
        for color_label in style.colors:
            color = style.colors.get(color_label)
            print(color_label, color)

        # Modificar color existente
        new_color = Colors.update_hsv("#9954bb", vd=0.15)
        ```
    """

    def __init__(
            self,
            primary: str,
            secondary: str,
            success: str,
            info: str,
            warning: str,
            danger: str,
            light: str,
            dark: str,
            bg: str,
            fg: str,
            selectbg: str,
            selectfg: str,
            border: str,
            inputfg: str,
            inputbg: str,
            active: str,
    ):
        """Inicializa un nuevo objeto Colors.

        Args:
            primary: Color principal del tema
            secondary: Color secundario/acento
            success: Color de éxito (verde)
            info: Color informativo (azul)
            warning: Color de advertencia (naranja)
            danger: Color de peligro (rojo)
            light: Color claro
            dark: Color oscuro
            bg: Color de fondo
            fg: Color de texto
            selectbg: Color de fondo para selección
            selectfg: Color de texto para selección
            border: Color de bordes
            inputfg: Color de texto para inputs
            inputbg: Color de fondo para inputs
            active: Color de elemento activo
        """
        self.primary = primary
        self.secondary = secondary
        self.success = success
        self.info = info
        self.warning = warning
        self.danger = danger
        self.light = light
        self.dark = dark
        self.bg = bg
        self.fg = fg
        self.selectbg = selectbg
        self.selectfg = selectfg
        self.border = border
        self.inputfg = inputfg
        self.inputbg = inputbg
        self.active = active

    def get(self, color_label: str) -> str:
        """Obtiene un color por su nombre.

        Args:
            color_label: Nombre del color a obtener

        Returns:
            Valor hexadecimal del color
        """
        return self.__dict__.get(color_label)

    def set(self, color_label: str, color_value: str) -> None:
        """Establece un valor de color.

        Args:
            color_label: Nombre del color
            color_value: Valor hexadecimal del color
        """
        self.__dict__[color_label] = color_value

    def get_foreground(self, color_label: str) -> str:
        """Retorna el color de texto apropiado para un color de fondo.

        Args:
            color_label: Nombre del color de fondo

        Returns:
            Color de texto apropiado
        """
        if color_label == "light":
            return self.dark
        elif color_label == "dark":
            return self.light
        else:
            return self.selectfg

    @staticmethod
    def make_transparent(alpha: float, foreground: str, background: str = '#ffffff') -> str:
        """Simula transparencia de color.

        Args:
            alpha: Nivel de transparencia (0-1)
            foreground: Color de frente
            background: Color de fondo

        Returns:
            Color resultante
        """
        fg = ImageColor.getrgb(foreground)
        bg = ImageColor.getrgb(background)
        rgb_float = [alpha * c1 + (1 - alpha) * c2 for (c1, c2) in zip(fg, bg)]
        rgb_int = [int(x) for x in rgb_float]
        return '#{:02x}{:02x}{:02x}'.format(*rgb_int)

    @staticmethod
    def hex_to_rgb(color: str) -> Tuple[float, float, float]:
        """Convierte color hexadecimal a RGB (0-1).

        Args:
            color: Color hexadecimal

        Returns:
            Tupla RGB normalizada (0-1)
        """
        r, g, b = ImageColor.getrgb(color)
        return r / 255, g / 255, b / 255

    @staticmethod
    def rgb_to_hex(r: float, g: float, b: float) -> str:
        """Convierte RGB a hexadecimal.

        Args:
            r: Rojo (0-1)
            g: Verde (0-1)
            b: Azul (0-1)

        Returns:
            Color hexadecimal
        """
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return '#{:02x}{:02x}{:02x}'.format(r_, g_, b_)

    @staticmethod
    def update_hsv(color: str, hd: float = 0, sd: float = 0, vd: float = 0) -> str:
        """Modifica los valores HSV de un color.

        Args:
            color: Color hexadecimal
            hd: Delta de matiz (-1 a 1)
            sd: Delta de saturación (-1 a 1)
            vd: Delta de valor (-1 a 1)

        Returns:
            Color hexadecimal modificado
        """
        r, g, b = Colors.hex_to_rgb(color)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # Ajustar matiz
        h = max(0, min(1, h * (1 + hd)))
        # Ajustar saturación
        s = max(0, min(1, s * (1 + sd)))
        # Ajustar valor
        v = max(0.05, min(0.95, v * (1 + vd)))

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Colors.rgb_to_hex(r, g, b)

    def __iter__(self) -> Iterator[str]:
        """Itera sobre los colores principales del tema."""
        return iter([
            "primary", "secondary", "success", "info",
            "warning", "danger", "light", "dark"
        ])

    @staticmethod
    def label_iter() -> Iterator[str]:
        """Itera sobre todos los nombres de colores disponibles."""
        return iter([
            "primary", "secondary", "success", "info",
            "warning", "danger", "light", "dark", "bg",
            "fg", "selectbg", "selectfg", "border",
            "inputfg", "inputbg", "active"
        ])

    def __repr__(self) -> str:
        """Representación string del objeto."""
        out = tuple(zip(self.__dict__.keys(), self.__dict__.values()))
        return str(out)