from neopixel import NeoPixel
from machine import Pin

from ..settings import settings

from .base import BaseDisplay, BaseDigit
from .glyphs import glyphs
from .color import Color, WHITE, BLACK


__all__ = 'Display', 'Digit'



class Display(BaseDisplay):
	"""Controls a 4-digit display using neopixels."""

	def __init__ (self) -> None:
		# Populate the `Digit`s
		self.digits = [Digit(pin_id) for pin_id in settings.display_gpio_pins]



class Digit(BaseDigit):
	"""Controls a 7-segment digit."""

	PIXEL_COUNT: int = 23

	_np: NeoPixel


	def __init__ (self, pin: Pin | int) -> None:
		if isinstance(pin, int):
			# Wrap a pin ID in a `machine.Pin` object
			pin = Pin(pin, Pin.OUT)

		self._np = NeoPixel(pin, self.PIXEL_COUNT)


	def set (self, value: int, color: Color = WHITE, background: Color = BLACK) -> None:
		"""Updates the digit's value."""

		super().set(value, color, background)

		# Set and send the pixels
		for i, pixel_color in enumerate(glyphs.get_glyph_colors(value, color, background)):
			self._np[i] = pixel_color
		self._np.write()


	def __del__ (self) -> None:
		"""Blank the display when shutting down."""

		self.fill()


	def fill (self, color: Color = BLACK) -> None:
		"""Show a solid color instead of a number."""

		self._np.fill(color)
		self._np.write()
