from .base import BaseDisplay, BaseDigit
from .color import Color, WHITE, BLACK


__all__ = 'FakeDisplay', 'FakeDigit'



class FakeDisplay(BaseDisplay):
	"""Simulates a 4-digit display."""

	def __init__ (self) -> None:
		self.digits = [FakeDigit() for _ in range(4)]


	def __repr__ (self) -> str:
		return f"<{self.__class__.__name__}: {self.__str__()}>"


	def __str__ (self) -> str:
		return f"[{self.digits[0]}{self.digits[1]}:{self.digits[2]}{self.digits[3]}]"



class FakeDigit(BaseDigit):
	"""Simulates a 7-segment digit."""

	_value: str | None
	_color: Color
	_background: Color


	def __init__ (self):
		self._value = None
		self._color = WHITE
		self._background = BLACK


	def set (self, value: int, color: Color = WHITE, background: Color = BLACK) -> None:
		"""Updates the digit."""

		super().set(value, color, background)

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
