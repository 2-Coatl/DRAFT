from PIL import ImageColor
from colorsys import rgb_to_hls

RGB = 'rgb'
HSL = 'hsl'
HEX = 'hex'
NAME = 'name'

HUE = 360
SAT = 100
LUM = 100


def color_to_rgb(color, model=HEX):
    """Convert color value to rgb.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.

    Parameters:

        color (Any):
            The color values for the model being converted.

        model (str):
            The color model being converted.

    Returns:

        Tuple[int, int, int]:
            The rgb color values.
    """
    color_ = conform_color_model(color, model)
    try:
        return ImageColor.getrgb(color_)
    except:
        print('this')


def color_to_hex(color, model=RGB):
    """Convert color value to hex.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.

    Parameters:

        color (Any):
            The color values for the model being converted.

        model (str):
            The color model being converted.

    Returns:

        str:
            The hexadecimal color value.
    """
    r, g, b = color_to_rgb(color, model)
    return f'#{r:02x}{g:02x}{b:02x}'


def color_to_hsl(color, model=HEX):
    """Convert color value to hsl.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.

    Parameters:

        color (Any):
            The color values for the model being converted.

        model (str):
            The color model being converted.

    Returns:

        Tuple[int, int, int]:
            The hsl color values.
    """
    r, g, b = color_to_rgb(color, model)
    hls = rgb_to_hls(r / 255, g / 255, b / 255)
    h = int(hls[0] * HUE)
    l = int(hls[1] * LUM)
    s = int(hls[2] * SAT)
    return h, s, l

def conform_color_model(color, model):
    """Conform the color values to a string that can be interpreted
    by the `PIL.ImageColor.getrgb method`.

    Parameters:

        color (Union[Tuple[int, int, int], str]):
            The color value to conform.

        model (str):
            One of 'HSL', 'RGB', or 'HEX'

    Returns:

        str:
            A color value string that can be used as a parameter in the
            PIL.ImageColor.getrgb method.
    """
    if model == HSL:
        h, s, l = color
        return f'hsl({h},{s}%,{l}%)'
    elif model == RGB:
        r, g, b = color
        return f'rgb({r},{g},{b})'
    else:
        return color
