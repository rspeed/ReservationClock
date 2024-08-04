from time import sleep
from logging import getLogger

from ntptime import settime


__all__ = 'set_clock'

log = getLogger(__name__)



def set_clock ():
	for _ in range(3):
		try:
			settime()
			break
		except OSError as e:
			log.error("NTP timed out.")
			sleep(0.5)
