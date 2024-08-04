from time import sleep
from ntptime import settime

from .logging import get_logger


__all__ = 'set_clock'

log = get_logger(__name__)



def set_clock ():
	for _ in range(3):
		try:
			settime()
			break
		except OSError as e:
			log.error("NTP timed out.")
			sleep(0.5)
