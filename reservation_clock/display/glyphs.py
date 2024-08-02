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
