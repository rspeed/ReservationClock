"""Workaround to allow testing on the Unix port despite it not having a `machine.Timer`."""

try:
	from machine import Timer
except ImportError:
	Timer = None

__all__ = 'Timer'



class FakeTimer:
	"""Placeholder for `machine.Timer` which just calls the callback immediately."""

	PERIODIC: int = 1
	ONE_SHOT: int = 2


	def __init__ (self, *args, callback = None, **_) -> None:
		callback(self)


	# noinspection SpellCheckingInspection
	def deinit (self) -> None:
		...



if Timer is None:
	Timer = FakeTimer
