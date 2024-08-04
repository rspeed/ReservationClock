from datetime import datetime
from micropython import schedule

from .util.timezone import et
from .util.timer import Timer

from .display import display
from .display.color import Color, BLACK, RED, ORANGE, GREEN

from typing import Callable


__all__ = 'Clock'



class Clock:
	"""Displays the current time."""

	_timer: Timer
	_countdown_target: datetime | None


	def __init__ (self):
		self._timer = Timer()
		self._countdown_target = None

		self.clear_countdown()


	def __del__ (self) -> None:
		"""Avoids edge cases by stopping the timer before being deleted."""

		self._timer.deinit()


	def set_countdown (self, target: datetime) -> None:
		"""Switch to displaying a countdown."""

		# Avoid setting the same target every time the reservations update
		if self._countdown_target is not None and self._countdown_target == target:
			return

		self._countdown_target = target
		self._set_timer(self.update_countdown)


	def clear_countdown (self) -> None:
		"""Switch to displaying the current time."""

		self._set_timer(self.update_time)
		self._countdown_target = None


	@property
	def now (self) -> datetime:
		"""The current local `datetime`."""

		return datetime.now(tz = et)


	def _set_timer (self, callback: Callable) -> None:
		"""Changes the current operating mode by setting the timer callback."""

		# Halt current timer
		self._timer.deinit()

		# Run the callback every second
		# Use `micropython.schedule` to ensure the callback is executed between opcodes
		self._timer.init(period = 1_000, mode = Timer.PERIODIC, callback = lambda t: schedule(callback, t))


	def update_time (self, _: Timer | None = None) -> None:
		"""Periodically displays the current time."""

		now: datetime = self.now
		display.set(hours = now.hour, minutes = now.minute)


	def update_countdown (self, _: Timer | None = None) -> None:
		"""Periodically displays the remaining time."""

		remaining_seconds: int = int((self._countdown_target - self.now).total_seconds())

		if remaining_seconds <= 0:
			# TODO: Audio alarm

			# Time's up!
			display.blank(RED)
			self.clear_countdown()
			return

		# Let's break it down
		hours: int = remaining_seconds // 3_600
		minutes: int = remaining_seconds // 60 % 60
		seconds: int = remaining_seconds % 60

		# Set the display colors based on the amount of remaining time
		color: Color = GREEN
		background: Color = BLACK

		if minutes <= 5:
			# This should get their attention!
			if seconds <= 2:
				# Blink for a few seconds every minute
				color = RED
				background = BLACK
			else:
				color = BLACK
				background = RED

		if minutes <= 10:
			color = BLACK
			background = RED

		elif minutes <= 20:
			color = ORANGE

		# Switch to displaying minutes and seconds when less than an hour remains
		if hours == 0:
			hours = minutes
			minutes = seconds

		display.set(hours = hours, minutes = minutes, color = color, background = background)
