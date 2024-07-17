from typing import Tuple


__all__ = 'Color'

# Micropython isn't set up to subscript the builtin tuple type
Color: type = Tuple[int, int, int]

# Keep brightness consistent: 85 + 85 + 85 = 255
WHITE: Color = (85, 85, 85)

BLACK: Color = (0, 0, 0)

RED: Color = (255, 0, 0)

ORANGE: Color = (155, 100, 0)

YELLOW: Color = (128, 128, 0)

GREEN: Color = (0, 255, 0)

BLUE: Color = (0, 0, 255)

INDIGO: Color = (75, 0, 130)

VIOLET: Color = (100, 55, 100)
