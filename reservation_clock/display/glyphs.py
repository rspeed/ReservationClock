from typing import Iterator

from ..settings import settings

from .color import Color, WHITE, BLACK


__all__ = 'glyphs', 'Glyphs'



class Glyphs:
	"""Efficiently stores and retrieves glyph data."""

	"""
	The default bit offset vs. pixel location. These correspond to the LED strip order.
	
	|-  00  01  02  03  04
	00 [06][07][20][21][34]
	01 [05][08][19][22][33]
	02 [04][09][18][23][32]
	03 [03][10][17][24][31]
	04 [02][11][16][25][30]
	05 [01][12][15][26][29]
	06 [00][13][14][27][28]
	"""
	GLYPH_DATA: bytearray = bytearray.fromhex(settings.display_glyphs)
	BYTES_PER_GLYPH: int = len(GLYPH_DATA) // 10


	@classmethod
	def __getitem__ (cls, digit: int) -> bytearray:
		"""Make individual glyphs accessible, indexed by their value."""

		offset: int = cls.BYTES_PER_GLYPH * digit
		return cls.GLYPH_DATA[offset: offset + cls.BYTES_PER_GLYPH]


	def get_glyph_colors (self, digit: int, on_color: Color = WHITE, off_color: Color = BLACK) -> Iterator[Color]:
		"""Builds an iterable of pixel colors corresponding to the pixel states."""

		#TODO: Support callables for color parameters to enable per-pixel colors.

		# A single glyph is small enough to store as an int
		glyph: int = int.from_bytes(self[digit], 'big')

		for offset in range(settings.display_pixel_count):
			if glyph >> offset & 1:
				yield on_color
			else:
				yield off_color



glyphs: Glyphs = Glyphs()
