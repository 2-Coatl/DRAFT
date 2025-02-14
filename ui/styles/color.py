from typing import Dict, Any
from ui.styles.utils import color_helpers

class Colors:
    """Gestiona los colores fundamentales del sistema de temas."""

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
            active: str
    ):
        """Inicializa el esquema de colores."""
        self._colors: Dict[str, str] = {
            'primary': primary,
            'secondary': secondary,
            'success': success,
            'info': info,
            'warning': warning,
            'danger': danger,
            'light': light,
            'dark': dark,
            'bg': bg,
            'fg': fg,
            'selectbg': selectbg,
            'selectfg': selectfg,
            'border': border,
            'inputfg': inputfg,
            'inputbg': inputbg,
            'active': active
        }

    def get_color(self, color_name: str) -> str:
        """Obtiene el valor de un color específico."""
        return self._colors.get(color_name)

    def set_color(self, color_name: str, color_value: str) -> None:
        """Establece el valor de un color específico."""
        if color_name in self._colors:
            self._colors[color_name] = color_value

    def get_foreground_color(self, color_label: str) -> str:
        """Determina el color de texto apropiado para un fondo."""
        if color_label == "light":
            return self.get_color('dark')
        elif color_label == "dark":
            return self.get_color('light')
        return self.get_color('selectfg')

    def get_primary_colors(self) -> list[str]:
        """Obtiene la lista de colores primarios del tema."""
        return [
            'primary',
            'secondary',
            'success',
            'info',
            'warning',
            'danger'
        ]

    def get_all_colors(self) -> list[str]:
        """Obtiene la lista de todos los colores disponibles."""
        return list(self._colors.keys())

    def __str__(self) -> str:
        """Representación en texto del esquema de colores."""
        return f"Colors({', '.join(f'{k}={v}' for k, v in self._colors.items())})"

    def hex_to_rgb(self, color: str) -> tuple[float, float, float]:
        """Convert hexadecimal color to rgb color value

        Parameters:

            color (str):
                A hexadecimal color value

        Returns:

            tuple[float, float, float]:
                An rgb color value.
        """
        r, g, b = color_helpers.color_to_rgb(color)
        return r/255, g/255, b/255

    @staticmethod
    def rgb_to_hex(r: float, g: float, b: float) -> str:
        """Convert rgb to hexadecimal color value

        Parameters:

            r (float):
                red

            g (float):
                green

            b (float):
                blue

        Returns:

            str:
                A hexadecimal color value
        """
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return color_helpers.color_to_hex((r_, g_, b_))