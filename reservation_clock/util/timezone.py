from datetime import datetime, timedelta, tzinfo


__all__ = 'et'



class EasternTimeZone(tzinfo):
	"""US Eastern Time Zone"""


	_OFFSET: timedelta = timedelta(hours = -5)

	_dst_range_cache: dict[int, tuple[datetime, datetime]]


	def __init__ (self, *args, **kwargs):
		self._dst_range_cache = {}

		super().__init__(*args, **kwargs)


	def utcoffset (self, dt: datetime) -> timedelta:
		"""The difference between this timezone and UTC for the given ``datetime``."""

		return self._OFFSET + self.dst(dt)


	def dst (self, dt: datetime) -> timedelta:
		"""DST offset for the given ``datetime``."""

		dst_start: datetime
		dst_end: datetime

		# Pull from the cache
		try:
			dst_start, dst_end = self._dst_range_cache[dt.year]

		# Cache miss
		except KeyError:
			# Second Sunday of March
			dst_start = datetime(year = dt.year, month = 3, day = 1, hour = 2)
			dst_start += timedelta(13 - dst_start.weekday())

			# First Sunday of November
			dst_end = dst_start.replace(month = 11)
			dst_end += timedelta(6 - dst_end.weekday())

			# Set cache
			self._dst_range_cache[dt.year] = dst_start, dst_end

		# Check if dt is within the DST range
		if dst_start <= dt.replace(tzinfo = None) < dst_end:
			return timedelta(hours = 1)

		else:
			return timedelta(0)


	def tzname (self, dt: datetime) -> str:
		if self.dst(dt):
			return 'EDT'
		return 'EST'



et: tzinfo = EasternTimeZone()
