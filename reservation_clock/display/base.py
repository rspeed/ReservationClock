from .color import Color, WHITE, BLACK


__all__ = 'BaseDisplay', 'BaseDigit'



class BaseDisplay:
	"""Base class for displays."""

	digits = ('h0', 'h1', 'm0', 'm1')

	h0: 'BaseDigit'
	h1: 'BaseDigit'
	m0: 'BaseDigit'
	m1: 'BaseDigit'


	def set (self, *, hours: int, minutes: int, color: Color = WHITE, background: Color = BLACK) -> None:
		"""Updates the display."""

		h0:int = hours // 10
		if not h0:
			# Hide the first hour digit if it is zero
			self.h0.fill(background)
		else:
			self.h0.set(h0, color, background)
		self.h1.set(hours % 10, color, background)

		self.m0.set(minutes // 10, color, background)
		self.m1.set(minutes % 10, color, background)


	def fill (self, color: Color = BLACK) -> None:
		"""Clears the entire display."""

		self.h0.fill(color)
		self.h1.fill(color)
		self.m0.fill(color)
		self.m1.fill(color)



class BaseDigit:
	"""Base class for display digits."""

	def set (self, value: int, color: Color = WHITE, background: Color = BLACK) -> None:
		"""Updates the digit."""

		if 0 > value > 9:
			raise ValueError("Value needs to be an integer between 0 and 9.")


	def fill (self, color: Color = BLACK) -> None:
		"""Clears the digit."""

		raise NotImplementedError
