try:
	from .display import Display, Digit
except ImportError:
	from .fakedisplay import FakeDisplay as Display, FakeDigit as Digit

from .color import Color, WHITE, BLACK, RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET


__all__ = 'display', 'Display', 'Digit', 'Color', 'WHITE', 'BLACK', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'INDIGO', 'VIOLET'

# Use a shared instance, rather than a singleton
display = Display()
