from .base import BaseDisplay, BaseDigit
from .color import Color, WHITE, BLACK


__all__ = 'FakeDisplay', 'FakeDigit'



class FakeDisplay(BaseDisplay):
	"""Simulates a 4-digit display."""

	__slots__ = ()


	def __init__ (self) -> None:
		for digit_name in BaseDisplay.__slots__:
			setattr(self, digit_name, FakeDigit())


	def __repr__ (self) -> str:
		return f"<{self.__class__.__name__}: {self.__str__()}>"


	def __str__ (self) -> str:
		return f"[{self.h0}{self.h1}:{self.m0}{self.m1}]"



class FakeDigit(BaseDigit):
	"""Simulates a 7-segment digit."""

	__slots__ = '_value', '_color', '_background'

	_value: str | None
	_color: Color
	_background: Color


	def __init__ (self):
		self._value = None
		self._color = WHITE
		self._background = BLACK


	def __call__ (self, value: int, color: Color = WHITE, background: Color = BLACK) -> None:
		"""Updates the digit."""

		super().__call__(value, color, background)

		self._value = str(value)
		self._color = color
		self._background = background


	def fill (self, color: Color = BLACK) -> None:
		"""Clears the digit."""

		self._value = None
		self._color = color
		self._background = color


	def __repr__ (self) -> str:
		return f"<{self.__class__} object [value: {self._value}, color: {self._color}, background {self._background}]>"


	def __str__ (self) -> str:
		if self._value is None:
			return "_"

		return str(self._value)
