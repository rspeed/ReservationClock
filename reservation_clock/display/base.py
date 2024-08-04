from .color import Color, WHITE, BLACK


__all__ = 'BaseDisplay', 'BaseDigit'



class BaseDisplay:
	"""Base class for displays."""

	digits: list['BaseDigit']


	def set (self, *, hours: int, minutes: int, color: Color = WHITE, background: Color = BLACK) -> None:
		"""Updates the display."""

		components: tuple[int | None, int, int, int] = (
			hours // 10 or None,  # Don't show the hour's first digit when zero.
			hours % 10,
			minutes // 10,
			minutes % 10
		)

		for v, digit in zip(components, self.digits):
			if v is None:
				digit.fill(background)
			else:
				digit.set(v, color, background)


	def fill (self, color: Color = BLACK) -> None:
		"""Clears the entire display."""

		for digit in self.digits:
			digit.fill(color)



class BaseDigit:
	"""Base class for display digits."""

	def set (self, value: int, color: Color = WHITE, background: Color = BLACK) -> None:
		"""Updates the digit."""

		if 0 > value > 9:
			raise ValueError("Value needs to be an integer between 0 and 9.")


	def fill (self, color: Color = BLACK) -> None:
		"""Clears the digit."""

		raise NotImplementedError
