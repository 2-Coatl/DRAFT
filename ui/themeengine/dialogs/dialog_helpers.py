from collections import namedtuple

STD_SHADES = [0.9, 0.8, 0.7, 0.4, 0.3]
STD_COLORS = [
    '#FF0000', '#FFC000', '#FFFF00', '#00B050',
    '#0070C0', '#7030A0', '#FFFFFF', '#000000'
]

ColorValues = namedtuple('ColorValues', 'h s l r g b hex')
ColorChoice = namedtuple('ColorChoice', 'rgb hsl hex')

PEN = '✛'

