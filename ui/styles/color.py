import colorsys
from PIL import ImageColor
from ui.styles.utils import color_utils

class Colors:
    """Clase que define el esquema de colores para un tema y proporciona
    métodos estáticos para manipular colores.

    Un objeto `Colors` está vinculado a un `ThemeDefinition` y también se puede
    acceder a través de la propiedad `Style.colors` para el tema actual.

    Ejemplos:
        ```python
        style = Style()

        # Notación de punto
        style.colors.primary

        # Método get
        style.colors.get('primary')
        ```

        Esta clase es un iterador, por lo que puedes iterar sobre las etiquetas
        de color principales (primary, secondary, success, info, warning, danger):

        ```python
        for color_label in style.colors:
            color = style.colors.get(color_label)
            print(color_label, color)
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
        """[La documentación se mantiene igual...]"""
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

    @staticmethod
    def make_transparent(alpha, foreground, background='#ffffff'):
        """Simula transparencia de color.

        Args:
            alpha (float): 
                Cantidad de transparencia; número entre 0 y 1.
            foreground (str): 
                Color de primer plano.
            background (str): 
                Color de fondo.

        Returns:
            str: Color hexadecimal que representa la versión "transparente" 
                 del color de primer plano contra el color de fondo.
        """
        fg = ImageColor.getrgb(foreground)
        bg = ImageColor.getrgb(background)
        rgb_float = [alpha * c1 + (1 - alpha) * c2 for (c1, c2) in zip(fg, bg)]
        rgb_int = [int(x) for x in rgb_float]
        return '#{:02x}{:02x}{:02x}'.format(*rgb_int)

    @staticmethod
    def hex_to_rgb(color: str) -> tuple[float, float, float]:
        """Convierte color hexadecimal a valores RGB.

        Args:
            color: Valor de color hexadecimal.

        Returns:
            Tupla con valores RGB normalizados (0-1).
        """
        r, g, b = color_utils.color_to_rgb(color)
        return r / 255, g / 255, b / 255

    @staticmethod
    def rgb_to_hex(r: float, g: float, b: float) -> str:
        """Convierte valores RGB a color hexadecimal.

        Args:
            r: Valor rojo (0-1).
            g: Valor verde (0-1).
            b: Valor azul (0-1).

        Returns:
            Color en formato hexadecimal.
        """
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return color_utils.color_to_hex((r_, g_, b_))

    def get_foreground(self, color_label: str) -> str:
        """Retorna el color de primer plano apropiado para la etiqueta 
        de color especificada.

        Args:
            color_label: Etiqueta de color correspondiente a una propiedad de clase.

        Returns:
            Color hexadecimal apropiado para el primer plano.
        """
        if color_label == "light":
            return self.dark
        elif color_label == "dark":
            return self.light
        return self.selectfg

    def get(self, color_label: str) -> str:
        """Busca un valor de color por su nombre.

        Args:
            color_label: Etiqueta de color correspondiente a una propiedad de clase.

        Returns:
            Valor de color hexadecimal.
        """
        return self.__dict__.get(color_label)

    def set(self, color_label: str, color_value: str) -> None:
        """Establece el valor de una propiedad de color.

        Args:
            color_label: Nombre del color a establecer (clave).
            color_value: Valor de color hexadecimal.
        """
        self.__dict__[color_label] = color_value

    def __iter__(self):
        """Permite iterar sobre los colores principales del tema."""
        return iter([
            "primary",
            "secondary",
            "success",
            "info",
            "warning",
            "danger",
            "light",
            "dark",
        ])

    def __repr__(self) -> str:
        """Representación del objeto Colors."""
        out = tuple(zip(self.__dict__.keys(), self.__dict__.values()))
        return str(out)

    @staticmethod
    def label_iter():
        """Itera sobre todas las etiquetas de color en la clase Color.

        Returns:
            Iterador con los nombres de las etiquetas de color.
        """
        return iter([
            "primary",
            "secondary",
            "success",
            "info",
            "warning",
            "danger",
            "light",
            "dark",
            "bg",
            "fg",
            "selectbg",
            "selectfg",
            "border",
            "inputfg",
            "inputbg",
            "active",
        ])

    @staticmethod
    def update_hsv(color: str, hd: float = 0, sd: float = 0, vd: float = 0) -> str:
        """Modifica el tono, saturación y/o valor de un color hexadecimal 
        especificando el delta.

        Args:
            color: Valor de color hexadecimal a ajustar.
            hd: Cambio porcentual en tono (hue delta).
            sd: Cambio porcentual en saturación (saturation delta).
            vd: Cambio porcentual en valor (value delta).

        Returns:
            Color hexadecimal resultante.
        """
        r, g, b = Colors.hex_to_rgb(color)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # tono
        if h * (1 + hd) > 1:
            h = 1
        elif h * (1 + hd) < 0:
            h = 0
        else:
            h *= 1 + hd

        # saturación
        if s * (1 + sd) > 1:
            s = 1
        elif s * (1 + sd) < 0:
            s = 0
        else:
            s *= 1 + sd

        # valor
        if v * (1 + vd) > 1:
            v = 0.95
        elif v * (1 + vd) < 0.05:
            v = 0.05
        else:
            v *= 1 + vd

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Colors.rgb_to_hex(r, g, b)