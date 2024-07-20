from typing import Iterator

from ..settings import settings

from .color import Color, WHITE, BLACK


__all__ = 'glyphs', 'Glyphs'



class Glyphs:
	"""Efficiently stores and retrieves glyph data."""

	"""
	The bit offset vs. pixel location. These correspond to the LED strip order.
	
	|-  00  01  02  03  04
	00 [02][03][04][05][06]
	01 [01]            [07]
	02 [00]            [08]
	03 [19][20][21][22][09]
	04 [18]            [10]
	05 [17]            [11]
	06 [16][15][14][13][12]
	"""
	# noinspection SpellCheckingInspection
	GLYPH_DATA: bytearray = bytearray.fromhex(
		'0fffff'
		'001fc0'
		'7ff3fc'
		'61fffc'
		'781fc7'
		'79fe7f'
		'7ffe7f'
		'001ffc'
		'7fffff'
		'781fff'
	)
	BYTES_PER_GLYPH: int = len(GLYPH_DATA) // 10

	__slots__ = ()


	@classmethod
	def __getitem__ (cls, digit: int) -> bytearray:
		"""Make individual glyphs accessible, indexed by their value."""

		offset: int = cls.BYTES_PER_GLYPH * digit
		return cls.GLYPH_DATA[offset: offset + cls.BYTES_PER_GLYPH]


	def get_glyph_colors (self, digit: int, on_color: Color = WHITE, off_color: Color = BLACK) -> Iterator[Color]:
		"""Builds an iterable of pixel colors corresponding to the pixel states."""

		# A single glyph is small enough to store as an int
		glyph: int = int.from_bytes(self[digit], 'big')

		for offset in range(settings.display_pixel_count):
			if glyph >> offset & 1:
				yield on_color
			else:
				yield off_color



glyphs: Glyphs = Glyphs()



class OldGlyph:
	"""Represents a character glyph.

		Pixel state values are encoded as an integer for efficiency.
	"""

	__slots__ = '_bits', '_index'

	# Index vs pixel location. These correspond to the LED strip order.
	#
	# [02][03][04][05][06]
	# [01]            [07]
	# [00]            [08]
	# [19][20][21][22][09]
	# [18]            [10]
	# [17]            [11]
	# [16][15][14][13][12]

	_bits: int

	_index: int

	_LENGTH: int = 23


	def __init__ (self, bits: int = 0) -> None:
		self._bits = bits
		self._index = 0


	def __getitem__ (self, index: int) -> bool:
		"""The value of the bit at ``index``."""

		if index < 0:
			raise IndexError("Index must be positive")

		if index >= self._LENGTH:
			raise IndexError(f"Index must be less than {self._LENGTH}")

		return bool((self._bits >> index) & 1)


	def __setitem__ (self, index: int, value: bool) -> None:
		"""Set the value of the bit at ``index``."""

		if index < 0:
			raise IndexError("Index must be positive")

		if index >= self._LENGTH:
			raise IndexError(f"Index must be less than {self._LENGTH}")

		if value:
			self._bits |= 1 << index

		else:
			self._bits &= ~(1 << index)


	def __len__ (self) -> int:
		"""Our glyphs have 23 bits."""

		return self._LENGTH


	def __iter__ (self) -> 'OldGlyph':
		"""Start iterating."""

		self._index = 0

		return self


	def __next__ (self) -> bool:
		"""Continue iterating."""

		if self._index >= self._LENGTH:
			raise StopIteration

		current = self[self._index]

		self._index += 1

		return current



"""The pixel states of glyphs representing digits 0-9."""
DIGIT_GLYPHS: dict[int | str, tuple[bool]] = {i: tuple(OldGlyph(g)) for i, g in enumerate([1048575, 8128, 8385532, 6422524, 7872455, 7995007, 8388223, 8188, 8388607, 7872511])}
