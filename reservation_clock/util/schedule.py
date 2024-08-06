try:
	from micropython import schedule
except ImportError:
	schedule = None

from typing import Callable, Any


__all__ = 'schedule'



def fake_schedule (func: Callable, arg: Any):
	func(arg)



if schedule is None:
	schedule = fake_schedule
